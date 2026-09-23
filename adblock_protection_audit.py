#!/usr/bin/env python3
"""Cross-check OpenClash and sing-box adblock safety coverage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

REQUIRED_RULE_NAMES = {"ads_domain", "tracker-domain"}
REQUIRED_SINGBOX_TAGS = {"ads-domain", "tracker-domain"}


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit_openclash(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    providers = data.get("rule-providers") or {}
    rules = [str(rule) for rule in data.get("rules") or []]
    dns = data.get("dns") or {}
    if data.get("mode") != "rule":
        _fail(errors, "mode harus rule")
    if dns.get("enable") is not True:
        _fail(errors, "DNS protection tidak aktif")
    used = {part.strip() for rule in rules if rule.upper().startswith("RULE-SET,") for part in rule.split(",")[1:2]}
    for name in REQUIRED_RULE_NAMES:
        if name not in providers:
            _fail(errors, f"provider wajib hilang: {name}")
        if name not in used:
            _fail(errors, f"provider tidak dipakai: {name}")
    allow_positions = [i for i, rule in enumerate(rules) if any(token in rule for token in ("DIRECT", "BANK", "SAFE"))]
    reject_positions = [i for i, rule in enumerate(rules) if "REJECT" in rule.upper()]
    if reject_positions and allow_positions and min(allow_positions) > min(reject_positions):
        _fail(errors, "allowlist/safe rules berada setelah reject")
    return errors


def audit_singbox(path: Path) -> list[str]:
    errors: list[str] = []
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    dns = data.get("dns") or {}
    route = data.get("route") or {}
    tags = {str(item.get("tag")) for item in route.get("rule_set") or [] if isinstance(item, dict)}
    if not dns.get("servers"):
        _fail(errors, "DNS server sing-box kosong")
    if not REQUIRED_SINGBOX_TAGS <= tags:
        _fail(errors, f"rule-set sing-box kurang: {sorted(REQUIRED_SINGBOX_TAGS - tags)}")
    reject = [rule for rule in route.get("rules") or [] if rule.get("action") == "reject"]
    if not reject:
        _fail(errors, "route reject adblock tidak ditemukan")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openclash", type=Path, default=Path("openclash_lite.yaml"))
    parser.add_argument("--singbox", type=Path, default=Path("singbox_android.json"))
    args = parser.parse_args()
    failures = audit_openclash(args.openclash) + audit_singbox(args.singbox)
    if failures:
        for failure in failures:
            print(f"[ERROR] {failure}")
        return 1
    print(f"[OK] protection audit: {args.openclash} + {args.singbox}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
