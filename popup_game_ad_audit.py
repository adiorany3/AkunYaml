#!/usr/bin/env python3
from pathlib import Path
import yaml

SUFFIXES = (
    "popads.net","popcash.net","propellerads.com","adsterra.com","onclickalgo.com",
    "onclickperformance.com","hilltopads.net","richads.com","clickadu.com","adcash.com",
    "applovin.com","applvn.com","unityads.unity3d.com","supersonicads.com","ironsrc.com",
    "vungle.com","vunglecloud.com","chartboost.com","inmobi.com","adcolony.com",
    "mintegral.com","mtgglobals.com","rayjump.com","pangle.io","pangleglobal.com",
    "tapjoy.com","tapjoyads.com","startappservice.com","startapp.com","fyber.com","inner-active.mobi",
    "adpushup.com","adroll.com","taboola.com","outbrain.com","criteo.com","revcontent.com",
    "yieldmo.com","pubmatic.com","rubiconproject.com","openx.net","smartadserver.com",
    "mgid.com","trafficjunky.net","adnxs.com","appnext.com","adform.net","smaato.net",
    "smartclip.net","pushengage.com","onesignal.com","webpushr.com",
)
FILES=("openclash_auto.yaml","openclash_lite.yaml","openclash_fresh_pool.yaml","openclash_android.yaml")
BAD=("DOMAIN-SUFFIX,googlevideo.com,REJECT","DOMAIN-SUFFIX,spotifycdn.com,REJECT","DOMAIN-SUFFIX,akamaized.net,REJECT")
root=Path(__file__).resolve().parent
failed=False
for fn in FILES:
    p=root/fn
    cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    rules=set(map(str,cfg.get("rules",[]) or []))
    missing=[d for d in SUFFIXES if f"DOMAIN-SUFFIX,{d},REJECT" not in rules]
    broad=[r for r in BAD if r in rules]
    if missing or broad:
        failed=True
        print(f"[FAIL] {fn}: missing={len(missing)} broad={broad}")
        for d in missing[:10]: print("  missing",d)
    else:
        print(f"[OK] {fn}: {len(SUFFIXES)}/{len(SUFFIXES)} intrusive-ad suffixes, no broad media CDN block")
raise SystemExit(1 if failed else 0)
