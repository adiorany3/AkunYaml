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
for domain in (
    "livetech.shopee.co.id",
    "sg-live.slatic.net",
    "business-api.tiktok.com",
    "log.byteoversea.com",
):
    assert domain not in reject_domains, domain

node = SimpleNamespace(
    clash={
        "type": "vmess", "server": "example.com", "port": 443,
        "uuid": "00000000-0000-4000-8000-000000000001", "cipher": "auto",
        "tls": True, "servername": "example.com", "network": "ws",
        "ws-opts": {"path": "/"},
    },
    type="vmess", tier="MANUAL", name="self-check",
)
generated = json.loads(_build_singbox_android_json([node]))
rules = generated["route"]["rules"]
proxy_outbound = next(outbound for outbound in generated["outbounds"] if outbound.get("tag") == "proxy")
assert proxy_outbound["default"] == "self-check"
assert proxy_outbound["outbounds"][0] == "self-check"
payment_rule_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("outbound") == "direct" and "shopee.co.id" in rule.get("domain_suffix", [])
)
grab_rule_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("outbound") == "proxy" and "grab.com" in rule.get("domain_suffix", [])
)
marketplace_rule_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("outbound") == "proxy" and "slatic.net" in rule.get("domain_suffix", [])
)
quic_reject_index = next(
    index
    for index, rule in enumerate(rules)
    if rule.get("action") == "reject" and rule.get("network") == "udp" and rule.get("port") == 443
)
assert payment_rule_index < quic_reject_index
assert grab_rule_index < quic_reject_index
assert marketplace_rule_index < quic_reject_index
assert "grabtaxi.com" in rules[grab_rule_index]["domain_suffix"]
assert "grabfood.com" in rules[grab_rule_index]["domain_suffix"]
assert "shopeemobile.com" in rules[payment_rule_index]["domain_suffix"]
assert "spaylater.co.id" in rules[payment_rule_index]["domain_suffix"]
marketplace_rule = rules[marketplace_rule_index]
assert "business-api.tiktok.com" in marketplace_rule["domain"]
assert "tiktok.com" not in marketplace_rule["domain_suffix"]
generated_reject_domains = {
    domain
    for rule in rules
    if rule.get("action") == "reject"
    for domain in rule.get("domain_suffix", []) + rule.get("domain", [])
}
assert "livetech.shopee.co.id" not in generated_reject_domains
assert "sg-live.slatic.net" not in generated_reject_domains
assert "ads.tiktok.com" in generated_reject_domains
marketplace_dns_rules = [
    rule for rule in generated["dns"]["rules"]
    if rule.get("server") == "local" and "slatic.net" in rule.get("domain_suffix", [])
]
assert marketplace_dns_rules
print("OK")
