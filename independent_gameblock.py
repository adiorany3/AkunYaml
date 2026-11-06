"""Generate gameblock locally from editable policy and independent upstream feeds."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

import yaml

from build_support import PROFILE, fetch, publish, validate
from feed_guard import _parse_domains


def materialize(content, fmt, destination, core):
    if fmt not in {"text", "yaml", "mrs"}:
        raise ValueError("Format feed tidak didukung")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "text":
        domains = _parse_domains(content.decode("utf-8"))
        if len(domains) < 10:
            raise ValueError("Feed domain memiliki kurang dari 10 entri valid")
        text = destination.with_suffix(".txt")
        text.write_text("\n".join("+." + d for d in sorted(domains)) + "\n")
        subprocess.run([str(core), "convert-ruleset", "domain", "text", str(text), str(destination)], check=True, capture_output=True, timeout=90)
        text.unlink()
        return len(domains)
    if fmt == "yaml":
        obj = yaml.safe_load(content)
        if not isinstance(obj, dict) or not isinstance(obj.get("payload"), list) or len(obj["payload"]) < 10 or not all(isinstance(item, str) for item in obj["payload"]):
            raise ValueError("Provider YAML kosong/tidak valid")
    elif fmt == "mrs" and not content.startswith(b"\x28\xb5\x2f\xfd"):
        raise ValueError("Header provider MRS tidak valid")
    destination.write_bytes(content)
    return None


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError("Katalog feed harus berupa object yang tidak kosong")
    paths = set()
    for name, spec in manifest.items():
        if not isinstance(spec, dict) or not all(isinstance(spec.get(k), str) for k in ("url", "format", "path")):
            raise ValueError(f"Spesifikasi feed tidak valid: {name}")
        relative = Path(spec["path"])
        if relative.is_absolute() or ".." in relative.parts or len(relative.parts) < 2 or relative.parts[0] != "rule_providers":
            raise ValueError("Path sumber tidak aman")
        if relative.as_posix() in paths:
            raise ValueError("Path feed duplikat")
        paths.add(relative.as_posix())
        if spec["format"] not in {"text", "yaml", "mrs"}:
            raise ValueError("Format feed tidak didukung")
        if not spec["url"].startswith("https://raw.githubusercontent.com/") or "/adiorany3/" in spec["url"]:
            raise ValueError("URL sumber bukan feed independen yang diizinkan")


def update(root, refresh=False):
    root = root.resolve()
    policy = root / "gameblock_policy"
    manifest = json.loads((policy / "sources.json").read_text())
    validate_manifest(manifest)
    output = root / "local_build" / "gameblock"
    cache = root / ".runtime_cache" / "independent_gameblock"
    core = root / ".local_bin" / "mihomo"
    output.parent.mkdir(parents=True, exist_ok=True)
    cache.parent.mkdir(parents=True, exist_ok=True)
    lock = cache.parent / "gameblock.lock"
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        with tempfile.TemporaryDirectory(dir=output.parent, prefix="independent-") as temp:
            stage = Path(temp) / "release"
            shutil.copytree(policy / "baseline", stage)
            config = yaml.safe_load((stage / PROFILE).read_text())
            old_report = json.loads((cache / "build_report.json").read_text()) if (cache / "build_report.json").exists() else {}
            old_assets = {a["name"]: a for a in old_report.get("assets", [])}

            def build_feed(item):
                name, spec = item
                relative = Path(spec["path"])
                if relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "rule_providers":
                    raise ValueError("Path sumber tidak aman")
                if "/adiorany3/" in spec["url"]:
                    raise ValueError("Feed tidak boleh bergantung pada output HerYaml/AkunYaml")
                destination = stage / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if refresh:
                    content = fetch(spec["url"])
                    count = materialize(content, spec["format"], destination, core)
                    previous_count = old_assets.get(name, {}).get("entries")
                    if count and previous_count and count < previous_count * 0.5:
                        raise ValueError(f"Feed {name} menyusut lebih dari 50%; publikasi dibatalkan")
                    stamp = datetime.now(UTC).isoformat()
                else:
                    prior = old_assets.get(name)
                    if not prior or not (cache / relative).is_file():
                        raise FileNotFoundError("Cache feed belum tersedia; jalankan --refresh")
                    if any(prior.get(key) != spec[key] for key in ("url", "path", "format")):
                        raise ValueError("Sumber/format cache berbeda dari katalog; jalankan --refresh")
                    shutil.copy2(cache / relative, destination)
                    if hashlib.sha256(destination.read_bytes()).hexdigest() != prior["sha256"]:
                        raise ValueError("Integritas cache feed gagal")
                    count, stamp = prior.get("entries"), prior["fetched_at"]
                return {"name": name, "url": spec["url"], "format": spec["format"], "path": str(relative), "entries": count,
                        "fetched_at": stamp, "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}

            with ThreadPoolExecutor(max_workers=4) as pool:
                assets = list(pool.map(build_feed, manifest.items()))
            for name, spec in manifest.items():
                config["rule-providers"][name] = {"type": "file", "behavior": "domain", "format": "mrs" if spec["format"] == "text" else spec["format"], "path": "./" + spec["path"]}
                rule = f"RULE-SET,{name},REJECT"
                if rule not in config["rules"]:
                    config["rules"].insert(-1, rule)
            (stage / PROFILE).write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
            report = {"generator": "independent-local", "built_at": datetime.now(UTC).isoformat(),
                      "mode": "refresh" if refresh else "offline", "rules": len(config["rules"]),
                      "providers": len(config["rule-providers"]), "assets": assets,
                      "policy_sha256": hashlib.sha256((policy / "baseline" / PROFILE).read_bytes()).hexdigest(),
                      "note": "Baseline khusus lokal + feed independen; tidak ada unduhan HerYaml, API AI, atau proxy."}
            (stage / "build_report.json").write_text(json.dumps(report, indent=2) + "\n")
            validate(stage, core)
            with tempfile.TemporaryDirectory(dir=cache.parent) as cached:
                copy = Path(cached) / "release"
                shutil.copytree(stage, copy)
                publish(copy, cache)
            publish(stage, output)
        return output / PROFILE
    finally:
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--workdir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        print(f"[OK] {update(args.workdir, args.refresh)}")
    except (OSError, ValueError, RuntimeError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(f"[ERROR] {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())