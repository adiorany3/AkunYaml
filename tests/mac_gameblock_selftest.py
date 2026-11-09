"""Run: .venv/bin/python tests/mac_gameblock_selftest.py"""
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
path = root / "output/mihomo-mac/gameblock/openclash_noproxy_gameblock.yaml"
config = yaml.safe_load(path.read_text())
assert not any(config.get(k) for k in ("proxies", "proxy-providers", "proxy-groups"))
assert config["bind-address"] == "127.0.0.1" and not config["allow-lan"]
assert config["tun"]["enable"] is False
assert config["rules"][:2] == ["RULE-SET,game-block-online,REJECT", "RULE-SET,games-category,REJECT"]
assert config["rules"][-1] == "MATCH,DIRECT"
assert all(p["type"] == "inline" for p in config["rule-providers"].values())
provider = config["rule-providers"]["game-block-online"]
assert provider["behavior"] == "domain"
for host in ("games.co.id", "easy-games.io", "coolgamesfree.org", "poki.com", "crazygames.com", "y8.com", "friv.com"):
    assert f"DOMAIN-SUFFIX,{host}" in provider["payload"] or f"DOMAIN-SUFFIX,{host},REJECT" in config["rules"], host
print(f"PASS: {len(config['rules'])} rules, self-contained providers, game priority, no proxy")
