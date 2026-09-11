#!/usr/bin/env python3
"""Guard conservative gambling regex against false positives."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[OK] {message}")


def main() -> int:
    provider = yaml.safe_load((ROOT / "rule_providers/security-gambling.yaml").read_text(encoding="utf-8")) or {}
    rules = [str(rule) for rule in provider.get("payload", [])]
    patterns = [re.compile(rule.split(",", 2)[1]) for rule in rules if rule.startswith("DOMAIN-REGEX,")]
    check(patterns, "gambling regex loaded")

    def blocked(host: str) -> bool:
        return any(pattern.search(host) for pattern in patterns)

    for host in ("login.judol88.example", "promo-togel.example", "casino.example", "api.sports.bet.example"):
        check(blocked(host), f"blocks {host}")
    for host in ("api.depositphotos.com", "bonusly.com", "spin.com", "withdrawal.example", "bettermode.com"):
        check(not blocked(host), f"allows {host}")
    check(not any(word in "\n".join(rules).lower() for word in ("deposit", "withdraw", "bonus", "spin", "betting", "taruhan")), "no ambiguous keyword blocking")
    print("[OK] conservative gambling guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
