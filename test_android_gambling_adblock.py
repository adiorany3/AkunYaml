#!/usr/bin/env python3
import json
from pathlib import Path
from types import SimpleNamespace

from generate_yaml import _build_singbox_android_json

artifact = json.loads((Path(__file__).parent / "singbox_android.json").read_text(encoding="utf-8"))
reject_domains = {
    domain
    for rule in artifact["route"]["rules"]
    if rule.get("action") == "reject"
    for domain in rule.get("domain_suffix", []) + rule.get("domain", [])
}
assert "casino-netflix.com" in reject_domains
assert "netflix.com" not in reject_domains
assert "ads.spotify.com" in reject_domains
assert "googlevideo.com" not in reject_domains
assert "youtube.com" not in reject_domains

node = SimpleNamespace(
    clash={
        "type": "vmess", "server": "example.com", "port": 443,
        "uuid": "00000000-0000-4000-8000-000000000001", "cipher": "auto",
        "tls": True, "servername": "example.com", "network": "ws",
        "ws-opts": {"path": "/"},
    },
    type="vmess", tier="MANUAL", name="self-check",
)
rules = json.loads(_build_singbox_android_json([node]))["route"]["rules"]
payment_rule_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("outbound") == "direct" and "shopee.co.id" in rule.get("domain_suffix", [])
)
quic_reject_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("action") == "reject" and rule.get("network") == "udp" and rule.get("port") == 443
)
assert payment_rule_index < quic_reject_index
assert "shopeemobile.com" in rules[payment_rule_index]["domain_suffix"]
assert "spaylater.co.id" in rules[payment_rule_index]["domain_suffix"]
print("OK")
