#!/usr/bin/env python3
"""
ConvertYAML Local Runner v2.0

Final consolidated runner:
- no GitHub Actions dependency;
- verified TLS with retry + curl fallback;
- Mihomo/sing-box bootstrap;
- upstream compatibility patches;
- YAML sanitation;
- ad/tracker/malware protection;
- YouTube playback guard + browser filter;
- Mihomo validation with clear output.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import platform
import re
import shutil
import ssl
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable

APP_VERSION = "2.2"
GITHUB_API = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"

CORE_REPO = "adiorany3/ConvertYAML"
MIHOMO_REPO = "MetaCubeX/mihomo"
SINGBOX_REPO = "SagerNet/sing-box"

CORE_FILES = ("generate_yaml.py", "sumberyaml_core.py", "requirements.txt")
OUTPUT_YAMLS = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

DEFAULT_ENV = {
    "MAX_NODES": "20",
    "MIN_OUTPUT_NODES": "10",
    "URLTEST_POOL_NODES": "60",
    "NEKOBOX_POOL_NODES": "30",
    "FRESH_POOL_NODES": "30",
    "REQUIRE_URL_TEST": "true",
    "REQUIRE_NEKOBOX_TEST": "false",
    "REQUIRE_OPENCLASH_COMPAT": "true",
    "OPENCLASH_COMPAT_TIMEOUT_SEC": "6",
    "OPENCLASH_COMPAT_WORKERS": "6",
    "OPENCLASH_COMPAT_POOL_MULTIPLIER": "4",
    "URL_TEST_URL": "https://www.gstatic.com/generate_204",
    "NEKOBOX_TEST_URL": "https://www.gstatic.com/generate_204",
    "TEST_URL": "https://www.gstatic.com/generate_204",
    "URL_TEST_TIMEOUT_MS": "6000",
    "NEKOBOX_TEST_TIMEOUT_MS": "8000",
    "FORCE_WS_ONLY": "true",
    "REQUIRE_WS_UPGRADE": "true",
    "PREFER_WS": "true",
    "CANDIDATE_MULTIPLIER": "50",
    "CANDIDATE_MIN": "1200",
    "RESERVE_POOL_NODES": "120",
    "ATTEMPTS": "3",
    "REQUIRE_SUCCESSES": "2",
    "TCP_TIMEOUT": "3.0",
    "FETCH_TIMEOUT": "12",
    "MAX_WORKERS": "64",
    "HEALTH_TIMEOUT_MS": "6000",
    "RULE_MODE": "Lite",
    "ADBLOCK_PROFILE": "balanced",
    "ADBLOCK_PROVIDER_INTERVAL": "43200",
    # Default off for maximum OpenClash portability. Security rules still block.
    "ADBLOCK_DNS_MODE": "off",
    "YOUTUBE_ADBLOCK_MODE": "enhanced",
    "YOUTUBE_BROWSER_FILTER_FILE": "youtube_browser_filters.txt",
    "SUBSCRIPTION_LINKS_FILE": "subscription_links.txt",
    "MANUAL_NODES_FILE": "manual_nodes.txt",
    "OUTPUT_YAML": "openclash_auto.yaml",
    "OUTPUT_ANDROID_YAML": "openclash_android.yaml",
    "OUTPUT_LITE_YAML": "openclash_lite.yaml",
    "OUTPUT_FRESH_YAML": "openclash_fresh_pool.yaml",
    "OUTPUT_CSV": "openclash_auto_report.csv",
    "OUTPUT_AKUN": "akun.txt",
    "OUTPUT_MANUAL_AKUN": "akun_manual.txt",
    "OUTPUT_URLTEST_REPORT": "urltest_report.csv",
    "OUTPUT_NEKOBOX_REPORT": "nekobox_test_report.csv",
    "OUTPUT_OPENCLASH_COMPAT_REPORT": "openclash_compat_report.csv",
    "OUTPUT_NODE_QUALITY_REPORT": "node_quality_report.md",
    "OUTPUT_STAMP": "last_update.txt",
}

SECURITY_PROVIDERS = {
    "tracker-domain": {
        "type": "http",
        "behavior": "domain",
        "format": "mrs",
        "interval": 43200,
        "path": "./ruleset/tracker.mrs",
        "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tracker.mrs",
    },
}

YOUTUBE_PLAYBACK_DOMAINS = (
    "youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "googlevideo.com",
    "ytimg.com",
    "youtubei.googleapis.com",
    "youtube.googleapis.com",
    "ggpht.com",
)

YOUTUBE_BROWSER_FILTERS_SAFE = """\
! ConvertYAML Local Runner v2.0
! Cosmetic YouTube filters. Do not block googlevideo.com.
youtube.com##ytd-display-ad-renderer
youtube.com##ytd-ad-slot-renderer
youtube.com##ytd-promoted-video-renderer
youtube.com##ytd-promoted-sparkles-web-renderer
youtube.com##ytd-in-feed-ad-layout-renderer
youtube.com##ytd-banner-promo-renderer
youtube.com##ytd-companion-slot-renderer
youtube.com##.ytp-ad-module
youtube.com##.video-ads
youtube.com##.ytp-ad-overlay-container
youtube.com##.ytp-ad-player-overlay
youtube.com##.ytp-ad-text-overlay
youtube.com##.ytp-ad-image-overlay
youtube.com##.ytp-ad-progress-list
"""

YOUTUBE_BROWSER_FILTERS_ENHANCED = """\
! Additional endpoints separated from the main media CDN.
||googleads.g.doubleclick.net^$domain=youtube.com
||static.doubleclick.net^$domain=youtube.com
||pagead2.googlesyndication.com^$domain=youtube.com
||tpc.googlesyndication.com^$domain=youtube.com
||www.googleadservices.com^$domain=youtube.com
||youtube.com/api/stats/ads^$xhr,domain=youtube.com
||youtube.com/pagead/*$xhr,domain=youtube.com
||youtube.com/ptracking^$xhr,domain=youtube.com
"""


def log(message: str) -> None:
    print(f"[LOCAL] {message}", flush=True)


def _headers(json_api: bool = False) -> dict[str, str]:
    headers = {"User-Agent": f"ConvertYAML-Local-Runner/{APP_VERSION}"}
    if json_api:
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = GITHUB_API_VERSION
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    try:
        import certifi  # type: ignore
        cafile = certifi.where()
        if cafile and Path(cafile).exists():
            context.load_verify_locations(cafile=cafile)
    except Exception:
        pass
    return context


def _curl_available() -> bool:
    return shutil.which("curl") is not None


def _curl_base() -> list[str]:
    args = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--retry", "4", "--retry-delay", "2", "--retry-max-time", "90",
        "--connect-timeout", "20", "--max-time", "180", "--http1.1",
        "-A", f"ConvertYAML-Local-Runner/{APP_VERSION}",
    ]
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        args += ["-H", f"Authorization: Bearer {token}"]
    return args


def request_json(url: str) -> dict:
    errors: list[str] = []
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=_headers(True))
            with urllib.request.urlopen(req, timeout=45, context=_ssl_context()) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            errors.append(f"urllib #{attempt}: {exc}")
            if attempt < 3:
                log(f"GitHub API via Python gagal, retry {attempt}/3")
                time.sleep(attempt * 2)

    if _curl_available():
        log("Fallback ke curl sistem dengan TLS verification aktif")
        cmd = _curl_base() + [
            "-H", "Accept: application/vnd.github+json",
            "-H", f"X-GitHub-Api-Version: {GITHUB_API_VERSION}",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return json.loads(result.stdout)
        errors.append("curl: " + (result.stderr.strip() or str(result.returncode)))

    raise RuntimeError(
        "Gagal mengakses GitHub API.\n"
        + "\n".join(f"  - {item}" for item in errors)
        + "\nTes manual: curl -I https://api.github.com"
    )


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    for attempt in range(1, 4):
        part = destination.with_suffix(destination.suffix + ".part")
        part.unlink(missing_ok=True)
        try:
            req = urllib.request.Request(url, headers=_headers(False))
            with urllib.request.urlopen(req, timeout=120, context=_ssl_context()) as response, part.open("wb") as out:
                shutil.copyfileobj(response, out)
            if not part.exists() or part.stat().st_size == 0:
                raise RuntimeError("hasil download kosong")
            part.replace(destination)
            return
        except Exception as exc:
            part.unlink(missing_ok=True)
            errors.append(f"urllib #{attempt}: {exc}")
            if attempt < 3:
                log(f"Download via Python gagal, retry {attempt}/3")
                time.sleep(attempt * 2)

    if _curl_available():
        log("Fallback download ke curl sistem")
        part = destination.with_suffix(destination.suffix + ".part")
        part.unlink(missing_ok=True)
        result = subprocess.run(
            _curl_base() + ["--output", str(part), url],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and part.exists() and part.stat().st_size > 0:
            part.replace(destination)
            return
        part.unlink(missing_ok=True)
        errors.append("curl: " + (result.stderr.strip() or str(result.returncode)))

    raise RuntimeError(f"Gagal mengunduh {url}\n" + "\n".join(errors))


def raw_github_url(repo: str, filename: str, branch: str = "main") -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{filename}"


def ensure_core_files(workdir: Path, refresh: bool) -> None:
    targets = list(CORE_FILES) if refresh else [name for name in CORE_FILES if not (workdir / name).exists()]
    if not targets:
        log("Core ConvertYAML sudah tersedia")
        return
    for name in targets:
        log(f"Mengunduh core: {name}")
        download(raw_github_url(CORE_REPO, name), workdir / name)


def ensure_input_files(workdir: Path) -> None:
    defaults = {
        "subscription_links.txt": "# Tambahkan subscription publik/milik Anda. Satu URL per baris.\n",
        "manual_nodes.txt": "# Node manual opsional. Satu URI per baris.\n",
        "adblock_allowlist.txt": "# Domain yang tidak boleh diblokir. Satu domain per baris.\n",
    }
    for name, body in defaults.items():
        path = workdir / name
        if not path.exists():
            path.write_text(body, encoding="utf-8")


def install_dependencies() -> None:
    try:
        import requests  # noqa: F401
        import yaml  # noqa: F401
        import certifi  # noqa: F401
        return
    except Exception:
        pass
    log("Memasang requests, PyYAML, certifi")
    subprocess.run(
        [
            sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
            "requests>=2.31", "PyYAML>=6.0", "certifi>=2024.2.2",
        ],
        check=True,
    )


def normalized_platform() -> tuple[str, str]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system not in {"windows", "linux", "darwin"}:
        raise RuntimeError(f"OS belum didukung: {platform.system()}")
    if machine in {"x86_64", "amd64", "x64"}:
        arch = "amd64"
    elif machine in {"arm64", "aarch64"}:
        arch = "arm64"
    else:
        raise RuntimeError(f"Arsitektur belum didukung: {platform.machine()}")
    return system, arch


def executable_name(name: str) -> str:
    return name + (".exe" if platform.system().lower() == "windows" else "")


def make_executable(path: Path) -> None:
    if platform.system().lower() != "windows":
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def select_mihomo_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    prefix = f"mihomo-{os_name}-{arch}"
    candidates: list[tuple[int, int, dict]] = []
    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if not name.startswith(prefix) or "debug" in name:
            continue
        if not (name.endswith(".gz") or name.endswith(".zip")):
            continue
        score = 0
        if "compatible" in name:
            score += 20
        if "-v1-" in name or "-v2-" in name or "-v3-" in name:
            score += 10
        candidates.append((score, len(name), asset))
    if not candidates:
        raise RuntimeError(f"Asset Mihomo tidak ditemukan untuk {os_name}/{arch}")
    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


def select_singbox_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    needle = f"-{os_name}-{arch}"
    candidates = []
    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if name.startswith("sing-box-") and needle in name and (name.endswith(".tar.gz") or name.endswith(".zip")):
            candidates.append(asset)
    if not candidates:
        raise RuntimeError(f"Asset sing-box tidak ditemukan untuk {os_name}/{arch}")
    return sorted(candidates, key=lambda asset: len(str(asset.get("name", ""))))[0]


def extract_binary(archive: Path, binary_name: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if archive.name.endswith(".tar.gz"):
        with tarfile.open(archive, "r:gz") as tf:
            members = [m for m in tf.getmembers() if m.isfile() and Path(m.name).name.lower() == binary_name.lower()]
            if not members:
                raise RuntimeError(f"{binary_name} tidak ada dalam {archive.name}")
            src = tf.extractfile(members[0])
            if src is None:
                raise RuntimeError("Gagal extract")
            with output.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    elif archive.name.endswith(".zip"):
        with zipfile.ZipFile(archive) as zf:
            names = [name for name in zf.namelist() if Path(name).name.lower() == binary_name.lower()]
            if not names:
                raise RuntimeError(f"{binary_name} tidak ada dalam {archive.name}")
            with zf.open(names[0]) as src, output.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    elif archive.name.endswith(".gz"):
        with gzip.open(archive, "rb") as src, output.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    else:
        raise RuntimeError(f"Archive tidak didukung: {archive.name}")
    make_executable(output)


def ensure_binary(workdir: Path, repo: str, program: str, selector, refresh: bool) -> Path:
    bin_dir = workdir / ".local_bin"
    bin_dir.mkdir(exist_ok=True)
    exe = executable_name(program)
    local = bin_dir / exe

    if local.exists() and not refresh:
        log(f"{program} lokal: {local}")
        return local

    if not refresh:
        system_binary = shutil.which(exe) or shutil.which(program)
        if system_binary:
            path = Path(system_binary).resolve()
            log(f"{program} dari PATH: {path}")
            return path

    os_name, arch = normalized_platform()
    log(f"Mencari {program} terbaru untuk {os_name}/{arch}")
    release = request_json(f"{GITHUB_API}/repos/{repo}/releases/latest")
    asset = selector(release.get("assets") or [], os_name, arch)

    with tempfile.TemporaryDirectory(prefix=f"{program}-") as temp_dir:
        archive = Path(temp_dir) / str(asset["name"])
        download(str(asset["browser_download_url"]), archive)
        extract_binary(archive, exe, local)
    return local


def load_config(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Config JSON harus object")
    return {str(key): str(value) for key, value in data.items()}


def patch_core_compatibility(workdir: Path) -> None:
    changed = []
    for filename in ("generate_yaml.py", "sumberyaml_core.py"):
        path = workdir / filename
        if not path.exists():
            continue
        source = path.read_text(encoding="utf-8", errors="ignore")
        original = source

        source = re.sub(
            r"(?m)^[ \t]*[\"']global-client-fingerprint[\"'][ \t]*:[ \t]*[^\n]+?,[ \t]*\n",
            "",
            source,
        )
        source = re.sub(
            r"(?m)^[ \t]*global-client-fingerprint[ \t]*:[ \t]*chrome[ \t]*\n",
            "",
            source,
        )
        if filename == "generate_yaml.py":
            source = source.replace(
                'refs_available = set(proxy_names) | set(keep_group_names) | {"REJECT", "GLOBAL"}',
                'refs_available = set(proxy_names) | set(groups.keys()) | {"DIRECT", "REJECT", "GLOBAL"}',
            )

            compat_marker = "def _mihomo_openclash_compatibility_filter("
            if compat_marker not in source:
                compat_code = '\ndef _mihomo_openclash_compatibility_filter(\n    nodes: list[Any],\n    *,\n    label: str,\n) -> tuple[list[Any], list[dict[str, Any]]]:\n    """Keep only nodes accepted by the current Mihomo proxy parser.\n\n    Each node is tested in an isolated minimal configuration. A malformed or\n    obsolete account therefore cannot prevent the rest of the batch from\n    starting in OpenClash/Mihomo.\n    """\n    rows: list[dict[str, Any]] = []\n    if not nodes:\n        return [], rows\n    if not _env_bool("REQUIRE_OPENCLASH_COMPAT", True):\n        for node in nodes:\n            rows.append({\n                "source": label,\n                "name": _node_name(node),\n                "type": str((getattr(node, "clash", {}) or {}).get("type") or getattr(node, "type", "")),\n                "network": node_network(node),\n                "compatible": "skipped",\n                "reason": "compatibility filter disabled",\n            })\n        return nodes, rows\n\n    core_path = os.getenv("MIHOMO_PATH", "./mihomo").strip() or "./mihomo"\n    if not Path(core_path).exists():\n        raise SystemExit(\n            f"Mihomo binary tidak ditemukan di {core_path}; "\n            "OpenClash compatibility filter wajib aktif."\n        )\n\n    timeout_s = max(2.0, _env_float("OPENCLASH_COMPAT_TIMEOUT_SEC", 6.0))\n    workers = max(1, min(16, _env_int("OPENCLASH_COMPAT_WORKERS", 6)))\n\n    def check_one(index: int, node: Any) -> tuple[int, Any, dict[str, Any]]:\n        clash = dict(getattr(node, "clash", {}) or {})\n        name = str(clash.get("name") or _node_name(node) or f"NODE-{index + 1}")\n        proto = str(clash.get("type") or getattr(node, "type", "")).lower()\n        network = node_network(node)\n        row = {\n            "source": label,\n            "name": name,\n            "type": proto,\n            "network": network,\n            "compatible": "no",\n            "reason": "",\n        }\n        if not clash:\n            row["reason"] = "empty proxy config"\n            return index, node, row\n\n        clash["name"] = name\n        tmp_obj = tempfile.TemporaryDirectory(prefix="openclash-compat-")\n        tmpdir = Path(tmp_obj.name)\n        config_path = tmpdir / "config.yaml"\n        config = {\n            "proxies": [clash],\n            "proxy-groups": [\n                {\n                    "name": "OPENCLASH-COMPAT",\n                    "type": "select",\n                    "proxies": [name],\n                }\n            ],\n            "rules": ["MATCH,OPENCLASH-COMPAT"],\n        }\n        try:\n            config_path.write_text(\n                yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140),\n                encoding="utf-8",\n            )\n            proc = subprocess.run(\n                [core_path, "-t", "-d", str(tmpdir), "-f", str(config_path)],\n                stdout=subprocess.PIPE,\n                stderr=subprocess.STDOUT,\n                text=True,\n                timeout=timeout_s,\n                check=False,\n            )\n            output = (proc.stdout or "").strip().replace("\\n", " | ")\n            if proc.returncode == 0:\n                row["compatible"] = "yes"\n                row["reason"] = "mihomo config test ok"\n            else:\n                row["reason"] = output[-500:] or f"mihomo exit {proc.returncode}"\n        except subprocess.TimeoutExpired:\n            row["reason"] = f"mihomo config test timeout > {timeout_s:.1f}s"\n        except Exception as exc:\n            row["reason"] = f"{type(exc).__name__}: {str(exc)[:300]}"\n        finally:\n            tmp_obj.cleanup()\n        return index, node, row\n\n    from concurrent.futures import ThreadPoolExecutor, as_completed\n\n    results: list[tuple[int, Any, dict[str, Any]]] = []\n    with ThreadPoolExecutor(max_workers=workers) as executor:\n        futures = [executor.submit(check_one, i, node) for i, node in enumerate(nodes)]\n        for future in as_completed(futures):\n            results.append(future.result())\n\n    results.sort(key=lambda item: item[0])\n    passed: list[Any] = []\n    for _index, node, row in results:\n        rows.append(row)\n        ok = row["compatible"] == "yes"\n        setattr(node, "openclash_compatible", ok)\n        setattr(node, "openclash_compat_status", row["reason"])\n        if ok:\n            passed.append(node)\n        else:\n            print(\n                f"[SKIP] OpenClash incompatible [{label}] "\n                f"{row[\'name\']} type={row[\'type\']} network={row[\'network\']}: {row[\'reason\']}"\n            )\n\n    print(f"[INFO] OpenClash compatibility [{label}]: {len(passed)}/{len(nodes)} passed")\n    return passed, rows\n\n\ndef _build_openclash_compat_report_csv(rows: list[dict[str, Any]]) -> str:\n    import csv\n    import io\n\n    fields = ["source", "name", "type", "network", "compatible", "reason"]\n    buffer = io.StringIO()\n    writer = csv.DictWriter(buffer, fieldnames=fields)\n    writer.writeheader()\n    for row in rows:\n        writer.writerow({field: row.get(field, "") for field in fields})\n    return buffer.getvalue()\n\n'
                anchor = "def _mihomo_url_test_nodes("
                if anchor in source:
                    source = source.replace(anchor, compat_code + "\n" + anchor, 1)

            report_anchor = '    output_nekobox_report = os.getenv("OUTPUT_NEKOBOX_REPORT", "nekobox_test_report.csv")\n'
            if 'output_openclash_compat_report = os.getenv(' not in source and report_anchor in source:
                source = source.replace(
                    report_anchor,
                    report_anchor + '    output_openclash_compat_report = os.getenv("OUTPUT_OPENCLASH_COMPAT_REPORT", "openclash_compat_report.csv")\n',
                    1,
                )

            manual_anchor = '    manual_nodes, manual_skipped = parse_manual_nodes_unscreened(manual_text)\n'
            if 'manual_compat_rows = _mihomo_openclash_compatibility_filter' not in source and manual_anchor in source:
                source = source.replace(
                    manual_anchor,
                    manual_anchor + '    manual_nodes, manual_compat_rows = _mihomo_openclash_compatibility_filter(manual_nodes, label="manual")\n',
                    1,
                )

            pool_anchor = '    urltest_pool_nodes = max(max_nodes, _env_int("URLTEST_POOL_NODES", max(30, max_nodes * 3)))\n'
            if 'compat_pool_multiplier = max(1, _env_int("OPENCLASH_COMPAT_POOL_MULTIPLIER"' not in source and pool_anchor in source:
                source = source.replace(
                    pool_anchor,
                    '    compat_pool_multiplier = max(1, _env_int("OPENCLASH_COMPAT_POOL_MULTIPLIER", 4))\n'
                    + '    urltest_pool_nodes = max(max_nodes * compat_pool_multiplier, _env_int("URLTEST_POOL_NODES", max(30, max_nodes * 3)))\n',
                    1,
                )

            auto_anchor = '    nekobox_pool_nodes = max(max_nodes, _env_int("NEKOBOX_POOL_NODES", max(20, max_nodes * 3)))\n'
            if 'auto_compat_rows = _mihomo_openclash_compatibility_filter' not in source and auto_anchor in source:
                source = source.replace(
                    auto_anchor,
                    '    auto_pool_nodes, auto_compat_rows = _mihomo_openclash_compatibility_filter(auto_pool_nodes, label="automatic")\n' + auto_anchor,
                    1,
                )

            write_anchor = '    Path(output_nekobox_report).write_text(_build_nekobox_report_csv(nekobox_rows), encoding="utf-8")\n'
            if '_build_openclash_compat_report_csv(auto_compat_rows + manual_compat_rows)' not in source and write_anchor in source:
                source = source.replace(
                    write_anchor,
                    write_anchor + '    Path(output_openclash_compat_report).write_text(_build_openclash_compat_report_csv(auto_compat_rows + manual_compat_rows), encoding="utf-8")\n',
                    1,
                )

        if source != original:
            path.write_text(source, encoding="utf-8")
            changed.append(filename)

    if changed:
        log("Core patched: " + ", ".join(changed))


def build_environment(args, workdir: Path, mihomo: Path, singbox: Path | None) -> dict[str, str]:
    env = os.environ.copy()
    env.update(DEFAULT_ENV)
    env.update(load_config(args.config))
    env["MAX_NODES"] = str(args.max_nodes)
    env["MIN_OUTPUT_NODES"] = str(min(args.min_nodes, args.max_nodes))
    env["MIHOMO_PATH"] = str(mihomo.resolve())
    if singbox is not None:
        env["SINGBOX_PATH"] = str(singbox.resolve())
    if args.no_nekobox:
        env["REQUIRE_NEKOBOX_TEST"] = "false"
    if args.no_ws_only:
        env["FORCE_WS_ONLY"] = "false"
    if args.candidate_min is not None:
        env["CANDIDATE_MIN"] = str(args.candidate_min)
    if args.urltest_pool is not None:
        env["URLTEST_POOL_NODES"] = str(args.urltest_pool)
    if args.nekobox_pool is not None:
        env["NEKOBOX_POOL_NODES"] = str(args.nekobox_pool)
    return env


def load_allowlist(workdir: Path) -> list[str]:
    path = workdir / "adblock_allowlist.txt"
    if not path.exists():
        return []
    domains = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = raw.strip().lower().rstrip(".")
        if not value or value.startswith("#"):
            continue
        value = re.sub(r"^https?://", "", value).split("/", 1)[0]
        if value.startswith("*.") or value.startswith("+."):
            value = value[2:]
        if re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", value) and "." in value and ".." not in value:
            domains.append(value)
    return sorted(set(domains))


def _safe_provider_path(name: str, provider: dict) -> str:
    fmt = str(provider.get("format") or "yaml").lower()
    ext = ".mrs" if fmt == "mrs" else ".txt" if fmt == "text" else ".yaml"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "provider"
    return f"./ruleset/{slug}{ext}"


def _valid_policies(config: dict) -> set[str]:
    names = {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
    for item in config.get("proxies", []) or []:
        if isinstance(item, dict) and item.get("name"):
            names.add(str(item["name"]))
    for item in config.get("proxy-groups", []) or []:
        if isinstance(item, dict) and item.get("name"):
            names.add(str(item["name"]))
    return names


def _default_route(config: dict) -> str:
    valid = _valid_policies(config)
    rules = config.get("rules") or []
    for raw in reversed(rules):
        parts = [part.strip() for part in str(raw).split(",")]
        if len(parts) >= 2 and parts[0].upper() in {"MATCH", "FINAL"} and parts[1] in valid:
            return parts[1]
    for name in ("GLOBAL", "PROXY", "Proxy", "AUTO", "Auto"):
        if name in valid:
            return name
    groups = [
        group.get("name") for group in config.get("proxy-groups", []) or []
        if isinstance(group, dict) and group.get("name")
    ]
    return str(groups[0]) if groups else "DIRECT"


def sanitize_yaml(path: Path) -> bool:
    import yaml

    if not path.exists():
        return False
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise RuntimeError(f"{path.name}: YAML tidak dapat diparse: {exc}") from exc
    if not isinstance(config, dict):
        raise RuntimeError(f"{path.name}: root YAML bukan mapping")

    changed = False

    if "global-client-fingerprint" in config:
        config.pop("global-client-fingerprint", None)
        log(f"{path.name}: hapus global-client-fingerprint")
        changed = True

    # Portable local output should not contain OpenClash runtime absolute UI paths.
    external_ui = config.get("external-ui")
    if isinstance(external_ui, str) and external_ui.startswith("/"):
        config.pop("external-ui", None)
        log(f"{path.name}: hapus external-ui absolut dari output portable")
        changed = True

    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            # Remove only stale keys injected by older runner versions.
            if "geosite:category-ads-all,tracker" in policy:
                policy.pop("geosite:category-ads-all,tracker", None)
                changed = True
            for domain in YOUTUBE_PLAYBACK_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in policy:
                        policy.pop(key, None)
                        changed = True

    legacy_security_providers = {
        "security-tif-mini",
        "popup-ads",
        "hagezi-pro-mini",
        "awavenue-ads",
    }
    providers0 = config.get("rule-providers")
    if isinstance(providers0, dict):
        for old_name in legacy_security_providers:
            if old_name in providers0:
                providers0.pop(old_name, None)
                log(f"{path.name}: hapus provider TXT lama {old_name}")
                changed = True

    providers = config.get("rule-providers")
    if providers is not None and not isinstance(providers, dict):
        config["rule-providers"] = {}
        providers = config["rule-providers"]
        changed = True

    if isinstance(providers, dict):
        for name, provider in list(providers.items()):
            if not isinstance(provider, dict):
                continue
            if str(provider.get("type") or "").lower() == "http":
                provider_path = str(provider.get("path") or "").strip()
                path_parts = Path(provider_path).parts if provider_path else ()
                if not provider_path or provider_path.startswith("/") or ".." in path_parts:
                    provider["path"] = _safe_provider_path(str(name), provider)
                    log(f"{path.name}: normalisasi path provider {name}")
                    changed = True
                if "interval" not in provider:
                    provider["interval"] = 43200
                    changed = True

    rules = config.get("rules")
    if not isinstance(rules, list):
        rules = []
        config["rules"] = rules
        changed = True

    known_providers = set((config.get("rule-providers") or {}).keys())
    cleaned_rules: list[str] = []
    seen_rules = set()
    for raw in rules:
        value = str(raw).strip()
        if not value:
            changed = True
            continue
        if re.match(
            r"(?i)^RULE-SET\s*,\s*(security-tif-mini|popup-ads|hagezi-pro-mini|awavenue-ads)\s*,",
            value,
        ):
            log(f"{path.name}: hapus RULE-SET provider TXT lama")
            changed = True
            continue

        if re.match(r"(?i)^GEOSITE\s*,\s*tracker\s*,", value):
            log(f"{path.name}: hapus GEOSITE,tracker yang tidak portable")
            changed = True
            continue

        parts = [part.strip() for part in value.split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET":
            provider_name = parts[1]
            if known_providers and provider_name not in known_providers:
                log(f"{path.name}: hapus RULE-SET tanpa provider: {provider_name}")
                changed = True
                continue

        if value not in seen_rules:
            cleaned_rules.append(value)
            seen_rules.add(value)
        else:
            changed = True
    config["rules"] = cleaned_rules

    proxies = [
        proxy for proxy in config.get("proxies", []) or []
        if isinstance(proxy, dict) and str(proxy.get("name") or "").strip()
    ]
    proxy_names = {str(proxy["name"]) for proxy in proxies}
    groups = [
        group for group in config.get("proxy-groups", []) or []
        if isinstance(group, dict) and str(group.get("name") or "").strip()
    ]
    group_names = {str(group["name"]) for group in groups}
    valid_refs = proxy_names | group_names | {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
    fallback = sorted(proxy_names)[0] if proxy_names else "DIRECT"

    for group in groups:
        refs = group.get("proxies")
        if not isinstance(refs, list):
            continue
        new_refs = []
        seen = set()
        for ref in refs:
            name = str(ref)
            if name in valid_refs and name not in seen:
                new_refs.append(name)
                seen.add(name)
        if new_refs != refs:
            log(f"{path.name}: bersihkan referensi group {group.get('name')}")
            group["proxies"] = new_refs
            changed = True
        if not group.get("proxies"):
            group["proxies"] = [fallback]
            changed = True

    if "MANUAL" not in group_names:
        fixed_rules = []
        route = _default_route(config)
        for rule in config["rules"]:
            parts = [part.strip() for part in str(rule).split(",")]
            if len(parts) >= 2:
                idx = -2 if parts[-1] == "no-resolve" and len(parts) >= 3 else -1
                if parts[idx] == "MANUAL":
                    parts[idx] = route
                    changed = True
            fixed_rules.append(",".join(parts))
        config["rules"] = fixed_rules

    if changed:
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=160),
            encoding="utf-8",
        )
    return changed


def apply_security(path: Path, profile: str, workdir: Path, interval: int, dns_mode: str) -> bool:
    """
    OpenClash-safe security profile.

    Generic DNS blocklist TXT providers from older runner versions are
    intentionally removed. They are not native Mihomo rulesets, so one
    incompatible domain expression can make the entire OpenClash config fail
    with "invalid domain".

    Safe default:
      GEOSITE,category-ads-all,REJECT
      RULE-SET,tracker-domain,REJECT

    tracker-domain uses the official MetaCubeX MRS ruleset.
    """
    import yaml

    if not path.exists():
        return False
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        return False

    changed = False
    providers = config.setdefault("rule-providers", {})
    if not isinstance(providers, dict):
        providers = {}
        config["rule-providers"] = providers
        changed = True

    managed_names = {
        "security-tif-mini",
        "popup-ads",
        "tracker-domain",
        "hagezi-pro-mini",
        "awavenue-ads",
    }

    # Always remove all security providers managed by old versions first.
    for name in managed_names:
        if name in providers:
            providers.pop(name, None)
            changed = True

    if profile != "off":
        provider = dict(SECURITY_PROVIDERS["tracker-domain"])
        provider["interval"] = interval
        providers["tracker-domain"] = provider
        changed = True

    current_rules = [str(item) for item in config.get("rules", []) or []]
    managed_prefixes = (
        "RULE-SET,security-tif-mini,",
        "RULE-SET,popup-ads,",
        "RULE-SET,tracker-domain,",
        "RULE-SET,hagezi-pro-mini,",
        "RULE-SET,awavenue-ads,",
        "GEOSITE,category-ads-all,",
        "GEOSITE,tracker,",
    )
    cleaned = [rule for rule in current_rules if not rule.startswith(managed_prefixes)]

    allow_rules = [f"DOMAIN-SUFFIX,{domain},DIRECT" for domain in load_allowlist(workdir)]
    security_rules = list(allow_rules)

    if profile != "off":
        security_rules.extend([
            "GEOSITE,category-ads-all,REJECT",
            "RULE-SET,tracker-domain,REJECT",
        ])

    new_rules = security_rules + cleaned
    if new_rules != current_rules:
        config["rules"] = new_rules
        changed = True

    # Keep DNS-level ad blocking off by default. Network rules above remain
    # active and are more portable across OpenClash installations.
    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            for stale in (
                "geosite:category-ads-all,tracker",
                "geosite:tracker",
            ):
                if stale in policy:
                    policy.pop(stale, None)
                    changed = True

            if dns_mode == "off" or profile == "off":
                if "geosite:category-ads-all" in policy:
                    policy.pop("geosite:category-ads-all", None)
                    changed = True
            elif dns_mode == "geosite":
                if policy.get("geosite:category-ads-all") != "rcode://success":
                    policy["geosite:category-ads-all"] = "rcode://success"
                    changed = True

    if changed:
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=160),
            encoding="utf-8",
        )
    return changed

def apply_youtube_guard(path: Path, mode: str) -> bool:
    import yaml

    if not path.exists():
        return False
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        return False

    current = [str(item) for item in config.get("rules", []) or []]
    domains = set(YOUTUBE_PLAYBACK_DOMAINS)
    cleaned = []
    for rule in current:
        parts = [part.strip() for part in rule.split(",")]
        if len(parts) >= 3 and parts[0].upper() in {"DOMAIN", "DOMAIN-SUFFIX"} and parts[1].lower() in domains:
            continue
        cleaned.append(rule)

    if mode == "off":
        new_rules = cleaned
    else:
        route = _default_route(config)
        guard = [f"DOMAIN-SUFFIX,{domain},{route}" for domain in YOUTUBE_PLAYBACK_DOMAINS]
        insert_at = 0
        for index, rule in enumerate(cleaned):
            if rule.startswith((
                "RULE-SET,tracker-domain,",
                "GEOSITE,category-ads-all,",
            )):
                insert_at = index
                break
        new_rules = cleaned[:insert_at] + guard + cleaned[insert_at:]

    if new_rules != current:
        config["rules"] = new_rules
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=160),
            encoding="utf-8",
        )
        return True
    return False


def write_youtube_filters(workdir: Path, mode: str, filename: str) -> None:
    path = workdir / filename
    if mode == "off":
        path.unlink(missing_ok=True)
        return
    body = YOUTUBE_BROWSER_FILTERS_SAFE
    if mode == "enhanced":
        body += "\n" + YOUTUBE_BROWSER_FILTERS_ENHANCED
    body += """
! Keep the browser blocker's own filter lists enabled and updated.
! DNS/Mihomo alone cannot reliably distinguish every YouTube video ad from
! normal media when they share delivery infrastructure.
"""
    path.write_text(body, encoding="utf-8")


def optimize_outputs(
    workdir: Path,
    files: Iterable[str],
    profile: str,
    interval: int,
    dns_mode: str,
    youtube_mode: str,
    youtube_filter_file: str,
) -> None:
    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue
        sanitize_yaml(path)
        if apply_security(path, profile, workdir, interval, dns_mode):
            log(f"Security [{profile}] diterapkan: {filename}")
        if apply_youtube_guard(path, youtube_mode):
            log(f"YouTube guard [{youtube_mode}] diterapkan: {filename}")
        sanitize_yaml(path)
    write_youtube_filters(workdir, youtube_mode, youtube_filter_file)


def validate_yaml(workdir: Path, mihomo: Path, files: Iterable[str]) -> bool:
    ok = True
    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue
        log(f"Validasi Mihomo: {filename}")
        result = subprocess.run(
            [str(mihomo), "-t", "-d", str(workdir), "-f", str(path)],
            cwd=workdir,
            capture_output=True,
            text=True,
            check=False,
        )
        output = (result.stdout or "") + (result.stderr or "")
        if output.strip():
            print(output.rstrip())
        if result.returncode != 0:
            print(f"[ERROR] {filename} gagal validasi, exit={result.returncode}")
            ok = False
        else:
            print(f"[OK] {filename}")
    return ok


def network_test() -> int:
    print(f"ConvertYAML Local Runner v{APP_VERSION}")
    print(f"Python : {sys.version.split()[0]}")
    print(f"OpenSSL: {ssl.OPENSSL_VERSION}")
    print(f"curl   : {shutil.which('curl') or 'tidak ada'}")
    try:
        release = request_json(f"{GITHUB_API}/repos/{MIHOMO_REPO}/releases/latest")
        print(f"GitHub : OK, latest Mihomo={release.get('tag_name')}")
        return 0
    except Exception as exc:
        print(f"GitHub : GAGAL\n{exc}")
        return 1


def parse_args():
    parser = argparse.ArgumentParser(description="ConvertYAML local runner v2.0")
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--max-nodes", type=int, default=20)
    parser.add_argument("--min-nodes", type=int, default=10)
    parser.add_argument("--candidate-min", type=int)
    parser.add_argument("--urltest-pool", type=int)
    parser.add_argument("--nekobox-pool", type=int)
    parser.add_argument("--refresh-core", action="store_true")
    parser.add_argument("--refresh-binaries", action="store_true")
    parser.add_argument("--no-nekobox", action="store_true")
    parser.add_argument("--no-ws-only", action="store_true")
    parser.add_argument("--no-install-deps", action="store_true")
    parser.add_argument("--network-test", action="store_true")
    parser.add_argument("--adblock-profile", choices=("off", "balanced", "strict"))
    parser.add_argument("--dns-adblock", choices=("off", "geosite"))
    parser.add_argument("--youtube-mode", choices=("off", "safe", "enhanced"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.network_test:
        return network_test()

    workdir = args.workdir.expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    log(f"Folder kerja: {workdir}")

    if args.max_nodes < 1 or args.min_nodes < 1:
        raise SystemExit("max/min nodes minimal 1")

    ensure_core_files(workdir, args.refresh_core)
    patch_core_compatibility(workdir)
    ensure_input_files(workdir)

    if not args.no_install_deps:
        install_dependencies()

    mihomo = ensure_binary(workdir, MIHOMO_REPO, "mihomo", select_mihomo_asset, args.refresh_binaries)

    preliminary = dict(DEFAULT_ENV)
    preliminary.update(load_config(args.config))
    if args.no_nekobox:
        preliminary["REQUIRE_NEKOBOX_TEST"] = "false"
    need_singbox = str(preliminary.get("REQUIRE_NEKOBOX_TEST", "false")).strip().lower() in {"1", "true", "yes", "y", "on", "aktif"}
    singbox = None
    if need_singbox:
        singbox = ensure_binary(workdir, SINGBOX_REPO, "sing-box", select_singbox_asset, args.refresh_binaries)
    else:
        log("NekoBox/sing-box test nonaktif; download sing-box dilewati")

    env = build_environment(args, workdir, mihomo, singbox)

    log("Menjalankan generate_yaml.py")
    result = subprocess.run([sys.executable, "generate_yaml.py"], cwd=workdir, env=env, check=False)
    if result.returncode != 0:
        print(f"[ERROR] Pipeline generator gagal, exit={result.returncode}")
        return result.returncode

    output_files = (
        env.get("OUTPUT_YAML", OUTPUT_YAMLS[0]),
        env.get("OUTPUT_ANDROID_YAML", OUTPUT_YAMLS[1]),
        env.get("OUTPUT_LITE_YAML", OUTPUT_YAMLS[2]),
        env.get("OUTPUT_FRESH_YAML", OUTPUT_YAMLS[3]),
    )

    profile = (args.adblock_profile or env.get("ADBLOCK_PROFILE", "balanced")).strip().lower()
    if profile not in {"off", "balanced", "strict"}:
        profile = "balanced"

    dns_mode = (args.dns_adblock or env.get("ADBLOCK_DNS_MODE", "off")).strip().lower()
    if dns_mode not in {"off", "geosite"}:
        dns_mode = "off"

    youtube_mode = (args.youtube_mode or env.get("YOUTUBE_ADBLOCK_MODE", "enhanced")).strip().lower()
    if youtube_mode not in {"off", "safe", "enhanced"}:
        youtube_mode = "enhanced"

    try:
        interval = max(3600, int(env.get("ADBLOCK_PROVIDER_INTERVAL", "43200")))
    except ValueError:
        interval = 43200

    youtube_filter_file = env.get("YOUTUBE_BROWSER_FILTER_FILE", "youtube_browser_filters.txt").strip() or "youtube_browser_filters.txt"

    optimize_outputs(
        workdir,
        output_files,
        profile,
        interval,
        dns_mode,
        youtube_mode,
        youtube_filter_file,
    )

    if not validate_yaml(workdir, mihomo, output_files):
        print("\n[ERROR] Ada YAML yang gagal validasi.")
        print("Gunakan error tepat di atas untuk diagnosis.")
        return 2

    print("\n[OK] Semua output yang tersedia lolos validasi Mihomo.")
    for name in (
        *output_files,
        env.get("OUTPUT_AKUN", "akun.txt"),
        env.get("OUTPUT_CSV", "openclash_auto_report.csv"),
        env.get("OUTPUT_OPENCLASH_COMPAT_REPORT", "openclash_compat_report.csv"),
        youtube_filter_file,
    ):
        output_path = workdir / name
        if output_path.exists():
            print(f"  - {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
