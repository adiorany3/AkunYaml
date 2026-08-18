#!/usr/bin/env python3
from __future__ import annotations

import copy
import os
import yaml

import sumberyaml_core as core


def make_node(name: str = "TEST") -> core.ProxyNode:
    clash = {
        "name": name,
        "type": "vless",
        "server": "192.0.2.10",
        "port": 443,
        "uuid": "11111111-1111-1111-1111-111111111111",
        "tls": True,
        "servername": "example.com",
        "network": "ws",
        "ws-opts": {"path": "/", "headers": {"Host": "example.com"}},
        "skip-cert-verify": True,
    }
    return core.ProxyNode(name, "vless", "example.com", 443, "vless://dummy", clash, output_server="", key=name)


def main() -> int:
    original_servers = core.TARGET_SERVERS
    original_mode = core.BUG_MODE
    original_cap = core.BUG_MAX_VARIANTS_PER_NODE
    original_total_cap = core.BUG_TOTAL_VARIANTS_CAP
    original_min_base = core.BUG_MIN_BASE_NODES
    try:
        core.TARGET_SERVERS = ("192.0.2.10", "192.0.2.11", "192.0.2.12")
        core.BUG_MODE = "fallback"
        core.BUG_MAX_VARIANTS_PER_NODE = 2
        core.BUG_TOTAL_VARIANTS_CAP = 24
        core.BUG_MIN_BASE_NODES = 8
        variants = core.expand_multi_host_variants([make_node()])
        assert len(variants) == 2, len(variants)
        assert [v.clash["server"] for v in variants] == ["192.0.2.10", "192.0.2.11"]
        assert len({v.clash["name"] for v in variants}) == 2

        core.BUG_MAX_VARIANTS_PER_NODE = 3
        capped = core.expand_multi_host_variants([make_node(f"N{i}") for i in range(10)])
        assert len(capped) == 24, len(capped)
        preserved = core.expand_multi_host_variants([make_node(f"P{i}") for i in range(30)])
        assert len(preserved) == 30, len(preserved)

        core.BUG_MODE = "distribute"
        distributed = core.expand_multi_host_variants([make_node("A"), make_node("B"), make_node("C")])
        servers = [v.clash["server"] for v in distributed]
        assert set(servers) == {"192.0.2.10", "192.0.2.11", "192.0.2.12"}, servers

        core.BUG_MODE = "primary"
        primary = core.expand_multi_host_variants([make_node()])
        assert len(primary) == 1
        print("[OK] multi-host parser/fallback/distribute/primary + global variant budget")
        return 0
    finally:
        core.TARGET_SERVERS = original_servers
        core.BUG_MODE = original_mode
        core.BUG_MAX_VARIANTS_PER_NODE = original_cap
        core.BUG_TOTAL_VARIANTS_CAP = original_total_cap
        core.BUG_MIN_BASE_NODES = original_min_base


if __name__ == "__main__":
    raise SystemExit(main())
