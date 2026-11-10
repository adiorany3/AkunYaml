import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from domain_policy_tools import domain, explain, matches, provider_rules
from node_history import identity, load, record, save, summary
from release_tools import preview, public_export
from singbox_gameblock import build


def test_explain_order_provider_and_suffix_boundary(tmp_path):
    (tmp_path / "ads.yaml").write_text("payload: ['+.example.com']\n")
    config = {"rule-providers": {"ads": {"behavior": "domain", "format": "yaml", "path": "ads.yaml"}},
              "rules": ["DOMAIN,allow.example.com,DIRECT", "RULE-SET,ads,REJECT", "MATCH,DIRECT"]}
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config))
    assert explain(path, "allow.example.com", Path("missing"))["policy"] == "DIRECT"
    result = explain(path, "a.example.com", Path("missing"))
    assert result["source"] == "ads" and result["policy"] == "REJECT"
    assert result["uncertain_before"] == 0
    assert explain(path, "badexample.com", Path("missing"))["policy"] == "DIRECT"
    (tmp_path / "ads.yaml").unlink()
    assert explain(path, "example.com", Path("missing"))["uncertain_before"] == 1


@pytest.mark.parametrize("host", ["https://example.com", "a:443", "-bad.com", "a..com", "x\n.com"])
def test_domain_validation(host):
    with pytest.raises(ValueError):
        domain(host)


def test_provider_path_escape_and_wildcard_refused(tmp_path):
    with pytest.raises(ValueError, match="aman"):
        provider_rules(tmp_path, {"path": "../secret"}, Path("missing"))
    (tmp_path / "ads.txt").write_text("*.example.com")
    with pytest.raises(ValueError, match="Wildcard"):
        provider_rules(tmp_path, {"path": "ads.txt", "format": "text", "behavior": "domain"}, Path("missing"))


def test_translation_policy_and_unsupported_fail_closed(tmp_path):
    source = {"outbounds": [{"type": "direct", "tag": "direct"}], "route": {"rules": [{"protocol": "dns", "action": "hijack-dns"}]}}
    clash = {"rules": ["DOMAIN-SUFFIX,games.example,REJECT", "DOMAIN,ads.example,REJECT", "MATCH,DIRECT"]}
    result = build(source, clash, tmp_path, Path("missing"))
    assert result["route"]["final"] == "direct"
    rules = result["route"]["rules"]
    assert rules[0]["action"] == "hijack-dns"
    for host, expected in [("games.example", True), ("a.games.example", True), ("badgames.example", False), ("ads.example", True)]:
        blocked = any(matches("DOMAIN-SUFFIX", v, host) for r in rules for v in r.get("domain_suffix", [])) or any(host in r.get("domain", []) for r in rules)
        assert blocked == expected
    clash["rules"].insert(0, "PROCESS-NAME,game,REJECT")
    with pytest.raises(ValueError, match="Jenis rule"):
        build(source, clash, tmp_path, Path("missing"))


def test_preview_never_leaks_raw_credentials(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    for folder, rules in [(old, ["DOMAIN,secret.example,REJECT", "MATCH,DIRECT"]), (new, ["MATCH,DIRECT", "DOMAIN,secret.example,REJECT"])]:
        path = folder / "openclash/proxy/config.yaml"
        path.parent.mkdir(parents=True)
        path.write_text(yaml.safe_dump({"rules": rules, "proxies": [{"password": "SECRET"}]}))
    report = preview(old, new)
    assert report["changes"][0]["rule_order_changed"]
    assert "SECRET" not in json.dumps(report) and "secret.example" not in json.dumps(report)


def test_public_export_allowlist_and_preservation(tmp_path):
    source, target = tmp_path / "output", tmp_path / "public"
    (source / "security").mkdir(parents=True)
    block = source / "security/adaptive_blocklist.txt"
    block.write_text("ads.example\n")
    (source / "credentials.txt").write_text("SECRET")
    public_export(source, target)
    assert {p.name for p in target.iterdir()} == {"manifest.json", "adaptive_blocklist.txt"}
    assert "SECRET" not in "".join(p.read_text() for p in target.iterdir())
    block.write_text("https://secret.example/key\n")
    with pytest.raises(ValueError):
        public_export(source, target)
    assert (target / "adaptive_blocklist.txt").read_text() == "ads.example\n"
    with pytest.raises(ValueError):
        public_export(source, source / "nested")


def test_inline_provider_and_allowlist_precedence(tmp_path):
    source = {"outbounds": [{"type": "direct", "tag": "direct"}], "route": {}}
    clash = {"rules": ["DOMAIN,allow.games.example,DIRECT", "RULE-SET,games,REJECT", "MATCH,DIRECT"],
             "rule-providers": {"games": {"type": "inline", "behavior": "domain", "payload": ["+.games.example"]}}}
    result = build(source, clash, tmp_path, Path("missing"))
    rules = result["route"]["rules"]
    assert rules[0]["outbound"] == "direct"
    assert rules[0]["domain"] == ["allow.games.example"]
    assert rules[1]["action"] == "reject"
    assert rules[1]["domain_suffix"] == ["games.example"]


def test_history_penalizes_only_current_alive_nodes(tmp_path):
    from node_history import apply_history

    now = datetime(2026, 11, 10, tzinfo=UTC)
    node = SimpleNamespace(clash={"server": "example.com"}, original_server="example.com", best_delay_ms=50, status="dead", score=100)
    path = tmp_path / "history.json"
    apply_history([node], path, now - timedelta(minutes=2))
    apply_history([node], path, now - timedelta(minutes=1))
    node.status = "alive"
    apply_history([node], path, now)
    assert node.status == "alive" and node.score > 100
    node.status = "dead"
    node.score = 999999
    apply_history([node], path, now)
    assert node.status == "dead" and node.score == 999999


def test_public_export_refuses_unrelated_destination(tmp_path):
    source, target = tmp_path / "output", tmp_path / "documents"
    (source / "security").mkdir(parents=True)
    (source / "security/adaptive_blocklist.txt").write_text("ads.example\n")
    target.mkdir()
    (target / "keep.txt").write_text("keep")
    with pytest.raises(ValueError, match="menimpa"):
        public_export(source, target)
    assert (target / "keep.txt").read_text() == "keep"


def test_core_pipeline_still_imports():
    import sumberyaml_core

    assert callable(sumberyaml_core.process_sources)


def test_history_bounds_privacy_expiry_and_failure_rate(tmp_path):
    now = datetime(2026, 11, 10, tzinfo=UTC)
    node = SimpleNamespace(clash={"name": "SECRET", "server": "host.example", "password": "SECRET"}, original_server="host.example", best_delay_ms=50, status="alive")
    history = {}
    for i in range(25):
        record(history, node, now - timedelta(minutes=25 - i))
    node.status = "dead"
    record(history, node, now)
    values = history[identity(node)]
    assert len(values) == 20
    stats = summary(values, now)
    assert stats["success_ratio"] == 19 / 20
    assert stats["consecutive_failures"] == 1
    assert stats["median_ms"] == 50
    assert stats["last_success"] is not None
    assert summary(values, now + timedelta(days=8)) is None
    path = tmp_path / "history.json"
    save(path, history, now)
    assert load(path) == history
    assert "SECRET" not in path.read_text() and "host.example" not in path.read_text()
    assert path.stat().st_mode & 0o777 == 0o600
    path.write_text('{"raw-endpoint": []}')
    with pytest.raises(ValueError):
        load(path)
