#!/usr/bin/env python3
"""
ConvertYAML Local Runner

Menjalankan pipeline ConvertYAML secara lokal tanpa GitHub Actions:
1. Menyiapkan file core ConvertYAML jika belum ada.
2. Memasang dependency Python yang diperlukan.
3. Mengunduh Mihomo dan sing-box terbaru sesuai OS/arsitektur.
4. Menjalankan generate_yaml.py.
5. Memvalidasi YAML keluaran dengan Mihomo.

Catatan:
- Script ini memakai sumber subscription publik yang sudah didefinisikan oleh core ConvertYAML.
- Tambahan sumber milik Anda dapat ditulis satu URL per baris pada subscription_links.txt.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import ssl
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable

GITHUB_API = "https://api.github.com"
CORE_REPO = "adiorany3/ConvertYAML"
MIHOMO_REPO = "MetaCubeX/mihomo"
SINGBOX_REPO = "SagerNet/sing-box"

CORE_FILES = (
    "generate_yaml.py",
    "sumberyaml_core.py",
    "requirements.txt",
)

DEFAULT_ENV = {
    "MAX_NODES": "20",
    "MIN_OUTPUT_NODES": "20",
    "URLTEST_POOL_NODES": "60",
    "NEKOBOX_POOL_NODES": "30",
    "FRESH_POOL_NODES": "30",
    "REQUIRE_URL_TEST": "true",
    "REQUIRE_NEKOBOX_TEST": "true",
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
    "OUTPUT_NODE_QUALITY_REPORT": "node_quality_report.md",
    "OUTPUT_STAMP": "last_update.txt",
}


def log(message: str) -> None:
    print(f"[LOCAL] {message}", flush=True)


def _github_headers(accept_json: bool = False) -> dict[str, str]:
    headers = {
        "User-Agent": "ConvertYAML-Local-Runner/1.5",
    }
    if accept_json:
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2026-03-10"

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _ssl_context() -> ssl.SSLContext:
    """Create a verified SSL context.

    On Conda/Python installations, certifi may contain a more complete CA
    bundle than the interpreter's configured default. Verification is never
    disabled.
    """
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


def _curl_common_args() -> list[str]:
    args = [
        "curl",
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--retry", "4",
        "--retry-delay", "2",
        "--retry-max-time", "90",
        "--connect-timeout", "20",
        "--max-time", "180",
        "--http1.1",
        "-A", "ConvertYAML-Local-Runner/1.5",
    ]
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        args += ["-H", f"Authorization: Bearer {token}"]
    return args


def _curl_json(url: str) -> dict:
    if not _curl_available():
        raise RuntimeError("curl tidak tersedia.")

    cmd = _curl_common_args() + [
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2026-03-10",
        url,
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "curl gagal mengambil GitHub API: "
            + (result.stderr.strip() or f"exit code {result.returncode}")
        )
    return json.loads(result.stdout)


def _curl_download(url: str, destination: Path) -> None:
    if not _curl_available():
        raise RuntimeError("curl tidak tersedia.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destination.with_suffix(destination.suffix + ".part")
    temp_path.unlink(missing_ok=True)

    cmd = _curl_common_args() + [
        "--output", str(temp_path),
        url,
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(
            "curl gagal mengunduh file: "
            + (result.stderr.strip() or f"exit code {result.returncode}")
        )

    if not temp_path.exists() or temp_path.stat().st_size == 0:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError("curl menghasilkan file kosong.")

    temp_path.replace(destination)


def request_json(url: str) -> dict:
    """Fetch JSON with verified TLS, retries, then system curl fallback."""
    errors: list[str] = []
    headers = _github_headers(accept_json=True)

    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(
                req,
                timeout=45,
                context=_ssl_context(),
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            errors.append(f"urllib attempt {attempt}: {exc}")
            if attempt < 3:
                log(f"GitHub API gagal via Python, retry {attempt}/3...")
                time.sleep(attempt * 2)

    if _curl_available():
        log("TLS Python/Conda gagal. Mencoba fallback curl sistem...")
        try:
            return _curl_json(url)
        except Exception as exc:
            errors.append(f"curl: {exc}")

    raise RuntimeError(
        "Tidak dapat mengakses GitHub API dengan TLS terverifikasi.\n"
        + "\n".join(f"  - {item}" for item in errors)
        + "\nCoba cek koneksi/VPN/proxy, atau jalankan: curl -I https://api.github.com"
    )


def download(url: str, destination: Path) -> None:
    """Download with verified TLS and atomic write; curl is the fallback."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    headers = _github_headers(accept_json=False)

    for attempt in range(1, 4):
        temp_path = destination.with_suffix(destination.suffix + ".part")
        temp_path.unlink(missing_ok=True)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(
                req,
                timeout=120,
                context=_ssl_context(),
            ) as response, temp_path.open("wb") as out:
                shutil.copyfileobj(response, out)

            if not temp_path.exists() or temp_path.stat().st_size == 0:
                raise RuntimeError("hasil download kosong")

            temp_path.replace(destination)
            return
        except Exception as exc:
            temp_path.unlink(missing_ok=True)
            errors.append(f"urllib attempt {attempt}: {exc}")
            if attempt < 3:
                log(f"Download gagal via Python, retry {attempt}/3...")
                time.sleep(attempt * 2)

    if _curl_available():
        log("Download via Python gagal. Mencoba fallback curl sistem...")
        try:
            _curl_download(url, destination)
            return
        except Exception as exc:
            errors.append(f"curl: {exc}")

    raise RuntimeError(
        f"Gagal mengunduh {url}\n"
        + "\n".join(f"  - {item}" for item in errors)
    )


