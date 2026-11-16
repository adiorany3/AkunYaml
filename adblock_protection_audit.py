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
CRITICAL_ALLOWLIST_DOMAINS = {
    "challenges.cloudflare.com", "hcaptcha.com", "recaptcha.net", "telegram.org",
    "t.me", "simaster.ugm.ac.id", "speedtest.net", "ookla.com",
}


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit_feed_cache(path: Path) -> list[str]:
    """Check every feed in metadata still reports >=10 entries or is LKG."""
    if not path.exists():
        return []
    errors: list[str] = []
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return errors
    for name, item in meta.items():
        good = path.parent / "last_good" / f"{name}.txt"
        if not good.exists():
            _fail(errors, f"feed {name} tanpa last-known-good cache")
            continue
        try:
            valid_lines = [line for line in good.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip() and not line.lstrip().startswith("#")]
        except OSError:
            valid_lines = []
        expected = int(item.get("count") or 0)
        if len(valid_lines) < min(10, max(1, expected)):
            _fail(errors, f"feed LKG {name} terlalu kecil/kosong: {len(valid_lines)} baris; metadata={expected}")
    return errors


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
    match_positions = [i for i, rule in enumerate(rules) if rule.upper().startswith("MATCH,")]
    if reject_positions and match_positions and max(reject_positions) > min(match_positions):
        _fail(errors, "aturan REJECT berada setelah MATCH")
    for rule in rules:
        parts = [part.strip().lower() for part in rule.split(",")]
        if len(parts) >= 3 and parts[-1].startswith("reject") and parts[1] in CRITICAL_ALLOWLIST_DOMAINS:
            _fail(errors, f"domain allowlist kritis ditolak: {parts[1]}")
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
    ruleset_reject = [rule for rule in reject if set(rule.get("rule_set", [])) & REQUIRED_SINGBOX_TAGS]
    if not ruleset_reject:
        _fail(errors, "route reject tidak terhubung dengan rule-set iklan/tracker wajib")
    if route.get("final") == "reject":
        _fail(errors, "route final sing-box tidak boleh reject")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openclash", type=Path, action="append")
    parser.add_argument("--singbox", type=Path, default=Path("singbox_android.json"))
    parser.add_argument("--feed-cache", type=Path, default=Path(".feed_cache/last_good"))
    args = parser.parse_args()
    openclash_paths = args.openclash or [Path("openclash_lite.yaml")]
    failures = [error for path in openclash_paths for error in audit_openclash(path)]
    failures += audit_singbox(args.singbox)
    if args.feed_cache.exists():
        failures += audit_feed_cache(args.feed_cache.parent / "metadata.json")
    if failures:
        for failure in failures:
            print(f"[ERROR] {failure}")
        return 1
    profiles = ", ".join(str(path) for path in openclash_paths)
    print(f"[OK] protection audit: {profiles} + {args.singbox}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
