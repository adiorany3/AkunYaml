#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
FILES = ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml")
REQUIRED = {
    "https://1.1.1.1/dns-query",
    "https://dns.google/dns-query",
    "https://dns.quad9.net/dns-query",
}
failed = False
for name in FILES:
    config = yaml.safe_load((ROOT / name).read_text(encoding="utf-8")) or {}
    dns = config.get("dns") or {}
    fallback = set(dns.get("fallback") or [])
    proxy = set(dns.get("proxy-server-nameserver") or [])
    missing = sorted(REQUIRED - (fallback | proxy))
    if missing or dns.get("fallback-lazy-query") is not False:
        failed = True
        print(f"[FAIL] {name}: missing={missing}, fallback-lazy-query={dns.get('fallback-lazy-query')}")
    else:
        print(f"[OK] {name}: adaptive resolver pool active")
raise SystemExit(1 if failed else 0)