def raw_github_url(repo: str, file_name: str, branch: str = "main") -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{file_name}"


def ensure_core_files(workdir: Path, refresh: bool) -> None:
    missing = [name for name in CORE_FILES if not (workdir / name).exists()]
    targets = list(CORE_FILES) if refresh else missing
    if not targets:
        log("Core ConvertYAML sudah tersedia.")
        return

    for name in targets:
        log(f"Mengunduh core: {name}")
        download(raw_github_url(CORE_REPO, name), workdir / name)


def ensure_text_files(workdir: Path) -> None:
    sub_file = workdir / "subscription_links.txt"
    manual_file = workdir / "manual_nodes.txt"

    if not sub_file.exists():
        sub_file.write_text(
            "# Tambahkan URL subscription publik/milik Anda di bawah ini.\n"
            "# Satu URL per baris. Baris yang diawali # diabaikan.\n",
            encoding="utf-8",
        )
    if not manual_file.exists():
        manual_file.write_text(
            "# Node manual opsional. Satu URI VLESS/VMess/Trojan/SS per baris.\n",
            encoding="utf-8",
        )


def pip_install_dependencies(workdir: Path) -> None:
    try:
        import requests  # noqa: F401
        import yaml  # noqa: F401
        log("Dependency Python sudah tersedia.")
        return
    except Exception:
        pass

    log("Memasang dependency Python...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "requests>=2.31",
            "PyYAML>=6.0",
        ],
        cwd=workdir,
        check=True,
    )


def normalized_platform() -> tuple[str, str]:
    system_raw = platform.system().lower()
    machine_raw = platform.machine().lower()

    system_map = {
        "windows": "windows",
        "linux": "linux",
        "darwin": "darwin",
    }
    if system_raw not in system_map:
        raise RuntimeError(f"OS belum didukung otomatis: {platform.system()}")

    if machine_raw in {"x86_64", "amd64", "x64"}:
        arch = "amd64"
    elif machine_raw in {"arm64", "aarch64"}:
        arch = "arm64"
    else:
        raise RuntimeError(f"Arsitektur belum didukung otomatis: {platform.machine()}")

    return system_map[system_raw], arch


def executable_name(base: str) -> str:
    return base + (".exe" if platform.system().lower() == "windows" else "")


def make_executable(path: Path) -> None:
    if platform.system().lower() != "windows":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def select_mihomo_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    candidates: list[tuple[int, dict]] = []
    prefix = f"mihomo-{os_name}-{arch}"

    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if not name.startswith(prefix):
            continue
        if "debug" in name:
            continue
        if not (name.endswith(".gz") or name.endswith(".zip")):
            continue

        score = 50
        if arch == "amd64" and "compatible" in name:
            score -= 20
        if "-v1-" in name or "-v2-" in name or "-v3-" in name:
            score += 10
        if "go1" in name or "go120" in name or "go122" in name or "go124" in name:
            score += 5
        candidates.append((score, asset))

    if not candidates:
        raise RuntimeError(f"Tidak menemukan asset Mihomo untuk {os_name}/{arch}")

    candidates.sort(key=lambda item: (item[0], item[1].get("name", "")))
    return candidates[0][1]


def select_singbox_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    candidates: list[dict] = []
    needle = f"-{os_name}-{arch}"

    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if not name.startswith("sing-box-"):
            continue
        if needle not in name:
            continue
        if name.endswith(".tar.gz") or name.endswith(".zip"):
            candidates.append(asset)

    if not candidates:
        raise RuntimeError(f"Tidak menemukan asset sing-box untuk {os_name}/{arch}")

    candidates.sort(key=lambda x: len(str(x.get("name", ""))))
    return candidates[0]


