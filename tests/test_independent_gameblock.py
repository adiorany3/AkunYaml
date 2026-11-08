import json

import pytest
import yaml

import independent_gameblock as builder


def setup_policy(root):
    policy = root / "gameblock_policy"
    baseline = policy / "baseline"
    baseline.mkdir(parents=True)
    (baseline / builder.PROFILE).write_text(yaml.safe_dump({"rules": ["DOMAIN,pay.example,DIRECT", "MATCH,DIRECT"], "rule-providers": {}}))
    (policy / "sources.json").write_text(json.dumps({"games-category": {"url": "https://raw.githubusercontent.com/MetaCubeX/test/main/games.mrs", "format": "mrs", "path": "rule_providers/live/games.mrs"}}))


def test_independent_refresh_offline_and_failure(tmp_path, monkeypatch):
    setup_policy(tmp_path)
    calls = []

    def fetch(url):
        assert "adiorany3" not in url
        calls.append(url)
        return b"\x28\xb5\x2f\xfd-test-data"

    monkeypatch.setattr(builder, "fetch", fetch)
    monkeypatch.setattr(builder, "validate", lambda *args: None)
    output = builder.update(tmp_path, True)
    config = yaml.safe_load(output.read_text())
    assert config["rules"] == ["RULE-SET,games-category,REJECT", "DOMAIN,pay.example,DIRECT", "MATCH,DIRECT"]
    assert len(calls) == 1
    builder.update(tmp_path, False)
    assert len(calls) == 1
    previous = output.read_bytes()
    monkeypatch.setattr(builder, "fetch", lambda url: b"<html>broken feed</html>")
    with pytest.raises(ValueError):
        builder.update(tmp_path, True)
    assert output.read_bytes() == previous


def test_bad_domain_feed_rejected(tmp_path):
    with pytest.raises(ValueError):
        builder.materialize(b"<html>error</html>", "text", tmp_path / "bad.mrs", tmp_path / "core")


def test_catalog_independent():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "gameblock_policy" / "sources.json").read_text())
    assert "games-category" in manifest
    assert all("/adiorany3/" not in spec["url"] for spec in manifest.values())


def test_offline_rejects_changed_source(tmp_path, monkeypatch):
    setup_policy(tmp_path)
    monkeypatch.setattr(builder, "fetch", lambda url: b"\x28\xb5\x2f\xfd-test")
    monkeypatch.setattr(builder, "validate", lambda *args: None)
    output = builder.update(tmp_path, True)
    previous = output.read_bytes()
    path = tmp_path / "gameblock_policy/sources.json"
    manifest = json.loads(path.read_text())
    manifest["games-category"]["url"] += "?changed"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="cache berbeda"):
        builder.update(tmp_path, False)
    assert output.read_bytes() == previous


@pytest.mark.parametrize("path", ["", ".", "rule_providers", "../escape"])
def test_invalid_catalog_path(path):
    with pytest.raises(ValueError):
        builder.validate_manifest({"test": {"url": "https://raw.githubusercontent.com/a/b/main/f", "format": "mrs", "path": path}})


def test_duplicate_catalog_paths():
    spec = {"url": "https://raw.githubusercontent.com/a/b/main/f", "format": "mrs", "path": "rule_providers/test.mrs"}
    with pytest.raises(ValueError, match="duplikat"):
        builder.validate_manifest({"one": spec, "two": spec})


def test_unknown_feed_format(tmp_path):
    with pytest.raises(ValueError, match="Format"):
        builder.materialize(b"data", "unknown", tmp_path / "feed", tmp_path / "core")


def test_yaml_payload_must_be_list(tmp_path):
    with pytest.raises(ValueError):
        builder.materialize(b"payload: abcdefghijklmnop", "yaml", tmp_path / "feed", tmp_path / "core")