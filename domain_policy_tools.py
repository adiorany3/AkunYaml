"""Read local Clash policy without downloading providers or changing routing."""
from __future__ import annotations

import ipaddress
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

FIELDS = {"DOMAIN": "domain", "DOMAIN-SUFFIX": "domain_suffix", "DOMAIN-KEYWORD": "domain_keyword", "DOMAIN-REGEX": "domain_regex", "IP-CIDR": "ip_cidr", "IP-CIDR6": "ip_cidr"}


def domain(value):
    if not isinstance(value, str):
        raise TypeError("Domain harus teks")
    value = value.rstrip(".").encode("idna").decode("ascii").lower()
    if len(value) > 253 or not value or any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in value.split(".")):
        raise ValueError("Domain tidak valid; masukkan hostname tanpa URL/port")
    return value


def local_path(folder, relative):
    if not isinstance(relative, str):
        raise TypeError("Path provider harus teks")
    path = Path(relative)
    resolved = (folder / path).resolve()
    if path.is_absolute() or ".." in path.parts or not resolved.is_relative_to(folder.resolve()):
        raise ValueError("Path provider tidak aman")
    return resolved


def provider_rules(folder, provider, core):
    """Decode MRS through the installed target core; never fetch remote files."""
    behavior = provider.get("behavior", "classical")
    fmt = provider.get("format", "yaml")
    if provider.get("type") == "inline":
        payload = provider.get("payload")
        if not isinstance(payload, list):
            raise TypeError("Payload inline tidak valid")
        return parse_payload(payload, behavior)
    path = local_path(folder, provider.get("path"))
    if not path.is_file() or path.stat().st_size > 40 * 1024 * 1024:
        raise ValueError("Provider lokal hilang atau melebihi 40 MiB")
    if fmt == "mrs":
        if behavior not in {"domain", "ipcidr"}:
            raise ValueError("Behavior MRS tidak didukung")
        with tempfile.TemporaryDirectory() as temporary:
            decoded = Path(temporary) / "rules.txt"
            result = subprocess.run([str(core), "convert-ruleset", behavior, "mrs", str(path), str(decoded)], capture_output=True, timeout=120, check=False)
            if result.returncode or not decoded.is_file():
                raise ValueError("Dekode MRS gagal")
            text = decoded.read_text(encoding="utf-8")
        payload = text.splitlines()
    elif fmt == "yaml":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("payload"), list):
            raise ValueError("Payload provider tidak valid")
        payload = data["payload"]
    elif fmt == "text":
        payload = path.read_text(encoding="utf-8").splitlines()
    else:
        raise ValueError("Format provider tidak didukung")
    return parse_payload(payload, behavior)


def parse_payload(payload, behavior):
    rules = []
    for item in payload:
        if not isinstance(item, str):
            raise TypeError("Entri provider harus teks")
        item = item.strip()
        if not item or item.startswith(("#", "!")):
            continue
        if behavior == "domain":
            if item.startswith("+."):
                rules.append(("DOMAIN-SUFFIX", domain(item[2:])))
            elif item.startswith("."):
                # Clash .example.com excludes the apex domain.
                rules.append(("DOMAIN-REGEX", r"^.+\." + re.escape(domain(item[1:])) + "$"))
            elif "*" in item:
                raise ValueError("Wildcard provider belum dapat diterjemahkan dengan aman")
            else:
                rules.append(("DOMAIN", domain(item)))
        elif behavior == "ipcidr":
            rules.append(("IP-CIDR", str(ipaddress.ip_network(item, strict=False))))
        elif behavior == "classical":
            parts = item.split(",")
            if len(parts) not in {2, 3} or (len(parts) == 3 and parts[2] not in {"no-resolve", "REJECT", "REJECT-DROP", "DIRECT"}):
                raise ValueError("Rule classical tidak didukung")
            rules.append((parts[0], parts[1]))
        else:
            raise ValueError("Behavior provider tidak didukung")
    return rules


def matches(kind, value, host):
    if kind == "DOMAIN":
        return host == value.lower()
    if kind == "DOMAIN-SUFFIX":
        return host == value.lower() or host.endswith("." + value.lower())
    if kind == "DOMAIN-KEYWORD":
        return value.lower() in host
    if kind == "DOMAIN-REGEX":
        return re.search(value, host, re.IGNORECASE) is not None
    raise ValueError("Rule membutuhkan konteks selain domain")


def explain(config_path, host, core):
    host = domain(host)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(config.get("rules"), list):
        raise TypeError("Profil tidak valid")
    uncertain = 0
    for index, raw in enumerate(config["rules"], 1):
        parts = raw.split(",")
        if parts[0] == "MATCH" and len(parts) == 2:
            return {"domain": host, "position": index, "policy": parts[1], "rule": "MATCH", "source": "inline", "uncertain_before": uncertain}
        if len(parts) not in {3, 4} or (len(parts) == 4 and parts[3] != "no-resolve"):
            uncertain += 1
            continue
        kind, value, policy = parts[:3]
        source = "inline"
        if kind == "RULE-SET":
            source = value
            try:
                rules = provider_rules(config_path.parent, config.get("rule-providers", {})[value], core)
            except (KeyError, OSError, ValueError, TypeError, subprocess.SubprocessError):
                uncertain += 1
                continue
        else:
            rules = [(kind, value)]
        for rule_kind, rule_value in rules:
            try:
                if matches(rule_kind, rule_value, host):
                    return {"domain": host, "position": index, "policy": policy, "rule": rule_kind, "value": rule_value, "source": source, "uncertain_before": uncertain}
            except (ValueError, re.error):
                uncertain += 1
    return {"domain": host, "policy": None, "uncertain_before": uncertain}
