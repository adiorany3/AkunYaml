#!/usr/bin/env python3
import json
import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from generate_yaml import _build_singbox_android_json, _validate_singbox_json
from sumberyaml_core import ProxyNode, tls_bug_delay, ws_upgrade_delay


def node(name, **health):
    return SimpleNamespace(
        name=name, tier="MANUAL", type="vmess",
        clash={"type": "vmess", "server": "example.com", "port": 443,
               "uuid": "00000000-0000-4000-8000-000000000001", "cipher": "auto"},
        **health,
    )


def check(nodes, expected):
    config = json.loads(_build_singbox_android_json(nodes))
    groups = {item["tag"]: item for item in config["outbounds"]}
    manual = {n.name for n in nodes if n.tier == "MANUAL" and getattr(n, "tcp_reachable", None) is not False}
    assert "automatic" not in groups, groups
    assert {item["tag"] for item in config["outbounds"] if "server" in item} == manual
    for group in groups.values():
        if "outbounds" in group:
            assert group["outbounds"] and set(group["outbounds"]) <= groups.keys(), group
    proxy = next(item for item in config["outbounds"] if item["tag"] == "proxy")
    assert proxy["type"] == "selector" and proxy["default"] == "AUTO-FAST", proxy
    assert proxy["outbounds"][0] == "AUTO-FAST" and set(proxy["outbounds"][1:]) == manual, proxy
    auto = next(item for item in config["outbounds"] if item["tag"] == "AUTO-FAST")
    assert auto["type"] == "urltest" and set(auto["outbounds"]) == manual, auto
    for tag in ("BANK", "SOCIAL", "VMESS-VIDEO"):
        group = next(item for item in config["outbounds"] if item["tag"] == tag)
        assert group == {"type": "selector", "tag": tag, "outbounds": ["proxy"], "default": "proxy"}, group
    remote_rule_sets = config["route"]["rule_set"]
    assert {item["tag"] for item in remote_rule_sets} == {"ads-domain", "tracker-domain"}
    assert all(item["type"] == "remote" and item["format"] == "binary" for item in remote_rule_sets)
    assert all(item["url"].endswith(".srs") and item["update_interval"] == "12h" for item in remote_rule_sets)
    remote_reject = next(rule for rule in config["route"]["rules"] if "rule_set" in rule)
    assert remote_reject == {"rule_set": ["ads-domain", "tracker-domain"], "action": "reject"}
    _validate_singbox_json(json.dumps(config), os.getenv("SINGBOX_PATH", ".local_bin/sing-box"))
    return config


def main():
    failed = node("failed", url_test_success=False, url_test_status="HTTP 500")
    skipped = node("skipped", url_test_success=True, url_test_status="skipped-disabled")
    healthy = node("healthy", url_test_success=True, url_test_status="HTTP 204")
    other = node("other", url_test_success=True, url_test_status="HTTP 200")
    check([failed, skipped, healthy, other], "healthy")
    check([other, healthy, failed], "other")
    check([skipped, failed], "skipped")
    check([node("unknown"), failed], "unknown")
    check([failed], "failed")
    primary = node("primary")
    primary.tier = "PRIMARY"
    check([primary, failed, healthy], "healthy")
    tcp_failed = node("tcp-failed", tcp_reachable=False)
    tcp_passed = node("tcp-passed", tcp_reachable=True, status="dead")
    tcp_skipped = node("tcp-skipped", tcp_reachable=None)
    check([tcp_failed, tcp_passed, tcp_skipped], "tcp-passed")
    for probe in (tls_bug_delay, ws_upgrade_delay):
        sample = ProxyNode("probe", "vmess", "example.com", 443, "", dict(tcp_passed.clash))
        with patch("sumberyaml_core.socket.create_connection", side_effect=OSError("unreachable")):
            probe(sample, 0.1, 1)
        assert sample.tcp_reachable is False
        with patch("sumberyaml_core.socket.create_connection", return_value=MagicMock()), patch(
            "sumberyaml_core.ssl.create_default_context"
        ) as context:
            context.return_value.wrap_socket.side_effect = OSError("TLS failed, TCP passed")
            probe(sample, 0.1, 1)
        assert sample.tcp_reachable is True
        with patch("sumberyaml_core.socket.create_connection", side_effect=OSError("next host failed")):
            probe(sample, 0.1, 1)
        assert sample.tcp_reachable is True, "Any reachable target must survive later failures"
    unsupported = node("unsupported")
    unsupported.clash["type"] = "ss"
    invalid = node("invalid")
    invalid.clash.pop("uuid")
    for nodes in ([], [primary], [primary, unsupported], [invalid], [tcp_failed], [primary, tcp_failed]):
        try:
            _build_singbox_android_json(nodes)
        except ValueError as exc:
            assert "tidak ada node manual" in str(exc), exc
        else:
            raise AssertionError("No supported manual nodes must fail without automatic fallback")
    print("PASS: healthy manual priority, stable order, skipped/unknown fallback, account retention")
    print("PASS: mixed input excludes automatic nodes, no supported manual fails, real sing-box check")
    print("PASS: TCP failures excluded; TCP pass, skipped and untested retained; TLS failure is not TCP failure")


if __name__ == "__main__":
    main()