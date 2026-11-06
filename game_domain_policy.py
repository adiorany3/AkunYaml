"""Maintain approved game domains; import local connection logs for review only."""
import argparse
import ipaddress
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from feed_guard import _normalize_domain_line
from openclash_target import atomic_write_text


def domain(value):
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    if "://" in value:
        try:
            parsed = urlsplit(value)
        except ValueError:
            return None
        if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
            return None
        value = parsed.hostname or ""
    else:
        value = value.removeprefix("+.").removeprefix("*.")
        if ":" in value:
            host, port = value.rsplit(":", 1)
            if not port.isdigit() or not 1 <= int(port) <= 65535:
                return None
            value = host
    value = value.rstrip(".")
    try:
        ipaddress.ip_address(value)
        return None
    except ValueError:
        return _normalize_domain_line(value)


def read_list(path):
    result = []
    if not path.exists():
        return result
    for number, line in enumerate(path.read_text().splitlines(), 1):
        raw = line.split("#", 1)[0].strip()
        if not raw:
            continue
        item = domain(raw)
        if item is None:
            raise ValueError(f"Domain tidak valid di {path.name}, baris {number}")
        if item not in result:
            result.append(item)
    return result


def apply_policy(config, root):
    approved = read_list(root / "gameblock_policy/manual_domains.txt")
    allowed = read_list(root / "gameblock_policy/allow_domains.txt")
    for name in approved:
        if any(name == a or name.endswith("." + a) or a.endswith("." + name) for a in allowed):
            raise ValueError("Daftar game manual bertentangan dengan pengecualian game")
    prefix = [f"DOMAIN-SUFFIX,{name},REJECT" for name in approved]
    config["rules"] = prefix + [rule for rule in config["rules"] if rule not in prefix]
    # Candidate exclusions must never insert DIRECT ahead of malware rules.
    return approved


def observed_hosts(text):
    """JSON connection snapshots/JSONL or Mihomo text destination arrows only."""
    counts = Counter()

    def visit(value):
        if isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            metadata = value.get("metadata")
            if isinstance(metadata, dict):
                host = domain(metadata.get("host"))
                if host:
                    counts[host] += 1
            if "connections" in value:
                visit(value["connections"])

    try:
        visit(json.loads(text))
        return counts
    except json.JSONDecodeError:
        pass
    for line in text.splitlines():
        try:
            visit(json.loads(line))
        except json.JSONDecodeError:
            match = re.search(r"(?:-->|→)\s+([a-zA-Z0-9.-]+)(?::\d+)?(?=\s|$)", line)
            if match and (host := domain(match.group(1))):
                counts[host] += 1
    return counts


def import_log(source, root):
    if source.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("Log melebihi batas 20 MiB; ekspor bagian yang relevan")
    counts = observed_hosts(source.read_text())
    approved = read_list(root / "gameblock_policy/manual_domains.txt")
    allowed = read_list(root / "gameblock_policy/allow_domains.txt")
    candidates = [{"domain": host, "observations": count, "decision": "review"}
                  for host, count in sorted(counts.items())
                  if not any(host == a or host.endswith("." + a) for a in approved + allowed)]
    destination = root / ".runtime_cache/game_candidates.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(destination, json.dumps({"auto_blocked": 0, "note": "Observed host is not proof of a game. Review shared CDN/login/payment services before approval.", "candidates": candidates}, indent=2) + "\n")
    destination.chmod(0o600)
    return destination, len(candidates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    try:
        path, count = import_log(args.log, Path(__file__).resolve().parent)
        print(f"[OK] {count} kandidat untuk review: {path}; tidak ada auto-block")
    except (OSError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())