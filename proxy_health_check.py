#!/usr/bin/env python3
"""Check proxy health and filter candidate URLs.
Reads candidates from `fresh_candidates.txt` (one per line), attempts a TCP
connection to the host on port 443 with a timeout from config, and writes the
alive ones back to the same file.
"""

import socket
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("config.yaml")
if CONFIG_PATH.is_file():
    _config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
else:
    _config = {}

PROXY_HEALTH_CHECK_ENABLED = _config.get("PROXY_HEALTH_CHECK_ENABLED", False)
PROXY_HEALTH_TIMEOUT = _config.get("PROXY_HEALTH_TIMEOUT", 5)

CANDIDATES_FILE = Path(__file__).parent / "fresh_pool" / "fresh_candidates.txt"


def _is_alive(url: str) -> bool:
    try:
        # Extract host (ignore scheme and path)
        host = url.split('://')[1].split('/')[0].split(':')[0]
        with socket.create_connection((host, 443), timeout=PROXY_HEALTH_TIMEOUT):
            return True
    except Exception:
        return False


def main():
    if not PROXY_HEALTH_CHECK_ENABLED:
        print("Proxy health check disabled via config.")
        return
    if not CANDIDATES_FILE.is_file():
        print(f"Candidates file {CANDIDATES_FILE} not found")
        return
    candidates = [line.strip() for line in CANDIDATES_FILE.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith('#')]
    alive = [c for c in candidates if _is_alive(c)]
    CANDIDATES_FILE.write_text("\n".join(alive), encoding="utf-8")
    print(f"Filtered {len(candidates)} candidates to {len(alive)} alive proxies")

if __name__ == "__main__":
    main()
