#!/usr/bin/env python3
from pathlib import Path
import hashlib
import yaml

ROUTER_FILES = [
    Path('openclash_auto.yaml'),
    Path('openclash_lite.yaml'),
    Path('openclash_fresh_pool.yaml'),
]
ANDROID = Path('openclash_android.yaml')
PROVIDER = 'gambling-mini'
RULE = 'RULE-SET,gambling-mini,REJECT'
PLAYBACK_SAFE = ('googlevideo.com', 'static.doubleclick.net', 'ytimg.com', 'youtubei.googleapis.com', 'youtube.googleapis.com')


def fail(msg: str) -> None:
    raise SystemExit(f'[FAIL] {msg}')

for path in ROUTER_FILES:
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    providers = data.get('rule-providers') or {}
    rules = [str(x) for x in (data.get('rules') or [])]
    provider = providers.get(PROVIDER)
    if not isinstance(provider, dict):
        fail(f'{path}: provider {PROVIDER} missing')
    if str(provider.get('behavior')) != 'domain' or str(provider.get('format')) != 'text':
        fail(f'{path}: provider format/behavior invalid')
    if RULE not in rules:
        fail(f'{path}: gambling reject rule missing')
    idx = rules.index(RULE)
    tif = next((i for i,r in enumerate(rules) if r.startswith('RULE-SET,threat-tif-mini,')), -1)
    broad_ad = next((i for i,r in enumerate(rules) if r.startswith(('RULE-SET,hagezi-pro-plus-mini,','RULE-SET,popup-ads,','RULE-SET,ads_indonesia,','RULE-SET,ads_domain,','RULE-SET,tracker-domain,'))), len(rules))
    if tif >= 0 and idx <= tif:
        fail(f'{path}: gambling rule must follow threat TIF')
    if idx >= broad_ad:
        fail(f'{path}: gambling rule must precede broad ad/tracker providers')
    for host in PLAYBACK_SAFE:
        if any(host in r.lower() and ',reject' in r.lower() for r in rules):
            fail(f'{path}: playback host rejected: {host}')
    if any(r.upper().startswith('DOMAIN-KEYWORD,') and any(k in r.lower() for k in ('gambl','casino','slot','bet')) for r in rules):
        fail(f'{path}: overbroad gambling keyword rule found')
    print(f'[OK] {path}: gambling sponsor destination guard active')

data = yaml.safe_load(ANDROID.read_text(encoding='utf-8')) or {}
if PROVIDER in (data.get('rule-providers') or {}):
    fail('Android unexpectedly received router gambling provider')
if RULE in [str(x) for x in (data.get('rules') or [])]:
    fail('Android unexpectedly received router gambling rule')
base = Path('v47_android_baseline_sha256.txt').read_text().strip()
cur = hashlib.sha256(ANDROID.read_bytes()).hexdigest()
if base != cur:
    fail('Android output changed')
print('[OK] Android remains byte-identical and outside router gambling layer')
print('[OK] YouTube gambling sponsor guard v4.7 audit')
