#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

REQUIRED_PROVIDERS = {"ads_domain", "tracker-domain"}
REQUIRED_ENHANCED_RULES = {
    "DOMAIN,googleads.g.doubleclick.net,REJECT",
    "DOMAIN,ad.doubleclick.net,REJECT",
    "DOMAIN,pagead2.googlesyndication.com,REJECT",
    "DOMAIN,imasdk.googleapis.com,REJECT",
    "DOMAIN-SUFFIX,googlesyndication.com,REJECT",
}
COMPAT_DOMAINS = {
    "static.doubleclick.net",
    "jnn-pa.googleapis.com",
}
PLAYBACK_DOMAINS = {
    "youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "googlevideo.com",
    "ytimg.com",
    "youtubei.googleapis.com",
    "youtube.googleapis.com",
    "ggpht.com",
}


def audit_file(path: Path, enhanced: bool) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return ["root YAML bukan mapping"]

    providers = data.get("rule-providers") or {}
    missing = REQUIRED_PROVIDERS - set(providers if isinstance(providers, dict) else {})
    if missing:
        errors.append("provider hilang: " + ", ".join(sorted(missing)))

    rules = [str(x) for x in (data.get("rules") or [])]
    rule_set = set(rules)
    if "RULE-SET,ads_domain,REJECT" not in rule_set:
        errors.append("RULE-SET ads_domain REJECT tidak ada")
    if "RULE-SET,tracker-domain,REJECT" not in rule_set:
        errors.append("RULE-SET tracker-domain REJECT tidak ada")

    if enhanced:
        missing_rules = REQUIRED_ENHANCED_RULES - rule_set
        if missing_rules:
            errors.append("enhanced rule hilang: " + "; ".join(sorted(missing_rules)))

    # Never reject primary playback or compatibility hosts explicitly.
    for rule in rules:
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) < 3:
            continue
        if parts[0].upper() not in {"DOMAIN", "DOMAIN-SUFFIX"}:
            continue
        domain = parts[1].lower()
        if domain in PLAYBACK_DOMAINS and parts[2].upper().startswith("REJECT"):
            errors.append(f"playback domain terblokir: {rule}")
        if domain in COMPAT_DOMAINS and parts[2].upper().startswith("REJECT"):
            errors.append(f"compatibility domain terblokir: {rule}")
        if rule == "DOMAIN-SUFFIX,doubleclick.net,REJECT":
            errors.append("doubleclick.net diblokir terlalu luas; static.doubleclick.net dibutuhkan sebagian playback")

    # googlevideo and static.doubleclick guards must be before broad MRS ad block.
    try:
        guard_idx = next(i for i, r in enumerate(rules) if r.startswith("DOMAIN-SUFFIX,googlevideo.com,"))
        ads_idx = rules.index("RULE-SET,ads_domain,REJECT")
        if guard_idx >= ads_idx:
            errors.append("googlevideo guard berada setelah ads_domain")
    except (StopIteration, ValueError):
        errors.append("googlevideo playback guard atau ads_domain tidak ditemukan")

    try:
        compat_idx = next(i for i, r in enumerate(rules) if r.startswith("DOMAIN,static.doubleclick.net,"))
        ads_idx = rules.index("RULE-SET,ads_domain,REJECT")
        if compat_idx >= ads_idx:
            errors.append("static.doubleclick.net compatibility guard berada setelah ads_domain")
    except (StopIteration, ValueError):
        errors.append("static.doubleclick.net compatibility guard atau ads_domain tidak ditemukan")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit YouTube adblock rules AkunYaml")
    parser.add_argument("files", nargs="*", default=list(FILES))
    parser.add_argument("--mode", choices=("safe", "enhanced"), default="enhanced")
    args = parser.parse_args()

    failed = False
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"[SKIP] {path}: tidak ada")
            continue
        errors = audit_file(path, args.mode == "enhanced")
        if errors:
            failed = True
            print(f"[ERROR] YouTube adblock audit: {path.name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[OK] YouTube adblock audit: {path.name}")

    filter_path = Path("youtube_browser_filters.txt")
    if filter_path.exists():
        text = filter_path.read_text(encoding="utf-8", errors="ignore")
        if "googlevideo.com" in text and "||googlevideo.com" in text:
            failed = True
            print("[ERROR] youtube_browser_filters.txt memblokir googlevideo.com")
        elif "||static.doubleclick.net" in text:
            failed = True
            print("[ERROR] browser filter memblokir static.doubleclick.net dan dapat merusak playback")
        else:
            print("[OK] Browser filter menjaga googlevideo.com dan static.doubleclick.net")
    else:
        print("[WARN] youtube_browser_filters.txt tidak ditemukan")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
