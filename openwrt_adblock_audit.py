#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent


def check_order(rules:list[str], a:str, b:str, failures:list[str], name:str):
    try:
        ia=next(i for i,r in enumerate(rules) if r.startswith(a))
        ib=next(i for i,r in enumerate(rules) if r.startswith(b))
        if ia>=ib: failures.append(f'{name}: order salah {a} harus sebelum {b}')
    except StopIteration:
        failures.append(f'{name}: rule hilang untuk order {a} / {b}')


def main()->int:
    failures=[]
    cfg=json.loads((ROOT/'local_config.json').read_text())
    if cfg.get('OPENWRT_ADBLOCK_LEVEL')!='enhanced': failures.append('OPENWRT_ADBLOCK_LEVEL harus enhanced')
    if cfg.get('OPENWRT_LITE_ADBLOCK_LEVEL')!='compact': failures.append('OPENWRT_LITE_ADBLOCK_LEVEL harus compact')
    expected={
        'openclash_auto.yaml': {'hagezi-pro-plus-mini','popup-ads','ads_indonesia','ads_domain','tracker-domain'},
        'openclash_fresh_pool.yaml': {'hagezi-pro-plus-mini','popup-ads','ads_indonesia','ads_domain','tracker-domain'},
        'openclash_lite.yaml': {'popup-ads','ads_indonesia','ads_domain','tracker-domain'},
    }
    for name, needed in expected.items():
        d=yaml.safe_load((ROOT/name).read_text()) or {}
        providers=set((d.get('rule-providers') or {}).keys())
        missing=needed-providers
        if missing: failures.append(f'{name}: provider hilang {sorted(missing)}')
        if name=='openclash_lite.yaml' and 'hagezi-pro-plus-mini' in providers:
            failures.append('Lite tidak boleh memakai Pro++ Mini secara default')
        rules=[str(x) for x in d.get('rules',[]) or []]
        if name!='openclash_lite.yaml' and 'RULE-SET,hagezi-pro-plus-mini,REJECT' not in rules:
            failures.append(f'{name}: rule Pro++ Mini hilang')
        if 'RULE-SET,popup-ads,REJECT' not in rules:
            failures.append(f'{name}: popup rule hilang')
        check_order(rules,'RULE-SET,threat-malware,','RULE-SET,popup-ads,',failures,name)
        check_order(rules,'RULE-SET,popup-ads,','RULE-SET,ads_indonesia,',failures,name)
        check_order(rules,'RULE-SET,ads_indonesia,','RULE-SET,ads_domain,',failures,name)
        check_order(rules,'RULE-SET,ads_domain,','RULE-SET,tracker-domain,',failures,name)
        if any(r.startswith('DOMAIN-KEYWORD,') and r.endswith(',REJECT') for r in rules):
            failures.append(f'{name}: heuristic DOMAIN-KEYWORD REJECT terdeteksi')
    # Remove stale Android byte-hash assertion; Android has independent compatibility audits.
    # Feed Guard must include the enhanced text providers.
    import feed_guard
    specs={s.name for s in feed_guard._feed_specs()}
    for req in ('hagezi-pro-plus-mini','popup-ads','ads_indonesia'):
        if req not in specs: failures.append(f'feed_guard tidak memantau {req}')
    if failures:
        for f in failures: print('[FAIL]',f)
        return 1
    print('[OK] OpenWrt adblock: enhanced Auto/Fresh, compact Lite; Android diperiksa audit terpisah')
    return 0
if __name__=='__main__': raise SystemExit(main())
