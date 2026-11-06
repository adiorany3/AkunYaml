import copy

import pytest
import yaml

from unified_update import bundle_yaml, collect, mac_profile, validate_bundle


def test_mac_profile_preserves_policy():
    source = {"redir-port": 7892, "tproxy-port": 7895, "allow-lan": True, "dns": {"listen": "0.0.0.0:7874"}, "rules": ["MATCH,DIRECT"]}
    before = copy.deepcopy(source)
    result = mac_profile(source)
    assert source == before
    assert "redir-port" not in result and "tproxy-port" not in result
    assert result["allow-lan"] is False
    assert result["dns"]["listen"] == "127.0.0.1:7874"
    assert result["rules"] == source["rules"]


def test_bundle_copies_provider(tmp_path):
    source = tmp_path / "input.yaml"
    (tmp_path / "rules.yaml").write_text("payload: []\n")
    source.write_text(yaml.safe_dump({"rules": ["MATCH,DIRECT"], "rule-providers": {"ads": {"type": "file", "path": "rules.yaml"}}}))
    bundle_yaml(source, tmp_path / "bundle", "config.yaml")
    assert (tmp_path / "bundle/rules.yaml").exists()


def test_missing_input_preserves_output(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    (output / "previous.txt").write_text("keep")
    with pytest.raises(FileNotFoundError):
        collect(tmp_path, "offline")
    assert (output / "previous.txt").read_text() == "keep"


def test_provider_traversal_rejected(tmp_path):
    source = tmp_path / "input.yaml"
    source.write_text(yaml.safe_dump({"rule-providers": {"ads": {"type": "file", "path": "../escape"}}}))
    with pytest.raises(ValueError):
        bundle_yaml(source, tmp_path / "bundle", "config.yaml")


def test_all_profile_types_validated(tmp_path, monkeypatch):
    from types import SimpleNamespace

    import unified_update
    paths = ["openclash/proxy/auto.yaml", "openclash/direct/direct.yaml", "mihomo-mac/direct/config.yaml", "sing-box/profile.json"]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(unified_update.subprocess, "run", run)
    validate_bundle(tmp_path, tmp_path)
    assert len(calls) == 4
    assert any("check" in command for command in calls)
    assert {command[-1] for command in calls} == {str(tmp_path / p) for p in paths}


def test_invalid_singbox_aborts_validation(tmp_path, monkeypatch):
    from types import SimpleNamespace

    import unified_update
    folder = tmp_path / "sing-box"
    folder.mkdir()
    (folder / "bad.json").write_text("{}")
    monkeypatch.setattr(unified_update.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="invalid"))
    with pytest.raises(RuntimeError, match="Sing-box"):
        validate_bundle(tmp_path, tmp_path)