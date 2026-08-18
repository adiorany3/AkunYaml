#!/usr/bin/env python3
"""Security feed preflight, Last-Known-Good cache, and Android YAML snapshot.

The router still consumes its normal HTTP providers.  This module validates the
upstream text feeds during generation, records a known-good copy for audit and
rollback, and converts ABPindo's plain domain feed to a YAML snapshot for the
Android compatibility profile.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import ipaddress
import json
import os
import re
import ssl
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from security_policy import (
    ROUTER_BASE_PROVIDERS,
    ROUTER_ENHANCED_AD_PROVIDERS,
    ROUTER_GAMBLING_PROVIDERS,
    ROUTER_THREAT_SAFE_PROVIDERS,
    ROUTER_THREAT_IP_PROVIDERS,
)

DOMAIN_RE = re.compile(
    r"^(?:\*\.)?(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class FeedSpec:
    name: str
    url: str
    kind: str = "domain"
    min_entries: int = 10


def _ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    try:
        import certifi  # type: ignore
        context.load_verify_locations(cafile=certifi.where())
    except Exception:
        pass
    return context


def _fetch(url: str, timeout: int = 20) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ConvertYAML-FeedGuard/3.8", "Accept": "text/plain,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout, context=_ssl_context()) as response:
        data = response.read()
    if not data:
        raise ValueError("empty response")
    return data


def _normalize_domain_line(raw: str) -> str | None:
    line = raw.strip().lower()
    if not line or line.startswith(("#", "!", ";")):
        return None
    # Handle common domain-list prefixes without accepting full adblock syntax.
    if line.startswith("+."):
        line = line[2:]
    if line.startswith("*."):
        line = line[2:]
    if line.startswith("."):
        line = line[1:]
    line = line.rstrip(".")
    if DOMAIN_RE.fullmatch(line) and ".." not in line:
        return line
    return None


def _parse_domains(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in text.splitlines():
        domain = _normalize_domain_line(raw)
        if domain and domain not in seen:
            seen.add(domain)
            out.append(domain)
    return out


def _parse_ipcidrs(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "!", ";")):
            continue
        token = line.split()[0].strip()
        try:
            value = str(ipaddress.ip_network(token, strict=False))
        except ValueError:
            continue
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _load_meta(path: Path) -> dict[str, Any]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _bool_env(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _float_env(name: str, default: float, minimum: float, maximum: float) -> float:
    try:
        value = float(os.environ.get(name, str(default)))
    except ValueError:
        value = default
    return max(minimum, min(maximum, value))


def _feed_specs() -> list[FeedSpec]:
    catalogs = [
        ROUTER_BASE_PROVIDERS,
        ROUTER_ENHANCED_AD_PROVIDERS,
        ROUTER_GAMBLING_PROVIDERS,
        ROUTER_THREAT_SAFE_PROVIDERS,
        ROUTER_THREAT_IP_PROVIDERS,
    ]
    names_seen: set[str] = set()
    specs: list[FeedSpec] = []
    for catalog in catalogs:
        for name, provider in catalog.items():
            if name in names_seen or str(provider.get("format") or "").lower() != "text":
                continue
            url = str(provider.get("url") or "").strip()
            if not url:
                continue
            names_seen.add(name)
            behavior = str(provider.get("behavior") or "domain").lower()
            minimum = 50 if name == "ads_indonesia" else 100 if name == "threat-fake-scam" else 10
            if name == "threat-tif-mini":
                minimum = 1000
            elif name == "hagezi-pro-plus-mini":
                minimum = 10000
            elif name == "popup-ads":
                minimum = 100
            elif name == "gambling-mini":
                minimum = 50000
            specs.append(FeedSpec(name=name, url=url, kind="ipcidr" if behavior == "ipcidr" else "domain", min_entries=minimum))
    return specs


def refresh_security_feeds(workdir: Path, *, refresh: bool = True, log=print) -> dict[str, dict[str, Any]]:
    """Validate managed text feeds and maintain a Last-Known-Good cache.

    A failed or suspicious refresh never overwrites the previous known-good copy.
    The function is intentionally non-fatal because generated HTTP providers can
    continue using Mihomo's own cached provider when the workstation is offline.
    """
    cache_dir = workdir / ".feed_cache" / "last_good"
    cache_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = workdir / ".feed_cache" / "metadata.json"
    metadata = _load_meta(metadata_path)
    max_drop = _float_env("FEED_MAX_DROP_RATIO", 0.65, 0.05, 0.95)
    max_growth = _float_env("FEED_MAX_GROWTH_RATIO", 4.0, 1.1, 20.0)
    report: dict[str, dict[str, Any]] = {}
    specs = _feed_specs()
    fetched: dict[str, bytes | Exception] = {}
    if refresh and specs:
        workers = min(6, len(specs))
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {executor.submit(_fetch, spec.url): spec for spec in specs}
            for future, spec in ((f, future_map[f]) for f in future_map):
                try:
                    fetched[spec.name] = future.result()
                except Exception as exc:
                    fetched[spec.name] = exc

    for spec in specs:
        ext = ".txt"
        good_path = cache_dir / f"{spec.name}{ext}"
        old = metadata.get(spec.name) if isinstance(metadata.get(spec.name), dict) else {}
        old_count = int(old.get("count") or 0)
        status = "cached" if good_path.exists() else "unavailable"
        detail = ""
        count = old_count
        sha256 = str(old.get("sha256") or "")

        if refresh:
            try:
                raw_or_error = fetched.get(spec.name, RuntimeError("feed fetch missing"))
                if isinstance(raw_or_error, Exception):
                    raise raw_or_error
                raw = raw_or_error
                text = raw.decode("utf-8", errors="replace")
                entries = _parse_ipcidrs(text) if spec.kind == "ipcidr" else _parse_domains(text)
                count = len(entries)
                if count < spec.min_entries:
                    raise ValueError(f"valid entries too small: {count} < {spec.min_entries}")
                if old_count:
                    lower = max(spec.min_entries, int(old_count * (1.0 - max_drop)))
                    upper = max(old_count + 10, int(old_count * max_growth))
                    if count < lower:
                        raise ValueError(f"suspicious drop: {old_count} -> {count}")
                    if count > upper:
                        raise ValueError(f"suspicious growth: {old_count} -> {count}")
                normalized = ("\n".join(entries) + "\n").encode("utf-8")
                sha256 = hashlib.sha256(normalized).hexdigest()
                _atomic_write(good_path, normalized)
                metadata[spec.name] = {
                    "count": count,
                    "sha256": sha256,
                    "updated_unix": int(time.time()),
                    "kind": spec.kind,
                    "url": spec.url,
                }
                status = "updated"
            except Exception as exc:
                detail = str(exc)
                status = "last-known-good" if good_path.exists() else "unavailable"

        report[spec.name] = {
            "status": status,
            "count": count,
            "sha256": sha256,
            "detail": detail,
            "path": str(good_path.relative_to(workdir)) if good_path.exists() else "",
        }
        if detail:
            log(f"Feed guard {spec.name}: {status} ({detail})")
        else:
            log(f"Feed guard {spec.name}: {status}, {count} entries")

    _atomic_write(metadata_path, (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    _write_android_indonesia_snapshot(workdir, report, log=log)
    _write_report(workdir, report)
    return report


def _write_android_indonesia_snapshot(workdir: Path, report: dict[str, dict[str, Any]], *, log=print) -> None:
    item = report.get("ads_indonesia") or {}
    source_rel = str(item.get("path") or "")
    if not source_rel:
        return
    source = workdir / source_rel
    if not source.exists():
        return
    domains = _parse_domains(source.read_text(encoding="utf-8", errors="ignore"))
    if not domains:
        return
    out = workdir / "rule_providers" / "ads_indonesia_android.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {"payload": [f".{domain}" for domain in domains]}
    _atomic_write(out, yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=140).encode("utf-8"))
    log(f"Android Indonesia snapshot: {len(domains)} entries")


def _write_report(workdir: Path, report: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# Security Feed Guard Report",
        "",
        "A refresh is promoted only after format/count sanity checks. Suspicious updates keep the previous Last-Known-Good cache.",
        "",
        "| Provider | Status | Entries | SHA-256 |",
        "|---|---:|---:|---|",
    ]
    for name in sorted(report):
        item = report[name]
        digest = str(item.get("sha256") or "")[:16]
        lines.append(f"| `{name}` | {item.get('status','')} | {item.get('count',0)} | `{digest}` |")
    lines.append("")
    (workdir / "security_feed_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    root = Path(os.environ.get("WORKDIR", ".")).resolve()
    refresh_security_feeds(root, refresh=_bool_env("REFRESH_SECURITY_FEEDS", True))
