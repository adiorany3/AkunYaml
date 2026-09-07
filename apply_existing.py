#!/usr/bin/env python3
"""Apply target-pinned cleanup/reference profile to existing AkunYaml outputs."""

from __future__ import annotations

import argparse
import copy
import json
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
    parser.add_argument("--android-offline", action="store_true", help="Regenerate Android locally without probes or account writes")
    return parser.parse_args()


def regenerate_android_offline(workdir: Path, core: Path) -> None:
    import yaml
    import generate_yaml as generator
    from openclash_target import atomic_write_text, validate_generated_text_with_core

    paths = [workdir / "openclash_android.yaml", workdir / "singbox_android.json"]
    originals = {path: path.read_text(encoding="utf-8") for path in paths}
    existing = yaml.safe_load(originals[paths[0]])
    nodes, skipped = generator.parse_manual_nodes_unscreened(
        (workdir / "manual_nodes.txt").read_text(encoding="utf-8")
    )
    if skipped or not nodes:
        raise RuntimeError("Manual source invalid; existing outputs preserved")
    manual = {node.name: node for node in nodes}
    yaml_nodes = []
    for proxy in existing["proxies"]:
        if proxy["name"] not in manual:
            continue
        node = copy.deepcopy(manual[proxy["name"]])
        for key in ("type", "uuid", "password"):
            if proxy.get(key) != node.clash.get(key):
                raise RuntimeError("Manual credentials differ; existing outputs preserved")
        node.clash = copy.deepcopy(proxy)
        yaml_nodes.append(node)
    text = generator.build_openclash_android_yaml(yaml_nodes, 30, 40, generator.ALT_TEST_URL)
    text = generator.add_manual_group_to_yaml_text(text, yaml_nodes, android=True)
    text = generator._enforce_no_selector_no_direct_yaml_text(text)
    text = generator._ensure_ping_check_group_yaml_text(text)
    text = generator._prune_missing_proxy_group_refs_yaml_text(text)
    if yaml.safe_load(text)["proxies"] != [node.clash for node in yaml_nodes]:
        raise RuntimeError("Offline generation changed manual endpoints; outputs preserved")
    singbox = generator._build_singbox_android_json(nodes)
    previous_nodes = [item for item in json.loads(originals[paths[1]])["outbounds"] if item.get("server")]
    new_nodes = [item for item in json.loads(singbox)["outbounds"] if item.get("server")]
    if previous_nodes != new_nodes:
        raise RuntimeError("Offline generation changed sing-box nodes; outputs preserved")
    validate_generated_text_with_core(text, label=paths[0].name, core_path=core, require_exact_core=True)
    generator._validate_singbox_json(singbox, str(workdir / ".local_bin" / "sing-box"))
    # ponytail: per-file atomic publication; rollback pair on ordinary write failure.
    try:
        for path, content in zip(paths, (text, singbox)):
            atomic_write_text(path, content)
    except Exception:
        for path, content in originals.items():
            atomic_write_text(path, content)
        raise
    print(f"[OK] Offline Android regenerated: {len(yaml_nodes)} YAML / {len(new_nodes)} sing-box manual nodes; both core checks passed")

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
    if args.android_offline:
        if args.restore or args.static_only:
            raise SystemExit("--android-offline requires core validation and cannot restore")
        core, _ = discover_mihomo_core(explicit=args.core, workdir=workdir, require_exact=True)
        if core is None:
            raise SystemExit(f"Exact Mihomo {MIHOMO_TARGET_LABEL} required")
        os.chdir(workdir)
        regenerate_android_offline(workdir, core)
        return 0
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
