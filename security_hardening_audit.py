#!/usr/bin/env python3
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import yaml

import feed_guard
from security_policy import provider_catalog, provider_reject_rules

ROOT = Path(__file__).resolve().parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[OK] {message}")


def audit_single_source() -> None:
    core = (ROOT / "sumberyaml_core.py").read_text(encoding="utf-8")
    runner = (ROOT / "local_runner.py").read_text(encoding="utf-8")
    check("shared_security_provider_catalog" in core, "core uses shared security provider catalog")
    check("shared_provider_catalog" in runner, "local runner uses shared security provider catalog")
    check("ROUTER_THREAT_SAFE_SECURITY_PROVIDERS = {" not in runner, "runner no longer owns duplicate threat-safe provider definitions")


def audit_policy() -> None:
    router = provider_catalog(
        platform="router", profile="threat-safe", lite=False,
        indonesia_ads=True, threat_ip=True, interval=43200,
    )
    for name in ("threat-malware", "threat-phishing", "threat-cryptominers", "threat-fake-scam", "threat-tif-mini", "threat-tif-ip", "ads_indonesia"):
        check(name in router, f"router threat-safe provider present: {name}")
    lite = provider_catalog(
        platform="router", profile="threat-safe", lite=True,
        indonesia_ads=True, threat_ip=True, interval=43200,
    )
    check("threat-tif-ip" not in lite, "Lite skips IP threat provider")
    android = provider_catalog(
        platform="android", profile="threat-safe", indonesia_ads=True,
        threat_ip=False, android_snapshot_exists=True,
    )
    check(android.get("ads_indonesia", {}).get("type") == "file", "Android Indonesia provider uses local YAML snapshot")
    check(all(str(p.get("format") or "").lower() not in {"mrs", "text"} for p in android.values()), "Android security providers remain YAML/file compatible")

    rules = provider_reject_rules(
        platform="router", profile="threat-safe", lite=False,
        indonesia_ads=True, threat_ip=True,
    )
    positions = {name: next(i for i, r in enumerate(rules) if f"RULE-SET,{name}," in r) for name in ("threat-malware", "threat-phishing", "threat-tif-mini", "ads_indonesia", "ads_domain")}
    check(positions["threat-malware"] < positions["threat-tif-mini"] < positions["ads_indonesia"] < positions["ads_domain"], "threat providers stay ahead of regional/global ads")


def audit_outputs() -> None:
    for name in ("openclash_auto.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml", "openclash_android.yaml"):
        path = ROOT / name
        check(path.exists(), f"output exists: {name}")
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rules = [str(x) for x in cfg.get("rules", []) or []]
        check("DOMAIN-SUFFIX,doubleclick.net,REJECT" not in rules, f"no broad doubleclick suffix reject: {name}")
        check("DOMAIN,static.doubleclick.net,YOUTUBE" in rules or name == "openclash_android.yaml", f"YouTube compatibility guard retained: {name}")


def audit_feed_lkg() -> None:
    original_specs = feed_guard._feed_specs
    original_fetch = feed_guard._fetch
    old_drop = os.environ.get("FEED_MAX_DROP_RATIO")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feed_guard._feed_specs = lambda: [feed_guard.FeedSpec("test-feed", "https://invalid.local/test", "domain", 2)]
            feed_guard._fetch = lambda url, timeout=20: b"one.example\ntwo.example\n"
            report1 = feed_guard.refresh_security_feeds(root, refresh=True, log=lambda *_: None)
            check(report1["test-feed"]["status"] == "updated", "feed guard promotes a valid refresh")
            good = root / ".feed_cache" / "last_good" / "test-feed.txt"
            before = good.read_text(encoding="utf-8")

            feed_guard._fetch = lambda url, timeout=20: b"one.example\n"
            report2 = feed_guard.refresh_security_feeds(root, refresh=True, log=lambda *_: None)
            check(report2["test-feed"]["status"] == "last-known-good", "feed guard rejects suspicious/too-small refresh")
            check(good.read_text(encoding="utf-8") == before, "rejected refresh does not overwrite Last-Known-Good")
    finally:
        feed_guard._feed_specs = original_specs
        feed_guard._fetch = original_fetch
        if old_drop is None:
            os.environ.pop("FEED_MAX_DROP_RATIO", None)
        else:
            os.environ["FEED_MAX_DROP_RATIO"] = old_drop


def main() -> int:
    audit_single_source()
    audit_policy()
    audit_outputs()
    audit_feed_lkg()
    print("[OK] Security hardening audit complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
