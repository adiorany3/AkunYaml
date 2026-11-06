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


def test_direct_subscription_has_openclash_group_without_fake_accounts(tmp_path):
    config = {"rules": ["DOMAIN,ads.example,REJECT", "MATCH,DIRECT"]}
    result = subscription_profile(config, tmp_path, tmp_path)
    assert result["proxies"] == []
    assert result["proxy-groups"] == [
        {"name": "DIRECT-ONLY", "type": "select", "proxies": ["DIRECT"]}
    ]
    assert result["rules"] == config["rules"]
    assert "proxies" not in config
    assert "proxy-groups" not in config


def test_existing_account_group_not_replaced(tmp_path):
    config = {"proxies": [{"name": "account"}], "proxy-groups": [
        {"name": "PROXY", "type": "select", "proxies": ["account"]}
    ]}
    assert subscription_profile(config, tmp_path, tmp_path) == config