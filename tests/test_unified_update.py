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
    validated = validate_bundle(tmp_path, tmp_path)
    assert len(validated) == 4
    assert any(path.suffix == ".json" for path in validated)
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


@pytest.mark.parametrize("stage,code,expected,mode", [
    ("local_runner.py", 3, 0, "security-refresh-retained-accounts"),
    ("local_runner.py", 2, 2, None),
    ("local_update.py", 3, 3, None),
])
def test_runner_partial_only_allows_security_update(tmp_path, monkeypatch, stage, code, expected, mode):
    from types import SimpleNamespace

    import unified_update
    monkeypatch.setattr(unified_update, "__file__", str(tmp_path / "unified_update.py"))
    monkeypatch.setattr("sys.argv", ["unified_update.py"])
    monkeypatch.setattr(unified_update, "refresh_adaptive_guard", lambda root: None)
    calls, published = [], []

    def run(command, **kwargs):
        name = command[1].split("/")[-1]
        calls.append(name)
        return SimpleNamespace(returncode=code if name == stage else 0)

    monkeypatch.setattr(unified_update.subprocess, "run", run)
    monkeypatch.setattr(unified_update, "collect", lambda root, status: published.append(status) or root / "output")
    assert unified_update.main() == expected
    assert published == ([mode] if mode else [])
    if mode:
        assert calls == ["local_runner.py", "local_update.py", "independent_gameblock.py"]
    assert not (tmp_path / ".runtime_cache/unified_update.lock").exists()