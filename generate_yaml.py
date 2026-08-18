from __future__ import annotations

import os
import re
import socket
import subprocess
import tempfile
import time
from contextlib import suppress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse, urlunparse

import base64
import json
import yaml
import requests

from openclash_target import (
    MIHOMO_TARGET_LABEL,
    assert_target_mihomo,
    validate_generated_text_with_core,
)

from sumberyaml_core import (
    ALT_TEST_URL,
    DEFAULT_LINKS,
    TARGET_SERVER,
    ONLY_PORT,
    b64decode_text,
    build_akun_txt,
    build_csv,
    build_openclash_android_yaml,
    build_openclash_yaml,
    extract_uris,
    looks_like_ip,
    node_network,
    normalize_name,
    parse_uri,
    process_sources,
    provider_label_from_original_server,
    safe_proxy_name,
    unique_names,
)


def _read_text_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8", errors="ignore")


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"[WARN] {name}={value!r} tidak valid, pakai default {default}.")
        return default


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        print(f"[WARN] {name}={value!r} tidak valid, pakai default {default}.")
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name, "").strip().lower()
    if not value:
        return default
    return value in {"1", "true", "yes", "y", "on", "aktif"}



def _target_core_path() -> str:
    return os.getenv("MIHOMO_PATH", "./mihomo").strip() or "./mihomo"


def _require_target_core() -> str:
    core_path = _target_core_path()
    strict = _env_bool("REQUIRE_EXACT_MIHOMO_CORE", True)
    try:
        version = assert_target_mihomo(core_path, strict=strict)
    except RuntimeError as exc:
        raise SystemExit(f"[ERROR] {exc}") from exc
    print(f"[INFO] Mihomo validator: {version}")
    if strict:
        print(f"[INFO] Exact target aktif: {MIHOMO_TARGET_LABEL}")
    return core_path


def _free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _expected_statuses() -> set[int]:
    raw = os.getenv("URL_TEST_EXPECTED_STATUS", os.getenv("REAL_CHECK_EXPECTED_STATUS", "204,200,301,302")).strip()
    statuses: set[int] = set()
    for item in raw.replace("/", ",").replace(";", ",").split(","):
        item = item.strip()
        if not item:
            continue
        try:
            statuses.add(int(item))
        except ValueError:
            pass
    return statuses or {204, 200, 301, 302}


def _wait_controller(controller_url: str, timeout_s: float = 10.0) -> bool:
    deadline = time.time() + max(1.0, timeout_s)
    while time.time() < deadline:
        try:
            response = requests.get(controller_url + "/proxies", timeout=0.6)
            if response.status_code < 500:
                return True
        except Exception:
            time.sleep(0.2)
    return False


def _node_name(node: Any) -> str:
    return str(node.clash.get("name") or node.name or "")



