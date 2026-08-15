#!/usr/bin/env python3
"""Perbaiki YAML ConvertYAML yang sudah terlanjur dibuat, tanpa mencari ulang akun."""

from __future__ import annotations

import subprocess
import sys
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


def repair(path: Path) -> bool:
    if not path.exists():
        return False

    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        return False

    changed = False

    if "global-client-fingerprint" in config:
        config.pop("global-client-fingerprint", None)
        changed = True

    proxies = [
        p for p in config.get("proxies", [])
        if isinstance(p, dict) and str(p.get("name") or "").strip()
    ]
    proxy_names = {str(p["name"]) for p in proxies}

    groups = [
        g for g in config.get("proxy-groups", [])
        if isinstance(g, dict) and str(g.get("name") or "").strip()
    ]
    group_names = {str(g["name"]) for g in groups}
    valid = proxy_names | group_names | {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}

    for group in groups:
        refs = group.get("proxies")
        if not isinstance(refs, list):
            continue

        cleaned = []
        seen = set()
        for ref in refs:
            name = str(ref)
            if name in valid and name not in seen:
                cleaned.append(name)
                seen.add(name)

        if cleaned != refs:
            removed = [str(x) for x in refs if str(x) not in valid]
            if removed:
                print(
                    f"[FIX] {path.name}: {group.get('name')} "
                    f"hapus referensi tidak ada: {', '.join(removed)}"
                )
            group["proxies"] = cleaned
            changed = True

        if not group.get("proxies"):
            if proxy_names:
                group["proxies"] = [next(iter(proxy_names))]
                changed = True
            elif str(group.get("type") or "").lower() == "select":
                group["proxies"] = ["DIRECT"]
                changed = True

    if "MANUAL" not in group_names:
        rules = config.get("rules")
        if isinstance(rules, list):
            out = []
            for rule in rules:
                value = str(rule)
                parts = value.split(",")
                idx = -2 if parts and parts[-1].strip() == "no-resolve" else -1
                if len(parts) >= 2 and parts[idx].strip() == "MANUAL":
                    parts[idx] = "GLOBAL"
                    value = ",".join(parts)
                    changed = True
                out.append(value)
            config["rules"] = out

    if changed:
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            backup.write_bytes(path.read_bytes())
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140),
            encoding="utf-8",
        )
        print(f"[OK] Diperbaiki: {path.name} | backup: {backup.name}")
    else:
        print(f"[OK] Tidak perlu diperbaiki: {path.name}")

    return changed


def main() -> int:
    workdir = Path(__file__).resolve().parent
    for name in FILES:
        repair(workdir / name)

    mihomo = workdir / ".local_bin" / ("mihomo.exe" if sys.platform.startswith("win") else "mihomo")
    if not mihomo.exists():
        print("[INFO] Mihomo lokal tidak ditemukan. Perbaikan selesai tanpa validasi.")
        return 0

    failed = False
    for name in FILES:
        path = workdir / name
        if not path.exists():
            continue
        print(f"[TEST] {name}")
        result = subprocess.run(
            [str(mihomo), "-t", "-d", str(workdir), "-f", str(path)],
            cwd=workdir,
            check=False,
        )
        if result.returncode != 0:
            failed = True

    if failed:
        print("[ERROR] Ada YAML yang masih gagal validasi.")
        return 1

    print("[OK] Semua YAML yang tersedia lolos validasi Mihomo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
