#!/usr/bin/env python3
"""Repair existing ConvertYAML YAML for OpenClash geodata compatibility."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML belum tersedia. Jalankan: python -m pip install PyYAML")
    raise SystemExit(1)

FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

YOUTUBE_DOMAINS = (
    "youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "googlevideo.com",
    "ytimg.com",
    "youtubei.googleapis.com",
    "youtube.googleapis.com",
    "ggpht.com",
)

TRACKER_PROVIDER = {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "interval": 43200,
    "path": "./ruleset/tracker.mrs",
    "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tracker.mrs",
}


def repair(path: Path) -> bool:
    if not path.exists():
        return False

    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        print(f"[ERROR] {path.name}: YAML root bukan object.")
        return False

    backup = path.with_suffix(path.suffix + ".pre-v15-openclash.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"[BACKUP] {backup.name}")

    changed = False

    if "global-client-fingerprint" in config:
        config.pop("global-client-fingerprint", None)
        print(f"[FIX] {path.name}: hapus global-client-fingerprint")
        changed = True

    providers = config.setdefault("rule-providers", {})
    if not isinstance(providers, dict):
        providers = {}
        config["rule-providers"] = providers
        changed = True

    if providers.get("tracker-domain") != TRACKER_PROVIDER:
        providers["tracker-domain"] = dict(TRACKER_PROVIDER)
        print(f"[FIX] {path.name}: tambah tracker-domain.mrs")
        changed = True

    # Ensure all HTTP providers have a relative path.
    for name, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        if str(provider.get("type") or "").lower() != "http":
            continue
        fmt = str(provider.get("format") or "yaml").lower()
        ext = ".mrs" if fmt == "mrs" else ".txt" if fmt == "text" else ".yaml"
        p = str(provider.get("path") or "").strip()
        if not p or p.startswith("/"):
            safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(name))
            provider["path"] = f"./ruleset/{safe}{ext}"
            print(f"[FIX] {path.name}: provider {name} path={provider['path']}")
            changed = True

    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            old = "geosite:category-ads-all,tracker"
            if old in policy:
                value = policy.pop(old)
                policy.setdefault("geosite:category-ads-all", value)
                print(f"[FIX] {path.name}: DNS policy tracker geosite dihapus")
                changed = True

            # Remove explicit YouTube wildcard policies injected by v1.3.
            for domain in YOUTUBE_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in policy:
                        policy.pop(key, None)
                        changed = True

    rules = config.get("rules")
    if not isinstance(rules, list):
        rules = []

    cleaned = []
    insert_at = None
    tracker_exists = False

    for rule in rules:
        value = str(rule)
        if value.startswith("GEOSITE,tracker,"):
            print(f"[FIX] {path.name}: hapus {value}")
            changed = True
            continue
        if value.startswith("RULE-SET,tracker-domain,"):
            tracker_exists = True
        cleaned.append(value)

    # Put tracker-domain immediately after category-ads-all where possible.
    if not tracker_exists:
        for i, value in enumerate(cleaned):
            if value.startswith("GEOSITE,category-ads-all,"):
                insert_at = i + 1
                break
        if insert_at is None:
            insert_at = 0
        cleaned.insert(insert_at, "RULE-SET,tracker-domain,REJECT")
        print(f"[FIX] {path.name}: tambah RULE-SET,tracker-domain,REJECT")
        changed = True

    config["rules"] = cleaned

    if changed:
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=160),
            encoding="utf-8",
        )
        print(f"[OK] Diperbaiki: {path.name}")
    else:
        print(f"[OK] Tidak perlu perubahan: {path.name}")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    args = parser.parse_args()

    workdir = args.workdir.expanduser().resolve()
    found = 0
    for name in FILES:
        path = workdir / name
        if path.exists():
            found += 1
            repair(path)

    if not found:
        print("Tidak menemukan YAML ConvertYAML di folder ini.")
        return 1

    print("\nSelesai.")
    print("Gunakan openclash_auto.yaml yang sudah diperbaiki untuk test OpenClash.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
