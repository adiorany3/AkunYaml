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
for domain in (
    "pagead2.googlesyndication.com",
    "googletagservices.com",
    "metrics.samsung.com",
    "tracking.miui.com",
    "data.mistat.intl.xiaomi.com",
):
    assert domain in reject_domains, domain
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
    if rule.get("outbound") == "proxy" and "shopee.co.id" in rule.get("domain_suffix", [])
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
    and "domain_suffix" not in rule
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

# Tunnel-only first-party traffic must not hit legacy payment DIRECT rules.
for config in (generated, artifact):
    route_rules = config["route"]["rules"]
    payment_index = next(
        i for i, rule in enumerate(route_rules)
        if rule.get("outbound") == "proxy"
        and "shopeepay.co.id" in rule.get("domain_suffix", [])
    )
    threat_index = next(
        i for i, rule in enumerate(route_rules) if rule.get("action") == "reject"
    )
    assert threat_index < payment_index
    assert all(
        i > payment_index
        for i, rule in enumerate(route_rules)
        if rule.get("action") == "reject" and i != threat_index
        and "shopeepay.co.id" not in rule.get("domain_suffix", [])
    )
    app_suffixes = route_rules[payment_index]["domain_suffix"]
    assert {"gojek.com", "gojekapi.com", "gopay.co.id", "shopee.co.id", "shopeepay.co.id"} <= set(app_suffixes)
    for host in [host for domain in app_suffixes for host in (domain, "help.cs." + domain)]:
        for network in ("tcp", "udp"):
            # Evaluate public HTTPS domain rules; sniff/DNS/private-IP are not routes here.
            matched = next((
                rule for rule in route_rules
                if rule.get("action") in ("route", "reject")
                and not rule.get("ip_is_private")
                and rule.get("network", network) == network
                and rule.get("port", 443) == 443
                and (
                    not ("domain" in rule or "domain_suffix" in rule)
                    or host in rule.get("domain", [])
                    or any(host == d or host.endswith("." + d) for d in rule.get("domain_suffix", []))
                )
            ), {})
            if network == "udp":
                assert matched.get("action") == "reject", (host, network)
            else:
                assert matched.get("outbound") == "proxy", (host, network)
        dns_rule = next(
            rule for rule in config["dns"]["rules"]
            if host in rule.get("domain", [])
            or any(host == d or host.endswith("." + d) for d in rule.get("domain_suffix", []))
        )
        assert dns_rule.get("action") == "route" and dns_rule.get("server") == "local"
    assert config["dns"]["servers"] == [{"type": "local", "tag": "local"}]
    assert config["dns"]["final"] == "local"
    assert "shopeepay.co.id" not in route_rules[threat_index].get("domain_suffix", [])
    assert any(rule.get("outbound") == "proxy" and "midtrans.com" in rule.get("domain_suffix", []) for rule in route_rules)
    assert all(rule.get("ip_is_private") is True for rule in route_rules if rule.get("outbound") == "direct")
print("OK")
