#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
NORMAL_OUTPUTS = ("openclash_auto.yaml", "openclash_fresh_pool.yaml")
LIGHT_OUTPUTS = ("openclash_android.yaml", "openclash_lite.yaml")
VALID_STRATEGIES = {"consistent-hashing", "round-robin", "sticky-sessions"}
SENSITIVE_POLICIES = {
    "AI",
    "AI-OPENAI",
    "AI-CLAUDE",
    "AI-GEMINI",
    "AI-OTHER",
    "REDDIT",
    "YOUTUBE",
    "SOCIAL-MEDIA",
    "STREAMING",
    "EDUKASI",
    "MANUAL",
    "DIRECT",
    "REJECT",
}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def group_map(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(group.get("name")): group
        for group in config.get("proxy-groups", []) or []
        if isinstance(group, dict) and group.get("name")
    }


def rule_policy(rule: str) -> str:
    parts = [part.strip() for part in rule.split(",")]
    if len(parts) < 2:
        return ""
    return parts[-2] if parts[-1].lower() == "no-resolve" else parts[-1]


def manual_policy_errors(config: dict[str, Any]) -> list[str]:
    groups = group_map(config)
    errors = []
    if (groups.get("REDDIT") or {}).get("proxies") != ["MANUAL"]:
        errors.append("REDDIT harus menunjuk hanya ke MANUAL")
    manual = groups.get("MANUAL") or {}
    if manual.get("type") != "fallback":
        errors.append("MANUAL harus berupa fallback")
    physical = {
        proxy["name"]
        for proxy in config.get("proxies", []) or []
        if isinstance(proxy, dict)
        and isinstance(proxy.get("name"), str)
        and proxy["name"].startswith("MANUAL-")
        and proxy["name"] not in groups
        and proxy.get("type") not in (None, "", "direct", "reject", "pass", "dns")
    }
    members = manual.get("proxies")
    if not isinstance(members, list) or not members or any(
        not isinstance(name, str) or name not in physical for name in members
    ):
        errors.append("MANUAL harus berisi proxy fisik manual yang valid dan tidak kosong")
    return errors


def main() -> int:
    failures: list[str] = []
    settings = json.loads((ROOT / "local_config.json").read_text(encoding="utf-8"))
    limit = max(2, min(8, int(settings.get("LOAD_BALANCE_NODE_LIMIT", 4))))
    expected_strategy = str(settings.get("LOAD_BALANCE_STRATEGY", "sticky-sessions")).strip().lower()
    if expected_strategy not in VALID_STRATEGIES:
        expected_strategy = "sticky-sessions"

    for filename in NORMAL_OUTPUTS:
        path = ROOT / filename
        if not path.is_file():
            failures.append(f"{filename}: output hilang")
            continue
        config = load_yaml(path)
        groups = group_map(config)
        proxies = {
            str(proxy.get("name"))
            for proxy in config.get("proxies", []) or []
            if isinstance(proxy, dict) and proxy.get("name")
        }
        balance = groups.get("LOAD-BALANCE")
        if not balance:
            failures.append(f"{filename}: LOAD-BALANCE hilang")
            continue
        candidates = [str(name) for name in balance.get("proxies", []) or []]
        if balance.get("type") != "load-balance":
            failures.append(f"{filename}: tipe LOAD-BALANCE invalid")
        if balance.get("strategy") != expected_strategy:
            failures.append(f"{filename}: strategy {balance.get('strategy')!r} != {expected_strategy!r}")
        if not candidates or len(candidates) > limit:
            failures.append(f"{filename}: jumlah kandidat {len(candidates)} di luar 1..{limit}")
        if len(candidates) != len(set(candidates)):
            failures.append(f"{filename}: kandidat duplikat")
        invalid = [name for name in candidates if name not in proxies]
        if invalid:
            failures.append(f"{filename}: kandidat bukan proxy fisik: {invalid}")
        global_group = groups.get("GLOBAL") or {}
        if (global_group.get("proxies") or [None])[0] != "LOAD-BALANCE":
            failures.append(f"{filename}: GLOBAL tidak default ke LOAD-BALANCE")
        failures.extend(f"{filename}: {error}" for error in manual_policy_errors(config))
        rules = [str(rule) for rule in config.get("rules", []) or []]
        if filename == "openclash_auto.yaml":
            if "RULE-SET,manual-routing,MANUAL" not in rules:
                failures.append(f"{filename}: manual-routing ke MANUAL hilang")
            for domain in ("x.com", "twitter.com"):
                if f"DOMAIN-SUFFIX,{domain},REDDIT" not in rules:
                    failures.append(f"{filename}: {domain} tidak terkunci ke REDDIT")
        match_indexes = [index for index, rule in enumerate(rules) if rule.startswith(("MATCH,", "FINAL,"))]
        if not match_indexes:
            failures.append(f"{filename}: catch-all hilang")
        else:
            catch_all = match_indexes[-1]
            if rule_policy(rules[catch_all]) != "GLOBAL":
                failures.append(f"{filename}: catch-all bukan GLOBAL")
            late_sensitive = [rule for rule in rules[catch_all + 1 :] if rule_policy(rule) in SENSITIVE_POLICIES]
            if late_sensitive:
                failures.append(f"{filename}: rule sensitif sesudah catch-all")
        if config.get("keep-alive-interval") != int(settings.get("KEEP_ALIVE_INTERVAL", 15)):
            failures.append(f"{filename}: keep-alive-interval tidak konsisten")
        if config.get("keep-alive-idle") != int(settings.get("KEEP_ALIVE_IDLE", 30)):
            failures.append(f"{filename}: keep-alive-idle tidak konsisten")

    for filename in LIGHT_OUTPUTS:
        path = ROOT / filename
        if not path.is_file():
            failures.append(f"{filename}: output hilang")
            continue
        config = load_yaml(path)
        groups = group_map(config)
        if "LOAD-BALANCE" in groups:
            failures.append(f"{filename}: LOAD-BALANCE bocor ke profil ringan")
        failures.extend(f"{filename}: {error}" for error in manual_policy_errors(config))
        rules = [str(rule) for rule in config.get("rules", []) or []]
        for domain in ("x.com", "twitter.com"):
            if f"DOMAIN-SUFFIX,{domain},REDDIT" not in rules:
                failures.append(f"{filename}: {domain} tidak terkunci ke REDDIT")

    print("Load-balance policy audit:", "OK" if not failures else "FAIL")
    for failure in failures:
        print(" -", failure)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
