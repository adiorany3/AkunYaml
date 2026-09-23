#!/usr/bin/env python3
"""Local adblock telemetry: aggregate outcomes without sending domains remotely."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from ai_adblock_classifier import normalize_domain


def read_events(path: Path) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    if not path.exists():
        return events
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        domain = normalize_domain(str(item.get("domain", "")))
        outcome = str(item.get("outcome", "")).lower()
        if domain and outcome in {"blocked", "allowed", "error"}:
            events.append({"domain": domain, "outcome": outcome})
    return events


def build_report(events: list[dict[str, str]], *, min_events: int = 3) -> dict[str, object]:
    stats: dict[str, Counter[str]] = defaultdict(Counter)
    for event in events:
        stats[event["domain"]][event["outcome"]] += 1
    false_positive: list[dict[str, int | str]] = []
    for domain, counts in sorted(stats.items()):
        blocked = counts["blocked"]
        allowed = counts["allowed"]
        if allowed >= min_events and allowed > blocked:
            false_positive.append({"domain": domain, "allowed": allowed, "blocked": blocked})
    has_observation = bool(events)
    return {
        "events": len(events),
        "domains": len(stats),
        "telemetry_state": "observed" if has_observation else "missing",
        "confidence_ceiling": 1.0 if has_observation else 0.0,
        "outcomes": dict(Counter(event["outcome"] for event in events)),
        # Empty telemetry produces no false-positive claims. AI/feed inference
        # must remain separate from observed runtime behavior.
        "false_positive_candidates": false_positive if has_observation else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate local adblock telemetry")
    parser.add_argument("events", type=Path, default=Path(".runtime_cache/adblock_events.jsonl"), nargs="?")
    parser.add_argument("--output", type=Path, default=Path(".runtime_cache/adblock_telemetry_report.json"))
    parser.add_argument("--min-events", type=int, default=3)
    args = parser.parse_args()
    if args.min_events < 1:
        parser.error("--min-events harus >= 1")
    report = build_report(read_events(args.events), min_events=args.min_events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
