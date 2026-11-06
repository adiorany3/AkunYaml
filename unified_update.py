"""One update entry point and a private, organized output directory."""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import yaml

from build_support import publish


def mac_profile(source):
    config = copy.deepcopy(source)
    for key in ("redir-port", "tproxy-port", "tun", "lan-allowed-ips", "secret", "external-controller"):
        config.pop(key, None)
    config.update({"allow-lan": False, "bind-address": "127.0.0.1"})
    if "dns" in config:
        config["dns"]["listen"] = "127.0.0.1:7874"
    return config


def bundle_yaml(source, folder, name, *, mac=False):
    config = yaml.safe_load(source.read_text())
    if not isinstance(config, dict) or not isinstance(config.get("rules"), list) or not config["rules"]:
        raise ValueError(f"Profil YAML tidak memiliki aturan: {source.name}")
    if mac:
        config = mac_profile(config)
    folder.mkdir(parents=True, exist_ok=True)
    for provider in config.get("rule-providers", {}).values():
        if provider.get("type") != "file":
            continue
        relative = Path(provider["path"])
        origin = (source.parent / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not origin.is_relative_to(source.parent.resolve()):
            raise ValueError("Path provider tidak aman")
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target)
    (folder / name).write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))


def validate_bundle(stage, root):
    """Check every published profile, not just transformed Mac variants."""
    profiles = list((stage / "openclash").glob("*/*.yaml"))
    profiles += list((stage / "mihomo-mac").glob("*/config.yaml"))
    for config in profiles:
        command = [str(root / ".local_bin/mihomo"), "-t", "-d", str(config.parent), "-f", str(config)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
        if result.returncode:
            raise RuntimeError(f"Validasi Mihomo gagal: {config.relative_to(stage)}\n" + (result.stdout + result.stderr)[-2000:])
    for config in (stage / "sing-box").glob("*.json"):
        result = subprocess.run([str(root / ".local_bin/sing-box"), "check", "-c", str(config)], cwd=config.parent, capture_output=True, text=True, timeout=120, check=False)
        if result.returncode:
            raise RuntimeError(f"Validasi Sing-box gagal: {config.name}\n" + (result.stdout + result.stderr)[-2000:])
    return profiles


def collect(root, mode):
    """Publish only after every expected file and local dependency is present."""
    output = root / "output"
    with tempfile.TemporaryDirectory(prefix="output-stage-", dir=root) as tmp:
        stage = Path(tmp) / "release"
        stage.mkdir(mode=0o700)
        sources = []
        for source_name in ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml"):
            source = root / source_name
            bundle_yaml(source, stage / "openclash" / "proxy", source_name)
            sources.append(source)
        for source, section in ((root / "local_build/openclash_noproxy.yaml", "direct"), (root / "local_build/gameblock/openclash_noproxy_gameblock.yaml", "gameblock")):
            bundle_yaml(source, stage / "openclash" / section, source.name)
            bundle_yaml(source, stage / "mihomo-mac" / section, "config.yaml", mac=True)
            sources.append(source)
        bundle_yaml(root / "openclash_auto.yaml", stage / "mihomo-mac/proxy", "config.yaml", mac=True)
        for source, target in (
            (root / "singbox_android.json", "sing-box/singbox_android.json"),
            (root / "local_build/singbox_direct_adblock.json", "sing-box/singbox_direct_adblock.json"),
            (root / "akun.txt", "akun/akun.txt"),
        ):
            destination = stage / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix == ".json":
                json.loads(source.read_text())
            shutil.copy2(source, destination)
            sources.append(source)
        profiles = validate_bundle(stage, root)
        # Validators may download caches; retain only declared profiles/providers.
        for directory in {config.parent for config in profiles}:
            declared = {config.name for config in profiles if config.parent == directory}
            for item in directory.iterdir():
                if item.name not in declared | {"rule_providers"}:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
        report = {
            "mode": mode, "packaged_at": datetime.now(UTC).isoformat(),
            "warning": "Offline hanya snapshot; waktu packaging bukan bukti akun aktif. Sing-box gameblock belum tersedia.",
            "sources": [{"path": str(p.relative_to(root)), "modified_at": datetime.fromtimestamp(p.stat().st_mtime, UTC).isoformat(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
        }
        (stage / "manifest.json").write_text(json.dumps(report, indent=2) + "\n")
        (stage / "README.txt").write_text(
            "HASIL UTAMA AKUNYAML\n"
            "akun/: daftar akun hasil generator (rahasia).\n"
            "openclash/proxy|direct|gameblock/: profil OpenWrt; salin provider bersama YAML.\n"
            "sing-box/: Android proxy dan direct/adblock; BELUM ada gameblock.\n"
            "mihomo-mac/proxy|direct|gameblock/: config.yaml untuk Mihomo Mac.\n"
            "Mac: gunakan system proxy HTTP/SOCKS 127.0.0.1:7890; bukan TUN otomatis.\n"
            "Jalankan hanya satu profil Mac sekaligus. OpenClash bukan aplikasi macOS.\n"
            "manifest.json mencatat waktu sumber; snapshot offline tidak memperbarui akun.\n"
            "Folder ini dilacak Git atas persetujuan pemilik; repository publik mengekspos kredensial proxy.\n"
            "Permission lokal tidak melindungi file di GitHub. Jangan sertakan .secrets/.\n"
        )
        for item in stage.rglob("*"):
            item.chmod(0o700 if item.is_dir() else 0o600)
        publish(stage, output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Build dari sumber/cache tanpa refresh; validator Mihomo bisa membutuhkan database lokal")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    lock = root / ".runtime_cache/unified_update.lock"
    lock.parent.mkdir(exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        print("[ERROR] Update terpadu lain sedang berjalan atau lock tersisa.")
        return 2
    os.close(fd)
    try:
        commands = []
        if not args.offline:
            commands.append([sys.executable, str(root / "local_runner.py"), "--workdir", str(root), "--config", str(root / "local_config.json"), "--no-install-deps"])
        commands.append([sys.executable, str(root / "local_update.py")])
        commands.append([sys.executable, str(root / "independent_gameblock.py")] + ([] if args.offline else ["--refresh"]))
        for command in commands:
            print(f"[RUN] {Path(command[1]).name}", flush=True)
            result = subprocess.run(command, cwd=root, check=False)
            if result.returncode:
                print(f"[ERROR] Tahap gagal/parsial (exit {result.returncode}); output terpadu lama tidak diganti.")
                return result.returncode
        print(f"[OK] Semua hasil: {collect(root, 'offline-snapshot' if args.offline else 'online-refresh')}")
        return 0
    except (OSError, ValueError, RuntimeError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(f"[ERROR] {exc}; output terpadu lama dipertahankan.")
        return 2
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())