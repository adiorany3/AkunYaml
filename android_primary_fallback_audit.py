#!/usr/bin/env python3
"""Regression audit for Android v4.2 H1-primary + cold H2/H3 fallback."""
import os
import sys
import yaml
import sumberyaml_core as core


def make_node(i: int, delay: int) -> core.ProxyNode:
    name = f"AKUN-{i:03d}-CF-{delay}MS"
    clash = {
        "name": name,
        "type": "vless",
        "server": "origin.example",
        "port": 443,
        "uuid": f"00000000-0000-0000-0000-{i:012d}",
        "udp": True,
        "tls": True,
        "servername": "example.com",
        "network": "ws",
        "client-fingerprint": "chrome",
        "skip-cert-verify": True,
        "ws-opts": {"path": "/", "headers": {"Host": "example.com"}},
    }
    return core.ProxyNode(
        name=name,
        type="vless",
        original_server="origin.example",
        port=443,
        raw="",
        clash=clash,
        best_delay_ms=delay,
        bug_best_delay_ms=delay,
        score=delay,
    )


def main() -> int:
    saved = {
        "TARGET_SERVERS": core.TARGET_SERVERS,
        "TARGET_SERVER": core.TARGET_SERVER,
        "ANDROID_MULTI_HOST_MODE": core.ANDROID_MULTI_HOST_MODE,
        "ANDROID_FALLBACK_HOST_LIMIT": core.ANDROID_FALLBACK_HOST_LIMIT,
        "ANDROID_FALLBACK_TOTAL_CAP": core.ANDROID_FALLBACK_TOTAL_CAP,
        "ANDROID_FALLBACK_INTERVAL": core.ANDROID_FALLBACK_INTERVAL,
        "ANDROID_FALLBACK_LAZY": core.ANDROID_FALLBACK_LAZY,
        "ANDROID_GLOBAL_FALLBACK_INTERVAL": core.ANDROID_GLOBAL_FALLBACK_INTERVAL,
        "ANDROID_GLOBAL_FALLBACK_LAZY": core.ANDROID_GLOBAL_FALLBACK_LAZY,
        "ANDROID_AUTO_FAST_LAZY": core.ANDROID_AUTO_FAST_LAZY,
    }
    old_profile = os.environ.get("ADBLOCK_PROFILE")
    try:
        core.TARGET_SERVERS = ("104.17.3.81", "104.17.2.81", "104.16.1.81")
        core.TARGET_SERVER = core.TARGET_SERVERS[0]
        core.ANDROID_MULTI_HOST_MODE = "primary-cold-fallback"
        core.ANDROID_FALLBACK_HOST_LIMIT = 3
        core.ANDROID_FALLBACK_TOTAL_CAP = 24
        core.ANDROID_FALLBACK_INTERVAL = 300
        core.ANDROID_FALLBACK_LAZY = True
        core.ANDROID_GLOBAL_FALLBACK_INTERVAL = 180
        core.ANDROID_GLOBAL_FALLBACK_LAZY = True
        core.ANDROID_AUTO_FAST_LAZY = True
        os.environ["ADBLOCK_PROFILE"] = "off"

        nodes = [make_node(i, 70 + i * 10) for i in range(1, 11)]
        text = core.build_openclash_android_yaml(nodes, 60, 40, "https://www.gstatic.com/generate_204", 5000)
        cfg = yaml.safe_load(text)
        proxies = cfg.get("proxies") or []
        groups = cfg.get("proxy-groups") or []
        by_name = {g.get("name"): g for g in groups if isinstance(g, dict)}

        if cfg.get("mode") != "rule":
            raise AssertionError(f"Android must remain in rule mode, got {cfg.get('mode')!r}")
        if not (cfg.get("rules") or []) or (cfg.get("rules") or [])[-1] != "MATCH,GLOBAL":
            raise AssertionError("Android rule mode must end in MATCH,GLOBAL even with adblock off")

        # 10 H1 + 10 H2 + 4 H3 = cap 24. H1 is never removed.
        if len(proxies) != 24:
            raise AssertionError(f"expected 24 physical proxies under cap, got {len(proxies)}")
        servers = [p.get("server") for p in proxies]
        if servers.count(core.TARGET_SERVERS[0]) != 10:
            raise AssertionError("every base account must retain exactly one H1 primary")
        if servers.count(core.TARGET_SERVERS[1]) != 10 or servers.count(core.TARGET_SERVERS[2]) != 4:
            raise AssertionError("backup allocation must fill H2 before H3")

        if any(str(g.get("name", "")).endswith("-FB") for g in groups):
            raise AssertionError("per-account fallback groups must not exist in v4.2")

        h2 = by_name.get("ANDROID-BACKUP-H2")
        h3 = by_name.get("ANDROID-BACKUP-H3")
        cold = by_name.get("ANDROID-COLD-BACKUP")
        if not h2 or not h3 or not cold:
            raise AssertionError("host-level cold backup groups H2/H3 are required")
        if cold.get("proxies") != ["ANDROID-BACKUP-H2", "ANDROID-BACKUP-H3"]:
            raise AssertionError(f"cold backup host priority changed: {cold.get('proxies')}")
        for group in (h2, h3, cold):
            if group.get("lazy") is not True:
                raise AssertionError(f"{group.get('name')} must be lazy/cold")

        # Normal groups must contain primary account labels only.
        for outer_name in ("WARM-UP", "WARM-UP-CF", "AUTO-FAST", "STREAMING-FAST", "FALLBACK", "PING-CHECK"):
            group = by_name.get(outer_name)
            if not group:
                continue
            refs = [str(x) for x in group.get("proxies", [])]
            if any("-H2" in x or "-H3" in x or x.startswith("ANDROID-BACKUP-") for x in refs):
                raise AssertionError(f"{outer_name} leaked secondary-host endpoints: {refs}")

        global_group = by_name.get("GLOBAL")
        if not global_group or global_group.get("type") != "fallback":
            raise AssertionError("GLOBAL must be a shallow fallback")
        if global_group.get("proxies") != ["WARM-UP", "AUTO-FAST", "ANDROID-COLD-BACKUP"]:
            raise AssertionError(f"GLOBAL topology is not shallow/ordered: {global_group.get('proxies')}")
        if global_group.get("lazy") is not True or int(global_group.get("interval") or 0) < 180:
            raise AssertionError("GLOBAL fallback must be lazy and low-frequency")
        if by_name["WARM-UP"].get("lazy") is not False:
            raise AssertionError("WARM-UP must remain the only hot primary pool")
        if by_name["AUTO-FAST"].get("lazy") is not True:
            raise AssertionError("AUTO-FAST must be lazy on Android v4.2")

        print("[OK] Android H1 is the only normal-routing host")
        print("[OK] H2/H3 are grouped as lazy host-level cold backup")
        print("[OK] no per-account nested fallback remains")
        print("[OK] GLOBAL is shallow, lazy, and ordered primary -> cold backup")
        print("[OK] Android remains in rule mode even when adblock is off")
        return 0
    finally:
        for key, value in saved.items():
            setattr(core, key, value)
        if old_profile is None:
            os.environ.pop("ADBLOCK_PROFILE", None)
        else:
            os.environ["ADBLOCK_PROFILE"] = old_profile


if __name__ == "__main__":
    sys.exit(main())
