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