import json
import socket

import pytest
import yaml

from local_update import build, direct_clash, direct_singbox


def test_clash_direct():
    source = {"proxies": [{"password": "private"}], "rules": ["DOMAIN,ads.example,REJECT", "IP-CIDR,10.0.0.0/8,MANUAL,no-resolve", "MATCH,AUTO"]}
    result = direct_clash(source)
    assert "proxies" not in result
    assert "proxies" in source
    assert result["rules"] == ["DOMAIN,ads.example,REJECT", "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve", "MATCH,DIRECT"]


def test_singbox_direct():
    source = {"outbounds": [{"type": "trojan", "password": "private"}], "route": {"final": "proxy", "rules": [{"action": "reject"}, {"outbound": "proxy"}]}}
    result = direct_singbox(source)
    assert result["outbounds"] == [{"type": "direct", "tag": "direct"}]
    assert result["route"]["rules"] == [{"action": "reject"}, {"outbound": "direct"}]
    assert source["route"]["final"] == "proxy"


def sources(root):
    (root / "openclash_auto.yaml").write_text(yaml.safe_dump({"rules": ["MATCH,AUTO"]}))
    (root / "singbox_android.json").write_text(json.dumps({"route": {"rules": [{"action": "reject"}]}}))


def test_build_offline(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Network forbidden")
    monkeypatch.setattr(socket, "socket", forbidden)
    sources(tmp_path)
    files = build(tmp_path, tmp_path / "out")
    assert len(files) == 3
    assert all(path.exists() for path in files)
    assert json.loads(files[-1].read_text())["proxy_accounts"] == 0


def test_reject_root_output(tmp_path):
    with pytest.raises(ValueError):
        build(tmp_path, tmp_path)


def test_missing_provider_does_not_publish(tmp_path):
    sources(tmp_path)
    (tmp_path / "openclash_auto.yaml").write_text(yaml.safe_dump({"rules": ["RULE-SET,ads,REJECT"], "rule-providers": {"ads": {"type": "file", "path": "missing.yaml"}}}))
    with pytest.raises(FileNotFoundError):
        build(tmp_path, tmp_path / "out")
    assert not (tmp_path / "out").exists()