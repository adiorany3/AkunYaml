#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--workdir',type=Path,default=Path('.')); args=ap.parse_args(); root=args.workdir
    failures=[]
    auto=yaml.safe_load((root/'openclash_auto.yaml').read_text()) or {}
    rules=[str(x) for x in auto.get('rules',[]) or []]
    inline=[x for x in rules if x.endswith(',MANUAL') and x.split(',',1)[0] in {'DOMAIN','DOMAIN-SUFFIX','DOMAIN-KEYWORD'}]
    if inline: failures.append(f'inline MANUAL rules remain: {len(inline)}')
    if 'RULE-SET,manual-routing,MANUAL' not in rules: failures.append('manual-routing RULE-SET missing')
    provider=(auto.get('rule-providers') or {}).get('manual-routing') or {}
    if provider.get('type')!='file' or provider.get('behavior')!='classical': failures.append('manual-routing provider invalid')
    payload_path=root/'rule_providers'/'manual-routing.yaml'
    if not payload_path.exists(): failures.append('manual-routing payload file missing')
    else:
        payload=(yaml.safe_load(payload_path.read_text()) or {}).get('payload',[])
        if len(payload)<250: failures.append(f'manual-routing payload unexpectedly small: {len(payload)}')
        if not any(str(x).startswith('DOMAIN-KEYWORD,') for x in payload): failures.append('keyword semantics not preserved')
    if len(rules)>=250: failures.append(f'auto rules not sufficiently compressed: {len(rules)}')
    android=yaml.safe_load((root/'openclash_android.yaml').read_text()) or {}
    if 'manual-routing' in (android.get('rule-providers') or {}): failures.append('manual provider leaked into Android')
    print('Optimization v4.8 audit:', 'OK' if not failures else 'FAIL')
    for x in failures: print(' -',x)
    return 0 if not failures else 1

if __name__=='__main__': raise SystemExit(main())
