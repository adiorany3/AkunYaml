#!/usr/bin/env python3
from pathlib import Path
import yaml

EXCLUDE={"static.doubleclick.net"}
ROOT=Path(__file__).resolve().parent

def source_domains():
    out=[]
    for raw in (ROOT/'turtlecute_d3host.txt').read_text(encoding='utf-8',errors='ignore').splitlines():
        line=raw.strip()
        if not line or line.startswith('#'): continue
        parts=line.split()
        if len(parts)>=2 and parts[0] in {'0.0.0.0','127.0.0.1'}:
            d=parts[1].lower().rstrip('.')
            if d not in out: out.append(d)
    return out

def covered(path, domains):
    cfg=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    providers=cfg.get('rule-providers') or {}
    inline=set()
    p=providers.get('turtlecute-coverage') or {}
    for d in p.get('payload') or []: inline.add(str(d).lower())
    exact=set()
    for r in cfg.get('rules') or []:
        parts=str(r).split(',')
        if len(parts)>=3 and parts[0]=='DOMAIN' and parts[2]=='REJECT':
            exact.add(parts[1].lower())
    return cfg, [d for d in domains if d in inline or d in exact], bool(p)

domains=source_domains()
expected=[d for d in domains if d not in EXCLUDE]
for name in ['openclash_auto.yaml','openclash_android.yaml','openclash_lite.yaml','openclash_fresh_pool.yaml']:
    p=ROOT/name
    cfg, got, has_benchmark=covered(p,expected)
    rules=[str(r) for r in cfg.get('rules') or []]
    if has_benchmark:
        missing=sorted(set(expected)-set(got))
        print(f'{name}: {len(got)}/{len(expected)} benchmark hosts covered (full mode)')
        if missing:
            print('  missing:', ', '.join(missing))
            raise SystemExit(1)
    else:
        # v3 lean mode deliberately removes the benchmark-only provider. The
        # production MRS ad/tracker providers remain authoritative.
        provider_names=set((cfg.get('rule-providers') or {}).keys())
        if not {'ads_domain','tracker-domain'}.issubset(provider_names):
            raise SystemExit(f'{name}: lean mode missing ads_domain/tracker-domain')
        if 'DOMAIN,static.doubleclick.net,REJECT' in rules or 'DOMAIN-SUFFIX,doubleclick.net,REJECT' in rules:
            raise SystemExit(f'{name}: compatibility host/tree is overblocked')
        print(f'{name}: benchmark provider intentionally disabled (lean mode); MRS ads+tracker active')
print(f'Intentionally excluded for compatibility: {", ".join(sorted(EXCLUDE))}')
