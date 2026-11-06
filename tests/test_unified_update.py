import copy

import pytest
import yaml

from unified_update import bundle_yaml, collect, mac_profile


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