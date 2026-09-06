#!/usr/bin/env python3
"""Offline regression checks for account-independent manual routing policy."""
from copy import deepcopy

from load_balance_policy_audit import manual_policy_errors


def main() -> None:
    valid = {
        "proxies": [
            {"name": "MANUAL-renamed-primary", "type": "vmess"},
            {"name": "MANUAL-renamed-backup", "type": "vless"},
        ],
        "proxy-groups": [
            {"name": "REDDIT", "type": "select", "proxies": ["MANUAL"]},
            {"name": "MANUAL", "type": "fallback", "proxies": [
                "MANUAL-renamed-primary", "MANUAL-renamed-backup",
            ]},
        ],
    }
    assert not manual_policy_errors(valid)
    for target in ([], ["DIRECT"], ["MANUAL-renamed-primary"], ["MANUAL", "DIRECT"], "MANUAL"):
        config = deepcopy(valid)
        config["proxy-groups"][0]["proxies"] = target
        assert manual_policy_errors(config), target
    config = deepcopy(valid)
    config["proxy-groups"].pop()
    assert manual_policy_errors(config)
    config = deepcopy(valid)
    config["proxy-groups"][1]["type"] = "select"
    assert manual_policy_errors(config)
    for members in ([], None, "MANUAL-renamed-primary", ["MANUAL-missing"], ["DIRECT"], ["REDDIT"], [{}]):
        config = deepcopy(valid)
        config["proxy-groups"][1]["proxies"] = members
        assert manual_policy_errors(config), members
    for node in (
        {"name": "automatic-node", "type": "vmess"},
        {"name": "MANUAL-direct", "type": "direct"},
        {"name": "MANUAL-no-type"},
    ):
        config = deepcopy(valid)
        config["proxies"].append(node)
        config["proxy-groups"][1]["proxies"] = [node["name"]]
        assert manual_policy_errors(config), node
    config = deepcopy(valid)
    config["proxy-groups"].append({"name": "MANUAL-renamed-primary", "type": "select"})
    assert manual_policy_errors(config)
    print("Load-balance policy selftest: OK")


if __name__ == "__main__":
    main()