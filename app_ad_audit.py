#!/usr/bin/env python3
from pathlib import Path
import yaml
import local_runner as lr

BASE = Path(__file__).resolve().parent
FILES = ["openclash_auto.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml", "openclash_android.yaml"]
BROAD_BAD = {
    "DOMAIN-SUFFIX,googlevideo.com,REJECT",
    "DOMAIN-SUFFIX,spotifycdn.com,REJECT",
    "DOMAIN-SUFFIX,akamaized.net,REJECT",
    "DOMAIN-SUFFIX,microsoft.com,REJECT",
    "DOMAIN-SUFFIX,apple.com,REJECT",
    "DOMAIN-SUFFIX,xiaomi.com,REJECT",
    "DOMAIN-SUFFIX,heytapmobile.com,REJECT",
}
failed = False
for name in FILES:
    d = yaml.safe_load((BASE/name).read_text()) or {}
    rules = [str(x) for x in d.get("rules", []) or []]
    providers = d.get("rule-providers", {}) or {}
    if name == "openclash_android.yaml":
        missing_exact = [x for x in lr.APP_SAFE_EXACT_DOMAINS if f"DOMAIN,{x},REJECT" not in rules]
        missing_suffix = [x for x in lr.APP_SAFE_SUFFIXES if f"DOMAIN-SUFFIX,{x},REJECT" not in rules]
        mrs = [k for k,v in providers.items() if isinstance(v,dict) and (str(v.get("format","")).lower()=="mrs" or str(v.get("url","")).lower().endswith(".mrs"))]
        ok = not missing_exact and not missing_suffix and not mrs
    else:
        p = providers.get("app-ad-safe") or {}
        payload = p.get("payload") or []
        expected = list(lr.APP_SAFE_EXACT_DOMAINS) + [f".{x}" for x in lr.APP_SAFE_SUFFIXES]
        ok = p.get("type") == "inline" and p.get("behavior") == "domain" and all(x in payload for x in expected) and "RULE-SET,app-ad-safe,REJECT" in rules
    bad = sorted(BROAD_BAD.intersection(rules))
    if not ok or bad:
        failed = True
        print(f"[FAIL] {name}: app-safe={ok}, broad_bad={bad}")
    else:
        print(f"[OK] {name}: {len(lr.APP_SAFE_EXACT_DOMAINS)} exact + {len(lr.APP_SAFE_SUFFIXES)} suffix app-ad targets")
raise SystemExit(1 if failed else 0)
