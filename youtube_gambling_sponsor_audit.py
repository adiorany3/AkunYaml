#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
ROUTER_FILES = [
    ROOT / 'openclash_auto.yaml',
    ROOT / 'openclash_lite.yaml',
    ROOT / 'openclash_fresh_pool.yaml',
]
ANDROID = ROOT / 'openclash_android.yaml'
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
        fail(f'{path.name}: provider {PROVIDER} missing')
    provider_type = str(provider.get('type') or '').lower()
    provider_format = str(provider.get('format') or '').lower()
    valid_remote = provider_type == 'http' and provider_format == 'text'
    valid_compiled = provider_type == 'file' and provider_format == 'mrs'
    if str(provider.get('behavior')) != 'domain' or not (valid_remote or valid_compiled):
        fail(f'{path.name}: provider format/behavior invalid')
    if valid_compiled:
        local_path = ROOT / str(provider.get('path') or '').removeprefix('./')
        if not local_path.is_file() or local_path.stat().st_size == 0:
            fail(f'{path.name}: compiled gambling provider missing/empty')
    if RULE not in rules:
        fail(f'{path.name}: gambling reject rule missing')
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
print('[OK] Android remains outside router-only gambling layer')
print('[OK] YouTube gambling sponsor guard audit')
