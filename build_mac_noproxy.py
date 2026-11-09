"""Build a single-file Mac direct profile using local, validated provider snapshots."""
import argparse
import copy
from pathlib import Path
import subprocess
import tempfile

import yaml

from openclash_target import atomic_write_text

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "output/mihomo-mac/direct/config.yaml"
TARGET = ROOT / "output/mihomo-mac/direct/openclash_mac_noproxy.yaml"
REFERENCE = "https://raw.githubusercontent.com/adiorany3/HerYaml/refs/heads/main/openclash_mac_noproxy.yaml"


def build(gameblock=False):
    source = ROOT / "output/mihomo-mac/gameblock/config.yaml" if gameblock else SOURCE
    target = source.with_name("openclash_noproxy_gameblock.yaml") if gameblock else TARGET
    reference = REFERENCE.replace("openclash_mac_noproxy.yaml", "openclash_noproxy_gameblock.yaml") if gameblock else REFERENCE
    config = copy.deepcopy(yaml.safe_load(source.read_text()))
    if gameblock:
        game_rules = [f"RULE-SET,{name},REJECT" for name in ("game-block-online", "games-category")]
        for name in ("game-block-online", "games-category"):
            if name not in config.get("rule-providers", {}):
                raise ValueError(f"Missing game provider: {name}")
        config["rules"] = game_rules + [rule for rule in config["rules"] if rule not in game_rules]
    for key in ("proxies", "proxy-providers", "proxy-groups", "redir-port", "tproxy-port", "lan-allowed-ips", "external-controller", "secret"):
        config.pop(key, None)
    config.update({"mixed-port": 7890, "allow-lan": False, "bind-address": "127.0.0.1", "mode": "rule"})
    # ponytail: system proxy first; enable TUN only after client-specific tunnel testing.
    config["tun"] = {"enable": False, "stack": "system", "auto-route": True,
                     "auto-detect-interface": True, "dns-hijack": ["any:53", "tcp://any:53"]}
    dns = config["dns"]
    dns.update({"listen": "127.0.0.1:7874", "respect-rules": False,
                "nameserver": ["https://1.1.1.1/dns-query", "https://9.9.9.9/dns-query"],
                "default-nameserver": ["https://1.1.1.1/dns-query", "https://9.9.9.9/dns-query"]})
    for key in ("fallback", "fallback-filter", "nameserver-policy", "proxy-server-nameserver"):
        dns.pop(key, None)
    for name, provider in config.get("rule-providers", {}).items():
        if "path" not in provider:
            continue
        path = (source.parent / provider["path"]).resolve()
        if not path.is_relative_to(source.parent.resolve()):
            raise ValueError(f"Unsafe provider path: {name}")
        if not path.is_file():
            if provider.get("type") != "http" or not provider.get("url", "").startswith("https://"):
                raise FileNotFoundError(path)
            # Remote providers remain HTTPS downloads, never silently dropped.
            continue
        if provider.get("format") == "mrs":
            with tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "rules.txt"
                subprocess.run([str(ROOT / ".local_bin/mihomo"), "convert-ruleset",
                                provider["behavior"], "mrs", str(path), str(output)], check=True)
                payload = output.read_text().splitlines()
        elif provider.get("format", "yaml") == "yaml":
            payload = yaml.safe_load(path.read_text())["payload"]
        else:
            payload = [line.strip() for line in path.read_text().splitlines()
                       if line.strip() and not line.startswith(("#", "//"))]
        config["rule-providers"][name] = {"type": "inline", "behavior": provider["behavior"], "payload": payload}
    assert not config.get("proxies") and not config.get("proxy-providers")
    for rule in config["rules"]:
        parts = rule.split(",")
        policy = parts[-2] if parts[-1] == "no-resolve" else parts[-1]
        assert policy in {"DIRECT", "REJECT", "REJECT-DROP", "PASS"}, rule
    text = "# Mac no-proxy; reference: " + reference + "\n# Enable System Proxy in your Mihomo-compatible client; TUN is off.\n"
    text += yaml.safe_dump(config, sort_keys=False, allow_unicode=True)
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / target.name
        candidate.write_text(text)
        result = subprocess.run([str(ROOT / ".local_bin/mihomo"), "-t", "-d", tmp, "-f", str(candidate)],
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-4000:])
    atomic_write_text(target, text)
    print(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gameblock", action="store_true")
    build(gameblock=parser.parse_args().gameblock)
