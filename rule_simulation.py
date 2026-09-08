#!/usr/bin/env python3
"""Simulate representative DNS rule matches without making network requests."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "openclash_auto.yaml"
CASES = (
    ("YouTube ad", "ads.youtube.com", "REJECT"),
    ("Google ad", "pagead2.googlesyndication.com", "REJECT"),
    ("Android/app ad", "ads.applovin.com", "REJECT"),
    ("Popup ad", "popads.net", "REJECT"),
    ("Gambling sponsor", "promo-slot88.example", "REJECT"),
    ("Gambling TLD", "example.bet", "REJECT"),
    ("YouTube playback", "r3---sn.googlevideo.com", "YOUTUBE"),
    ("YouTube image", "i.ytimg.com", "YOUTUBE"),
    ("Netflix playback", "ipv4-c009-xxx.1.oca.nflxvideo.net", None),
)


def host_match(kind: str, value: str, host: str) -> bool:
    if kind == "DOMAIN":
        return host == value
    if kind == "DOMAIN-SUFFIX":
        return host == value or host.endswith("." + value)
    if kind == "DOMAIN-REGEX":
        try:
            return re.search(value, host, re.IGNORECASE) is not None
        except re.error as exc:
            raise SystemExit(f"invalid regex {value!r}: {exc}") from exc
    return False


def payload_rules(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [str(x) for x in data.get("payload", []) or []]


def main() -> int:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    providers = data.get("rule-providers") or {}
    rules = [str(x) for x in data.get("rules", []) or []]
    provider_payloads: dict[str, list[str]] = {}
    for name, provider in providers.items():
        if not isinstance(provider, dict) or provider.get("format") != "yaml":
            continue
        path = ROOT / str(provider.get("path", "")).removeprefix("./")
        if path.is_file():
            provider_payloads[name] = payload_rules(path)

    def match(host: str) -> tuple[str, str] | None:
        for rule in rules:
            parts = rule.split(",", 2)
            if len(parts) != 3:
                continue
            kind, value, policy = parts
            if kind == "RULE-SET":
                for payload in provider_payloads.get(value, []):
                    p = payload.split(",", 2)
                    if len(p) == 3 and host_match(p[0], p[1], host):
                        return rule, p[2]
            elif host_match(kind, value, host):
                return rule, policy
        return None

    failed = False
    for label, host, expected in CASES:
        result = match(host)
        policy = result[1] if result else None
        ok = policy == expected if expected is not None else policy not in {"REJECT", "REJECT-DROP"}
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {label}: {host} => {policy or 'UNMATCHED'}")
        if not ok:
            failed = True
    print("[OK] DNS rule simulation passed" if not failed else "[FAIL] DNS rule simulation failed")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())

# Self-check: suffix matching must not match a lookalike domain.
assert host_match("DOMAIN-SUFFIX", "example.com", "badexample.com") is False

# ponytail: compiled MRS providers stay engine-tested; add MRS decoding only if static coverage becomes necessary.
