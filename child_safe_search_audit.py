#!/usr/bin/env python3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)
EXPECTED = {
    "www.google.com": "forcesafesearch.google.com",
    "www.google.co.id": "forcesafesearch.google.com",
    "www.youtube.com": "restrictmoderate.youtube.com",
    "m.youtube.com": "restrictmoderate.youtube.com",
    "youtubei.googleapis.com": "restrictmoderate.youtube.com",
    "youtube.googleapis.com": "restrictmoderate.youtube.com",
    "www.youtube-nocookie.com": "restrictmoderate.youtube.com",
}

failed = False
for filename in FILES:
    config = yaml.safe_load((ROOT / filename).read_text(encoding="utf-8")) or {}
    hosts = config.get("hosts") or {}
    missing = {domain: target for domain, target in EXPECTED.items() if hosts.get(domain) != target}
    if missing:
        failed = True
        print(f"[FAIL] {filename}: child-safe hosts missing={missing}")
    else:
        print(f"[OK] {filename}: Google SafeSearch + YouTube Restricted Mode forced")

raise SystemExit(1 if failed else 0)
