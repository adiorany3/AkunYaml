#!/usr/bin/env python3
"""Detect safe-to-report semantic overlaps in Mihomo rule lists.

The audit never rewrites rules automatically. It only reports cases where a
more specific DOMAIN rule is shadowed by an earlier DOMAIN-SUFFIX rule with the
same policy, plus exact duplicate domain-pattern/provider references.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def _policy(parts: list[str]) -> str:
    if len(parts) < 3:
        return ""
    if parts[-1].lower() == "no-resolve" and len(parts) >= 4:
        return parts[-2]
    return parts[-1]


def audit_config(config: dict[str, Any]) -> list[dict[str, Any]]:
    rules = [str(x).strip() for x in config.get("rules", []) or [] if str(x).strip()]
    suffixes: list[tuple[int, str, str]] = []
    findings: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    for index, rule in enumerate(rules):
        if rule in seen:
            findings.append({"type": "exact-duplicate", "index": index, "covered_by": seen[rule], "rule": rule})
            continue
        seen[rule] = index
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) < 3:
            continue
        kind = parts[0].upper()
        value = parts[1].lower().rstrip(".")
        policy = _policy(parts)
        if kind == "DOMAIN":
            for prev_index, suffix, prev_policy in suffixes:
                if policy == prev_policy and (value == suffix or value.endswith("." + suffix)):
                    findings.append({
                        "type": "domain-shadowed-by-suffix",
                        "index": index,
                        "covered_by": prev_index,
                        "rule": rule,
                        "suffix": suffix,
                    })
                    break
        elif kind == "DOMAIN-SUFFIX":
            suffixes.append((index, value, policy))
    return findings



def remove_safe_shadowed_domains(config: dict[str, Any]) -> int:
    """Remove DOMAIN rules already covered by an earlier same-policy DOMAIN-SUFFIX.

    This is deliberately narrow. DOMAIN-KEYWORD, RULE-SET, different policies,
    and later suffix rules are never rewritten.
    """
    rules_obj = config.get("rules")
    if not isinstance(rules_obj, list):
        return 0
    suffixes: list[tuple[str, str]] = []
    out: list[str] = []
    removed = 0
    for raw in rules_obj:
        rule = str(raw).strip()
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) >= 3:
            kind = parts[0].upper()
            value = parts[1].lower().rstrip(".")
            policy = _policy(parts)
            if kind == "DOMAIN":
                if any(policy == suffix_policy and (value == suffix or value.endswith("." + suffix)) for suffix, suffix_policy in suffixes):
                    removed += 1
                    continue
            elif kind == "DOMAIN-SUFFIX":
                suffixes.append((value, policy))
        out.append(rule)
    if removed:
        config["rules"] = out
    return removed

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--report", type=Path, default=Path("semantic_rule_report.md"))
    args = parser.parse_args()
    all_rows: list[tuple[str, dict[str, Any]]] = []
    for path in args.files:
        if not path.exists():
            continue
        obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(obj, dict):
            continue
        for row in audit_config(obj):
            all_rows.append((path.name, row))

    lines = ["# Semantic Rule Audit", "", f"Findings: **{len(all_rows)}**", ""]
    if all_rows:
        lines += ["| File | Type | Rule index | Covered by | Rule |", "|---|---|---:|---:|---|"]
        for filename, row in all_rows:
            lines.append(
                f"| `{filename}` | {row['type']} | {row['index']} | {row['covered_by']} | `{row['rule']}` |"
            )
    else:
        lines.append("No safe semantic overlaps detected.")
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Semantic audit: {len(all_rows)} finding(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
