#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

from local_runner import OUTPUT_YAMLS, optimize_outputs, validate_yaml


def main() -> int:
    workdir = Path(__file__).resolve().parent
    files = [name for name in OUTPUT_YAMLS if (workdir / name).exists()]
    if not files:
        print("Tidak ada YAML ConvertYAML di folder ini.")
        return 1

    backup_dir = workdir / "backup_invalid_domain"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for name in files:
        src = workdir / name
        backup = backup_dir / f"{name}.{stamp}.bak"
        shutil.copy2(src, backup)
        print(f"[BACKUP] {backup}")

    optimize_outputs(
        workdir,
        files,
        "balanced",
        43200,
        "off",
        "enhanced",
        "youtube_browser_filters.txt",
    )

    mihomo = workdir / ".local_bin" / (
        "mihomo.exe" if sys.platform.startswith("win") else "mihomo"
    )
    if not mihomo.exists():
        print("[INFO] Mihomo lokal tidak ditemukan. YAML tetap sudah dibersihkan.")
        return 0

    if not validate_yaml(workdir, mihomo, files):
        print("[ERROR] Masih ada config error. Baca pesan Mihomo tepat di atas.")
        return 2

    print("[OK] Provider TXT lama dihapus.")
    print("[OK] Security OpenClash-safe: category-ads-all + tracker.mrs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
