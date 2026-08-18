#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
path = ROOT / 'openclash_android.yaml'
config = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
rules = [str(r) for r in config.get('rules', [])]
errors=[]

def idx(rule: str) -> int:
    try: return rules.index(rule)
    except ValueError: return -1

critical = [
    'RULE-SET,threat-malware,REJECT',
    'RULE-SET,threat-phishing,REJECT',
    'RULE-SET,threat-cryptominers,REJECT',
]
for r in critical:
    if idx(r) < 0: errors.append(f'missing critical threat rule: {r}')

guards = [
    'DOMAIN-SUFFIX,shopee.co.id,GLOBAL',
    'DOMAIN-SUFFIX,shopeemobile.com,GLOBAL',
    'DOMAIN-SUFFIX,susercontent.com,GLOBAL',
    'DOMAIN-SUFFIX,tokopedia.com,GLOBAL',
    'DOMAIN-SUFFIX,lazada.co.id,GLOBAL',
    'DOMAIN-SUFFIX,lazcdn.com,GLOBAL',
    'DOMAIN-SUFFIX,tiktokv.com,GLOBAL',
    'DOMAIN-SUFFIX,tiktokcdn.com,GLOBAL',
    'DOMAIN-SUFFIX,ibytedtos.com,GLOBAL',
    'DOMAIN-SUFFIX,byteimg.com,GLOBAL',
    'DOMAIN,business-api.tiktok.com,GLOBAL',
    'DOMAIN,log.byteoversea.com,GLOBAL',
]
for r in guards:
    if idx(r) < 0: errors.append(f'missing marketplace guard: {r}')

threat_end=max([idx(r) for r in critical] or [-1])
guard_indexes=[idx(r) for r in guards if idx(r)>=0]
if guard_indexes and min(guard_indexes) <= threat_end:
    errors.append('marketplace guard must run after critical threat rules')
for broad in ('RULE-SET,privacy-extra,REJECT','RULE-SET,ads_domain,REJECT','RULE-SET,tracker-domain,REJECT'):
    bi=idx(broad)
    if bi>=0 and guard_indexes and max(guard_indexes) >= bi:
        errors.append(f'marketplace guard must run before {broad}')

# Preserve TikTok ad blocking. Do not whitelist the whole tiktok.com suffix.
if 'DOMAIN-SUFFIX,tiktok.com,GLOBAL' in rules:
    errors.append('overbroad tiktok.com whitelist found')
if 'DOMAIN,ads.tiktok.com,REJECT' not in rules:
    errors.append('TikTok ad endpoint protection missing')

fake=set((config.get('dns') or {}).get('fake-ip-filter') or [])
for item in ('+.shopee.co.id','+.susercontent.com','+.tokopedia.com','+.lazada.co.id','+.tiktokv.com','+.tiktokcdn.com'):
    if item not in fake: errors.append(f'missing fake-ip bypass: {item}')

skip=set((config.get('sniffer') or {}).get('skip-domain') or [])
for item in ('+.shopee.co.id','+.susercontent.com','+.tokopedia.com','+.lazada.co.id','+.tiktokv.com'):
    if item not in skip: errors.append(f'missing sniffer skip: {item}')

policy=(config.get('dns') or {}).get('nameserver-policy') or {}
for item in ('+.shopee.co.id','+.susercontent.com','+.tokopedia.com','+.lazada.co.id','+.tiktokv.com'):
    if item not in policy: errors.append(f'missing normal DNS policy: {item}')

if errors:
    print('[ERROR] Android marketplace-live audit')
    for e in errors: print(' -',e)
    sys.exit(1)
print('[OK] Android marketplace-live compatibility audit')
print(f' guards={len(guards)} rules={len(rules)}')
