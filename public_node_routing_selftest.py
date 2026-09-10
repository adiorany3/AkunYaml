"""Offline regression: public traffic never bypasses proxy nodes."""
from pathlib import Path

import yaml

import generate_yaml
from sumberyaml_core import _enforce_no_selector_no_direct_config

ROOT = Path(__file__).resolve().parent
FILES = ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml")
LAN_PREFIXES = (
    "DOMAIN-SUFFIX,local,", "DOMAIN-SUFFIX,lan,", "DOMAIN-SUFFIX,localhost,",
    "IP-CIDR,127.0.0.0/8,", "IP-CIDR,10.0.0.0/8,", "IP-CIDR,172.16.0.0/12,",
    "IP-CIDR,192.168.0.0/16,", "IP-CIDR,169.254.0.0/16,", "GEOIP,LAN,",
)
BYPASS = {"DIRECT", "PASS", "COMPATIBLE"}

for filename in FILES:
    config = yaml.safe_load((ROOT / filename).read_text(encoding="utf-8")) or {}
    assert config.get("proxies"), f"{filename}: tidak ada node"
    for group in config.get("proxy-groups", []):
        assert group.get("proxies"), f"{filename}: grup kosong {group.get('name')}"
        assert not BYPASS.intersection(map(str, group["proxies"])), f"{filename}: bypass dalam {group.get('name')}"
    for rule in config.get("rules", []):
        parts = str(rule).split(",")
        policy = parts[-2].strip() if parts[-1].strip() == "no-resolve" else parts[-1].strip()
        assert policy not in BYPASS or str(rule).startswith(LAN_PREFIXES), f"{filename}: bypass publik {rule}"
    assert config.get("rules", [])[-1] == "MATCH,GLOBAL", f"{filename}: final bukan GLOBAL"

fixture = {
    "proxies": [{"name": "node", "type": "ss"}],
    "proxy-groups": [{"name": "GLOBAL", "type": "select", "proxies": ["DIRECT", "node"]}],
    "rules": ["DOMAIN-SUFFIX,local,DIRECT", "DOMAIN-SUFFIX,example.com,DIRECT", "MATCH,GLOBAL"],
}
for processed in (
    _enforce_no_selector_no_direct_config(fixture),
    yaml.safe_load(generate_yaml._enforce_no_selector_no_direct_yaml_text(yaml.safe_dump(fixture))),
):
    assert processed["rules"][0] == "DOMAIN-SUFFIX,local,DIRECT"
    assert processed["rules"][1] == "DOMAIN-SUFFIX,example.com,GLOBAL"
    assert "DIRECT" not in processed["proxy-groups"][0]["proxies"]

print("PASS: semua trafik publik memakai node; DIRECT hanya LAN/private")
