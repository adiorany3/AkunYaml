#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

REQUIRED_BASE_PROVIDERS = {"ads_domain", "tracker-domain"}
LEAN_OVERLAP_PROVIDERS = {
    "hagezi-pro-mini",
    "popup-ads",
    "turtlecute-coverage",
    "streaming-ad-safe",
}
REQUIRED_ENHANCED_RULES = {
    "DOMAIN,googleads.g.doubleclick.net,REJECT",
    "DOMAIN,ad.doubleclick.net,REJECT",
    "DOMAIN,pagead2.googlesyndication.com,REJECT",
    "DOMAIN,imasdk.googleapis.com,REJECT",
    "DOMAIN,ads.youtube.com,REJECT",
    "DOMAIN-SUFFIX,googlesyndication.com,REJECT",
    "DOMAIN,adtrafficquality.google,REJECT",
    "DOMAIN-SUFFIX,googleadapis.com,REJECT",
    "DOMAIN,mobileads.google.com,REJECT",
    "DOMAIN,pagead.l.google.com,REJECT",
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


def _find_rule(rules: list[str], prefix: str) -> tuple[int, str] | None:
    for idx, rule in enumerate(rules):
        if rule.startswith(prefix):
            return idx, rule
    return None


def audit_file(path: Path, enhanced: bool, lean: bool) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return ["root YAML bukan mapping"]

    providers = data.get("rule-providers") or {}
    provider_names = set(providers if isinstance(providers, dict) else {})
    missing = REQUIRED_BASE_PROVIDERS - provider_names
    if missing:
        errors.append("provider hilang: " + ", ".join(sorted(missing)))

    is_android = path.name == "openclash_android.yaml"
    if not is_android and "youtube_domain" not in provider_names:
        errors.append("provider youtube_domain MRS tidak ada pada profil router")

    if lean and not is_android:
        allowed_overlap: set[str] = set()
        try:
            cfg = json.loads((path.parent / "local_config.json").read_text(encoding="utf-8"))
            level_key = "OPENWRT_LITE_ADBLOCK_LEVEL" if path.name == "openclash_lite.yaml" else "OPENWRT_ADBLOCK_LEVEL"
            level = str(cfg.get(level_key, "standard")).strip().lower()
            if level in {"compact", "enhanced"}:
                allowed_overlap.add("popup-ads")
        except Exception:
            pass
        overlap = sorted((provider_names & LEAN_OVERLAP_PROVIDERS) - allowed_overlap)
        if overlap:
            errors.append("provider overlap masih aktif dalam lean mode: " + ", ".join(overlap))

    groups = {
        str(g.get("name")): g
        for g in (data.get("proxy-groups") or [])
        if isinstance(g, dict) and g.get("name")
    }
    youtube = groups.get("YOUTUBE")
    if not isinstance(youtube, dict):
        errors.append("proxy-group YOUTUBE tidak ada")
    else:
        if str(youtube.get("type") or "").lower() != "fallback":
            errors.append("YOUTUBE bukan fallback otomatis")
        if youtube.get("lazy") is not True:
            errors.append("YOUTUBE health-check tidak lazy")
        interval = int(youtube.get("interval") or 0)
        if interval < 60 or interval > 300:
            errors.append(f"interval YOUTUBE tidak wajar: {interval}")
        if not youtube.get("proxies"):
            errors.append("YOUTUBE tidak punya kandidat proxy")

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

    # Dedicated playback and compatibility routes must precede broad blockers.
    ads_mrs = _find_rule(rules, "RULE-SET,ads_domain,REJECT")
    ads_idx = ads_mrs[0] if ads_mrs else 10**9

    for domain in COMPAT_DOMAINS:
        match = _find_rule(rules, f"DOMAIN,{domain},")
        if not match:
            errors.append(f"compatibility guard hilang: {domain}")
            continue
        idx, rule = match
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) < 3 or parts[2] != "YOUTUBE":
            errors.append(f"compatibility guard bukan YOUTUBE: {rule}")
        if idx >= ads_idx:
            errors.append(f"compatibility guard setelah ads_domain: {domain}")

    for domain in PLAYBACK_DOMAINS:
        match = _find_rule(rules, f"DOMAIN-SUFFIX,{domain},")
        if not match:
            errors.append(f"playback guard hilang: {domain}")
            continue
        idx, rule = match
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) < 3 or parts[2] != "YOUTUBE":
            errors.append(f"playback tidak menuju YOUTUBE: {rule}")
        if idx >= ads_idx:
            errors.append(f"playback guard setelah ads_domain: {domain}")

    # Router profiles should move the compact YouTube MRS into the same guard.
    if not is_android:
        match = _find_rule(rules, "RULE-SET,youtube_domain,")
        if not match:
            errors.append("RULE-SET youtube_domain hilang")
        else:
            idx, rule = match
            if rule != "RULE-SET,youtube_domain,YOUTUBE":
                errors.append(f"youtube_domain bukan YOUTUBE: {rule}")
            if idx >= ads_idx:
                errors.append("youtube_domain berada setelah ads_domain")

    # Exact ad endpoints under youtube.com must be rejected before the suffix
    # playback guard, otherwise DOMAIN-SUFFIX,youtube.com would shadow them.
    ad_yt = _find_rule(rules, "DOMAIN,ads.youtube.com,REJECT")
    yt_guard = _find_rule(rules, "DOMAIN-SUFFIX,youtube.com,YOUTUBE")
    if ad_yt and yt_guard and ad_yt[0] >= yt_guard[0]:
        errors.append("ads.youtube.com ter-shadow oleh youtube.com playback guard")

    for rule in rules:
        if rule == "DOMAIN-SUFFIX,doubleclick.net,REJECT":
            errors.append("doubleclick.net diblokir terlalu luas; static.doubleclick.net dibutuhkan sebagian playback")
        if rule.startswith("DOMAIN-SUFFIX,googlevideo.com,") and rule.endswith("REJECT"):
            errors.append("googlevideo.com terblokir")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit YouTube/adblock v3 AkunYaml")
    parser.add_argument("files", nargs="*", default=list(FILES))
    parser.add_argument("--mode", choices=("safe", "enhanced"), default="enhanced")
    parser.add_argument("--dedup", choices=("lean", "full"), default="lean")
    args = parser.parse_args()

    failed = False
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"[SKIP] {path}: tidak ada")
            continue
        errors = audit_file(path, args.mode == "enhanced", args.dedup == "lean")
        if errors:
            failed = True
            print(f"[ERROR] YouTube/adblock v3 audit: {path.name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[OK] YouTube/adblock v3 audit: {path.name}")

    filter_path = Path("youtube_browser_filters.txt")
    if filter_path.exists():
        text = filter_path.read_text(encoding="utf-8", errors="ignore")
        bad = []
        if "||googlevideo.com" in text:
            bad.append("googlevideo.com")
        if "||static.doubleclick.net" in text:
            bad.append("static.doubleclick.net")
        if bad:
            failed = True
            print("[ERROR] browser filter memblokir host playback/compatibility: " + ", ".join(bad))
        elif "||ads.youtube.com^$domain=youtube.com" not in text:
            failed = True
            print("[ERROR] browser filter ads.youtube.com belum ada")
        else:
            print("[OK] Browser filter menjaga playback dan menambah ads.youtube.com")
    else:
        print("[WARN] youtube_browser_filters.txt tidak ditemukan")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