def extract_binary(archive_path: Path, binary_name: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if archive_path.name.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:gz") as tar:
            members = [
                m for m in tar.getmembers()
                if m.isfile() and Path(m.name).name.lower() == binary_name.lower()
            ]
            if not members:
                raise RuntimeError(f"Binary {binary_name} tidak ditemukan di {archive_path.name}")
            member = members[0]
            extracted = tar.extractfile(member)
            if extracted is None:
                raise RuntimeError(f"Gagal mengekstrak {binary_name}")
            with output_path.open("wb") as out:
                shutil.copyfileobj(extracted, out)

    elif archive_path.name.endswith(".zip"):
        with zipfile.ZipFile(archive_path) as zf:
            members = [
                n for n in zf.namelist()
                if Path(n).name.lower() == binary_name.lower()
            ]
            if not members:
                raise RuntimeError(f"Binary {binary_name} tidak ditemukan di {archive_path.name}")
            with zf.open(members[0]) as src, output_path.open("wb") as out:
                shutil.copyfileobj(src, out)

    elif archive_path.name.endswith(".gz"):
        with gzip.open(archive_path, "rb") as src, output_path.open("wb") as out:
            shutil.copyfileobj(src, out)

    else:
        raise RuntimeError(f"Format archive belum didukung: {archive_path.name}")

    make_executable(output_path)


def ensure_binary(
    workdir: Path,
    repo: str,
    program: str,
    selector,
    force_download: bool,
) -> Path:
    bin_dir = workdir / ".local_bin"
    bin_dir.mkdir(exist_ok=True)

    exe = executable_name(program)
    output_path = bin_dir / exe

    if output_path.exists() and not force_download:
        log(f"{program} sudah tersedia: {output_path}")
        return output_path

    if not force_download:
        system_binary = shutil.which(exe) or shutil.which(program)
        if system_binary:
            system_path = Path(system_binary).resolve()
            log(f"Menggunakan {program} dari PATH: {system_path}")
            return system_path

    os_name, arch = normalized_platform()
    log(f"Mencari {program} terbaru untuk {os_name}/{arch}...")

    try:
        release = request_json(f"{GITHUB_API}/repos/{repo}/releases/latest")
    except Exception as exc:
        raise RuntimeError(
            f"Gagal mendapatkan metadata release {program} dari GitHub.\n"
            f"{exc}\n\n"
            "Runner tidak mematikan verifikasi SSL. Pada macOS/Conda, "
            "fallback curl akan digunakan otomatis bila tersedia."
        ) from exc
    assets = release.get("assets") or []
    asset = selector(assets, os_name, arch)

    asset_name = str(asset["name"])
    asset_url = str(asset["browser_download_url"])
    log(f"Mengunduh {asset_name}")

    with tempfile.TemporaryDirectory(prefix=f"{program}-download-") as tempdir:
        archive = Path(tempdir) / asset_name
        download(asset_url, archive)
        extract_binary(archive, exe, output_path)

    version = subprocess.run(
        [str(output_path), "version"] if program == "sing-box" else [str(output_path), "-v"],
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    first_line = (version.stdout or "").strip().splitlines()
    if first_line:
        log(f"{program}: {first_line[0]}")
    return output_path


def load_config(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Config tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("local_config.json harus berupa object JSON.")
    return {str(k): str(v) for k, v in data.items()}


def build_environment(args, workdir: Path, mihomo: Path, singbox: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(DEFAULT_ENV)
    env.update(load_config(args.config))

    env["MAX_NODES"] = str(args.max_nodes)
    env["MIN_OUTPUT_NODES"] = str(min(args.min_nodes, args.max_nodes))
    env["MIHOMO_PATH"] = str(mihomo.resolve())
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



# Security / adblock provider sources. These are domain-only lists so they work
# with Mihomo rule-provider behavior=domain and format=text.
SECURITY_PROVIDERS = {
    "security-tif-mini": {
        "type": "http",
        "behavior": "domain",
        "format": "text",
        "interval": 43200,
        "path": "./ruleset/security-tif-mini.txt",
        "url": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/tif.mini-onlydomains.txt",
    },
    "popup-ads": {
        "type": "http",
        "behavior": "domain",
        "format": "text",
        "interval": 43200,
        "path": "./ruleset/popup-ads.txt",
        "url": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/popupads-onlydomains.txt",
    },
    "awavenue-ads": {
        "type": "http",
        "behavior": "domain",
        "format": "text",
        "interval": 43200,
        "path": "./ruleset/awavenue-ads.txt",
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/AdvertisingLite/AdvertisingLite_Domain.txt",
    },
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
! ConvertYAML Local Runner - YouTube Optimized
! Mode: safe
! Fokus: menyembunyikan slot iklan/promosi tanpa memblokir CDN video.
! Kompatibel dengan uBlock Origin / AdGuard yang menerima sintaks filter ABP/uBO.
!
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
! ConvertYAML Local Runner - YouTube Optimized
! Mode: enhanced
! Lapisan tambahan untuk endpoint iklan/telemetri yang terpisah dari CDN video.
! Tidak memblokir googlevideo.com agar playback utama tetap aman.
!
||googleads.g.doubleclick.net^$domain=youtube.com
||static.doubleclick.net^$domain=youtube.com
||pagead2.googlesyndication.com^$domain=youtube.com
||tpc.googlesyndication.com^$domain=youtube.com
||www.googleadservices.com^$domain=youtube.com
||youtube.com/api/stats/ads^$xhr,domain=youtube.com
||youtube.com/pagead/*$xhr,domain=youtube.com
||youtube.com/ptracking^$xhr,domain=youtube.com
"""


def _valid_policies(config: dict) -> set[str]:
    names = {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
    for proxy in config.get("proxies", []) or []:
        if isinstance(proxy, dict) and proxy.get("name"):
            names.add(str(proxy["name"]))
    for group in config.get("proxy-groups", []) or []:
        if isinstance(group, dict) and group.get("name"):
            names.add(str(group["name"]))
    return names


def detect_default_routing_policy(config: dict) -> str:
    """Return the final routing target already used by the generated YAML."""
    valid = _valid_policies(config)
    rules = config.get("rules") or []

    for raw in reversed(rules):
        parts = [p.strip() for p in str(raw).split(",")]
        if len(parts) >= 2 and parts[0].upper() in {"MATCH", "FINAL"}:
            policy = parts[1]
            if policy in valid:
                return policy

    for preferred in ("GLOBAL", "PROXY", "Proxy", "AUTO", "Auto"):
        if preferred in valid:
            return preferred

    groups = [
        str(g["name"]) for g in config.get("proxy-groups", []) or []
        if isinstance(g, dict) and g.get("name")
    ]
    if groups:
        return groups[0]

    proxies = [
        str(p["name"]) for p in config.get("proxies", []) or []
        if isinstance(p, dict) and p.get("name")
    ]
    if proxies:
        return proxies[0]

    return "DIRECT"


def _normal_dns_resolvers(config: dict):
    dns = config.get("dns")
    if not isinstance(dns, dict):
        return None
    resolvers = dns.get("nameserver")
    if isinstance(resolvers, list) and resolvers:
        return list(resolvers)
    if isinstance(resolvers, str) and resolvers.strip():
        return resolvers.strip()
    return None


def apply_youtube_network_guard(path: Path, mode: str) -> bool:
    """Keep YouTube playback/API domains away from broad DNS/ad reject rules.

    This does not attempt to block video ads at DNS level. It preserves the
    YAML's existing final routing policy and lets the browser filter handle
    YouTube-specific page/request filtering.
    """
    if not path.exists():
        return False

    import yaml
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        return False

    changed = False
    current_rules = config.get("rules")
    if not isinstance(current_rules, list):
        current_rules = []

    managed_domains = set(YOUTUBE_PLAYBACK_DOMAINS)
    cleaned_rules = []
    for rule in current_rules:
        value = str(rule)
        parts = [p.strip() for p in value.split(",")]
        if len(parts) >= 3 and parts[0].upper() in {"DOMAIN", "DOMAIN-SUFFIX"}:
            if parts[1].lower() in managed_domains and parts[2] != "REJECT":
                continue
        cleaned_rules.append(value)

    # Remove managed DNS guard entries when mode is off.
    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            for domain in YOUTUBE_PLAYBACK_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in policy:
                        policy.pop(key, None)
                        changed = True

    if mode == "off":
        if cleaned_rules != current_rules:
            config["rules"] = cleaned_rules
            changed = True
        if changed:
            path.write_text(
                yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140),
                encoding="utf-8",
            )
        return changed

    route_policy = detect_default_routing_policy(config)
    guard_rules = [
        f"DOMAIN-SUFFIX,{domain},{route_policy}"
        for domain in YOUTUBE_PLAYBACK_DOMAINS
    ]

    # Insert before security blockers. If none exist, put them at the beginning.
    insert_at = 0
    for i, rule in enumerate(cleaned_rules):
        value = str(rule)
        if value.startswith((
            "RULE-SET,security-tif-mini,",
            "RULE-SET,popup-ads,",
            "RULE-SET,awavenue-ads,",
            "RULE-SET,tracker-domain,",
            "GEOSITE,category-ads-all,",
            "GEOSITE,tracker,",
        )):
            insert_at = i
            break

    new_rules = cleaned_rules[:insert_at] + guard_rules + cleaned_rules[insert_at:]
    if new_rules != current_rules:
        config["rules"] = new_rules
        changed = True

    # OpenClash compatibility:
    # Do not inject YouTube wildcard domains into nameserver-policy.
    # Older cores can be stricter when parsing domain policy keys. The routing
    # rules above are sufficient to keep YouTube playback away from REJECT.
    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            for domain in YOUTUBE_PLAYBACK_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in policy:
                        policy.pop(key, None)
                        changed = True

    if changed:
        path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140),
            encoding="utf-8",
        )
        log(f"YouTube network guard [{mode}] -> {path.name} | route={route_policy}")

    return changed


def write_youtube_browser_filters(workdir: Path, mode: str, filename: str) -> Path | None:
    path = workdir / filename

    if mode == "off":
        if path.exists():
            path.unlink()
            log(f"Filter browser YouTube dihapus: {filename}")
        return None

    body = YOUTUBE_BROWSER_FILTERS_SAFE
    if mode == "enhanced":
        body += "\n" + YOUTUBE_BROWSER_FILTERS_ENHANCED

    body += """\

! Catatan:
! - Jangan tambahkan ||googlevideo.com^ karena domain tersebut juga membawa video utama.
! - Filter YouTube berubah dari waktu ke waktu. Gunakan filter bawaan blocker juga.
! - Jika playback bermasalah, ganti mode ke safe atau off.
"""
    path.write_text(body, encoding="utf-8")
    log(f"Filter browser YouTube [{mode}] dibuat: {filename}")
    return path



def patch_core_compatibility(workdir: Path) -> None:
    """Patch known compatibility issues in the downloaded ConvertYAML core."""
    changed_files: list[str] = []

    generate_path = workdir / "generate_yaml.py"
    if generate_path.exists():
        source = generate_path.read_text(encoding="utf-8", errors="ignore")
        original = source

        # New Mihomo releases removed this global option. Per-proxy
        # client-fingerprint remains untouched.
        source = re.sub(
            r'(?m)^[ \t]*"global-client-fingerprint"[ \t]*:[ \t]*"chrome",[ \t]*\n',
            "",
            source,
        )

        # Fix upstream lite YAML builder leaving GLOBAL -> MANUAL even when
        # MANUAL does not exist.
        source = source.replace(
            'refs_available = set(proxy_names) | set(keep_group_names) | {"REJECT", "GLOBAL"}',
            'refs_available = set(proxy_names) | set(groups.keys()) | {"DIRECT", "REJECT", "GLOBAL"}',
        )

        if source != original:
            generate_path.write_text(source, encoding="utf-8")
            changed_files.append(generate_path.name)

    core_path = workdir / "sumberyaml_core.py"
    if core_path.exists():
        source = core_path.read_text(encoding="utf-8", errors="ignore")
        original = source
        source = re.sub(
            r'(?m)^[ \t]*"global-client-fingerprint"[ \t]*:[ \t]*"chrome",[ \t]*\n',
            "",
            source,
        )
        if source != original:
            core_path.write_text(source, encoding="utf-8")
            changed_files.append(core_path.name)

    if changed_files:
        log("Patch kompatibilitas diterapkan: " + ", ".join(changed_files))


def load_adblock_allowlist(workdir: Path) -> list[str]:
    path = workdir / "adblock_allowlist.txt"
    if not path.exists():
        path.write_text(
            "# Domain yang tidak boleh diblokir. Satu domain per baris.\n"
            "# Contoh: example.com\n",
            encoding="utf-8",
        )
        return []

    domains: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = raw.strip().lower().rstrip(".")
        if not value or value.startswith("#"):
            continue
        value = re.sub(r"^https?://", "", value).split("/", 1)[0]
        if value.startswith("*."):
            value = value[2:]
        if value.startswith("+."):
            value = value[2:]
        if re.fullmatch(r"[a-z0-9][a-z0-9.-]*[a-z0-9]", value) and "." in value:
            domains.append(value)
    return sorted(set(domains))


def sanitize_generated_yaml(path: Path) -> bool:
    """Repair stale group references and removed Mihomo settings."""
    if not path.exists():
        return False
    try:
        import yaml
        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        log(f"Skip sanitasi {path.name}: YAML tidak dapat dibaca ({exc})")
        return False
    if not isinstance(config, dict):
        return False

    changed = False
    if "global-client-fingerprint" in config:
        config.pop("global-client-fingerprint", None)
        log(f"{path.name}: hapus global-client-fingerprint yang sudah deprecated")
        changed = True

    # Remove compatibility leftovers from older v1.2/v1.3 generated files.
    dns = config.get("dns")
    if isinstance(dns, dict):
        ns_policy = dns.get("nameserver-policy")
        if isinstance(ns_policy, dict):
            old_combo = "geosite:category-ads-all,tracker"
            if old_combo in ns_policy:
                value = ns_policy.pop(old_combo)
                ns_policy.setdefault("geosite:category-ads-all", value)
                log(f"{path.name}: DNS geosite tracker lama dipisahkan dari category-ads-all")
                changed = True

            # v1.3 inserted these explicit wildcard policies. Remove them for
            # maximum compatibility with OpenClash cores.
            for domain in YOUTUBE_PLAYBACK_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in ns_policy:
                        ns_policy.pop(key, None)
                        changed = True

    # Remove stale geosite:tracker rules. The security stage re-adds tracking
    # protection through tracker-domain.mrs.
    rules = config.get("rules")
    if isinstance(rules, list):
        fixed_rules = []
        for rule in rules:
            value = str(rule)
            if value.startswith("GEOSITE,tracker,"):
                log(f"{path.name}: hapus rule tidak kompatibel {value}")
                changed = True
                continue
            fixed_rules.append(value)
        config["rules"] = fixed_rules

    providers = config.get("rule-providers")
    if isinstance(providers, dict):
        for provider_name, provider in providers.items():
            if not isinstance(provider, dict):
                continue
            if str(provider.get("type") or "").lower() != "http":
                continue
            fmt = str(provider.get("format") or "yaml").lower()
            ext = ".mrs" if fmt == "mrs" else ".txt" if fmt == "text" else ".yaml"
            provider_path = str(provider.get("path") or "").strip()
            if not provider_path or provider_path.startswith("/"):
                safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", str(provider_name))
                provider["path"] = f"./ruleset/{safe_name}{ext}"
                log(f"{path.name}: set path provider {provider_name} -> {provider['path']}")
                changed = True

    proxies = [
        p for p in config.get("proxies", [])
        if isinstance(p, dict) and str(p.get("name") or "").strip()
    ]
    proxy_names = {str(p["name"]) for p in proxies}
    groups = [
        g for g in config.get("proxy-groups", [])
        if isinstance(g, dict) and str(g.get("name") or "").strip()
    ]
    group_names = {str(g["name"]) for g in groups}
    valid_refs = proxy_names | group_names | {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}

    for group in groups:
        refs = group.get("proxies")
        if not isinstance(refs, list):
            continue
        cleaned = []
        seen = set()
        for ref in refs:
            name = str(ref)
            if name in valid_refs and name not in seen:
                cleaned.append(name)
                seen.add(name)
        if cleaned != refs:
            missing = [str(ref) for ref in refs if str(ref) not in valid_refs]
            if missing:
                log(f"{path.name}: hapus referensi tidak ada dari {group.get('name')}: {', '.join(missing)}")
            group["proxies"] = cleaned
            changed = True
        if not group.get("proxies"):
            if proxy_names:
                group["proxies"] = [next(iter(proxy_names))]
                changed = True
            elif str(group.get("type") or "").lower() == "select":
                group["proxies"] = ["DIRECT"]
                changed = True

    if "MANUAL" not in group_names:
        rules = config.get("rules")
        if isinstance(rules, list):
            fixed = []
            for rule in rules:
                value = str(rule)
                parts = value.split(",")
                idx = -2 if parts and parts[-1].strip() == "no-resolve" else -1
                if len(parts) >= 2 and parts[idx].strip() == "MANUAL":
                    parts[idx] = "GLOBAL"
                    value = ",".join(parts)
                    changed = True
                fixed.append(value)
            config["rules"] = fixed

    if changed:
        path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    return changed


def apply_adblock_security(path: Path, profile: str, workdir: Path, interval: int = 43200) -> bool:
    """Inject layered ad, tracker, popup, malware and phishing blocking."""
    if not path.exists() or profile == "off":
        return False

    import yaml
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        return False

    changed = False
    providers = config.setdefault("rule-providers", {})
    if not isinstance(providers, dict):
        providers = {}
        config["rule-providers"] = providers
        changed = True

    selected = ["security-tif-mini", "popup-ads", "tracker-domain"]
    if profile == "strict":
        selected.append("awavenue-ads")

    for name in selected:
        provider = dict(SECURITY_PROVIDERS[name])
        provider["interval"] = interval
        if providers.get(name) != provider:
            providers[name] = provider
            changed = True

    # DNS-layer blocking for MetaCubeX geosite categories. MetaCubeX documents
    # rcode://success for category-ads-all. Tracker uses the same domain matcher.
    dns = config.setdefault("dns", {})
    if isinstance(dns, dict):
        policy = dns.setdefault("nameserver-policy", {})
        if not isinstance(policy, dict):
            policy = {}
            dns["nameserver-policy"] = policy
            changed = True
        # category-ads-all is present in the standard GeoSite.dat used by
        # OpenClash. Tracker is handled by tracker-domain.mrs instead, because
        # some OpenClash GeoSite.dat builds do not contain geosite:tracker.
        old_key = "geosite:category-ads-all,tracker"
        if old_key in policy:
            policy.pop(old_key, None)
            changed = True
        key = "geosite:category-ads-all"
        if policy.get(key) != "rcode://success":
            policy[key] = "rcode://success"
            changed = True

    allowlist_rules = [
        f"DOMAIN-SUFFIX,{domain},DIRECT"
        for domain in load_adblock_allowlist(workdir)
    ]

    security_rules = allowlist_rules + [
        "RULE-SET,security-tif-mini,REJECT",
        "RULE-SET,popup-ads,REJECT",
        "GEOSITE,category-ads-all,REJECT",
        "RULE-SET,tracker-domain,REJECT",
    ]
    if profile == "strict":
        security_rules.insert(len(allowlist_rules) + 2, "RULE-SET,awavenue-ads,REJECT")

    current_rules = config.get("rules")
    if not isinstance(current_rules, list):
        current_rules = []

    managed_prefixes = (
        "RULE-SET,security-tif-mini,",
        "RULE-SET,popup-ads,",
        "RULE-SET,awavenue-ads,",
        "RULE-SET,tracker-domain,",
        "GEOSITE,category-ads-all,",
        "GEOSITE,tracker,",
    )
    allow_domains = {r.split(",", 2)[1] for r in allowlist_rules}
    cleaned_rules = []
    for rule in current_rules:
        value = str(rule)
        if value.startswith(managed_prefixes):
            continue
        if value.startswith("DOMAIN-SUFFIX,"):
            parts = value.split(",")
            if len(parts) >= 3 and parts[1] in allow_domains and parts[2] == "DIRECT":
                continue
        cleaned_rules.append(value)

    new_rules = security_rules + cleaned_rules
    if new_rules != current_rules:
        config["rules"] = new_rules
        changed = True

    if changed:
        path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    return changed


def optimize_outputs(
    workdir: Path,
    files: Iterable[str],
    profile: str,
    interval: int,
    youtube_mode: str = "enhanced",
    youtube_filter_file: str = "youtube_browser_filters.txt",
) -> None:
    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue
        sanitize_generated_yaml(path)
        if apply_adblock_security(path, profile, workdir, interval):
            log(f"Adblock/security [{profile}] diterapkan: {filename}")
        apply_youtube_network_guard(path, youtube_mode)
        # Re-sanitize because adding rules can expose an old invalid group.
        sanitize_generated_yaml(path)

    write_youtube_browser_filters(workdir, youtube_mode, youtube_filter_file)


def validate_yaml(workdir: Path, mihomo: Path, files: Iterable[str]) -> None:
    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue
        log(f"Validasi Mihomo: {filename}")
        subprocess.run(
            [str(mihomo), "-t", "-d", str(workdir), "-f", str(path)],
            cwd=workdir,
            check=True,
        )


def print_outputs(workdir: Path) -> None:
    names = [
        "openclash_auto.yaml",
        "openclash_android.yaml",
        "openclash_lite.yaml",
        "openclash_fresh_pool.yaml",
        "akun.txt",
        "openclash_auto_report.csv",
        "urltest_report.csv",
        "nekobox_test_report.csv",
        "node_quality_report.md",
        "last_update.txt",
        "youtube_browser_filters.txt",
    ]
    print("\nHasil:")
    for name in names:
        p = workdir / name
        if p.exists():
            print(f"  - {p}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Jalankan pencarian dan validasi node ConvertYAML secara lokal."
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path.cwd(),
        help="Folder kerja. Default: folder terminal saat ini.",
    )
    parser.add_argument("--max-nodes", type=int, default=20, help="Jumlah node final.")
    parser.add_argument("--min-nodes", type=int, default=10, help="Target minimal node.")
    parser.add_argument("--candidate-min", type=int, default=None, help="Minimal kandidat awal.")
    parser.add_argument("--urltest-pool", type=int, default=None, help="Ukuran pool sebelum URL test.")
    parser.add_argument("--nekobox-pool", type=int, default=None, help="Ukuran pool sebelum tes sing-box.")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="File JSON untuk override environment variable.",
    )
    parser.add_argument(
        "--refresh-core",
        action="store_true",
        help="Unduh ulang generate_yaml.py dan sumberyaml_core.py dari repo.",
    )
    parser.add_argument(
        "--refresh-binaries",
        action="store_true",
        help="Unduh ulang Mihomo dan sing-box terbaru.",
    )
    parser.add_argument(
        "--no-nekobox",
        action="store_true",
        help="Lewati tes sing-box/NekoBox. Lebih cepat, tetapi validasi lebih sedikit.",
    )
    parser.add_argument(
        "--no-ws-only",
        action="store_true",
        help="Izinkan network selain WebSocket.",
    )
    parser.add_argument(
        "--adblock-profile",
        choices=("off", "balanced", "strict"),
        default=None,
        help="Profil pemblokiran: off, balanced (default), atau strict.",
    )
    parser.add_argument(
        "--youtube-mode",
        choices=("off", "safe", "enhanced"),
        default=None,
        help="Optimasi YouTube: off, safe, atau enhanced (default).",
    )
    parser.add_argument(
        "--network-test",
        action="store_true",
        help="Tes koneksi TLS ke GitHub API lalu keluar.",
    )
    parser.add_argument(
        "--no-install-deps",
        action="store_true",
        help="Jangan memasang dependency Python otomatis.",
    )
    return parser.parse_args()



def run_network_test() -> int:
    print("ConvertYAML network diagnostic")
    print(f"Python       : {sys.version.split()[0]}")
    print(f"Executable   : {sys.executable}")
    print(f"OpenSSL      : {ssl.OPENSSL_VERSION}")
    print(f"curl         : {shutil.which('curl') or 'tidak ditemukan'}")
    try:
        import certifi  # type: ignore
        print(f"certifi CA   : {certifi.where()}")
    except Exception:
        print("certifi CA   : tidak tersedia")

    url = f"{GITHUB_API}/repos/{MIHOMO_REPO}/releases/latest"

    print("\n[1] Tes urllib/Python...")
    try:
        req = urllib.request.Request(url, headers=_github_headers(True))
        with urllib.request.urlopen(
            req,
            timeout=20,
            context=_ssl_context(),
        ) as response:
            print(f"    OK HTTP {getattr(response, 'status', '?')}")
    except Exception as exc:
        print(f"    GAGAL: {exc}")

    print("[2] Tes jalur runner (dengan fallback curl)...")
    try:
        data = request_json(url)
        print(f"    OK release: {data.get('tag_name', '(tanpa tag)')}")
        return 0
    except Exception as exc:
        print(f"    GAGAL: {exc}")
        return 1



def main() -> int:
    args = parse_args()

    if args.network_test:
        return run_network_test()

    workdir = args.workdir.expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    if args.max_nodes < 1:
        raise SystemExit("--max-nodes minimal 1")
    if args.min_nodes < 1:
        raise SystemExit("--min-nodes minimal 1")

    log(f"Folder kerja: {workdir}")
    ensure_core_files(workdir, refresh=args.refresh_core)
    patch_core_compatibility(workdir)
    ensure_text_files(workdir)
    load_adblock_allowlist(workdir)

    if not args.no_install_deps:
        pip_install_dependencies(workdir)

    mihomo = ensure_binary(
        workdir,
        MIHOMO_REPO,
        "mihomo",
        select_mihomo_asset,
        args.refresh_binaries,
    )
    singbox = ensure_binary(
        workdir,
        SINGBOX_REPO,
        "sing-box",
        select_singbox_asset,
        args.refresh_binaries,
    )

    env = build_environment(args, workdir, mihomo, singbox)

    log("Menjalankan pencarian, penyaringan, dan pengujian node...")
    result = subprocess.run(
        [sys.executable, "generate_yaml.py"],
        cwd=workdir,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        print(
            "\nPipeline gagal. Coba jalankan lagi dengan kandidat lebih besar, misalnya:\n"
            "  python local_runner.py --candidate-min 3000 --urltest-pool 100\n",
            file=sys.stderr,
        )
        return result.returncode

    generated_yaml_files = (
        env.get("OUTPUT_YAML", "openclash_auto.yaml"),
        env.get("OUTPUT_ANDROID_YAML", "openclash_android.yaml"),
        env.get("OUTPUT_LITE_YAML", "openclash_lite.yaml"),
        env.get("OUTPUT_FRESH_YAML", "openclash_fresh_pool.yaml"),
    )

    adblock_profile = (args.adblock_profile or env.get("ADBLOCK_PROFILE", "balanced")).strip().lower()
    if adblock_profile not in {"off", "balanced", "strict"}:
        adblock_profile = "balanced"
    try:
        adblock_interval = max(3600, int(env.get("ADBLOCK_PROVIDER_INTERVAL", "43200")))
    except ValueError:
        adblock_interval = 43200

    youtube_mode = (
        args.youtube_mode or env.get("YOUTUBE_ADBLOCK_MODE", "enhanced")
    ).strip().lower()
    if youtube_mode not in {"off", "safe", "enhanced"}:
        youtube_mode = "enhanced"
    youtube_filter_file = env.get(
        "YOUTUBE_BROWSER_FILTER_FILE",
        "youtube_browser_filters.txt",
    ).strip() or "youtube_browser_filters.txt"

    optimize_outputs(
        workdir,
        generated_yaml_files,
        adblock_profile,
        adblock_interval,
        youtube_mode=youtube_mode,
        youtube_filter_file=youtube_filter_file,
    )
    validate_yaml(workdir, mihomo, generated_yaml_files)

    log("Selesai.")
    print_outputs(workdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
