#!/usr/bin/env python3
import json
import os
from types import SimpleNamespace

from generate_yaml import _build_singbox_android_json, _validate_singbox_json

node = SimpleNamespace(
    name="automatic-vmess",
    tier="PRIMARY",
    type="vmess",
    clash={
        "name": "automatic-vmess",
        "type": "vmess",
        "server": "example.com",
        "port": 443,
        "uuid": "00000000-0000-4000-8000-000000000001",
        "cipher": "auto",
    },
)
config_text = _build_singbox_android_json([node])
config = json.loads(config_text)
groups = {item["tag"]: item for item in config["outbounds"]}
for tag in ("proxy", "BANK", "SOCIAL", "VMESS-VIDEO"):
    assert groups[tag]["default"] == "automatic-vmess", groups[tag]
_validate_singbox_json(config_text, os.getenv("SINGBOX_PATH", ".local_bin/sing-box"))
print("PASS: automatic VMess replaces unavailable manual nodes")

for protocol in ("vless", "trojan"):
    node.type = protocol
    node.clash["type"] = protocol
    if protocol == "trojan":
        node.clash["password"] = "test-password"
    config_text = _build_singbox_android_json([node])
    groups = {item["tag"]: item for item in json.loads(config_text)["outbounds"]}
    for tag in ("proxy", "BANK", "SOCIAL", "VMESS-VIDEO"):
        assert groups[tag]["default"] == node.name, groups[tag]
        assert groups[tag]["outbounds"], groups[tag]
        assert set(groups[tag]["outbounds"]) <= groups.keys(), groups[tag]
    _validate_singbox_json(config_text, os.getenv("SINGBOX_PATH", ".local_bin/sing-box"))
print("PASS: VLESS-only and Trojan-only pools need no VMess")

try:
    _build_singbox_android_json([])
except ValueError:
    pass
else:
    raise AssertionError("Empty pool must fail closed")
