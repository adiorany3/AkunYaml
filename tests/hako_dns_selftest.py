"""Run with: .venv/bin/python tests/hako_dns_selftest.py"""
import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_update import hako_singbox

for name in ("singbox_android.json", "singbox_direct_adblock.json"):
    source = json.loads((ROOT / "output/sing-box" / name).read_text())
    original = copy.deepcopy(source)
    config = hako_singbox(source)
    assert source == original
    server = config["dns"]["servers"][0]
    assert server["type"] == "https" and server["server"] == "1.1.1.1"
    assert server["detour"] == "direct"
    assert server["tls"] == {"enabled": True, "server_name": "cloudflare-dns.com"}
    assert config["dns"]["rules"] == source["dns"]["rules"]
    assert config["outbounds"] == source["outbounds"]
    assert any(r.get("port") == 53 and r.get("action") == "hijack-dns"
               for r in config["route"]["rules"])
    assert hako_singbox(config) == config
    output = ROOT / "output/sing-box" / ("singbox_hako_proxy.json" if name == "singbox_android.json" else "singbox_hako_direct_adblock.json")
    assert json.loads(output.read_text()) == config
    subprocess.run([str(ROOT / ".local_bin/sing-box"), "check", "-c", str(output)], check=True)
print("PASS: Hako DNS bootstrap, direct DoH, preserved routing, core validation")
