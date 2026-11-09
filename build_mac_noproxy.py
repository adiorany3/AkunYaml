"""Build a single-file Mac direct profile using local, validated provider snapshots."""
import argparse
import copy
from pathlib import Path
import subprocess
import tempfile
import socket
import time
from concurrent.futures import ThreadPoolExecutor

import yaml

from openclash_target import atomic_write_text

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "output/mihomo-mac/direct/config.yaml"
TARGET = ROOT / "output/mihomo-mac/direct/openclash_mac_noproxy.yaml"
REFERENCE = "https://raw.githubusercontent.com/adiorany3/HerYaml/refs/heads/main/openclash_mac_noproxy.yaml"


def live_nodes():
    """Probe actual HTTPS traffic through each existing manual/public node."""
    nodes = yaml.safe_load((ROOT / "openclash_auto.yaml").read_text()).get("proxies", [])
    if not nodes:
        raise ValueError("No existing manual/public nodes to test")

    def probe(node):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.yaml"
            path.write_text(yaml.safe_dump({"mixed-port": port, "bind-address": "127.0.0.1",
                "allow-lan": False, "mode": "rule", "log-level": "silent",
                "proxies": [node], "rules": ["MATCH," + node["name"]]}))
            with (Path(tmp) / "core.log").open("w") as log:
                proc = subprocess.Popen([str(ROOT / ".local_bin/mihomo"), "-d", tmp, "-f", str(path)], stdout=log, stderr=log)
                try:
                    deadline = time.monotonic() + 5
                    while time.monotonic() < deadline and proc.poll() is None:
                        try:
                            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                                break
                        except OSError:
                            time.sleep(0.1)
                    result = subprocess.run(["curl", "--noproxy", "", "--proxy", f"http://127.0.0.1:{port}",
                        "--connect-timeout", "5", "--max-time", "12", "--silent", "--output", "/dev/null",
                        "--write-out", "%{http_code}", "https://www.gstatic.com/generate_204"],
                        capture_output=True, text=True, timeout=15)
                    alive = result.returncode == 0 and result.stdout.strip() == "204"
                    print(node["name"], "HTTPS 204" if alive else "FAILED", flush=True)
                    return node if alive else None
                finally:
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait()
    with ThreadPoolExecutor(max_workers=4) as pool:
        healthy = [node for node in pool.map(probe, nodes) if node is not None]
    if not healthy:
        raise RuntimeError("No node passed HTTPS testing; existing output preserved")
    return healthy


def build(gameblock=False, include_nodes=False):
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
    if include_nodes:
        config["proxies"] = live_nodes()
        names = [node["name"] for node in config["proxies"]]
        config["proxy-groups"] = [{"name": "OPTIONAL-PROXY", "type": "select", "proxies": ["DIRECT", *names]}]
    assert not config.get("proxy-providers")
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
    parser.add_argument("--include-live-nodes", action="store_true")
    args = parser.parse_args()
    build(gameblock=args.gameblock, include_nodes=args.include_live_nodes)
