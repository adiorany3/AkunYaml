#!/usr/bin/env python3
from pathlib import Path

import local_runner as runner

root = Path(__file__).resolve().parent
allowlist = set(runner.load_allowlist(root))
assert set(runner.SPEEDTEST_DOMAIN_SUFFIXES) <= allowlist
assert all(rule.endswith(",GLOBAL") for rule in runner.SPEEDTEST_NODE_RULES)
assert not any(rule.endswith(",DIRECT") for rule in runner.SPEEDTEST_NODE_RULES)
for domain in runner.SPEEDTEST_DOMAIN_SUFFIXES:
    assert any(domain == line or domain.endswith("." + line) for line in allowlist)
print("[OK] Speedtest official domains bypass blocklists via GLOBAL/node aktif")
