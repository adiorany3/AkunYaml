#!/usr/bin/env python3
"""Compress large contiguous MANUAL routing blocks into a local rule-provider.

The transformation is intentionally conservative: only one contiguous block of
DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD rules targeting MANUAL is compressed.
This preserves rule ordering exactly because the block is replaced in place by
one RULE-SET reference and the provider payload keeps the same match semantics.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_PROVIDER_NAME = "manual-routing"
_PROVIDER_PATH = "./rule_providers/manual-routing.yaml"
_ALLOWED_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}


def _manual_payload(rule: str) -> str | None:
    parts = [part.strip() for part in str(rule).split(",")]
    if len(parts) != 3:
        return None
    rule_type, value, policy = parts
    if rule_type.upper() not in _ALLOWED_TYPES or policy.upper() != "MANUAL" or not value:
        return None
    return f"{rule_type.upper()},{value}"


def _largest_contiguous_block(rules: list[str]) -> tuple[int, int, list[str]] | None:
    best: tuple[int, int, list[str]] | None = None
    start: int | None = None
    payload: list[str] = []

    def finish(end: int) -> None:
        nonlocal best, start, payload
        if start is None:
            return
        candidate = (start, end, payload[:])
        if best is None or len(candidate[2]) > len(best[2]):
            best = candidate
        start = None
        payload = []

    for index, rule in enumerate(rules):
        item = _manual_payload(rule)
        if item is None:
            finish(index)
            continue
        if start is None:
            start = index
        payload.append(item)
    finish(len(rules))
    return best


def compress_manual_routing(
    config: dict[str, Any],
    workdir: Path,
    *,
    threshold: int = 40,
    provider_name: str = _PROVIDER_NAME,
) -> dict[str, Any]:
    """Compress a large contiguous MANUAL block and return audit metadata."""
    rules_obj = config.get("rules")
    if not isinstance(rules_obj, list):
        return {"changed": False, "count": 0, "reason": "rules-not-list"}
    rules = [str(rule).strip() for rule in rules_obj if str(rule).strip()]
    block = _largest_contiguous_block(rules)
    if block is None:
        return {"changed": False, "count": 0, "reason": "no-manual-block"}
    start, end, payload = block
    if len(payload) < max(1, int(threshold)):
        return {"changed": False, "count": len(payload), "reason": "below-threshold"}

    # De-duplicate exact payload duplicates and remove only a DOMAIN entry that
    # is already covered by an earlier DOMAIN-SUFFIX in this same provider.
    # Keyword rules are never rewritten.
    seen: set[str] = set()
    suffixes: list[str] = []
    unique_payload: list[str] = []
    for item in payload:
        if item in seen:
            continue
        seen.add(item)
        parts = item.split(",", 1)
        kind = parts[0].upper() if parts else ""
        value = parts[1].lower().rstrip(".") if len(parts) == 2 else ""
        if kind == "DOMAIN" and any(value == suffix or value.endswith("." + suffix) for suffix in suffixes):
            continue
        if kind == "DOMAIN-SUFFIX":
            suffixes.append(value)
        unique_payload.append(item)

    provider_file = workdir / "rule_providers" / "manual-routing.yaml"
    provider_file.parent.mkdir(parents=True, exist_ok=True)
    provider_file.write_text(
        yaml.safe_dump({"payload": unique_payload}, allow_unicode=True, sort_keys=False, width=160),
        encoding="utf-8",
    )

    providers = config.setdefault("rule-providers", {})
    if not isinstance(providers, dict):
        providers = {}
        config["rule-providers"] = providers
    providers[provider_name] = {
        "type": "file",
        "behavior": "classical",
        "path": _PROVIDER_PATH,
    }

    replacement = f"RULE-SET,{provider_name},MANUAL"
    config["rules"] = rules[:start] + [replacement] + rules[end:]
    return {
        "changed": True,
        "count": len(payload),
        "unique_count": len(unique_payload),
        "start": start,
        "end": end,
        "provider": provider_name,
        "path": str(provider_file),
    }
