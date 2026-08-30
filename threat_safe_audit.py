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
        for provider in (
            "threat-malware",
            "threat-phishing",
            "threat-cryptominers",
            "threat-fake-scam",
            "threat-tif-mini",
        ):
            if provider not in providers or f"RULE-SET,{provider},REJECT" not in rules:
                errors.append(f"missing router provider/rule: {provider}")

        # Precision ordering: explicit active-threat categories must be checked
        # before the broader TIF safety net and before ad/tracker providers.
        order = [
            "RULE-SET,threat-malware,REJECT",
            "RULE-SET,threat-phishing,REJECT",
            "RULE-SET,threat-cryptominers,REJECT",
            "RULE-SET,threat-fake-scam,REJECT",
            "RULE-SET,threat-tif-mini,REJECT",
        ]
        positions = [rules.index(x) for x in order if x in rules]
        if len(positions) == len(order) and positions != sorted(positions):
            errors.append("precision threat rule order invalid")
        for ad_rule in ("RULE-SET,ads_domain,REJECT", "RULE-SET,tracker-domain,REJECT"):
            if ad_rule in rules and positions and rules.index(ad_rule) < positions[-1]:
                errors.append(f"{ad_rule} must run after threat precision layer")
        if name == "openclash_lite.yaml":
            if "threat-tif-ip" in providers or any(str(r).startswith("RULE-SET,threat-tif-ip,") for r in rules):
                errors.append("Lite should not include TIF IP provider")
        else:
            p = providers.get("threat-tif-ip") or {}
            provider_type = str(p.get("type") or "").lower()
            provider_format = str(p.get("format") or "").lower()
            valid_remote = provider_type == "http" and provider_format == "text"
            valid_compiled = provider_type == "file" and provider_format == "mrs"
            if p.get("behavior") != "ipcidr" or not (valid_remote or valid_compiled):
                errors.append("TIF IP provider invalid/missing")
            if valid_compiled:
                local_path = BASE / str(p.get("path") or "").removeprefix("./")
                if not local_path.is_file() or local_path.stat().st_size == 0:
                    errors.append("compiled TIF IP provider file missing/empty")
            if "RULE-SET,threat-tif-ip,REJECT,no-resolve" not in rules:
                errors.append("TIF IP rule missing")

    # Avoid heuristic keyword rejects in a precision profile. Category-aware
    # providers/DNS are safer than broad string matching.
    keyword_rejects = [r for r in rules if r.startswith("DOMAIN-KEYWORD,") and r.endswith(",REJECT")]
    if keyword_rejects:
        errors.append(f"overbroad keyword reject rules: {len(keyword_rejects)}")

    # Threat-safe intentionally enforces the category-safe resolver. This keeps
    # restricted-site filtering out of the YAML domain payload and avoids a huge
    # runtime rule-provider.
    dns = cfg.get("dns") or {}
    expected_family = [
        "https://family.dns.bebasid.com/dns-query",
        "tls://family.dns.bebasid.com:853",
    ]
    if dns.get("nameserver") != expected_family:
        errors.append("threat-safe family DNS is not enforced")
    if "fallback" in dns and dns.get("fallback") != expected_family:
        errors.append("threat-safe fallback DNS can bypass category filtering")

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
