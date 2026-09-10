#!/usr/bin/env python3
import json
import os
from types import SimpleNamespace
import yaml

from generate_yaml import _build_singbox_android_json, _validate_singbox_json, _prune_missing_proxy_group_refs_yaml_text

for available, expected in (("MANUAL", "MANUAL"), ("FALLBACK", "FALLBACK"), ("AUTO-FAST", "AUTO-FAST"), (None, "REJECT")):
    source = {
        "proxy-groups": [{"name": available, "type": "select", "proxies": ["REJECT"]}] if available else [],
        "rules": ["DOMAIN-SUFFIX,cloudflare.com,MANUAL", "IP-CIDR,1.1.1.1/32,MANUAL,no-resolve", "MATCH,REJECT"],
    }
    result = yaml.safe_load(_prune_missing_proxy_group_refs_yaml_text(yaml.safe_dump(source)))
    assert result["rules"] == [f"DOMAIN-SUFFIX,cloudflare.com,{expected}", f"IP-CIDR,1.1.1.1/32,{expected},no-resolve", "MATCH,REJECT"]
print("PASS: missing MANUAL policy uses automatic pool or REJECT")

node = SimpleNamespace(
    name="manual-vmess",
    tier="MANUAL",
    type="vmess",
    clash={
        "name": "manual-vmess",
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
# Global selector defaults to AUTO-FAST pool; categories follow the global selector.
assert groups["proxy"]["default"] == "AUTO-FAST", groups["proxy"]
assert groups["proxy"]["outbounds"] == ["AUTO-FAST", "manual-vmess"], groups["proxy"]
for tag in ("BANK", "SOCIAL", "VMESS-VIDEO"):
    assert groups[tag]["default"] == "proxy", groups[tag]
_validate_singbox_json(config_text, os.getenv("SINGBOX_PATH", ".local_bin/sing-box"))
print("PASS: manual VMess supplies sing-box selectors")

for protocol in ("vless", "trojan"):
    node.type = protocol
    node.clash["type"] = protocol
    if protocol == "trojan":
        node.clash["password"] = "test-password"
    config_text = _build_singbox_android_json([node])
    groups = {item["tag"]: item for item in json.loads(config_text)["outbounds"]}
    assert groups["proxy"]["default"] == "AUTO-FAST", groups["proxy"]
    for tag in ("BANK", "SOCIAL", "VMESS-VIDEO"):
        assert groups[tag]["default"] == "proxy", groups[tag]
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
