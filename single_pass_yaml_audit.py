#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path

import yaml
import local_runner


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,default=Path('.'))
    args=parser.parse_args()
    root=args.workdir.resolve()
    cfg=json.loads((root/'local_config.json').read_text())
    for k,v in cfg.items():
        os.environ[k]=json.dumps(v) if isinstance(v,(list,dict)) else str(v)
    os.environ['REFERENCE_PROFILE_MODE']='off'
    os.environ['MRS_COMPILE']='off'
    src=root/'openclash_lite.yaml'
    if not src.exists():
        raise SystemExit('openclash_lite.yaml missing')
    with tempfile.TemporaryDirectory(prefix='single-pass-audit-') as td:
        td=Path(td)
        for fn in ['openclash_lite.yaml']:
            shutil.copy2(root/fn,td/fn)
        local_runner.optimize_outputs(td,['openclash_lite.yaml'],cfg.get('ADBLOCK_PROFILE','threat-safe'),int(cfg.get('ADBLOCK_PROVIDER_INTERVAL','43200')),cfg.get('ADBLOCK_DNS_MODE','off'),cfg.get('YOUTUBE_ADBLOCK_MODE','enhanced'),cfg.get('YOUTUBE_BROWSER_FILTER_FILE','youtube_browser_filters.txt'))
        stats=local_runner.yaml_transaction_stats(td/'openclash_lite.yaml')
        ok=stats.get('loads')==1 and stats.get('writes',0)<=1
        print(('OK' if ok else 'FAIL'),stats)
        return 0 if ok else 1

if __name__=='__main__':
    raise SystemExit(main())
