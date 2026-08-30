#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent
DOMAINS={
    "video-akpcw.spotifycdn.com",
    "805ba.v.fwmrm.net",
    "tvm-mtv-freewheel.akamaized.net",
    "adeventtracker.spotify.com",
    "ads.spotify.com",
    "adstudio.spotify.com",
    "aet.spotify.com",
    "analytics.spotify.com",
    "bloodhound.spotify.com",
    "crashdump.spotify.com",
    "pixel.spotify.com",
    "pixel-static.spotify.com",
    "pixels.spotify.com",
}
FILES=["openclash_auto.yaml","openclash_android.yaml","openclash_lite.yaml","openclash_fresh_pool.yaml"]

for name in FILES:
    cfg=yaml.safe_load((ROOT/name).read_text(encoding="utf-8")) or {}
    rules=[str(r) for r in cfg.get("rules",[]) or []]
    providers=cfg.get("rule-providers") or {}

    # v3 lean mode stores these three high-confidence hosts as direct rules.
    exact={r.split(",")[1] for r in rules if r.startswith("DOMAIN,") and r.endswith(",REJECT") and len(r.split(","))>=3}
    got=set(exact)

    # Full/legacy mode can still keep the inline provider.
    p=providers.get("streaming-ad-safe") or {}
    got.update(str(x) for x in p.get("payload",[]) or [])
    if p and "RULE-SET,streaming-ad-safe,REJECT" not in rules:
        raise SystemExit(f"[FAIL] {name}: streaming provider exists but is not referenced")

    missing=DOMAINS-got
    if missing:
        raise SystemExit(f"[FAIL] {name}: missing {sorted(missing)}")

    # Guard against high-risk broad blocks.
    bad=("DOMAIN-SUFFIX,spotifycdn.com,REJECT","DOMAIN-SUFFIX,scdn.co,REJECT","DOMAIN-SUFFIX,fwmrm.net,REJECT","DOMAIN-SUFFIX,akamaized.net,REJECT")
    if any(x in rules for x in bad):
        raise SystemExit(f"[FAIL] {name}: broad streaming CDN block detected")
    mode="inline-provider" if p else "lean-exact"
    print(f"[OK] {name}: conservative streaming layer active ({mode})")
