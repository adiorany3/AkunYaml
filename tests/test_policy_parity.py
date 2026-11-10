"""Offline domain-policy parity checks, independent of real account credentials."""
from pathlib import Path

import pytest
import yaml

from domain_policy_tools import FIELDS, explain, matches
from singbox_gameblock import build


def decision(config, host):
    """Evaluate only the domain fields emitted by the translator under test."""
    for rule in config["route"]["rules"]:
        for kind, field in FIELDS.items():
            if kind.startswith("DOMAIN") and any(matches(kind, value, host) for value in rule.get(field, [])):
                return "REJECT" if rule["action"] == "reject" else "DIRECT"
    return "DIRECT"


@pytest.mark.parametrize("host,expected", [
    ("login.games.example", "DIRECT"),
    ("captcha.example", "DIRECT"),
    ("games.example", "REJECT"),
    ("play.games.example", "REJECT"),
    ("badgames.example", "DIRECT"),
    ("ads.example", "REJECT"),
    ("api.ads.example", "DIRECT"),
    ("phishing-login.example", "REJECT"),
    ("cdn.example", "DIRECT"),
])
def test_clash_singbox_same_domain_decision(tmp_path, host, expected):
    clash = {
        "rules": ["DOMAIN,login.games.example,DIRECT", "DOMAIN,captcha.example,DIRECT",
                  "DOMAIN,phishing-login.example,REJECT", "RULE-SET,games,REJECT",
                  "DOMAIN,ads.example,REJECT", "MATCH,DIRECT"],
        "rule-providers": {"games": {"type": "inline", "behavior": "domain", "payload": ["+.games.example"]}},
    }
    source = {"outbounds": [{"type": "direct", "tag": "direct"}], "route": {"rules": []}}
    translated = build(source, clash, tmp_path, Path("unused-core"))
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(clash))
    result = explain(path, host, Path("unused-core"))
    assert result["uncertain_before"] == 0
    assert result["policy"] == decision(translated, host) == expected


@pytest.mark.parametrize("rules", [
    ["MATCH,DIRECT", "DOMAIN,ads.example,REJECT", "MATCH,DIRECT"],
    ["DOMAIN,ads.example,REJECT", "MATCH,DIRECT", "MATCH,DIRECT"],
])
def test_early_match_never_silently_changes_policy(tmp_path, rules):
    with pytest.raises(ValueError, match="di akhir"):
        build({}, {"rules": rules}, tmp_path, Path("unused-core"))


@pytest.mark.parametrize("rules", [None, "MATCH,DIRECT", [None]])
def test_malformed_rule_input_rejected(tmp_path, rules):
    with pytest.raises(TypeError, match="teks"):
        build({}, {"rules": rules}, tmp_path, Path("unused-core"))
