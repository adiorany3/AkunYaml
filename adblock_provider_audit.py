#!/usr/bin/env python3
"""Audit ad/tracker/threat rule-provider configuration and optional upstream reachability."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import urllib.error
import urllib.request

import yaml

FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

MANAGED = {
    "ads_domain",
    "tracker-domain",
    "threat-tif-mini",
    "threat-malware",
    "threat-phishing",
    "threat-cryptominers",
    "hagezi-pro-mini",
    "popup-ads",
    "privacy-extra",
    "threat-fake-scam",
    "threat-tif-ip",
}


def check_url(url: str, timeout: float) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "AkunYaml-Adblock-Audit/2.9"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400, f"HTTP {resp.status}"
    except Exception:
        # Some raw/CDN endpoints do not handle HEAD consistently.
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AkunYaml-Adblock-Audit/2.9",
                "Range": "bytes=0-1023",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp.read(1024)
                return 200 <= resp.status < 400, f"HTTP {resp.status}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return False, str(exc)


def audit(path: Path, network: bool, timeout: float) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return ["root YAML bukan mapping"]

    providers = data.get("rule-providers") or {}
    if not isinstance(providers, dict):
        return ["rule-providers bukan mapping"]

    used = set()
    for rule in data.get("rules") or []:
        parts = [part.strip() for part in str(rule).split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET":
            used.add(parts[1])

    seen_paths: dict[str, str] = {}
    for name, provider in providers.items():
        if name not in MANAGED:
            continue
        if not isinstance(provider, dict):
            errors.append(f"provider {name} bukan mapping")
            continue
        if provider.get("type") != "http":
            errors.append(f"provider {name} harus type http")
        behavior = str(provider.get("behavior") or "")
        if behavior not in {"domain", "classical", "ipcidr"}:
            errors.append(f"provider {name} behavior tidak valid: {behavior}")
        try:
            interval = int(provider.get("interval") or 0)
        except (TypeError, ValueError):
            interval = 0
        if interval < 3600 or interval > 86400:
            errors.append(f"provider {name} interval tidak wajar: {interval}")
        url = str(provider.get("url") or "")
        if not url.startswith("https://"):
            errors.append(f"provider {name} URL bukan HTTPS")
        pth = str(provider.get("path") or "")
        if not pth:
            errors.append(f"provider {name} tidak punya path")
        elif pth in seen_paths and seen_paths[pth] != name:
            errors.append(f"path provider bentrok: {name} dan {seen_paths[pth]} -> {pth}")
        else:
            seen_paths[pth] = name
        if name not in used:
            errors.append(f"provider {name} ada tetapi tidak dipakai oleh RULE-SET")
        if network and url:
            ok, detail = check_url(url, timeout)
            if not ok:
                errors.append(f"provider {name} upstream gagal: {detail}")

    if path.name == "openclash_android.yaml":
        for name, provider in providers.items():
            if name not in MANAGED or not isinstance(provider, dict):
                continue
            fmt = str(provider.get("format") or "yaml").lower()
            url = str(provider.get("url") or "").lower()
            pth = str(provider.get("path") or "").lower()
            if fmt != "yaml" or url.endswith(".mrs") or pth.endswith(".mrs"):
                errors.append(f"Android provider {name} harus YAML-only")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", default=list(FILES))
    parser.add_argument("--network", action="store_true", help="cek upstream provider dengan HEAD/partial GET")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    failed = False
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"[SKIP] {path}: tidak ada")
            continue
        errors = audit(path, args.network, args.timeout)
        if errors:
            failed = True
            print(f"[ERROR] Adblock provider audit: {path.name}")
            for err in errors:
                print("  - " + err)
        else:
            suffix = " + upstream" if args.network else ""
            print(f"[OK] Adblock provider audit: {path.name}{suffix}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
