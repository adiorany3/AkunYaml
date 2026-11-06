from pathlib import Path

import pytest
import yaml


@pytest.mark.parametrize("host", ["games.co.id", "www.games.co.id", "play.games.co.id"])
def test_games_co_id_blocked_before_other_rules(host):
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml").read_text())
    rule = config["rules"][0].split(",")
    assert rule == ["DOMAIN-SUFFIX", "games.co.id", "REJECT"]
    assert host == rule[1] or host.endswith("." + rule[1])
    assert config["rules"].count(",".join(rule)) == 1


@pytest.mark.parametrize("host", ["easy-games.io", "www.easy-games.io", "play.easy-games.io"])
def test_easy_games_priority_suffix(host):
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml").read_text())
    rule = "DOMAIN-SUFFIX,easy-games.io,REJECT"
    assert config["rules"][1] == rule
    assert config["rules"].count(rule) == 1
    assert host == "easy-games.io" or host.endswith(".easy-games.io")


@pytest.mark.parametrize("host", ["coolgamesfree.org", "www.coolgamesfree.org", "play.coolgamesfree.org"])
def test_coolgamesfree_priority_suffix(host):
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml").read_text())
    rule = "DOMAIN-SUFFIX,coolgamesfree.org,REJECT"
    assert config["rules"][2] == rule
    assert config["rules"].count(rule) == 1
    assert host == "coolgamesfree.org" or host.endswith(".coolgamesfree.org")


@pytest.mark.parametrize("domain", ["poki.com", "crazygames.com", "y8.com", "friv.com"])
def test_existing_online_game_portals_remain_blocked(domain):
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml").read_text())
    assert f"DOMAIN-SUFFIX,{domain},REJECT" in config["rules"]