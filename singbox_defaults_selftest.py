#!/usr/bin/env python3
import json
import os
from types import SimpleNamespace

from generate_yaml import _build_singbox_android_json, _validate_singbox_json


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
    manual = {n.name for n in nodes if n.tier == "MANUAL"}
    assert "automatic" not in groups, groups
    assert {item["tag"] for item in config["outbounds"] if "server" in item} == manual
    for group in groups.values():
        if "outbounds" in group:
            assert group["outbounds"] and set(group["outbounds"]) <= groups.keys(), group
    for tag in ("proxy", "BANK", "SOCIAL", "VMESS-VIDEO"):
        group = next(item for item in config["outbounds"] if item["tag"] == tag)
        assert group["type"] == "selector", group
        assert group["default"] == expected, (tag, group["default"], expected)
        assert group["outbounds"][0] == expected, group
        assert manual == set(group["outbounds"]), group
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
    unsupported = node("unsupported")
    unsupported.clash["type"] = "ss"
    invalid = node("invalid")
    invalid.clash.pop("uuid")
    for nodes in ([], [primary], [primary, unsupported], [invalid]):
        try:
            _build_singbox_android_json(nodes)
        except ValueError as exc:
            assert "tidak ada node manual" in str(exc), exc
        else:
            raise AssertionError("No supported manual nodes must fail without automatic fallback")
    print("PASS: healthy manual priority, stable order, skipped/unknown fallback, account retention")
    print("PASS: mixed input excludes automatic nodes, no supported manual fails, real sing-box check")


if __name__ == "__main__":
    main()