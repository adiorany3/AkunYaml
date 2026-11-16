import json
from pathlib import Path

import adaptive_guard


def test_integrated_youtube_rules_preserve_combined_matches(tmp_path):
    from local_update import apply_youtube_singbox_rules

    original = {"route": {"rules": [
        {"domain": ["ads.youtube.com", "api.other.example"], "action": "reject"},
        {"domain_suffix": ["googlevideo.com", "malware-cdn.example"], "action": "reject"},
        {"domain_suffix": ["googlevideo.com", "doubleclick.net", "other.example"], "action": "reject"},
    ]}}
    result = apply_youtube_singbox_rules(original)["route"]["rules"]
    assert any("api.other.example" in r.get("domain", []) and r["action"] == "reject" for r in result)
    assert any("malware-cdn.example" in r.get("domain_suffix", []) and r["action"] == "reject" for r in result)
    assert any("other.example" in r.get("domain_suffix", []) and r["action"] == "reject" for r in result)
    assert next(r for r in result if "googlevideo.com" in r.get("domain_suffix", []))["outbound"] == "VMESS-VIDEO"
    assert original["route"]["rules"][1]["domain_suffix"][0] == "googlevideo.com"


def test_adaptive_rules_preserve_priority_and_playback(tmp_path, monkeypatch):
    root = tmp_path / "root"
    stage = tmp_path / "stage"
    root.mkdir()
    (root / "adblock_allowlist.txt").write_text("safe.example\n")
    baseline = root / "gameblock_policy/baseline"
    baseline.mkdir(parents=True)
    (baseline / "openclash_noproxy_gameblock.yaml").write_text("rules: []\n")
    folder = stage / "sing-box"
    folder.mkdir(parents=True)
    config = {"route": {"rules": [
        {"action": "sniff"},
        {"rule_set": ["threat-malware"], "action": "reject"},
        {"domain": ["ads.youtube.com"], "action": "route", "outbound": "block"},
        {"domain_suffix": ["googlevideo.com"], "action": "route", "outbound": "VMESS-VIDEO"},
        {"domain_suffix": ["safe.example"], "action": "route", "outbound": "block"},
    ]}}
    (folder / "config.json").write_text(json.dumps(config))
    monkeypatch.setattr(adaptive_guard, "snapshot", lambda _root: {
        "status": "fresh", "accepted": {
            "evil.example": {"category": "malware", "publishers": ["a", "b"]},
            "safe.example": {"category": "adblock", "publishers": ["a", "b"]},
        },
    })
    adaptive_guard.apply(stage, root)
    rules = json.loads((folder / "config.json").read_text())["route"]["rules"]
    malware = next(i for i, rule in enumerate(rules) if "threat-malware" in rule.get("rule_set", []))
    ads = next(i for i, rule in enumerate(rules) if "ads.youtube.com" in rule.get("domain", []))
    playback = next(i for i, rule in enumerate(rules) if "googlevideo.com" in rule.get("domain_suffix", []))
    adaptive = next(i for i, rule in enumerate(rules) if rule.get("domain") == ["evil.example"])
    assert malware < ads < playback < adaptive
    assert rules[adaptive]["action"] == "reject"
    assert all("safe.example" not in rule.get("domain", []) for rule in rules)
    assert rules[playback]["outbound"] == "VMESS-VIDEO"


if __name__ == "__main__":
    import tempfile
    test_adaptive_rules_preserve_priority_and_playback(Path(tempfile.mkdtemp()), lambda *_: None)
    print("PASS: adaptive threat ordering, allowlist, YouTube playback")

import json
from datetime import UTC, datetime, timedelta

import yaml

import adaptive_guard as guard


def test_telegram_domains_are_protected_from_adaptive_blocks(tmp_path):
    from adaptive_guard import protected_domains, evaluate

    allowlist = protected_domains(tmp_path)
    telegram = {"telegram.org", "t.me", "telegram-cdn.org", "telegra.ph"}
    assert telegram <= allowlist
    evidence = {
        "hagezi-ads": telegram,
        "abpindo-ads": telegram,
        "hagezi-threat": set(),
        "chocolate-threat": set(),
    }
    accepted, _ = evaluate(evidence, allowlist)
    assert not telegram.intersection(accepted)


