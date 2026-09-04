#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
OUTPUTS = (
    "openclash_auto.yaml",
    "openclash_lite.yaml",
    "openclash_android.yaml",
    "openclash_fresh_pool.yaml",
)
MAX_ACTIVE_DIRECT_PROBES_PER_MIN = 15.0
MAX_YAML_BYTES = 2 * 1024 * 1024


def analyze_yaml(path: Path) -> dict[str, Any]:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    proxies = {
        str(item.get("name"))
        for item in cfg.get("proxies", []) or []
        if isinstance(item, dict) and item.get("name")
    }
    rows = []
    active_rate = 0.0
    for group in cfg.get("proxy-groups", []) or []:
        if not isinstance(group, dict):
            continue
        if str(group.get("type") or "").lower() not in {"url-test", "fallback", "load-balance"}:
            continue
        interval = int(group.get("interval") or 0)
        direct = [str(name) for name in group.get("proxies", []) or [] if str(name) in proxies]
        lazy = bool(group.get("lazy", False))
        rate = (len(direct) * 60.0 / interval) if (interval > 0 and direct and not lazy) else 0.0
        active_rate += rate
        rows.append({
            "name": str(group.get("name") or ""),
            "type": str(group.get("type") or ""),
            "direct_nodes": len(direct),
            "interval": interval,
            "lazy": lazy,
            "active_direct_probes_per_min": round(rate, 2),
        })
    return {
        "file": path.name,
        "bytes": path.stat().st_size,
        "proxies": len(proxies),
        "groups": rows,
        "active_direct_probes_per_min": round(active_rate, 2),
    }


def main() -> int:
    cfg = json.loads((ROOT / "local_config.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    required = {
        "ADAPTIVE_CANDIDATES": "true",
        "SUBSCRIPTION_CACHE": "true",
        "PROVIDER_CACHE": "true",
        "PING_CHECK_LAZY": "true",
        "CF_WARMUP_LAZY": "true",
        "WARMUP_LAZY": "true",
        "STREAMING_HEALTH_LAZY": "true",
        "FALLBACK_LAZY": "true",
        "LOAD_BALANCE_LAZY": "true",
        "AUTO_FAST_LAZY": "true",
    }
    for key, expected in required.items():
        if str(cfg.get(key, "")).strip().lower() != expected:
            failures.append(f"{key} harus {expected}")

    try:
        if int(cfg.get("CANDIDATE_INITIAL", 999999)) > 500:
            failures.append("CANDIDATE_INITIAL terlalu besar")
        if int(cfg.get("BUG_TOTAL_VARIANTS_CAP", 999999)) > 32:
            failures.append("BUG_TOTAL_VARIANTS_CAP melebihi budget 32")
        if int(cfg.get("SUBSCRIPTION_CACHE_TTL_SEC", 0)) <= 0:
            failures.append("SUBSCRIPTION_CACHE_TTL_SEC harus > 0")
        if int(cfg.get("PROVIDER_CACHE_TTL_SEC", 0)) < 86400:
            failures.append("PROVIDER_CACHE_TTL_SEC terlalu pendek")
    except Exception as exc:
        failures.append(f"config numeric invalid: {exc}")

    summaries = []
    for name in OUTPUTS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"output hilang: {name}")
            continue
        summary = analyze_yaml(path)
        summaries.append(summary)
        if summary["active_direct_probes_per_min"] > MAX_ACTIVE_DIRECT_PROBES_PER_MIN:
            failures.append(
                f"{name}: active probe {summary['active_direct_probes_per_min']}/min > {MAX_ACTIVE_DIRECT_PROBES_PER_MIN}/min"
            )
        if summary["bytes"] > MAX_YAML_BYTES:
            failures.append(f"{name}: YAML terlalu besar ({summary['bytes']} bytes)")
        groups = {row["name"]: row for row in summary["groups"]}
        for lazy_name in ("PING-CHECK", "WARM-UP-CF", "STREAMING-FAST", "FALLBACK"):
            if lazy_name in groups and not groups[lazy_name]["lazy"]:
                failures.append(f"{name}: {lazy_name} seharusnya lazy")

    for summary in summaries:
        print(
            f"[PERF] {summary['file']}: proxies={summary['proxies']} "
            f"active_direct_probes/min={summary['active_direct_probes_per_min']} bytes={summary['bytes']}"
        )
    if failures:
        for item in failures:
            print("[FAIL]", item)
        return 1
    print("[OK] performance budget v4.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
