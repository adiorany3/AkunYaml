#!/usr/bin/env python3
import copy
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
    }
    try:
        core.TARGET_SERVERS = ("104.17.3.81", "104.17.2.81", "104.16.1.81")
        core.TARGET_SERVER = core.TARGET_SERVERS[0]
        core.ANDROID_MULTI_HOST_MODE = "primary-fallback"
        core.ANDROID_FALLBACK_HOST_LIMIT = 3
        core.ANDROID_FALLBACK_TOTAL_CAP = 24
        nodes = [make_node(1, 80), make_node(2, 120), make_node(3, 160)]
        text = core.build_openclash_android_yaml(nodes, 60, 40, "https://www.gstatic.com/generate_204", 5000)
        cfg = yaml.safe_load(text)
        proxies = cfg.get("proxies") or []
        groups = cfg.get("proxy-groups") or []
        proxy_server = {p["name"]: p["server"] for p in proxies}
        per_account = [g for g in groups if str(g.get("name", "")).endswith("-FB")]
        if len(per_account) != 3:
            raise AssertionError(f"expected 3 per-account fallback groups, got {len(per_account)}")
        expected = list(core.TARGET_SERVERS)
        for group in per_account:
            actual = [proxy_server[name] for name in group.get("proxies", [])]
            if actual != expected:
                raise AssertionError(f"primary/fallback order mismatch: {actual}")
        for outer_name in ("WARM-UP", "AUTO-FAST", "FALLBACK"):
            group = next(g for g in groups if g.get("name") == outer_name)
            if any("-H" in str(name) for name in group.get("proxies", [])):
                raise AssertionError(f"{outer_name} exposes raw host variants")
        auto = next(g for g in groups if g.get("name") == "AUTO-FAST")
        if not all(str(name).endswith("-FB") for name in auto.get("proxies", [])):
            raise AssertionError("AUTO-FAST must consume logical fallback nodes")
        print("[OK] Android primary host is always first")
        print("[OK] secondary hosts are per-account fallback only")
        print("[OK] outer health groups do not race raw host variants")
        return 0
    finally:
        for key, value in saved.items():
            setattr(core, key, value)


if __name__ == "__main__":
    sys.exit(main())