def test_only_corroborated_exact_host_and_allowlist():
    evidence = {"hagezi-threat": {"bad.example", "single.example", "safe.example", "1.2.3.4"}, "chocolate-threat": {"bad.example", "safe.example", "1.2.3.4"}}
    accepted, review = guard.evaluate(evidence, {"safe.example"})
    assert set(accepted) == {"bad.example", "safe.example"}
    assert review == 1


def create_cache(root, expires):
    now = datetime.now(UTC)
    path = root / ".runtime_cache/adaptive_guard.json"
    path.parent.mkdir()
    path.write_text(json.dumps({"policy": "two-publishers-exact-host-v1", "generated_at": (now - timedelta(hours=1)).isoformat(), "expires_at": expires.isoformat(), "accepted": {"bad.example": {"category": "malware", "publishers": ["hagezi", "chocolate4u"]}}}))


def test_allowlist_does_not_override_corroborated_malware(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) + timedelta(hours=1))
    (tmp_path / "adblock_allowlist.txt").write_text("bad.example\n")
    assert "bad.example" in guard.snapshot(tmp_path)["accepted"]


def test_snapshot_rejects_unknown_or_wrong_category_publishers(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) + timedelta(hours=1))
    path = tmp_path / ".runtime_cache/adaptive_guard.json"
    report = json.loads(path.read_text())
    report["accepted"]["bad.example"]["publishers"] = ["hagezi", "abpindo", "invented"]
    path.write_text(json.dumps(report))
    assert guard.snapshot(tmp_path)["accepted"] == {}


def test_overlay_preserves_singbox_technical_rules_and_proxy_route(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) + timedelta(hours=1))
    stage = tmp_path / "stage"
    path = stage / "sing-box/profile.json"
    path.parent.mkdir(parents=True)
    technical = [{"action": "sniff"}, {"protocol": "dns", "action": "hijack-dns"}]
    service = {"domain_suffix": ["login.example"], "action": "route", "outbound": "proxy"}
    path.write_text(json.dumps({"route": {"rules": technical + [service], "final": "proxy"}}))
    guard.apply(stage, tmp_path)
    route = json.loads(path.read_text())["route"]
    assert route["rules"][:2] == technical
    assert route["rules"][2] == {"domain": ["bad.example"], "action": "reject"}
    assert route["rules"][3] == service
    assert route["final"] == "proxy"


def test_expired_evidence_not_applied(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) - timedelta(minutes=1))
    assert guard.snapshot(tmp_path)["accepted"] == {}


def test_apply_both_platforms(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) + timedelta(hours=1))
    stage = tmp_path / "stage"
    clash = stage / "openclash/direct/profile.yaml"
    clash.parent.mkdir(parents=True)
    clash.write_text(yaml.safe_dump({"rules": ["MATCH,DIRECT"]}))
    sing = stage / "sing-box/profile.json"
    sing.parent.mkdir()
    sing.write_text(json.dumps({"route": {"rules": []}}))
    assert guard.apply(stage, tmp_path) == "fresh"
    assert yaml.safe_load(clash.read_text())["rules"][0] == "DOMAIN,bad.example,REJECT"
    assert json.loads(sing.read_text())["route"]["rules"][0] == {"domain": ["bad.example"], "action": "reject"}


def test_allowlist_rechecked_at_packaging(tmp_path):
    create_cache(tmp_path, datetime.now(UTC) + timedelta(hours=1))
    (tmp_path / "adblock_allowlist.txt").write_text("bad.example\n")
    path = tmp_path / ".runtime_cache/adaptive_guard.json"
    report = json.loads(path.read_text())
    report["accepted"]["bad.example"] = {"category": "adblock", "publishers": ["hagezi", "abpindo"]}
    path.write_text(json.dumps(report))
    assert guard.snapshot(tmp_path)["accepted"] == {}


def test_baseline_service_exception_protected(tmp_path):
    path = tmp_path / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump({"rules": ["DOMAIN-SUFFIX,pay.example,DIRECT", "MATCH,DIRECT"]}))
    accepted, _ = guard.evaluate({"hagezi-ads": {"api.pay.example"}, "abpindo-ads": {"api.pay.example"}}, guard.protected_domains(tmp_path))
    assert not accepted