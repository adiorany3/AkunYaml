import json
from datetime import UTC, datetime, timedelta

import yaml

import adaptive_guard as guard


def test_only_corroborated_exact_host_and_allowlist():
    evidence = {"hagezi-threat": {"bad.example", "single.example", "safe.example", "1.2.3.4"}, "chocolate-threat": {"bad.example", "safe.example", "1.2.3.4"}}
    accepted, review = guard.evaluate(evidence, {"safe.example"})
    assert set(accepted) == {"bad.example"}
    assert review == 1


def create_cache(root, expires):
    now = datetime.now(UTC)
    path = root / ".runtime_cache/adaptive_guard.json"
    path.parent.mkdir()
    path.write_text(json.dumps({"policy": "two-publishers-exact-host-v1", "generated_at": (now - timedelta(hours=1)).isoformat(), "expires_at": expires.isoformat(), "accepted": {"bad.example": {"category": "malware", "publishers": ["hagezi", "chocolate4u"]}}}))


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
    assert guard.snapshot(tmp_path)["accepted"] == {}


def test_baseline_service_exception_protected(tmp_path):
    path = tmp_path / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump({"rules": ["DOMAIN-SUFFIX,pay.example,DIRECT", "MATCH,DIRECT"]}))
    accepted, _ = guard.evaluate({"hagezi-threat": {"api.pay.example"}, "chocolate-threat": {"api.pay.example"}}, guard.protected_domains(tmp_path))
    assert not accepted