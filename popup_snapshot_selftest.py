"""Offline popup coverage without private feed cache or real accounts."""
import json
from types import SimpleNamespace
from unittest.mock import patch

from generate_yaml import _build_singbox_android_json
from security_policy import provider_catalog, provider_reject_rules

node = SimpleNamespace(
    name="manual-test", tier="MANUAL", type="vmess",
    clash={"type": "vmess", "server": "example.com", "port": 443,
           "uuid": "00000000-0000-4000-8000-000000000001", "cipher": "auto"},
)
reads = []

def read_fixture(path):
    reads.append(path)
    if path == "rule_providers/popup-ads_android.yaml":
        return "payload:\n- .popup-ad.example\n- .allowed.example\n"
    if path == "adblock_allowlist.txt":
        return "allowed.example\n"
    return ""

with patch("generate_yaml._read_text_file", side_effect=read_fixture):
    config = json.loads(_build_singbox_android_json([node]))
assert "rule_providers/popup-ads_android.yaml" in reads, "Published popup snapshot not consumed"
rules = config["route"]["rules"]
blocked = {domain for rule in rules if rule.get("action") == "reject"
           for domain in rule.get("domain_suffix", [])}
assert "popup-ad.example" in blocked, "Snapshot popup missing from reject rules"
assert "allowed.example" not in blocked, "Allowlist ignored"

providers = provider_catalog(platform="android", profile="app-safe", interval=43200)
popup = providers["popup-ads"]
assert popup == {
    "type": "http",
    "behavior": "domain",
    "path": "./rule_providers/popup-ads_android.yaml",
    "url": "https://raw.githubusercontent.com/adiorany3/AkunYaml/HEAD/rule_providers/popup-ads_android.yaml",
    "interval": 43200,
    "format": "yaml",
}
rules = provider_reject_rules(platform="android", profile="app-safe")
assert "RULE-SET,popup-ads,REJECT" in rules

print("PASS: published popup snapshot blocks sing-box and is portable to Clash Meta Android; allowlist preserved")
