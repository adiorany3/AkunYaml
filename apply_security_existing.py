#!/usr/bin/env python3
"""Terapkan adblock/security ke YAML ConvertYAML yang sudah ada tanpa mencari akun ulang."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from local_runner import optimize_outputs


FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=("off", "balanced", "strict"),
        default="balanced",
        help="Profil keamanan. Default: balanced.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=43200,
        help="Interval update rule-provider dalam detik.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workdir = Path(__file__).resolve().parent

    existing = [name for name in FILES if (workdir / name).exists()]
    if not existing:
        print("Tidak ada YAML hasil ConvertYAML di folder ini.")
        return 1

    for name in existing:
        path = workdir / name
        backup = path.with_suffix(path.suffix + ".pre-security.bak")
        if not backup.exists():
            backup.write_bytes(path.read_bytes())
            print(f"[BACKUP] {backup.name}")

    optimize_outputs(
        workdir,
        existing,
        args.profile,
        max(3600, args.interval),
    )

    mihomo = workdir / ".local_bin" / (
        "mihomo.exe" if sys.platform.startswith("win") else "mihomo"
    )
    if not mihomo.exists():
        print("[OK] Proteksi diterapkan. Mihomo lokal tidak ditemukan, jadi validasi dilewati.")
        return 0

    failed = False
    for name in existing:
        print(f"[TEST] {name}")
        result = subprocess.run(
            [str(mihomo), "-t", "-d", str(workdir), "-f", str(workdir / name)],
            cwd=workdir,
            check=False,
        )
        if result.returncode != 0:
            failed = True

    if failed:
        print("[ERROR] Ada YAML yang gagal validasi Mihomo.")
        return 1

    print(f"[OK] Profil {args.profile} diterapkan dan semua YAML lolos validasi Mihomo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
