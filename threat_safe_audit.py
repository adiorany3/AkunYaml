#!/usr/bin/env python3
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parent
FILES = ("openclash_auto.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml", "openclash_android.yaml")
BROAD_RISK = {
    "DOMAIN-SUFFIX,github.com,REJECT",
    "DOMAIN-SUFFIX,google.com,REJECT",
    "DOMAIN-SUFFIX,microsoft.com,REJECT",
    "DOMAIN-SUFFIX,apple.com,REJECT",
    "DOMAIN-SUFFIX,cloudflare.com,REJECT",
    "DOMAIN-SUFFIX,amazonaws.com,REJECT",
    "DOMAIN-SUFFIX,akamaized.net,REJECT",
    "DOMAIN-SUFFIX,googlevideo.com,REJECT",
}

failed = False
for name in FILES:
    path = BASE / name
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rules = [str(x) for x in cfg.get("rules", []) or []]
    providers = cfg.get("rule-providers", {}) or {}
    errors = []

    if name == "openclash_android.yaml":
        for provider in ("threat-malware", "threat-phishing", "threat-cryptominers"):
            if provider not in providers or f"RULE-SET,{provider},REJECT" not in rules:
                errors.append(f"missing Android provider/rule: {provider}")
        for pname, p in providers.items():
            if isinstance(p, dict):
                fmt = str(p.get("format") or "yaml").lower()
                if fmt == "mrs" or str(p.get("url") or "").lower().endswith(".mrs"):
                    errors.append(f"Android MRS provider: {pname}")
    else:
        for provider in ("threat-tif-mini", "threat-fake-scam"):
            if provider not in providers or f"RULE-SET,{provider},REJECT" not in rules:
                errors.append(f"missing router provider/rule: {provider}")
        if name == "openclash_lite.yaml":
            if "threat-tif-ip" in providers or any(str(r).startswith("RULE-SET,threat-tif-ip,") for r in rules):
                errors.append("Lite should not include TIF IP provider")
        else:
            p = providers.get("threat-tif-ip") or {}
            if p.get("behavior") != "ipcidr" or str(p.get("format") or "").lower() != "text":
                errors.append("TIF IP provider invalid/missing")
            if "RULE-SET,threat-tif-ip,REJECT,no-resolve" not in rules:
                errors.append("TIF IP rule missing")

    bad = sorted(BROAD_RISK.intersection(rules))
    if bad:
        errors.append(f"overbroad block rules: {bad}")

    if errors:
        failed = True
        print(f"[FAIL] {name}")
        for e in errors:
            print("  - " + e)
    else:
        mode = "domain-only" if name in {"openclash_lite.yaml", "openclash_android.yaml"} else "domain+IP"
        print(f"[OK] {name}: threat-safe {mode}")

raise SystemExit(1 if failed else 0)