def _mihomo_openclash_compatibility_filter(
    nodes: list[Any],
    *,
    label: str,
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Keep only nodes accepted by the current Mihomo proxy parser.

    The fast path validates all candidates in one Mihomo process. If that batch
    fails, smaller chunks are tested in parallel and only failing chunks fall
    back to per-node isolation. This keeps the original strictness while avoiding
    one process startup for every healthy node.
    """
    rows: list[dict[str, Any]] = []
    if not nodes:
        return [], rows
    if not _env_bool("REQUIRE_OPENCLASH_COMPAT", True):
        for node in nodes:
            rows.append({
                "source": label,
                "name": _node_name(node),
                "type": str((getattr(node, "clash", {}) or {}).get("type") or getattr(node, "type", "")),
                "network": node_network(node),
                "compatible": "skipped",
                "reason": "compatibility filter disabled",
            })
        return nodes, rows

    core_path = _target_core_path()
    if not Path(core_path).exists():
        raise SystemExit(
            f"Mihomo binary tidak ditemukan di {core_path}; "
            "OpenClash compatibility filter wajib aktif."
        )
    try:
        assert_target_mihomo(
            core_path,
            strict=_env_bool("REQUIRE_EXACT_MIHOMO_CORE", True),
        )
    except RuntimeError as exc:
        raise SystemExit(f"[ERROR] {exc}") from exc

    timeout_s = max(2.0, _env_float("OPENCLASH_COMPAT_TIMEOUT_SEC", 6.0))
    workers = max(1, min(16, _env_int("OPENCLASH_COMPAT_WORKERS", 6)))
    isolation_batch_size = max(2, min(32, _env_int("OPENCLASH_COMPAT_ISOLATION_BATCH_SIZE", 8)))

    def prepare(index: int, node: Any) -> tuple[int, Any, dict[str, Any], dict[str, Any]]:
        clash = dict(getattr(node, "clash", {}) or {})
        name = str(clash.get("name") or _node_name(node) or f"NODE-{index + 1}")
        proto = str(clash.get("type") or getattr(node, "type", "")).lower()
        network = node_network(node)
        row = {
            "source": label,
            "name": name,
            "type": proto,
            "network": network,
            "compatible": "no",
            "reason": "",
        }
        if clash:
            clash["name"] = name
        return index, node, row, clash

    def run_batch(batch: list[tuple[int, Any, dict[str, Any], dict[str, Any]]]) -> tuple[bool, str]:
        if not batch:
            return True, "empty batch"
        proxies = [item[3] for item in batch]
        names = [str(item[2]["name"]) for item in batch]
        tmp_obj = tempfile.TemporaryDirectory(prefix="openclash-compat-")
        tmpdir = Path(tmp_obj.name)
        config_path = tmpdir / "config.yaml"
        config = {
            "proxies": proxies,
            "proxy-groups": [
                {
                    "name": "OPENCLASH-COMPAT",
                    "type": "select",
                    "proxies": names,
                }
            ],
            "rules": ["MATCH,OPENCLASH-COMPAT"],
        }
        try:
            config_path.write_text(
                yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [core_path, "-t", "-d", str(tmpdir), "-f", str(config_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_s,
                check=False,
            )
            output = (proc.stdout or "").strip().replace("\n", " | ")
            if proc.returncode == 0:
                return True, "mihomo config test ok"
            return False, output[-500:] or f"mihomo exit {proc.returncode}"
        except subprocess.TimeoutExpired:
            return False, f"mihomo config test timeout > {timeout_s:.1f}s"
        except Exception as exc:
            return False, f"{type(exc).__name__}: {str(exc)[:300]}"
        finally:
            tmp_obj.cleanup()

    prepared = [prepare(i, node) for i, node in enumerate(nodes)]
    result_rows: dict[int, dict[str, Any]] = {}
    valid_items: list[tuple[int, Any, dict[str, Any], dict[str, Any]]] = []
    for item in prepared:
        index, _node, row, clash = item
        if clash:
            valid_items.append(item)
        else:
            row["reason"] = "empty proxy config"
            result_rows[index] = row

    def mark_pass(batch: list[tuple[int, Any, dict[str, Any], dict[str, Any]]], reason: str) -> None:
        for index, _node, row, _clash in batch:
            row["compatible"] = "yes"
            row["reason"] = reason
            result_rows[index] = row

    def mark_fail(item: tuple[int, Any, dict[str, Any], dict[str, Any]], reason: str) -> None:
        index, _node, row, _clash = item
        row["compatible"] = "no"
        row["reason"] = reason
        result_rows[index] = row

    if valid_items:
        full_ok, full_reason = run_batch(valid_items)
        if full_ok:
            mark_pass(valid_items, "mihomo batch config test ok")
        elif len(valid_items) == 1:
            mark_fail(valid_items[0], full_reason)
        else:
            chunks = [
                valid_items[i : i + isolation_batch_size]
                for i in range(0, len(valid_items), isolation_batch_size)
            ]
            failed_for_individual: list[tuple[int, Any, dict[str, Any], dict[str, Any]]] = []
            with ThreadPoolExecutor(max_workers=min(workers, len(chunks))) as executor:
                future_map = {executor.submit(run_batch, chunk): chunk for chunk in chunks}
                for future in as_completed(future_map):
                    chunk = future_map[future]
                    ok, reason = future.result()
                    if ok:
                        mark_pass(chunk, "mihomo isolation batch test ok")
                    elif len(chunk) == 1:
                        mark_fail(chunk[0], reason)
                    else:
                        failed_for_individual.extend(chunk)

            if failed_for_individual:
                with ThreadPoolExecutor(max_workers=min(workers, len(failed_for_individual))) as executor:
                    future_map = {
                        executor.submit(run_batch, [item]): item
                        for item in failed_for_individual
                    }
                    for future in as_completed(future_map):
                        item = future_map[future]
                        ok, reason = future.result()
                        if ok:
                            mark_pass([item], "mihomo individual config test ok")
                        else:
                            mark_fail(item, reason)

    passed: list[Any] = []
    for index, node in enumerate(nodes):
        row = result_rows[index]
        rows.append(row)
        ok = row["compatible"] == "yes"
        setattr(node, "openclash_compatible", ok)
        setattr(node, "openclash_compat_status", row["reason"])
        if ok:
            passed.append(node)
        else:
            print(
                f"[SKIP] OpenClash incompatible [{label}] "
                f"{row['name']} type={row['type']} network={row['network']}: {row['reason']}"
            )

    print(f"[INFO] OpenClash compatibility [{label}]: {len(passed)}/{len(nodes)} passed")
    return passed, rows

def _build_openclash_compat_report_csv(rows: list[dict[str, Any]]) -> str:
    import csv
    import io

    fields = ["source", "name", "type", "network", "compatible", "reason"]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buffer.getvalue()


def _mihomo_url_test_nodes(
    nodes: list[Any],
    *,
    target_count: int,
    test_url: str,
    timeout_ms: int,
) -> tuple[list[Any], int, str, list[dict[str, Any]]]:
    """Filter automatic nodes with a real Mihomo URL test.

    This test is intentionally applied only to automatic subscription nodes.
    Manual nodes are handled outside this function and are not filtered.
    """
    target_count = max(1, int(target_count))
    rows: list[dict[str, Any]] = []
    if not nodes:
        return [], 0, "no automatic nodes to URL test", rows

    if not _env_bool("REQUIRE_URL_TEST", True):
        final_nodes = nodes[:target_count]
        for node in final_nodes:
            node.url_test_status = "skipped-disabled"
            node.url_test_success = True
        return final_nodes, len(final_nodes), "URL test disabled", rows

    core_path = _target_core_path()
    if not Path(core_path).exists():
        raise SystemExit(f"Mihomo binary tidak ditemukan di {core_path}; URL test wajib aktif.")
    try:
        assert_target_mihomo(
            core_path,
            strict=_env_bool("REQUIRE_EXACT_MIHOMO_CORE", True),
        )
    except RuntimeError as exc:
        raise SystemExit(f"[ERROR] {exc}") from exc

    expected = _expected_statuses()
    proxy_port = _free_tcp_port()
    controller_port = _free_tcp_port()
    names = [_node_name(node) for node in nodes if _node_name(node)]
    if not names:
        return [], 0, "no usable proxy names for URL test", rows

    tmpdir_obj = tempfile.TemporaryDirectory(prefix="mihomo-urltest-")
    tmpdir = Path(tmpdir_obj.name)
    config_path = tmpdir / "config.yaml"
    config = {
        "mixed-port": proxy_port,
        "allow-lan": False,
        "bind-address": "127.0.0.1",
        "mode": "global",
        "log-level": os.getenv("MIHOMO_LOG_LEVEL", "error"),
        "ipv6": False,
        "unified-delay": True,
        "tcp-concurrent": True,
        "external-controller": f"127.0.0.1:{controller_port}",
        "profile": {"store-selected": False, "store-fake-ip": False},
        "dns": {
            "enable": True,
            "ipv6": False,
            "listen": "127.0.0.1:0",
            "enhanced-mode": "fake-ip",
            "fake-ip-range": "198.18.0.1/16",
            "cache-algorithm": "arc",
            "default-nameserver": ["1.1.1.1", "8.8.8.8"],
            "nameserver": ["https://1.1.1.1/dns-query", "https://dns.google/dns-query"],
        },
        "proxies": [node.clash for node in nodes],
        "proxy-groups": [{"name": "GLOBAL", "type": "select", "proxies": names}],
        "rules": ["MATCH,GLOBAL"],
    }
    config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")

    proc: subprocess.Popen[str] | None = None
    passed: list[Any] = []
    checked = 0
    reason = "ok"
    try:
        proc = subprocess.Popen(
            [core_path, "-d", str(tmpdir), "-f", str(config_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        controller_url = f"http://127.0.0.1:{controller_port}"
        if not _wait_controller(controller_url, timeout_s=float(os.getenv("MIHOMO_START_TIMEOUT", "10"))):
            raise SystemExit("Mihomo controller tidak start, URL test tidak bisa dilakukan.")

        proxy_url = f"http://127.0.0.1:{proxy_port}"
        request_timeout = max(1.0, float(timeout_ms) / 1000.0)
        settle_s = float(os.getenv("URL_TEST_SETTLE_SECONDS", "0.12"))
        user_agent = os.getenv("URL_TEST_USER_AGENT", "Mozilla/5.0 SumberYAML-URLTest/1.0")

        for node in nodes:
            if len(passed) >= target_count:
                break
            name = _node_name(node)
            checked += 1
            start = time.perf_counter()
            status_text = ""
            success = False
            try:
                switch = requests.put(controller_url + "/proxies/GLOBAL", json={"name": name}, timeout=1.5)
                if switch.status_code >= 400:
                    status_text = f"switch HTTP {switch.status_code}"
                else:
                    time.sleep(settle_s)
                    response = requests.get(
                        test_url,
                        proxies={"http": proxy_url, "https": proxy_url},
                        timeout=request_timeout,
                        allow_redirects=False,
                        headers={"User-Agent": user_agent},
                    )
                    status_text = f"HTTP {response.status_code}"
                    success = response.status_code in expected
            except Exception as exc:
                status_text = type(exc).__name__ + ": " + str(exc)[:120]

            elapsed = int((time.perf_counter() - start) * 1000)
            node.url_test_ms = elapsed
            node.url_test_status = status_text
            node.url_test_success = success
            row = {
                "name": name,
                "type": getattr(node, "type", ""),
                "network": node_network(node),
                "original_server": getattr(node, "original_server", ""),
                "bug_sni": getattr(node, "bug_sni", ""),
                "handshake_ms": getattr(node, "best_delay_ms", ""),
                "ws_upgrade_ms": getattr(node, "ws_best_delay_ms", ""),
                "url_test_ms": elapsed,
                "url_test_status": status_text,
                "url_test_success": "yes" if success else "no",
            }
            rows.append(row)

            if success:
                node.status = "alive"
                node.reason = (getattr(node, "reason", "") + "; URL test ok").strip("; ")
                passed.append(node)
            else:
                node.status = "dead"
                node.reason = (getattr(node, "reason", "") + "; URL test failed: " + status_text).strip("; ")

        reason = f"URL test passed {len(passed)}/{checked} tested"
        return passed, checked, reason, rows
    finally:
        if proc is not None:
            with suppress(Exception):
                proc.terminate()
            with suppress(Exception):
                proc.wait(timeout=3)
            if proc.poll() is None:
                with suppress(Exception):
                    proc.kill()
        tmpdir_obj.cleanup()


def _build_urltest_report_csv(rows: list[dict[str, Any]]) -> str:
    import csv
    import io
    fields = [
        "name", "type", "network", "original_server", "bug_sni",
        "handshake_ms", "ws_upgrade_ms", "url_test_ms", "url_test_status", "url_test_success",
    ]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buffer.getvalue()


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _ws_opts(node: Any) -> tuple[str, str]:
    clash = getattr(node, "clash", {}) or {}
    ws_opts = clash.get("ws-opts") if isinstance(clash.get("ws-opts"), dict) else {}
    path = str(ws_opts.get("path") or "/") or "/"
    headers = ws_opts.get("headers") if isinstance(ws_opts.get("headers"), dict) else {}
    host = str(headers.get("Host") or getattr(node, "bug_sni", "") or clash.get("servername") or clash.get("sni") or "").strip()
    return path, host


def _singbox_tls(clash: dict[str, Any], node: Any) -> dict[str, Any] | None:
    enabled = bool(clash.get("tls", True)) or str(clash.get("type", "")).lower() in {"vless", "trojan", "vmess"}
    if not enabled:
        return None
    server_name = str(clash.get("servername") or clash.get("sni") or getattr(node, "bug_sni", "") or "").strip()
    if not server_name:
        return None
    fingerprint = str(clash.get("client-fingerprint") or "chrome").strip().lower()
    allowed = {"chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random"}
    if fingerprint in {"randomized", "randomizedalpn"}:
        fingerprint = "random"
    if fingerprint not in allowed:
        fingerprint = "chrome"
    tls = {
        "enabled": True,
        "server_name": server_name,
        "insecure": bool(clash.get("skip-cert-verify", True)),
        "utls": {"enabled": True, "fingerprint": fingerprint},
    }
    alpn = clash.get("alpn")
    if isinstance(alpn, list) and alpn:
        # WebSocket is safest with HTTP/1.1. This avoids h2-first cases that can break WS.
        tls["alpn"] = ["http/1.1"] if node_network(node) == "ws" else [str(x) for x in alpn if str(x).strip()]
    elif node_network(node) == "ws":
        tls["alpn"] = ["http/1.1"]
    return tls


def _singbox_transport(node: Any) -> dict[str, Any] | None:
    network = node_network(node)
    if network != "ws":
        return None
    path, host = _ws_opts(node)
    transport: dict[str, Any] = {"type": "ws", "path": path or "/"}
    if host:
        transport["headers"] = {"Host": host}
    return transport


def _singbox_outbound_from_node(node: Any) -> dict[str, Any] | None:
    clash = getattr(node, "clash", {}) or {}
    proto = str(clash.get("type") or getattr(node, "type", "")).lower()
    server = str(clash.get("server") or TARGET_SERVER).strip()
    port = _as_int(clash.get("port"), ONLY_PORT) or ONLY_PORT
    base: dict[str, Any] = {"type": proto, "tag": "proxy", "server": server, "server_port": port}

    transport = _singbox_transport(node)
    tls = _singbox_tls(clash, node)

    if proto == "vless":
        uuid = str(clash.get("uuid") or "").strip()
        if not uuid:
            return None
        base["uuid"] = uuid
        if clash.get("flow"):
            base["flow"] = str(clash.get("flow"))
    elif proto == "trojan":
        password = str(clash.get("password") or "").strip()
        if not password:
            return None
        base["password"] = password
    elif proto == "vmess":
        uuid = str(clash.get("uuid") or "").strip()
        if not uuid:
            return None
        base["uuid"] = uuid
        # sing-box accepts common VMess security values. Keep it conservative.
        security = str(clash.get("cipher") or "auto").strip().lower() or "auto"
        if security not in {"auto", "none", "zero", "aes-128-gcm", "chacha20-poly1305"}:
            security = "auto"
        base["security"] = security
        if "alterId" in clash:
            base["alter_id"] = _as_int(clash.get("alterId"), 0)
    elif proto == "ss":
        method = str(clash.get("cipher") or "").strip()
        password = str(clash.get("password") or "").strip()
        if not method or not password:
            return None
        base["type"] = "shadowsocks"
        base["method"] = method
        base["password"] = password
    else:
        return None

    if tls and proto in {"vless", "trojan", "vmess"}:
        base["tls"] = tls
    if transport and proto in {"vless", "trojan", "vmess"}:
        base["transport"] = transport
    return base


def _wait_local_port(port: int, timeout_s: float = 8.0) -> bool:
    deadline = time.time() + max(1.0, timeout_s)
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", int(port)), timeout=0.3):
                return True
        except Exception:
            time.sleep(0.15)
    return False


def _singbox_url_test_nodes(
    nodes: list[Any],
    *,
    target_count: int,
    test_url: str,
    timeout_ms: int,
) -> tuple[list[Any], int, str, list[dict[str, Any]]]:
    """Filter automatic nodes with sing-box, as a NekoBox compatibility check.

    NekoBox for Android uses a sing-box based core, so this test is closer to
    NekoBox behavior than only relying on Mihomo/OpenClash. Manual nodes are not
    passed here and remain unfiltered by design.
    """
    target_count = max(1, int(target_count))
    rows: list[dict[str, Any]] = []
    if not nodes:
        return [], 0, "no automatic nodes to NekoBox/sing-box test", rows

    if not _env_bool("REQUIRE_NEKOBOX_TEST", True):
        final_nodes = nodes[:target_count]
        for node in final_nodes:
            node.nekobox_status = "skipped-disabled"
            node.nekobox_ready = True
        return final_nodes, len(final_nodes), "NekoBox/sing-box test disabled", rows

    core_path = os.getenv("SINGBOX_PATH", "./sing-box").strip() or "./sing-box"
    if not Path(core_path).exists():
        raise SystemExit(f"sing-box binary tidak ditemukan di {core_path}; NekoBox test wajib aktif.")

    expected = _expected_statuses()
    passed: list[Any] = []
    checked = 0
    request_timeout = max(1.0, float(timeout_ms) / 1000.0)
    start_timeout = float(os.getenv("SINGBOX_START_TIMEOUT", "8"))
    user_agent = os.getenv("NEKOBOX_TEST_USER_AGENT", "Mozilla/5.0 SumberYAML-NekoBoxTest/1.0")

    for node in nodes:
        if len(passed) >= target_count:
            break
        name = _node_name(node)
        checked += 1
        status_text = ""
        success = False
        elapsed = 0
        outbound = _singbox_outbound_from_node(node)
        if outbound is None:
            status_text = "unsupported for sing-box conversion"
            rows.append({
                "name": name,
                "type": getattr(node, "type", ""),
                "network": node_network(node),
                "original_server": getattr(node, "original_server", ""),
                "bug_sni": getattr(node, "bug_sni", ""),
                "mihomo_status": getattr(node, "url_test_status", ""),
                "nekobox_test_ms": "",
                "nekobox_status": status_text,
                "nekobox_ready": "no",
            })
            continue

        proxy_port = _free_tcp_port()
        tmpdir_obj = tempfile.TemporaryDirectory(prefix="singbox-nekobox-test-")
        tmpdir = Path(tmpdir_obj.name)
        config_path = tmpdir / "config.json"
        config = {
            "log": {"level": os.getenv("SINGBOX_LOG_LEVEL", "error")},
            "inbounds": [
                {
                    "type": "mixed",
                    "tag": "mixed-in",
                    "listen": "127.0.0.1",
                    "listen_port": proxy_port,
                    "sniff": False,
                }
            ],
            "outbounds": [outbound],
        }
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        proc: subprocess.Popen[str] | None = None
        start = time.perf_counter()
        try:
            proc = subprocess.Popen(
                [core_path, "run", "-c", str(config_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            if not _wait_local_port(proxy_port, timeout_s=start_timeout):
                status_text = "sing-box inbound did not start"
            else:
                proxy_url = f"http://127.0.0.1:{proxy_port}"
                response = requests.get(
                    test_url,
                    proxies={"http": proxy_url, "https": proxy_url},
                    timeout=request_timeout,
                    allow_redirects=False,
                    headers={"User-Agent": user_agent},
                )
                status_text = f"HTTP {response.status_code}"
                success = response.status_code in expected
        except Exception as exc:
            status_text = type(exc).__name__ + ": " + str(exc)[:140]
        finally:
            elapsed = int((time.perf_counter() - start) * 1000)
            if proc is not None:
                with suppress(Exception):
                    proc.terminate()
                with suppress(Exception):
                    proc.wait(timeout=2)
                if proc.poll() is None:
                    with suppress(Exception):
                        proc.kill()
            tmpdir_obj.cleanup()

        node.nekobox_test_ms = elapsed
        node.nekobox_status = status_text
        node.nekobox_ready = success
        row = {
            "name": name,
            "type": getattr(node, "type", ""),
            "network": node_network(node),
            "original_server": getattr(node, "original_server", ""),
            "bug_sni": getattr(node, "bug_sni", ""),
            "mihomo_status": getattr(node, "url_test_status", ""),
            "url_test_ms": getattr(node, "url_test_ms", ""),
            "nekobox_test_ms": elapsed,
            "nekobox_status": status_text,
            "nekobox_ready": "yes" if success else "no",
        }
        rows.append(row)
        if success:
            node.status = "alive"
            node.reason = (getattr(node, "reason", "") + "; NekoBox/sing-box ok").strip("; ")
            passed.append(node)
        else:
            node.status = "dead"
            node.reason = (getattr(node, "reason", "") + "; NekoBox/sing-box failed: " + status_text).strip("; ")

    reason = f"NekoBox/sing-box passed {len(passed)}/{checked} tested"
    return passed, checked, reason, rows


def _build_nekobox_report_csv(rows: list[dict[str, Any]]) -> str:
    import csv
    import io
    fields = [
        "name", "type", "network", "original_server", "bug_sni",
        "mihomo_status", "url_test_ms", "nekobox_test_ms", "nekobox_status", "nekobox_ready",
    ]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buffer.getvalue()


def build_links_text() -> str:
    links = list(DEFAULT_LINKS)
    extra_file = os.getenv("SUBSCRIPTION_LINKS_FILE", "subscription_links.txt")
    extra_text = _read_text_file(extra_file)
    extra_env = os.getenv("EXTRA_SUBSCRIPTION_LINKS", "")
    for source in (extra_text, extra_env):
        for line in source.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    unique: list[str] = []
    seen: set[str] = set()
    for link in links:
        if link not in seen:
            seen.add(link)
            unique.append(link)
    return "\n".join(unique)



def normalize_manual_uri_server(raw: str, target_server: str = TARGET_SERVER) -> str:
    """Return manual URI with its outbound server changed to the bug server.

    This is intentionally done before manual nodes are parsed, so manual_nodes.txt
    itself can be normalized and committed by GitHub Actions. SNI/Host/path and
    credentials are preserved; only the connect server and port are changed to
    104.17.3.81:443.
    """
    raw = str(raw or "").strip()
    if not raw or "://" not in raw:
        return raw
    scheme = raw.split("://", 1)[0].lower()
    try:
        if scheme == "vmess":
            payload = raw.split("://", 1)[1].split("#", 1)[0]
            decoded = b64decode_text(payload)
            if not decoded:
                return raw
            data = json.loads(decoded)
            data["add"] = str(target_server)
            if "server" in data:
                data["server"] = str(target_server)
            data["port"] = str(ONLY_PORT)
            encoded = base64.b64encode(
                json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).decode("ascii")
            return "vmess://" + encoded

        body, hash_sep, fragment = raw.partition("#")
        parsed = urlparse(body)
        if not parsed.netloc:
            return raw
        if "@" in parsed.netloc:
            userinfo, _serverpart = parsed.netloc.rsplit("@", 1)
            netloc = f"{userinfo}@{target_server}:{ONLY_PORT}"
        else:
            # Do not rewrite fully base64 ss:// payloads because changing the
            # server safely requires decoding all cipher/password forms.
            if scheme == "ss":
                return raw
            netloc = f"{target_server}:{ONLY_PORT}"
        new_body = urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, ""))
        return new_body + (("#" + fragment) if hash_sep else "")
    except Exception:
        return raw


def normalize_manual_nodes_text(manual_text: str) -> tuple[str, int]:
    """Normalize every supported URI in manual_nodes.txt to TARGET_SERVER:443.

    Comments and blank lines are preserved when a line only contains comments or
    text. URI lines are rewritten as one URI per line to avoid leaving stale
    original servers in the repository.
    """
    out: list[str] = []
    changed = 0
    for line in (manual_text or "").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out.append(line)
            continue
        uris = extract_uris(line)
        if not uris:
            out.append(line)
            continue
        for uri in uris:
            fixed = normalize_manual_uri_server(uri)
            if fixed != uri:
                changed += 1
            out.append(fixed)
    return "\n".join(out) + ("\n" if out else ""), changed


def _unique_manual_names(nodes: list[Any]) -> None:
    """Keep manual node names from source and only add MANUAL prefix.

    Example:
      source fragment: Singapore-VIP
      YAML name      : MANUAL-Singapore-VIP

    Manual nodes are intentionally not strict-filtered or tested. This function
    only ensures the final YAML proxy names stay unique, because OpenClash/Mihomo
    requires every proxy name to be unique and proxy-groups must reference the
    exact same names.
    """
    seen: set[str] = set()
    for i, node in enumerate(nodes, start=1):
        source_name = normalize_name(node.name, f"NODE-{i:03d}")
        node.original_name = node.original_name or source_name

        # Keep the user's/source fragment as much as possible. Only add MANUAL-
        # in front. Do not convert to provider/ASN naming for manual nodes.
        base_raw = f"MANUAL-{source_name}"
        base = normalize_name(base_raw, f"MANUAL-NODE-{i:03d}")
        base = base[:96].strip(" -_|/") or f"MANUAL-NODE-{i:03d}"

        name = base
        counter = 2
        while name in seen:
            suffix = f"-{counter}"
            name = (base[: 96 - len(suffix)] + suffix).strip(" -_|/")
            counter += 1

        seen.add(name)
        node.name = name
        node.clash["name"] = name
        node.status = "manual-unfiltered"
        node.tier = "MANUAL"
        node.reason = "manual_nodes.txt: added without strict filtering/testing; name kept from source with MANUAL prefix"

def parse_manual_nodes_unscreened(manual_text: str) -> tuple[list[Any], list[str]]:
    """Parse manual_nodes.txt and do not run strict SNI/WS filtering on it.

    This still requires the URI to be syntactically supported by the parser
    (vless/vmess/trojan/ss and the app's bug-server format), but it does not run
    the automatic subscription filters, WS strict test, timeout test, SNI strict
    selection, jitter filter, or quota limit.
    """
    nodes: list[Any] = []
    skipped: list[str] = []
    seen_keys: set[str] = set()
    for uri in extract_uris(manual_text or ""):
        node = parse_uri(uri, "manual_nodes.txt")
        if not node:
            skipped.append(uri[:180])
            continue
        # Do not filter strict. Only dedupe exact same parsed account so repeated
        # copy-paste lines do not break YAML with duplicates.
        key = node.key or uri
        if key in seen_keys:
            continue
        seen_keys.add(key)
        nodes.append(node)
    _unique_manual_names(nodes)
    return nodes, skipped


def _insert_once(values: list[str], item: str, index: int | None = None) -> None:
    if item in values:
        return
    if index is None or index < 0 or index > len(values):
        values.append(item)
    else:
        values.insert(index, item)


def add_manual_group_to_config(config: dict[str, Any], manual_nodes: list[Any], *, android: bool = False) -> dict[str, Any]:
    if not manual_nodes:
        return config

    manual_names = [str(node.clash.get("name") or node.name) for node in manual_nodes if node.clash.get("name")]
    if not manual_names:
        return config

    proxies = config.setdefault("proxies", [])
    existing_proxy_names = {str(p.get("name")) for p in proxies if isinstance(p, dict)}
    for node in manual_nodes:
        clash = node.clash
        name = str(clash.get("name") or "")
        if name and name not in existing_proxy_names:
            proxies.append(clash)
            existing_proxy_names.add(name)

    groups = config.setdefault("proxy-groups", [])
    # Remove previous manual helper groups when regenerating from an existing config.
    groups[:] = [
        g
        for g in groups
        if not (isinstance(g, dict) and g.get("name") in {"MANUAL", "MANUAL-WARMUP"})
    ]

    manual_group = {
        "name": "MANUAL",
        "type": "fallback",
        "proxies": manual_names or ["AUTO-FAST"],
        "url": "https://www.gstatic.com/generate_204",
        "interval": 30,
        "lazy": False,
        "timeout": 3000,
        "expected-status": "200/204/301/302",
        "max-failed-times": 2,
    }

    # Manual nodes remain outside the automatic quota. Smart mode keeps strict
    # automatic nodes first in FALLBACK, then appends manual nodes as late-stage
    # backup. This prevents untested/manual nodes from delaying the first usable route.
    for group in groups:
        if not isinstance(group, dict):
            continue
        name = str(group.get("name") or "")
        proxies_list = group.get("proxies")
        if not isinstance(proxies_list, list):
            continue
        if name == "FALLBACK":
            # Append individual manual nodes after strict automatic nodes. They are
            # still directly health-checked, but no longer delay the first fallback pick.
            for manual_name in manual_names:
                _insert_once(proxies_list, manual_name)
        elif name == "GLOBAL":
            # Keep MANUAL visible in the main selector too.
            if "DIRECT" in proxies_list:
                _insert_once(proxies_list, "MANUAL", proxies_list.index("DIRECT"))
            elif "FALLBACK" in proxies_list:
                _insert_once(proxies_list, "MANUAL", proxies_list.index("FALLBACK") + 1)
            else:
                _insert_once(proxies_list, "MANUAL", 0)
        elif (not android) and name == "PROXY":
            if "DIRECT" in proxies_list:
                _insert_once(proxies_list, "MANUAL", proxies_list.index("DIRECT"))
            else:
                _insert_once(proxies_list, "MANUAL", 1)

    groups.append(manual_group)
    return config


def add_manual_group_to_yaml_text(yaml_text: str, manual_nodes: list[Any], *, android: bool = False) -> str:
    if not manual_nodes:
        return yaml_text
    config = yaml.safe_load(yaml_text) or {}
    if not isinstance(config, dict):
        return yaml_text
    config = add_manual_group_to_config(config, manual_nodes, android=android)
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140)




# -----------------------------
# Manual unblock domain routing
# -----------------------------
def _strip_inline_comment(line: str) -> str:
    """Strip comments in simple txt lists without damaging URL fragments too much."""
    text = str(line or "").strip()
    if not text:
        return ""
    for marker in (" //", "\t//"):
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    # Treat # as a comment when it starts a line or is preceded by whitespace.
    if text.startswith("#"):
        return ""
    match = re.search(r"\s+#", text)
    if match:
        text = text[: match.start()].strip()
    return text.strip()


def _domain_from_manual_line(line: str) -> tuple[str, str] | None:
    """Convert one manual_unblock_domains.txt line into a Clash rule tuple.

    Supported active line formats:
      example.com
      *.example.com
      +.example.com
      https://example.com/path
      DOMAIN,example.com
      DOMAIN-SUFFIX,example.com
      DOMAIN-KEYWORD,keyword
      GEOSITE,category
    The target policy is always injected later as MANUAL.
    """
    text = _strip_inline_comment(line)
    if not text:
        return None
    text = text.strip().strip('"\'')
    if not text:
        return None

    upper = text.upper()
    if "," in text:
        parts = [p.strip() for p in text.split(",") if p.strip()]
        if len(parts) >= 2:
            kind = parts[0].upper()
            value = parts[1].strip().strip('"\'')
            if kind in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "GEOSITE"} and value:
                return kind, value.lower() if kind != "DOMAIN-KEYWORD" else value

    # Remove URL scheme/path/query if a full URL is pasted.
    if "://" in text:
        parsed = urlparse(text)
        text = parsed.hostname or parsed.netloc or text
    else:
        text = text.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]

    text = text.strip().strip(".").lower()
    for prefix in ("+.", "*.", "."):
        if text.startswith(prefix):
            text = text[len(prefix):].strip(".")
            break
    if not text or " " in text or ":" in text:
        return None
    if "*" in text:
        return None
    if looks_like_ip(text):
        return "IP-CIDR", f"{text}/32"
    if re.fullmatch(r"[a-z0-9][a-z0-9.-]*\.[a-z]{2,}", text):
        return "DOMAIN-SUFFIX", text
    return None


def _read_manual_unblock_domains_file() -> list[str]:
    path = os.getenv("MANUAL_UNBLOCK_DOMAINS_FILE", "manual_unblock_domains.txt").strip() or "manual_unblock_domains.txt"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.readlines()
    except FileNotFoundError:
        return []
    except Exception:
        return []


def _manual_unblock_domain_rules(target: str = "MANUAL") -> list[str]:
    """Build high-priority rules so listed domains always use the MANUAL group."""
    target = str(target or "MANUAL").strip() or "MANUAL"
    rules: list[str] = []
    seen: set[str] = set()
    for raw_line in _read_manual_unblock_domains_file():
        item = _domain_from_manual_line(raw_line)
        if not item:
            continue
        kind, value = item
        if kind == "IP-CIDR":
            rule = f"IP-CIDR,{value},{target},no-resolve"
        else:
            rule = f"{kind},{value},{target}"
        if rule not in seen:
            seen.add(rule)
            rules.append(rule)
    return rules


def _inject_manual_unblock_rules(rules: list[str], target: str = "MANUAL") -> list[str]:
    """Insert manual-unblock rules after LAN/DIRECT rules and before reject/category rules."""
    manual_rules = _manual_unblock_domain_rules(target=target)
    if not manual_rules:
        return rules

    out: list[str] = []
    seen: set[str] = set()
    for rule in rules:
        if rule not in seen:
            seen.add(rule)
            out.append(rule)

    # Remove older generated manual rules if this function is called repeatedly.
    out = [r for r in out if r not in manual_rules]

    insert_at = 0
    for idx, rule in enumerate(out):
        text = str(rule)
        if (
            ",DIRECT" in text
            or text.startswith("GEOIP,LAN,")
            or text.startswith("IP-CIDR,127.")
            or text.startswith("IP-CIDR,10.")
            or text.startswith("IP-CIDR,172.16.")
            or text.startswith("IP-CIDR,192.168.")
            or text.startswith("IP-CIDR,169.254.")
        ):
            insert_at = idx + 1
            continue
        break
    return out[:insert_at] + manual_rules + out[insert_at:]

def _delay_from_name(name: str) -> int:
    import re
    m = re.search(r"(\d+)MS\b", str(name).upper())
    return int(m.group(1)) if m else 999999


def _dedupe_values(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out




def _enforce_no_selector_no_direct_yaml_text(yaml_text: str) -> str:
    """Convert selector groups to automatic fallback groups and remove DIRECT from proxy-groups."""
    try:
        config = yaml.safe_load(yaml_text) or {}
    except Exception:
        return yaml_text
    if not isinstance(config, dict):
        return yaml_text
    groups = config.get("proxy-groups")
    if not isinstance(groups, list):
        return yaml_text
    proxy_names = [str(p.get("name")) for p in config.get("proxies", []) if isinstance(p, dict) and p.get("name")]
    group_names = [str(g.get("name")) for g in groups if isinstance(g, dict) and g.get("name")]
    defaults = ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "STREAMING-FAST", "FALLBACK", "LOAD-BALANCE", "PING-CHECK"]

    def dedupe(values: list[str]) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        for value in values:
            if value and value not in seen:
                seen.add(value)
                out.append(value)
        return out

    for group in groups:
        if not isinstance(group, dict):
            continue
        name = str(group.get("name") or "")
        if str(group.get("type") or "").lower() == "select":
            group["type"] = "fallback"
            group.setdefault("url", "https://www.gstatic.com/generate_204")
            group.setdefault("interval", 30 if name == "GLOBAL" else 60)
            group.setdefault("lazy", name != "GLOBAL")
            group.setdefault("timeout", 2500)
            group.setdefault("expected-status", "200/204/301/302")
            group.setdefault("max-failed-times", 2)
        if isinstance(group.get("proxies"), list):
            refs = []
            for ref in group.get("proxies") or []:
                text = str(ref).strip()
                if not text or text == "DIRECT" or text == name:
                    continue
                refs.append(text)
            refs = dedupe(refs)
            if not refs:
                refs = dedupe([x for x in defaults if x in group_names and x != name] + [x for x in proxy_names if x != name]) or ["REJECT"]
            group["proxies"] = refs
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140)



def _ensure_ping_check_group_yaml_text(yaml_text: str) -> str:
    """Add a lazy=false url-test group that probes every node so OpenClash shows delay/ping.

    This group is not meant as the main traffic route. It is a health-probe group
    so freshly generated accounts get checked by Mihomo/OpenClash immediately
    after import/reload, instead of staying grey/no-ping in the UI.
    """
    try:
        config = yaml.safe_load(yaml_text) or {}
    except Exception:
        return yaml_text
    if not isinstance(config, dict):
        return yaml_text
    proxies = [p for p in config.get("proxies", []) if isinstance(p, dict) and p.get("name")]
    proxy_names = _dedupe_values([str(p.get("name")) for p in proxies])
    if not proxy_names:
        return yaml_text
    groups = config.setdefault("proxy-groups", [])
    if not isinstance(groups, list):
        config["proxy-groups"] = groups = []
    existing = {str(g.get("name")): g for g in groups if isinstance(g, dict)}
    ping_group = {
        "name": "PING-CHECK",
        "type": "url-test",
        "proxies": proxy_names,
        "url": os.getenv("PING_CHECK_URL", os.getenv("TEST_URL", "https://www.gstatic.com/generate_204")),
        "interval": max(120, _env_int("PING_CHECK_INTERVAL", 180)),
        "tolerance": _env_int("PING_CHECK_TOLERANCE", 100),
        "lazy": False,
        "timeout": _env_int("PING_CHECK_TIMEOUT_MS", 4000),
        "expected-status": "200/204/301/302",
        "max-failed-times": 2,
    }
    if "PING-CHECK" in existing:
        existing["PING-CHECK"].update(ping_group)
    else:
        # Let OpenClash display the probe group near other automatic health groups.
        insert_at = 0
        for i, g in enumerate(groups):
            if isinstance(g, dict) and str(g.get("name")) in ("WARM-UP", "AUTO-FAST", "FALLBACK"):
                insert_at = i
                break
        groups.insert(insert_at, ping_group)
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140)

def _group_map(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(g.get("name")): g for g in config.get("proxy-groups", []) if isinstance(g, dict)}


def _build_lite_yaml_from_text(yaml_text: str) -> str:
    """Build a lightweight router config from the smart full YAML."""
    config = yaml.safe_load(yaml_text) or {}
    if not isinstance(config, dict):
        return yaml_text
    groups = _group_map(config)
    keep_group_names = ["GLOBAL", "PROXY", "WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK", "MANUAL"]
    proxies = [p for p in config.get("proxies", []) if isinstance(p, dict)]
    proxy_names = [str(p.get("name")) for p in proxies if p.get("name")]
    # Hanya group yang benar-benar dipertahankan di profile Lite boleh menjadi target.
    # Sebelumnya semua group dari profile full dimasukkan ke refs_available, sehingga
    # GLOBAL/PROXY masih menunjuk ke SOCIAL-MEDIA, YOUTUBE, STREAMING, dll. setelah
    # group-group tersebut dihapus dari openclash_lite.yaml.
    kept_group_names = {name for name in keep_group_names if name in groups}
    refs_available = set(proxy_names) | kept_group_names | {"DIRECT", "REJECT", "REJECT-DROP", "PASS", "COMPATIBLE"}

    lite_groups: list[dict[str, Any]] = []
    for name in keep_group_names:
        g = groups.get(name)
        if not g:
            continue
        new_g = dict(g)
        gtype = str(new_g.get("type") or "")
        refs = [str(x) for x in (new_g.get("proxies") or []) if str(x) in refs_available]
        if name == "GLOBAL":
            # GLOBAL selector intentionally has no DIRECT. Local/LAN traffic still goes DIRECT via rules.
            preferred = ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK", "MANUAL"]
            refs = _dedupe_values([x for x in preferred if x in refs_available] + [x for x in refs if x in refs_available and x != "DIRECT"])
        elif name == "PROXY":
            preferred = ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK", "MANUAL"]
            refs = _dedupe_values([x for x in preferred if x in refs_available] + [x for x in refs if x in refs_available])
        elif name == "WARM-UP":
            refs = refs[:5]
            new_g["interval"] = max(20, int(new_g.get("interval") or 20))
            new_g["timeout"] = min(int(new_g.get("timeout") or 3000), 3000)
        elif name == "WARM-UP-CF":
            refs = refs[:5]
            new_g["interval"] = max(25, int(new_g.get("interval") or 25))
            new_g["timeout"] = min(int(new_g.get("timeout") or 3000), 3000)
        elif name == "AUTO-FAST":
            refs = refs[:8]
            new_g["interval"] = max(45, int(new_g.get("interval") or 45))
            new_g["timeout"] = min(int(new_g.get("timeout") or 3000), 3000)
        elif name == "FALLBACK":
            new_g["interval"] = max(90, int(new_g.get("interval") or 90))
            new_g["timeout"] = max(4000, int(new_g.get("timeout") or 5000))
        if gtype in {"url-test", "fallback", "load-balance"} and not refs:
            refs = ["REJECT"]
        new_g["proxies"] = refs
        lite_groups.append(new_g)

    config["proxy-groups"] = lite_groups
    config.pop("rule-providers", None)
    config["rules"] = _inject_manual_unblock_rules([
        "DOMAIN-SUFFIX,local,DIRECT",
        "DOMAIN-SUFFIX,lan,DIRECT",
        "IP-CIDR,127.0.0.0/8,DIRECT,no-resolve",
        "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
        "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve",
        "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
        "MATCH,GLOBAL",
    ], target="MANUAL")
    config["log-level"] = "warning"
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140)


def _prune_missing_proxy_group_refs_yaml_text(yaml_text: str) -> str:
    """Remove dangling proxy-group references after profile transformations.

    This is intentionally run near final validation. It protects Lite and other
    generated profiles when a transform removes a group but another group still
    carries the old name in its `proxies` list.
    """
    config = yaml.safe_load(yaml_text) or {}
    if not isinstance(config, dict):
        return yaml_text

    proxies = [p for p in config.get("proxies", []) if isinstance(p, dict)]
    groups = [g for g in config.get("proxy-groups", []) if isinstance(g, dict)]
    proxy_names = {str(p.get("name")).strip() for p in proxies if str(p.get("name", "")).strip()}
    group_names = {str(g.get("name")).strip() for g in groups if str(g.get("name", "")).strip()}
    builtins = {"DIRECT", "REJECT", "REJECT-DROP", "PASS", "COMPATIBLE"}
    known = proxy_names | group_names | builtins

    for group in groups:
        refs = group.get("proxies")
        if not isinstance(refs, list):
            continue
        cleaned = _dedupe_values([
            str(ref).strip()
            for ref in refs
            if str(ref).strip() and str(ref).strip() in known
        ])

        gtype = str(group.get("type") or "").strip().lower()
        if not cleaned and not group.get("use"):
            # Keep the generated YAML structurally valid even if every old
            # reference was removed. Health groups cannot be left empty.
            if proxy_names:
                cleaned = [sorted(proxy_names)[0]]
            elif gtype == "select":
                cleaned = ["DIRECT"]
            else:
                cleaned = ["REJECT"]
        group["proxies"] = cleaned

    config["proxy-groups"] = groups
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=140)


def _build_node_quality_report(yaml_text: str, urltest_rows: list[dict[str, Any]], nekobox_rows: list[dict[str, Any]]) -> str:
    config = yaml.safe_load(yaml_text) or {}
    groups = _group_map(config if isinstance(config, dict) else {})
    url_map = {str(row.get("name")): row for row in urltest_rows}
    neko_map = {str(row.get("name")): row for row in nekobox_rows}

    proxy_names = [str(p.get("name")) for p in config.get("proxies", []) if isinstance(p, dict) and p.get("name")] if isinstance(config, dict) else []
    warmup = groups.get("WARM-UP", {}).get("proxies", []) or []
    warmup_cf = groups.get("WARM-UP-CF", {}).get("proxies", []) or []
    streaming = groups.get("STREAMING-FAST", {}).get("proxies", []) or []
    auto_fast = groups.get("AUTO-FAST", {}).get("proxies", []) or []
    fallback = groups.get("FALLBACK", {}).get("proxies", []) or []

    def metric(name: str) -> tuple[int, int, str]:
        u = url_map.get(name, {})
        n = neko_map.get(name, {})
        return _as_int(n.get("nekobox_test_ms"), 999999), _as_int(u.get("url_test_ms"), 999999), str(n.get("nekobox_ready") or "")

    ranked = sorted(proxy_names, key=lambda x: (_delay_from_name(x), metric(x)[0], metric(x)[1]))
    hot = [x for x in ranked if x in warmup]
    cf = [x for x in ranked if x in warmup_cf]
    stream = [x for x in ranked if x in streaming]
    manual = [x for x in fallback if str(x).startswith("MANUAL-")]
    risky = [name for name, row in neko_map.items() if str(row.get("nekobox_ready")) != "yes"]

    lines = [
        "# Node Quality Report - Smart Stable",
        "",
        "## Ringkasan",
        f"- Total proxy di YAML: {len(proxy_names)}",
        f"- WARM-UP harian: {len(warmup)} node",
        f"- WARM-UP-CF Cloudflare/Worker: {len(warmup_cf)} node",
        f"- STREAMING-FAST: {len(streaming)} node",
        f"- AUTO-FAST: {len(auto_fast)} node",
        f"- FALLBACK: {len(fallback)} referensi, manual backup: {len(manual)} node",
        "",
        "## Rekomendasi Pakai",
        "- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.",
        "- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.",
        "- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.",
        "- Router RAM kecil: pakai `openclash_lite.yaml`.",
        "",
        "## Tier 1 - WARM-UP",
    ]
    lines += [f"- {name}" for name in hot] or ["- Tidak ada"]
    lines += ["", "## Tier 1B - WARM-UP-CF"]
    lines += [f"- {name}" for name in cf] or ["- Tidak ada"]
    lines += ["", "## Streaming Pool"]
    lines += [f"- {name}" for name in stream] or ["- Tidak ada"]
    lines += ["", "## Node Berisiko dari NekoBox/sing-box Test"]
    lines += [f"- {name}: {neko_map[name].get('nekobox_status', '')}" for name in risky[:30]] or ["- Tidak ada yang gagal pada laporan terakhir"]
    lines += ["", "## Catatan Smart Mode", "- Health-check cepat hanya untuk pool kecil, bukan semua node.", "- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.", "- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan."]
    return "\n".join(lines) + "\n"


def _node_names_from_yaml_text(yaml_text: str) -> list[str]:
    try:
        config = yaml.safe_load(yaml_text) or {}
    except Exception:
        return []
    if not isinstance(config, dict):
        return []
    return [str(p.get("name")) for p in config.get("proxies", []) if isinstance(p, dict) and p.get("name")]


def _build_fresh_pool_report(
    fresh_nodes: list[Any],
    strict_nodes: list[Any],
    urltest_rows: list[dict[str, Any]],
    nekobox_rows: list[dict[str, Any]],
    fresh_yaml_text: str,
) -> str:
    url_map = {str(r.get("name") or ""): r for r in urltest_rows}
    neko_map = {str(r.get("name") or ""): r for r in nekobox_rows}
    fresh_names = [str(getattr(n, "name", "") or "") for n in fresh_nodes]
    strict_names = [str(getattr(n, "name", "") or "") for n in strict_nodes]
    yaml_names = _node_names_from_yaml_text(fresh_yaml_text)

    def row_for(name: str) -> tuple[str, str, str]:
        u = url_map.get(name, {})
        n = neko_map.get(name, {})
        url_ms = str(u.get("url_test_ms") or u.get("delay_ms") or "")
        neko_ms = str(n.get("nekobox_test_ms") or "")
        status = str(n.get("nekobox_ready") or u.get("url_test_status") or u.get("status") or "")
        return url_ms, neko_ms, status

    lines = [
        "# Fresh Candidate Pool",
        "",
        "File ini dibuat otomatis oleh GitHub Actions setelah node diuji.",
        "Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.",
        "",
        "## Output Fresh Pool",
        "- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.",
        "- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.",
        "- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.",
        "- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.",
        "",
        "## Ringkasan",
        f"- Kandidat fresh URL-tested: {len(fresh_names)}",
        f"- Kandidat strict NekoBox-tested: {len(strict_names)}",
        f"- Proxy di openclash_fresh_pool.yaml: {len(yaml_names)}",
        "",
        "## Cara Pakai di OpenWrt",
        "Jalankan manual saat node mulai mati:",
        "",
        "```sh",
        "sh /etc/mihomo-autopilot/openwrt_pull_fresh_pool.sh",
        "```",
        "",
        "Atau aktifkan guard otomatis:",
        "",
        "```sh",
        "sh /etc/mihomo-autopilot/openwrt_fresh_guard.sh",
        "```",
        "",
        "## Kandidat Fresh Teratas",
    ]
    for idx, name in enumerate(fresh_names[:30], start=1):
        url_ms, neko_ms, status = row_for(name)
        extra = []
        if url_ms:
            extra.append(f"url={url_ms}ms")
        if neko_ms:
            extra.append(f"nekobox={neko_ms}ms")
        if status:
            extra.append(f"status={status}")
        suffix = f" ({', '.join(extra)})" if extra else ""
        lines.append(f"{idx}. `{name}`{suffix}")
    if not fresh_names:
        lines.append("- Tidak ada kandidat fresh pada run terakhir.")

    lines += [
        "",
        "## Catatan",
        "Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.",
        "Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.",
    ]
    return "\n".join(lines) + "\n"


def _build_fresh_pool_json(fresh_nodes: list[Any], strict_nodes: list[Any], urltest_rows: list[dict[str, Any]], nekobox_rows: list[dict[str, Any]]) -> str:
    url_map = {str(r.get("name") or ""): r for r in urltest_rows}
    neko_map = {str(r.get("name") or ""): r for r in nekobox_rows}

    def item(node: Any) -> dict[str, Any]:
        name = str(getattr(node, "name", "") or "")
        u = url_map.get(name, {})
        n = neko_map.get(name, {})
        return {
            "name": name,
            "type": str(getattr(node, "type", "") or ""),
            "network": str(getattr(node, "network", "") or ""),
            "server": str(getattr(node, "server", "") or ""),
            "port": int(getattr(node, "port", 0) or 0),
            "url_test_ms": u.get("url_test_ms") or u.get("delay_ms"),
            "url_test_status": u.get("url_test_status") or u.get("status"),
            "nekobox_test_ms": n.get("nekobox_test_ms"),
            "nekobox_ready": n.get("nekobox_ready"),
        }

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fresh_count": len(fresh_nodes),
        "strict_count": len(strict_nodes),
        "fresh": [item(n) for n in fresh_nodes],
        "strict": [item(n) for n in strict_nodes],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    target_core_path = _require_target_core()
    output_yaml = os.getenv("OUTPUT_YAML", "openclash_auto.yaml")
    output_csv = os.getenv("OUTPUT_CSV", "openclash_auto_report.csv")
    output_akun = os.getenv("OUTPUT_AKUN", "akun.txt")
    output_manual_akun = os.getenv("OUTPUT_MANUAL_AKUN", "akun_manual.txt")
    output_manual_skipped = os.getenv("OUTPUT_MANUAL_SKIPPED", "manual_nodes_skipped.txt")
    output_urltest_report = os.getenv("OUTPUT_URLTEST_REPORT", "urltest_report.csv")
    output_nekobox_report = os.getenv("OUTPUT_NEKOBOX_REPORT", "nekobox_test_report.csv")
    output_openclash_compat_report = os.getenv("OUTPUT_OPENCLASH_COMPAT_REPORT", "openclash_compat_report.csv")
    output_android_yaml = os.getenv("OUTPUT_ANDROID_YAML", "openclash_android.yaml")
    output_lite_yaml = os.getenv("OUTPUT_LITE_YAML", "openclash_lite.yaml")
    output_node_quality_report = os.getenv("OUTPUT_NODE_QUALITY_REPORT", "node_quality_report.md")
    output_fresh_yaml = os.getenv("OUTPUT_FRESH_YAML", "openclash_fresh_pool.yaml")
    output_fresh_dir = os.getenv("OUTPUT_FRESH_DIR", "fresh_pool")
    output_stamp = os.getenv("OUTPUT_STAMP", "last_update.txt")
    manual_file = os.getenv("MANUAL_NODES_FILE", "manual_nodes.txt")

    max_nodes = max(1, _env_int("MAX_NODES", 10))
    min_output_nodes = max(1, _env_int("MIN_OUTPUT_NODES", 10))
    fetch_timeout = max(1, _env_int("FETCH_TIMEOUT", 12))
    tcp_timeout = max(0.1, _env_float("TCP_TIMEOUT", 2.0))
    max_workers = max(1, _env_int("MAX_WORKERS", 64))
    attempts = max(1, _env_int("ATTEMPTS", 2))
    require_successes = min(max(1, _env_int("REQUIRE_SUCCESSES", 1)), attempts)

    links_text = build_links_text()
    manual_text = _read_text_file(manual_file)
    manual_text, manual_server_changes = normalize_manual_nodes_text(manual_text)
    if manual_text:
        # GitHub Actions will commit this normalized manual_nodes.txt, so future
        # runs no longer contain original servers.
        Path(manual_file).write_text(manual_text, encoding="utf-8")
    manual_nodes, manual_skipped = parse_manual_nodes_unscreened(manual_text)
    manual_nodes, manual_compat_rows = _mihomo_openclash_compatibility_filter(manual_nodes, label="manual")

    print("[INFO] Generate YAML OpenClash otomatis")
    print(f"[INFO] Target output otomatis: {max_nodes} node, minimal: {min_output_nodes} node")
    print(f"[INFO] Links subscription: {len([x for x in links_text.splitlines() if x.strip()])}")
    print(f"[INFO] Manual nodes parsed: {len(manual_nodes)}; skipped: {len(manual_skipped)}")
    print(f"[INFO] Manual node server normalized to {TARGET_SERVER}:{ONLY_PORT}: {manual_server_changes} link")

    # Important: manual_text is intentionally NOT passed into process_sources.
    # Manual nodes must not be strict-filtered and must not reduce the automatic quota.
    # We first collect a small strict WS pool, then run a real URL test through Mihomo
    # and stop as soon as MAX_NODES alive nodes are found.
    compat_pool_multiplier = max(1, _env_int("OPENCLASH_COMPAT_POOL_MULTIPLIER", 4))
    urltest_pool_nodes = max(max_nodes * compat_pool_multiplier, _env_int("URLTEST_POOL_NODES", max(30, max_nodes * 3)))
    print(f"[INFO] Pool kandidat sebelum URL test: {urltest_pool_nodes} node")
    auto_pool_nodes, all_nodes, fetch_logs, skipped = process_sources(
        links_text=links_text,
        manual_text="",
        fetch_timeout=fetch_timeout,
        tcp_timeout=tcp_timeout,
        max_workers=max_workers,
        max_nodes=urltest_pool_nodes,
        fast_target_ms=_env_int("FAST_TARGET_MS", 123),
        fill_delay_ms=_env_int("FILL_DELAY_MS", 1200),
        min_output_nodes=min_output_nodes,
        attempts=attempts,
        require_successes=require_successes,
        require_original=_env_bool("REQUIRE_ORIGINAL", False),
        candidate_multiplier=_env_int("CANDIDATE_MULTIPLIER", 35),
        candidate_min=_env_int("CANDIDATE_MIN", 350),
        max_jitter_ms=_env_int("MAX_JITTER_MS", 0),
        prefer_ws=_env_bool("PREFER_WS", True),
        require_ws_upgrade=_env_bool("REQUIRE_WS_UPGRADE", True),
        force_ws_only=_env_bool("FORCE_WS_ONLY", True),
        reserve_pool_nodes=_env_int("RESERVE_POOL_NODES", urltest_pool_nodes),
        early_stop_good_nodes=_env_bool("EARLY_STOP_GOOD_NODES", True),
        test_batch_size=_env_int("TEST_BATCH_SIZE", 80),
    )

    auto_pool_nodes, auto_compat_rows = _mihomo_openclash_compatibility_filter(auto_pool_nodes, label="automatic")
    nekobox_pool_nodes = max(max_nodes, _env_int("NEKOBOX_POOL_NODES", max(20, max_nodes * 3)))
    mihomo_pass_nodes, urltest_checked_count, urltest_reason, urltest_rows = _mihomo_url_test_nodes(
        auto_pool_nodes,
        target_count=nekobox_pool_nodes,
        test_url=os.getenv("URL_TEST_URL", os.getenv("TEST_URL", ALT_TEST_URL)),
        timeout_ms=_env_int("URL_TEST_TIMEOUT_MS", _env_int("HEALTH_TIMEOUT_MS", 5000)),
    )
    print(f"[INFO] URL test Mihomo otomatis: {urltest_reason}")

    alive_nodes, nekobox_checked_count, nekobox_reason, nekobox_rows = _singbox_url_test_nodes(
        mihomo_pass_nodes,
        target_count=max_nodes,
        test_url=os.getenv("NEKOBOX_TEST_URL", os.getenv("URL_TEST_URL", os.getenv("TEST_URL", ALT_TEST_URL))),
        timeout_ms=_env_int("NEKOBOX_TEST_TIMEOUT_MS", _env_int("URL_TEST_TIMEOUT_MS", _env_int("HEALTH_TIMEOUT_MS", 5000))),
    )
    unique_names(alive_nodes)
    print(f"[INFO] NekoBox/sing-box test otomatis: {nekobox_reason}")

    yaml_text = build_openclash_yaml(
        alive_nodes,
        interval=_env_int("URLTEST_INTERVAL", 30),
        tolerance=_env_int("TOLERANCE", 40),
        test_url=os.getenv("TEST_URL", ALT_TEST_URL),
        health_timeout=_env_int("HEALTH_TIMEOUT_MS", 5000),
        rule_mode=os.getenv("RULE_MODE", "Lite"),
    )
    yaml_text = add_manual_group_to_yaml_text(yaml_text, manual_nodes, android=False)
    yaml_text = _enforce_no_selector_no_direct_yaml_text(yaml_text)
    yaml_text = _ensure_ping_check_group_yaml_text(yaml_text)

    android_yaml_text = build_openclash_android_yaml(
        alive_nodes,
        interval=_env_int("ANDROID_URLTEST_INTERVAL", _env_int("URLTEST_INTERVAL", 30)),
        tolerance=_env_int("ANDROID_TOLERANCE", _env_int("TOLERANCE", 40)),
        test_url=os.getenv("ANDROID_TEST_URL", os.getenv("TEST_URL", ALT_TEST_URL)),
        health_timeout=_env_int("ANDROID_HEALTH_TIMEOUT_MS", _env_int("HEALTH_TIMEOUT_MS", 5000)),
    )
    android_yaml_text = add_manual_group_to_yaml_text(android_yaml_text, manual_nodes, android=True)
    android_yaml_text = _enforce_no_selector_no_direct_yaml_text(android_yaml_text)
    android_yaml_text = _ensure_ping_check_group_yaml_text(android_yaml_text)

    lite_yaml_text = _build_lite_yaml_from_text(yaml_text)
    lite_yaml_text = _enforce_no_selector_no_direct_yaml_text(lite_yaml_text)
    lite_yaml_text = _ensure_ping_check_group_yaml_text(lite_yaml_text)
    lite_yaml_text = _prune_missing_proxy_group_refs_yaml_text(lite_yaml_text)
    node_quality_text = _build_node_quality_report(yaml_text, urltest_rows, nekobox_rows)

    fresh_pool_count = max(max_nodes, _env_int("FRESH_POOL_NODES", _env_int("NEKOBOX_POOL_NODES", max(25, max_nodes * 3))))
    fresh_nodes = mihomo_pass_nodes[:fresh_pool_count]
    fresh_yaml_text = build_openclash_yaml(
        fresh_nodes,
        interval=max(_env_int("URLTEST_INTERVAL", 30), 30),
        tolerance=_env_int("TOLERANCE", 40),
        test_url=os.getenv("TEST_URL", ALT_TEST_URL),
        health_timeout=_env_int("HEALTH_TIMEOUT_MS", 5000),
        rule_mode=os.getenv("RULE_MODE", "Lite"),
    )
    fresh_yaml_text = add_manual_group_to_yaml_text(fresh_yaml_text, manual_nodes, android=False)
    fresh_yaml_text = _enforce_no_selector_no_direct_yaml_text(fresh_yaml_text)
    fresh_yaml_text = _ensure_ping_check_group_yaml_text(fresh_yaml_text)
    fresh_report_text = _build_fresh_pool_report(fresh_nodes, alive_nodes, urltest_rows, nekobox_rows, fresh_yaml_text)
    fresh_json_text = _build_fresh_pool_json(fresh_nodes, alive_nodes, urltest_rows, nekobox_rows)

    csv_text = build_csv(all_nodes + manual_nodes)
    akun_text = build_akun_txt(alive_nodes)
    manual_akun_text = build_akun_txt(manual_nodes)
    manual_skipped_text = "\n".join(manual_skipped) + ("\n" if manual_skipped else "")

    # Final structural cleanup. This must happen after every group mutation.
    yaml_text = _prune_missing_proxy_group_refs_yaml_text(yaml_text)
    android_yaml_text = _prune_missing_proxy_group_refs_yaml_text(android_yaml_text)
    lite_yaml_text = _prune_missing_proxy_group_refs_yaml_text(lite_yaml_text)
    fresh_yaml_text = _prune_missing_proxy_group_refs_yaml_text(fresh_yaml_text)

    if _env_bool("FINAL_TARGET_VALIDATION", True):
        for _label, _text in (
            (output_yaml, yaml_text),
            (output_android_yaml, android_yaml_text),
            (output_lite_yaml, lite_yaml_text),
            (output_fresh_yaml, fresh_yaml_text),
        ):
            try:
                validate_generated_text_with_core(
                    _text,
                    label=_label,
                    core_path=target_core_path,
                    require_exact_core=_env_bool("REQUIRE_EXACT_MIHOMO_CORE", True),
                )
            except RuntimeError as exc:
                raise SystemExit(f"[ERROR] Final target validation gagal: {exc}") from exc
            print(f"[OK] Final target validation: {_label}")

    Path(output_yaml).write_text(yaml_text, encoding="utf-8")
    Path(output_android_yaml).write_text(android_yaml_text, encoding="utf-8")
    Path(output_lite_yaml).write_text(lite_yaml_text, encoding="utf-8")
    Path(output_fresh_yaml).write_text(fresh_yaml_text, encoding="utf-8")
    fresh_dir = Path(output_fresh_dir)
    fresh_dir.mkdir(parents=True, exist_ok=True)
    Path(output_node_quality_report).write_text(node_quality_text, encoding="utf-8")
    (fresh_dir / "fresh_candidates.txt").write_text(build_akun_txt(fresh_nodes), encoding="utf-8")
    (fresh_dir / "fresh_candidates_strict.txt").write_text(build_akun_txt(alive_nodes), encoding="utf-8")
    (fresh_dir / "fresh_candidates.json").write_text(fresh_json_text, encoding="utf-8")
    (fresh_dir / "fresh_candidates_report.md").write_text(fresh_report_text, encoding="utf-8")
    Path(output_csv).write_text(csv_text, encoding="utf-8")
    Path(output_akun).write_text(akun_text, encoding="utf-8")
    Path(output_manual_akun).write_text(manual_akun_text, encoding="utf-8")
    Path(output_manual_skipped).write_text(manual_skipped_text, encoding="utf-8")
    Path(output_urltest_report).write_text(_build_urltest_report_csv(urltest_rows), encoding="utf-8")
    Path(output_nekobox_report).write_text(_build_nekobox_report_csv(nekobox_rows), encoding="utf-8")
    Path(output_openclash_compat_report).write_text(_build_openclash_compat_report_csv(auto_compat_rows + manual_compat_rows), encoding="utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    summary = (
        f"Last update: {now}\n"
        f"Mode: FAST10 + Mihomo URL test + NekoBox/sing-box test early-stop\n"
        f"OpenClash YAML: {output_yaml}\n"
        f"Android YAML: {output_android_yaml}\n"
        f"Lite router YAML: {output_lite_yaml}\n"
        f"Fresh pool YAML: {output_fresh_yaml}\n"
        f"Fresh pool candidates: {len(fresh_nodes)}\n"
        f"Node quality report: {output_node_quality_report}\n"
        f"Automatic YAML nodes after NekoBox test: {len(alive_nodes)}\n"
        f"Automatic strict pool before URL test: {len(auto_pool_nodes)}\n"
        f"Automatic Mihomo URL-test checked: {urltest_checked_count}\n"
        f"Automatic Mihomo URL-test result: {urltest_reason}\n"
        f"Automatic NekoBox/sing-box checked: {nekobox_checked_count}\n"
        f"Automatic NekoBox/sing-box result: {nekobox_reason}\n"
        f"Manual group nodes: {len(manual_nodes)}\n"
        f"Akun txt automatic: {len([x for x in akun_text.splitlines() if x.strip()])}\n"
        f"Akun txt manual: {len([x for x in manual_akun_text.splitlines() if x.strip()])}\n"
        f"Parsed subscription nodes: {len(all_nodes)}\n"
        f"Fetched links: {len(fetch_logs)}\n"
        f"Skipped raw URI: {len(skipped)}\n"
        f"Skipped manual URI: {len(manual_skipped)}\n"
        f"Manual server normalized: {manual_server_changes} link\n"
        f"Manual nodes source file: {manual_file}\n"
        f"Bug server for akun txt/manual_nodes: {TARGET_SERVER}:443\n"
    )
    Path(output_stamp).write_text(summary, encoding="utf-8")

    print(summary)
    if len(alive_nodes) < min_output_nodes:
        print(f"[WARN] Node otomatis yang lolos NekoBox/sing-box test hanya {len(alive_nodes)}/{min_output_nodes}. YAML tetap dibuat dengan node yang tersedia.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
