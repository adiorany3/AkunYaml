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
AD_RULES = (
    "DOMAIN,adstatistics.av380.net,REJECT",
    "DOMAIN,logs.av380.net,REJECT",
    "DOMAIN,ad.av380.net,REJECT",
    "DOMAIN,ads.av380.net,REJECT",
    "DOMAIN,advert.av380.net,REJECT",
    "DOMAIN,advertising.av380.net,REJECT",
    "DOMAIN,promotion.av380.net,REJECT",
    "DOMAIN,promotions.av380.net,REJECT",
    "DOMAIN,app-ad.av380.net,REJECT",
    "DOMAIN,veepai-device-log.eye4.cn,REJECT",
    "DOMAIN,eulog.ezvizlife.com,REJECT",
    "DOMAIN,log.ezvizlife.com,REJECT",
    "DOMAIN,salog.ezvizlife.com,REJECT",
    "DOMAIN,sgplog.ezvizlife.com,REJECT",
    "DOMAIN,uslog.ezvizlife.com,REJECT",
    "DOMAIN,rum-apis.reolink.com,REJECT",
    "DOMAIN,sentry.tuyaus.com,REJECT",
    "DOMAIN,promotion-en.xmeye.net,REJECT",
)
SERVICE_RULE = "DOMAIN-SUFFIX,av380.net,DIRECT"
BROAD_VENDOR_REJECTS = {
    "DOMAIN-SUFFIX,av380.net,REJECT",
    "DOMAIN-SUFFIX,ezvizlife.com,REJECT",
    "DOMAIN-SUFFIX,reolink.com,REJECT",
    "DOMAIN-SUFFIX,tuyaus.com,REJECT",
    "DOMAIN-SUFFIX,xmeye.net,REJECT",
}
LAN_RULES = (
    "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve",
    "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
)

failed = False
for filename in FILES:
    config = yaml.safe_load((ROOT / filename).read_text(encoding="utf-8")) or {}
    rules = [str(rule) for rule in config.get("rules", []) or []]
    required = (*AD_RULES, SERVICE_RULE, *LAN_RULES)
    missing = [rule for rule in required if rule not in rules]
    broad_vendor_rejects = sorted(BROAD_VENDOR_REJECTS.intersection(rules))
    v380_ad_indexes = [rules.index(rule) for rule in AD_RULES if rule in rules and "av380.net" in rule]
    service_indexes = [rules.index(SERVICE_RULE)] if SERVICE_RULE in rules else []
    order_ok = not missing and bool(v380_ad_indexes) and max(v380_ad_indexes) < min(service_indexes)
    if missing or not order_ok or broad_vendor_rejects:
        failed = True
        print(f"[FAIL] {filename}: missing={missing}, v380-ad-before-service={order_ok}, broad-vendor-rejects={broad_vendor_rejects}")
    else:
        print(f"[OK] {filename}: V380 Pro LAN/cloud allowed; known ad/log hosts rejected first")

raise SystemExit(1 if failed else 0)
