#!/usr/bin/env python3
"""Terapkan optimasi YouTube ke YAML yang sudah ada tanpa pencarian akun ulang."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from local_runner import apply_youtube_network_guard, write_youtube_browser_filters

FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("off", "safe", "enhanced"),
        default="enhanced",
        help="Default: enhanced.",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Pulihkan YAML dari backup sebelum optimasi YouTube.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workdir = Path(__file__).resolve().parent
    existing = [workdir / name for name in FILES if (workdir / name).exists()]

    if not existing:
        print("Tidak ada YAML ConvertYAML di folder ini.")
        return 1

    if args.restore:
        restored = 0
        for path in existing:
            backup = path.with_suffix(path.suffix + ".pre-youtube.bak")
            if backup.exists():
                shutil.copy2(backup, path)
                print(f"[RESTORE] {path.name}")
                restored += 1
        filter_path = workdir / "youtube_browser_filters.txt"
        if filter_path.exists():
            filter_path.unlink()
        print(f"[OK] {restored} file dipulihkan.")
        return 0

    for path in existing:
        backup = path.with_suffix(path.suffix + ".pre-youtube.bak")
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"[BACKUP] {backup.name}")
        apply_youtube_network_guard(path, args.mode)

    write_youtube_browser_filters(
        workdir,
        args.mode,
        "youtube_browser_filters.txt",
    )

    mihomo = workdir / ".local_bin" / (
        "mihomo.exe" if sys.platform.startswith("win") else "mihomo"
    )
    if not mihomo.exists():
        print("[OK] Optimasi diterapkan. Mihomo lokal tidak ditemukan, validasi dilewati.")
        return 0

    failed = False
    for path in existing:
        print(f"[TEST] {path.name}")
        result = subprocess.run(
            [str(mihomo), "-t", "-d", str(workdir), "-f", str(path)],
            cwd=workdir,
            check=False,
        )
        if result.returncode != 0:
            failed = True

    if failed:
        print("[ERROR] Ada YAML yang gagal validasi. Gunakan --restore untuk rollback.")
        return 1

    print(f"[OK] YouTube mode {args.mode} diterapkan dan semua YAML lolos validasi.")
    print("[INFO] Import youtube_browser_filters.txt ke blocker browser Anda.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
