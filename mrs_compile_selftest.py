#!/usr/bin/env python3
from __future__ import annotations
import os
import stat
import tempfile
from pathlib import Path

from mrs_compile import apply_compiled_mrs, compile_lkg_to_mrs


def main() -> int:
    old = os.environ.get('MIHOMO_PATH')
    old_mode = os.environ.get('MRS_COMPILE')
    try:
        with tempfile.TemporaryDirectory(prefix='mrs-selftest-') as td:
            root=Path(td)
            src=root/'.feed_cache'/'last_good'/'test-domain.txt'
            src.parent.mkdir(parents=True,exist_ok=True)
            src.write_text('example.com\n.example.net\n',encoding='utf-8')
            fake=root/'mihomo'
            fake.write_text('''#!/usr/bin/env python3\nimport pathlib,sys\nif '-v' in sys.argv:\n print('Mihomo Meta alpha-ge183c58'); raise SystemExit(0)\nif len(sys.argv)>=6 and sys.argv[1]=='convert-ruleset':\n pathlib.Path(sys.argv[5]).write_bytes(b'MRS-SELFTEST\\n'+pathlib.Path(sys.argv[4]).read_bytes()); raise SystemExit(0)\nraise SystemExit(2)\n''',encoding='utf-8')
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
            os.environ['MIHOMO_PATH']=str(fake)
            os.environ['MRS_COMPILE']='auto'
            report={'test-domain':{'status':'cached','path':'.feed_cache/last_good/test-domain.txt','count':2}}
            catalog={'test-domain':{'type':'http','behavior':'domain','format':'text','path':'./rule_providers/test.txt','url':'https://example.invalid/test.txt'}}
            result=compile_lkg_to_mrs(root,report,catalog,log=lambda *_:None)
            if result.get('test-domain',{}).get('status')!='compiled':
                print('FAIL compile',result); return 1
            cfg={'rule-providers':{'test-domain':catalog['test-domain'].copy()}}
            changed=apply_compiled_mrs(cfg,root,result)
            p=cfg['rule-providers']['test-domain']
            ok=changed==1 and p.get('type')=='file' and p.get('format')=='mrs' and (root/p['path'].removeprefix('./')).exists()
            print('OK' if ok else 'FAIL',p)
            return 0 if ok else 1
    finally:
        if old is None: os.environ.pop('MIHOMO_PATH',None)
        else: os.environ['MIHOMO_PATH']=old
        if old_mode is None: os.environ.pop('MRS_COMPILE',None)
        else: os.environ['MRS_COMPILE']=old_mode

if __name__=='__main__': raise SystemExit(main())
