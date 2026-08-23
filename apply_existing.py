#!/usr/bin/env python3
"""Apply target-pinned cleanup/reference profile to existing AkunYaml outputs."""

from __future__ import annotations

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

from local_runner import OUTPUT_YAMLS, optimize_outputs
from openclash_target import (
    MIHOMO_TARGET_LABEL,
    OPENCLASH_TARGET_VERSION,
    assert_target_mihomo,
    discover_mihomo_core,
    validate_yaml_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Repair existing YAML for OpenClash {OPENCLASH_TARGET_VERSION} + {MIHOMO_TARGET_LABEL}"
    )
    parser.add_argument("--profile", choices=("off", "balanced", "strict", "child-safe", "app-safe", "threat-safe"), default="balanced")
    parser.add_argument("--dns-adblock", choices=("off", "geosite"), default="off")
    parser.add_argument("--youtube-mode", choices=("off", "safe", "enhanced"), default="enhanced")
    parser.add_argument("--interval", type=int, default=43200)
    parser.add_argument("--core", type=Path, help="Path Mihomo alpha-ge183c58")
    parser.add_argument("--static-only", action="store_true", help="Skip exact-core parser test")
    parser.add_argument("--restore", action="store_true")
    return parser.parse_args()


def restore_latest(workdir: Path, files: list[str], backup_dir: Path) -> int:
    restored = 0
    for name in files:
        backups = sorted(backup_dir.glob(f"{name}.*.bak"))
        if backups:
            shutil.copy2(backups[-1], workdir / name)
            print(f"[RESTORE] {name} <- {backups[-1].name}")
            restored += 1
    return restored


def main() -> int:
    args = parse_args()
    workdir = Path(__file__).resolve().parent
    existing = [name for name in OUTPUT_YAMLS if (workdir / name).is_file()]
    if not existing:
        print("[ERROR] Tidak ada YAML AkunYaml di folder ini.")
        return 1

    backup_dir = workdir / "backup_target"
    backup_dir.mkdir(exist_ok=True)

    if args.restore:
        count = restore_latest(workdir, existing, backup_dir)
        print(f"[OK] {count} file dipulihkan.")
        return 0

    core = None
    if not args.static_only:
        core, mismatches = discover_mihomo_core(
            explicit=args.core,
            workdir=workdir,
            require_exact=True,
        )
        if core is None:
            print(
                f"[ERROR] Mihomo exact target {MIHOMO_TARGET_LABEL} tidak ditemukan. "
                "Gunakan --core /path/ke/core atau --static-only."
            )
            for item in mismatches:
                print("  - " + item)
            return 2
        print(f"[CORE] {assert_target_mihomo(core, strict=True)}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backups: dict[str, Path] = {}
    for name in existing:
        src = workdir / name
        backup = backup_dir / f"{name}.{stamp}.bak"
        shutil.copy2(src, backup)
        backups[name] = backup
        print(f"[BACKUP] {backup.name}")

    os.environ["REFERENCE_PROFILE_MODE"] = "local-pinned"
    os.environ["REFERENCE_PROFILE_FILE"] = "reference_profile_v047156.yaml"

    try:
        optimize_outputs(
            workdir,
            existing,
            args.profile,
            max(3600, args.interval),
            args.dns_adblock,
            args.youtube_mode,
            "youtube_browser_filters.txt",
        )

        failed = False
        for name in existing:
            path = workdir / name
            errors = validate_yaml_file(
                path,
                core_path=core,
                require_exact_core=True,
                parser_test=not args.static_only,
            )
            if errors:
                failed = True
                print(f"[ERROR] {name}")
                for error in errors:
                    print("  - " + error)
            else:
                mode = "static" if args.static_only else "static + exact-core parser"
                print(f"[OK] {name} ({mode})")

        if failed:
            for name, backup in backups.items():
                shutil.copy2(backup, workdir / name)
            print("[ROLLBACK] Validasi gagal. Semua YAML dikembalikan ke backup sebelum perubahan.")
            return 3
    except Exception as exc:
        for name, backup in backups.items():
            shutil.copy2(backup, workdir / name)
        print(f"[ERROR] {exc}")
        print("[ROLLBACK] Semua YAML dikembalikan ke backup sebelum perubahan.")
        return 3

    print(f"[OK] Existing YAML sesuai paket target OpenClash {OPENCLASH_TARGET_VERSION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
