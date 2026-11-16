import pytest

from openwrt_export import manual_gameblock, subscription_profile


def test_gameblock_account_profiles_offer_blocked_and_unblocked_options(tmp_path):
    from openwrt_export import gameblock_account_profile

    game_folder = tmp_path / "gameblock"
    proxy_folder = tmp_path / "proxy"
    (game_folder / "rule_providers").mkdir(parents=True)
    (proxy_folder / "rule_providers").mkdir(parents=True)
    (game_folder / "rule_providers/games.mrs").write_bytes(b"games")
    (game_folder / "rule_providers/manual.txt").write_text("poki.com\n")
    game_config = {
        "rules": ["DOMAIN-SUFFIX,games.co.id,REJECT", "RULE-SET,games-category,REJECT", "RULE-SET,game-block-online,REJECT", "DOMAIN-SUFFIX,pay.example,DIRECT"],
        "rule-providers": {
            "games-blackmatrix": {"type": "file", "behavior": "classical", "format": "yaml", "path": "./rule_providers/games.mrs"},
            "games-category": {"type": "file", "behavior": "domain", "format": "mrs", "path": "./rule_providers/games.mrs"},
            "game-block-online": {"type": "file", "behavior": "domain", "format": "text", "path": "./rule_providers/manual.txt"},
        },
    }
    account_config = {"proxies": [{"name": "node"}], "rules": ["DOMAIN-SUFFIX,pay.example,DIRECT", "MATCH,GLOBAL"]}
    result = gameblock_account_profile(account_config, game_config, game_folder, proxy_folder)
    assert result["proxies"] == account_config["proxies"]
    assert result["rules"][:4] == [
        "RULE-SET,games-blackmatrix,REJECT",
        "RULE-SET,games-category,REJECT",
        "RULE-SET,game-block-online,REJECT",
        "DOMAIN-SUFFIX,games.co.id,REJECT",
    ]
    assert result["rules"].index("RULE-SET,game-block-online,REJECT") < result["rules"].index("DOMAIN-SUFFIX,pay.example,DIRECT")
    assert result["rule-providers"]["games-category"]["path"] == "./rule_providers/gameblock/games-category.mrs"
    assert (proxy_folder / "rule_providers/gameblock/game-block-online.txt").is_file()
    assert "RULE-SET,games-category,REJECT" not in account_config["rules"]
    assert "rule-providers" not in account_config

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


def test_heryaml_manual_layout():
    source = {"rules": ["DOMAIN,bad.example,REJECT", "DOMAIN,pay.example,DIRECT", "MATCH,DIRECT"]}
    accounts = [{"name": "LOCAL-ACCOUNT", "type": "vless"}]
    result = manual_gameblock(source, accounts)
    assert result["proxy-groups"] == [{"name": "MANUAL", "type": "select", "proxies": ["DIRECT", "LOCAL-ACCOUNT"]}]
    assert result["proxies"] == accounts
    assert result["rules"][:-1] == source["rules"][:-1]
    assert result["rules"][-1] == "MATCH,MANUAL"
    assert result["profile"]["store-selected"] is False
    assert source["rules"][-1] == "MATCH,DIRECT"


@pytest.mark.parametrize("accounts", [[], [{"name": "DIRECT"}], [{"name": "same"}, {"name": "same"}]])
def test_manual_layout_rejects_bad_account_names(accounts):
    with pytest.raises(ValueError):
        manual_gameblock({"rules": ["MATCH,DIRECT"]}, accounts)