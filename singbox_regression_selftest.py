"""Offline regression checks: reserved tags and gambling feed conversion."""
import json
from unittest.mock import patch

from generate_yaml import _build_singbox_android_json
from singbox_defaults_selftest import node


def main():
    feeds = {
        ".feed_cache/last_good/gambling-mini.txt": "casino-netflix.com\nnetflix.com\n",
        "adblock_allowlist.txt": "netflix.com\n",
    }
    with patch("generate_yaml._read_text_file", side_effect=lambda path: feeds.get(str(path), "")):
        config = json.loads(_build_singbox_android_json([node("AUTO-FAST"), node("AUTO-FAST-2")]))
    outbounds = config["outbounds"]
    tags = [outbound["tag"] for outbound in outbounds]
    assert len(tags) == len(set(tags)), tags
    automatic = next(outbound for outbound in outbounds if outbound["tag"] == "AUTO-FAST")
    assert automatic["type"] == "urltest"
    assert "AUTO-FAST" not in automatic["outbounds"]
    assert set(automatic["outbounds"]) == {"AUTO-FAST-2", "AUTO-FAST-2-2"}
    rejected = {
        domain
        for rule in config["route"]["rules"] if rule.get("action") == "reject"
        for domain in rule.get("domain_suffix", []) + rule.get("domain", [])
    }
    assert "casino-netflix.com" in rejected
    assert "netflix.com" not in rejected
    print("PASS: unique outbound tags; gambling feed retained; allowlist respected")


if __name__ == "__main__":
    main()
