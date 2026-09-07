#!/usr/bin/env python3
"""Offline regression checks for malformed config and classifier input."""
import json

from ai_adblock_classifier import parse_response
from openclash_target import validate_config_structure


def main() -> None:
    assert not validate_config_structure({})
    assert not validate_config_structure({
        "proxies": [], "proxy-groups": [], "rules": [], "rule-providers": {},
    })
    for field in ("proxies", "proxy-groups", "rules", "rule-providers"):
        invalid = (None, False, 0, "", [] if field == "rule-providers" else {})
        for value in invalid:
            assert validate_config_structure({field: value}), (field, value)
    for proxy in (None, "node", {}, {"name": None}, {"name": 123}, {"name": " "}):
        assert validate_config_structure({"proxies": [proxy]}), proxy
    for value in (None, False, 0, "", {}):
        assert validate_config_structure({"proxy-groups": [{
            "name": "TEST", "type": "select", "proxies": value, "use": ["provider"],
        }]}), value

    valid = {"domain": "ads.example", "label": "block", "category": "advertising",
             "confidence": 1, "reason": "Dedicated advertising host"}
    assert parse_response(json.dumps({"results": [valid]}), ["ads.example"])
    for field in ("domain", "label", "category", "reason"):
        for value in (None, False, 123, [], {}):
            item = {**valid, field: value}
            try:
                parse_response(json.dumps({"results": [item]}), ["ads.example"])
            except ValueError:
                pass
            else:
                raise AssertionError((field, value))
    try:
        parse_response(json.dumps({"results": [{**valid, "category": "invalid"}]}), ["ads.example"])
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown category accepted")
    print("PASS: malformed YAML structures and AI response schema rejected")


if __name__ == "__main__":
    main()