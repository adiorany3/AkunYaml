"""Private bounded handshake history; no raw endpoints, account names or URIs."""
import hashlib
import json
import math
import statistics
from datetime import UTC, datetime, timedelta
from pathlib import Path

from openclash_target import atomic_write_text


def identity(node):
    # Include full transport/auth identity in hash to distinguish accounts without storing them.
    data = dict(node.clash)
    data.pop("name", None)
    data["original_server"] = node.original_server
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def load(path):
    if not path.exists():
        return {}
    if path.stat().st_size > 40 * 1024 * 1024:
        raise ValueError("Riwayat node melebihi 40 MiB")
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or len(data) > 10000:
        raise ValueError("Riwayat node tidak valid")
    for key, values in data.items():
        if len(key) != 64 or any(c not in "0123456789abcdef" for c in key) or not isinstance(values, list) or len(values) > 20:
            raise ValueError("Entri riwayat node tidak valid")
        for item in values:
            stamp = datetime.fromisoformat(item["at"])
            if stamp.tzinfo is None or not isinstance(item.get("ok"), bool):
                raise ValueError("Sampel riwayat tidak valid")
            delay = item.get("ms")
            if delay is not None and (isinstance(delay, bool) or not isinstance(delay, (int, float)) or not math.isfinite(delay) or delay < 0):
                raise ValueError("Delay riwayat tidak valid")
    return data


def record(history, node, now):
    key = identity(node)
    ms = node.best_delay_ms
    ok = node.status == "alive"
    if ms is not None and (not math.isfinite(ms) or ms < 0):
        ms = None
    history[key] = (history.get(key, []) + [{"at": now.isoformat(), "ok": ok, "ms": ms if ok else None}])[-20:]


def summary(values, now):
    recent = [v for v in values if now - timedelta(days=7) <= datetime.fromisoformat(v["at"]) <= now]
    if not recent:
        return None
    delays = [v["ms"] for v in recent if v["ok"] and v["ms"] is not None]
    failures = 0
    for item in reversed(recent):
        if item["ok"]:
            break
        failures += 1
    return {"samples": len(recent), "success_ratio": sum(v["ok"] for v in recent) / len(recent),
            "median_ms": statistics.median(delays) if delays else None,
            "jitter_ms": max(delays) - min(delays) if delays else None,
            "consecutive_failures": failures, "last_checked": recent[-1]["at"],
            "last_success": next((v["at"] for v in reversed(recent) if v["ok"]), None)}


def apply_history(nodes, path, now=None):
    now = now or datetime.now(UTC)
    history = load(path)
    for node in nodes:
        if node.status not in {"alive", "dead"}:
            continue
        record(history, node, now)
        stats = summary(history[identity(node)], now)
        if node.status == "alive" and stats and stats["samples"] >= 3:
            node.score += round((1 - stats["success_ratio"]) * 1000)
    save(path, history, now)


def save(path: Path, history, now=None):
    now = now or datetime.now(UTC)
    history = {k: [s for s in v if now - timedelta(days=7) <= datetime.fromisoformat(s["at"]) <= now] for k, v in history.items()}
    history = {k: v for k, v in history.items() if v}
    history = dict(sorted(history.items(), key=lambda item: item[1][-1]["at"], reverse=True)[:10000])
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, json.dumps(history, sort_keys=True) + "\n")
    path.chmod(0o600)


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", type=Path, default=Path(__file__).resolve().parent / ".runtime_cache/node_history.json")
    args = parser.parse_args()
    try:
        data = load(args.history)
        now = datetime.now(UTC)
        report = {key: stats for key, values in data.items() if (stats := summary(values, now)) is not None}
        print(json.dumps({"scope": "handshake-only", "nodes": report}, indent=2))
    except (OSError, ValueError, TypeError, KeyError):
        parser.exit(2, "[ERROR] Riwayat tidak valid; file lama tidak diubah.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
