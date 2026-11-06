import json

import pytest

from game_domain_policy import apply_policy, domain, import_log, observed_hosts


@pytest.mark.parametrize("value,expected", [("https://WWW.Example.org/play", "www.example.org"), ("*.example.org", "example.org"), ("1.2.3.4:443", None), ("bad/path", None), ("https://[bad", None), ("example.org:notaport", None)])
def test_normalization(value, expected):
    assert domain(value) == expected


def test_approved_rules_deduplicate(tmp_path):
    policy = tmp_path / "gameblock_policy"
    policy.mkdir()
    (policy / "manual_domains.txt").write_text("game.example\ngame.example\n")
    config = {"rules": ["DOMAIN-SUFFIX,game.example,REJECT", "MATCH,DIRECT"]}
    apply_policy(config, tmp_path)
    assert config["rules"] == ["DOMAIN-SUFFIX,game.example,REJECT", "MATCH,DIRECT"]


def test_allow_conflict_fails(tmp_path):
    policy = tmp_path / "gameblock_policy"
    policy.mkdir()
    (policy / "manual_domains.txt").write_text("game.example\n")
    (policy / "allow_domains.txt").write_text("login.game.example\n")
    with pytest.raises(ValueError):
        apply_policy({"rules": ["MATCH,DIRECT"]}, tmp_path)


def test_log_formats_only_destination_hosts():
    data = {"connections": [{"metadata": {"host": "play.example", "sourceIP": "192.168.1.2"}}]}
    assert observed_hosts(json.dumps(data)) == {"play.example": 1}
    text = '[TCP] 192.168.1.2:123 --> cdn.example:443 match DIRECT\nhttps://unrelated.example/\n'
    assert observed_hosts(text) == {"cdn.example": 1}


def test_log_import_private_review_only(tmp_path):
    log = tmp_path / "connections.json"
    log.write_text(json.dumps({"connections": [{"metadata": {"host": "unknown.example", "sourceIP": "192.168.1.2"}}]}))
    path, count = import_log(log, tmp_path)
    report = json.loads(path.read_text())
    assert count == 1 and report["auto_blocked"] == 0
    assert report["candidates"][0]["decision"] == "review"
    assert "192.168.1.2" not in path.read_text()
    assert not (tmp_path / "gameblock_policy/manual_domains.txt").exists()