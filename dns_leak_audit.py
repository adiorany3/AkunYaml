#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
FILES = ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml")
PLAIN = {"1.1.1.1", "8.8.8.8", "9.9.9.9", "94.140.14.14"}
failed = False
for name in FILES:
    config = yaml.safe_load((ROOT / name).read_text(encoding="utf-8")) or {}
    dns = config.get("dns") or {}
    values = list(dns.get("nameserver") or []) + list(dns.get("fallback") or []) + list(dns.get("proxy-server-nameserver") or [])
    plain = sorted(PLAIN.intersection(str(value) for value in values))
    problems = []
    if dns.get("respect-rules") is not True:
        problems.append("respect-rules")
    if dns.get("use-system-hosts") is not False:
        problems.append("use-system-hosts")
    if plain:
        problems.append(f"plain-dns={plain}")
    if problems:
        failed = True
        print(f"[FAIL] {name}: {', '.join(problems)}")
    else:
        print(f"[OK] {name}: encrypted DNS and policy-aware resolution active")
raise SystemExit(1 if failed else 0)
