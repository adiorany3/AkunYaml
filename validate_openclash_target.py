#!/usr/bin/env python3
"""Validate AkunYaml outputs for OpenClash v0.47.156 + Mihomo alpha-ge183c58."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

from openclash_target import (
    DEFAULT_ROUTER_CORE,
    MIHOMO_TARGET_LABEL,
    OPENCLASH_TARGET_VERSION,
    assert_target_mihomo,
    validate_yaml_file,
)

DEFAULT_FILES = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Validate OpenClash {OPENCLASH_TARGET_VERSION} + {MIHOMO_TARGET_LABEL}"
    )
    parser.add_argument("files", nargs="*", default=list(DEFAULT_FILES))
    parser.add_argument("--core", type=Path, help="Path exact Mihomo target core")
    parser.add_argument("--static-only", action="store_true", help="Skip Mihomo parser test")
    parser.add_argument(
        "--allow-non-target-core",
        action="store_true",
        help="Development only. Parser may use a different Mihomo build.",
    )
    return parser.parse_args()


def discover_core(explicit: Path | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit.expanduser())
    env_core = os.getenv("MIHOMO_PATH", "").strip()
    if env_core:
        candidates.append(Path(env_core).expanduser())
    candidates.extend(
        [
            Path(DEFAULT_ROUTER_CORE),
            Path.cwd() / ".local_bin" / ("mihomo.exe" if os.name == "nt" else "mihomo"),
        ]
    )
    for name in ("mihomo", "clash-meta", "clash_meta"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_file():
            return candidate.resolve()
    return None


def main() -> int:
    args = parse_args()
    print(f"Target: OpenClash {OPENCLASH_TARGET_VERSION} + Mihomo {MIHOMO_TARGET_LABEL}")

    core = None if args.static_only else discover_core(args.core)
    strict = not args.allow_non_target_core
    if not args.static_only:
        if core is None:
            print(
                "[ERROR] Mihomo core tidak ditemukan. Gunakan --core /path/ke/core, "
                "set MIHOMO_PATH, atau jalankan --static-only."
            )
            return 2
        try:
            version = assert_target_mihomo(core, strict=strict)
        except RuntimeError as exc:
            print(f"[ERROR] {exc}")
            return 2
        print(f"Core  : {core}")
        print(f"Versi : {version}")

    failed = False
    checked = 0
    for raw in args.files:
        path = Path(raw)
        if not path.is_file():
            print(f"[SKIP] {path}: file tidak ada")
            continue
        checked += 1
        errors = validate_yaml_file(
            path,
            core_path=core,
            require_exact_core=strict,
            parser_test=not args.static_only,
        )
        if errors:
            failed = True
            print(f"[ERROR] {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            mode = "static" if args.static_only else "static + exact-core parser"
            print(f"[OK] {path} ({mode})")

    if checked == 0:
        print("[ERROR] Tidak ada YAML yang diperiksa.")
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
