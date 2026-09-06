#!/usr/bin/env python3
import json
from pathlib import Path

config = json.loads((Path(__file__).parent / "singbox_android.json").read_text(encoding="utf-8"))
rules = config["route"]["rules"]
reject_domains = {
    domain
    for rule in rules
    if rule.get("action") == "reject"
    for domain in rule.get("domain_suffix", []) + rule.get("domain", [])
}
assert "casino-netflix.com" in reject_domains
assert "netflix.com" not in reject_domains
assert "ads.spotify.com" in reject_domains
assert "googlevideo.com" not in reject_domains
assert "youtube.com" not in reject_domains
print("OK")
