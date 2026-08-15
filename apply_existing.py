#!/usr/bin/env python3
"""Apply v2.0 sanitation/security to existing ConvertYAML YAML files."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

from local_runner import OUTPUT_YAMLS, optimize_outputs, validate_yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("off", "balanced", "strict"), default="balanced")
    parser.add_argument("--dns-adblock", choices=("off", "geosite"), default="off")
    parser.add_argument("--youtube-mode", choices=("off", "safe", "enhanced"), default="enhanced")
    parser.add_argument("--interval", type=int, default=43200)
    parser.add_argument("--restore", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workdir = Path(__file__).resolve().parent
    existing = [name for name in OUTPUT_YAMLS if (workdir / name).exists()]
    if not existing:
        print("Tidak ada YAML ConvertYAML di folder ini.")
        return 1

    backup_dir = workdir / "backup_v2"
    backup_dir.mkdir(exist_ok=True)

    if args.restore:
        restored = 0
        for name in existing:
            backups = sorted(backup_dir.glob(f"{name}.*.bak"))
            if backups:
                shutil.copy2(backups[-1], workdir / name)
                print(f"[RESTORE] {name} <- {backups[-1].name}")
                restored += 1
        print(f"[OK] {restored} file dipulihkan.")
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for name in existing:
        source = workdir / name
        backup = backup_dir / f"{name}.{stamp}.bak"
        shutil.copy2(source, backup)
        print(f"[BACKUP] {backup.name}")

    optimize_outputs(
        workdir,
        existing,
        args.profile,
        max(3600, args.interval),
        args.dns_adblock,
        args.youtube_mode,
        "youtube_browser_filters.txt",
    )

    mihomo = workdir / ".local_bin" / ("mihomo.exe" if sys.platform.startswith("win") else "mihomo")
    if mihomo.exists():
        if not validate_yaml(workdir, mihomo, existing):
            print("[ERROR] Validasi gagal. Backup tersedia di backup_v2/.")
            return 2
    else:
        print("[INFO] Mihomo lokal tidak ditemukan. Sanitasi selesai tanpa validasi binary.")

    print("[OK] Existing YAML sudah diperbarui ke format v2.0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
