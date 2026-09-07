"""Offline regression: public routes and every selector stay manual-only."""
import copy
import json
from unittest.mock import patch

import yaml

import generate_yaml as generator
from sumberyaml_core import build_openclash_android_yaml


def check():
    nodes, skipped = generator.parse_manual_nodes_unscreened(
        "vless://00000000-0000-4000-8000-000000000001@example.com:443?security=tls&type=ws#fixture"
    )
    assert len(nodes) == 1 and not skipped
    manual = nodes[0]
    failed = copy.deepcopy(manual)
    failed.name = failed.clash["name"] = "failed-manual"
    failed.tcp_reachable = False
    automatic = copy.deepcopy(manual)
    automatic.name = automatic.clash["name"] = "subscription"
    automatic.tier = "PRIMARY"
    automatic.clash["uuid"] = "00000000-0000-4000-8000-000000000002"
    mixed = [automatic, failed, manual]

    with patch.object(generator, "_read_text_file", side_effect=lambda path: "" if "allowlist" in str(path) else "malware.example\n"):
        singbox = json.loads(generator._build_singbox_android_json(mixed))
    outbounds = {item["tag"]: item for item in singbox["outbounds"]}
    leaves = {tag for tag, item in outbounds.items() if item["type"] == "vless"}
    assert leaves == {manual.name}
    for item in outbounds.values():
        if item["type"] == "selector":
            assert item["outbounds"] and set(item["outbounds"]) <= leaves
            assert item["default"] in leaves
    assert singbox["route"]["final"] == "proxy"
    rules = singbox["route"]["rules"]
    assert all(rule.get("ip_is_private") is True for rule in rules if rule.get("outbound") == "direct")
    assert rules[3]["action"] == "reject" and "malware.example" in rules[3]["domain_suffix"]

    def android(nodes):
        return build_openclash_android_yaml(nodes, 30, 40, "https://www.gstatic.com/generate_204")

    for profile in ("off", "balanced", "threat-safe", "child-safe"):
        with patch.dict("os.environ", {"ADBLOCK_PROFILE": profile}):
            text = android(mixed)
        # Exercise the same post-processing stages as main().
        text = generator.add_manual_group_to_yaml_text(text, [manual], android=True)
        text = generator._enforce_no_selector_no_direct_yaml_text(text)
        text = generator._ensure_ping_check_group_yaml_text(text)
        config = yaml.safe_load(generator._prune_missing_proxy_group_refs_yaml_text(text))
        proxies = {item["name"]: item for item in config["proxies"]}
        assert proxies and all(item["uuid"] == manual.clash["uuid"] for item in proxies.values())
        assert not any("failed-manual" in name or "subscription" in name for name in proxies)
        groups = {item["name"]: item for item in config["proxy-groups"]}

        def walk(name, path=()):
            if name in proxies:
                return
            assert name in groups and name not in path, (name, path)
            group = groups[name]
            assert not group.get("use") and not group.get("include-all")
            assert group["proxies"]
            for ref in group["proxies"]:
                walk(ref, (*path, name))

        for name in groups:
            walk(name)
        lan_rules = {
            "DOMAIN-SUFFIX,local,DIRECT", "DOMAIN-SUFFIX,lan,DIRECT",
            "DOMAIN-SUFFIX,localhost,DIRECT", "GEOIP,LAN,DIRECT,no-resolve",
            *(f"IP-CIDR,{cidr},DIRECT,no-resolve" for cidr in (
                "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "169.254.0.0/16"
            )),
        }
        for rule in config["rules"]:
            parts = rule.split(",")
            policy = parts[-2] if parts[-1] == "no-resolve" else parts[-1]
            if policy == "DIRECT":
                assert rule in lan_rules
            elif policy not in {"REJECT", "REJECT-DROP"}:
                walk(policy)
        assert config["rules"][-1] == "MATCH,GLOBAL"
        if profile != "off":
            assert "RULE-SET,threat-malware,REJECT" in config["rules"]

    for build in (android, generator._build_singbox_android_json):
        for unusable in ([], [automatic], [failed], [automatic, failed]):
            try:
                build(unusable)
            except ValueError:
                pass
            else:
                raise AssertionError("Missing manual nodes must fail closed")
    print("OK: manual-only public routing, selectors, TCP failures, threats, empty input")


if __name__ == "__main__":
    check()