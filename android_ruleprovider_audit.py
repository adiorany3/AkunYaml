#!/usr/bin/env python3
"""Static compatibility audit for Clash Meta for Android rule providers."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml


def audit(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return ["root YAML bukan mapping"]

    if str(data.get("mode", "")).lower() != "rule":
        errors.append("mode harus rule agar blocklist RULE-SET dievaluasi")

    sniffer = data.get("sniffer") or {}
    if isinstance(sniffer, dict):
        sniff = sniffer.get("sniff") or {}
        if isinstance(sniff, dict) and "QUIC" in sniff:
            errors.append("sniffer QUIC tidak kompatibel dengan sebagian Clash Meta for Android; gunakan HTTP/TLS saja")

    providers = data.get("rule-providers") or {}
    if not isinstance(providers, dict):
        return errors + ["rule-providers bukan mapping"]

    for name, provider in providers.items():
        if not isinstance(provider, dict):
            errors.append(f"provider {name} bukan mapping")
            continue
        fmt = str(provider.get("format") or "yaml").lower()
        url = str(provider.get("url") or "")
        pth = str(provider.get("path") or "")
        if fmt != "yaml":
            errors.append(f"provider {name} memakai format non-YAML: {fmt}")
        if ".mrs" in url.lower() or ".mrs" in pth.lower():
            errors.append(f"provider {name} masih mereferensikan .mrs")
        if not pth.lower().endswith(".yaml"):
            errors.append(f"provider {name} path bukan .yaml: {pth}")
        if provider.get("behavior") not in {"domain", "ipcidr", "classical"}:
            errors.append(f"provider {name} behavior tidak valid")

    rules = [str(x) for x in data.get("rules", []) or []]
    known = set(providers)
    for rule in rules:
        parts = [x.strip() for x in rule.split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] not in known:
            errors.append(f"RULE-SET tanpa provider: {parts[1]}")
    if not rules or rules[-1] != "MATCH,GLOBAL":
        errors.append("rule terakhir harus MATCH,GLOBAL")

    required = {"ads_domain", "tracker-domain", "threat-malware", "threat-phishing", "threat-cryptominers"}
    missing = required - known
    if missing:
        errors.append("provider Android hilang: " + ", ".join(sorted(missing)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="openclash_android.yaml")
    args = parser.parse_args()
    path = Path(args.file)
    errors = audit(path)
    if errors:
        print(f"[ERROR] Android rule-provider audit: {path}")
        for error in errors:
            print("  - " + error)
        return 1
    print(f"[OK] Android rule-provider audit: {path}")
    print("  - mode: rule")
    print("  - provider: YAML only")
    print("  - MRS refs: 0")
    print("  - fallback: MATCH,GLOBAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
