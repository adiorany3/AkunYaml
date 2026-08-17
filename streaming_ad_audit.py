#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent
DOMAINS={
    "video-akpcw.spotifycdn.com",
    "805ba.v.fwmrm.net",
    "tvm-mtv-freewheel.akamaized.net",
}
FILES=["openclash_auto.yaml","openclash_android.yaml","openclash_lite.yaml","openclash_fresh_pool.yaml"]

for name in FILES:
    cfg=yaml.safe_load((ROOT/name).read_text(encoding="utf-8")) or {}
    rules=[str(r) for r in cfg.get("rules",[]) or []]
    providers=cfg.get("rule-providers") or {}
    if name=="openclash_android.yaml":
        got={r.split(",")[1] for r in rules if r.startswith("DOMAIN,") and r.endswith(",REJECT") and len(r.split(","))>=3}
        missing=DOMAINS-got
    else:
        p=providers.get("streaming-ad-safe") or {}
        got={str(x) for x in p.get("payload",[]) or []}
        missing=DOMAINS-got
        if "RULE-SET,streaming-ad-safe,REJECT" not in rules:
            raise SystemExit(f"[FAIL] {name}: streaming provider not referenced")
    if missing:
        raise SystemExit(f"[FAIL] {name}: missing {sorted(missing)}")
    # Guard against high-risk broad blocks.
    bad=("DOMAIN-SUFFIX,spotifycdn.com,REJECT","DOMAIN-SUFFIX,scdn.co,REJECT","DOMAIN-SUFFIX,fwmrm.net,REJECT","DOMAIN-SUFFIX,akamaized.net,REJECT")
    if any(x in rules for x in bad):
        raise SystemExit(f"[FAIL] {name}: broad streaming CDN block detected")
    print(f"[OK] {name}: conservative streaming layer active")
