import pytest

from openwrt_export import subscription_profile


def test_subscription_replaces_local_provider(tmp_path):
    folder = tmp_path / "openclash/proxy"
    provider = folder / "rule_providers/test.yaml"
    provider.parent.mkdir(parents=True)
    provider.write_text("payload: []")
    config = {"proxies": [{"name": "test"}], "rules": ["RULE-SET,test,REJECT"], "rule-providers": {"test": {"type": "file", "behavior": "classical", "format": "yaml", "path": "./rule_providers/test.yaml"}}}
    result = subscription_profile(config, folder, tmp_path)
    item = result["rule-providers"]["test"]
    assert item["type"] == "http"
    assert item["url"].endswith("/output/openclash/proxy/rule_providers/test.yaml")
    assert item["path"].startswith("./rule_provider/akunyaml-")
    assert result["proxies"] == config["proxies"]
    assert config["rule-providers"]["test"]["type"] == "file"


def test_missing_provider_blocks_export(tmp_path):
    config = {"rule-providers": {"missing": {"type": "file", "path": "missing.yaml"}}}
    with pytest.raises(FileNotFoundError):
        subscription_profile(config, tmp_path, tmp_path)