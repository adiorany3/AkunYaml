#!/usr/bin/env python3
"""Target compatibility helpers for OpenClash v0.47.156 + Mihomo alpha-ge183c58."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable

import yaml

OPENCLASH_TARGET_VERSION = "v0.47.156"
MIHOMO_TARGET_REVISION = "e183c58"
MIHOMO_TARGET_LABEL = "alpha-ge183c58"
DEFAULT_ROUTER_CORE = "/etc/openclash/core/clash_meta"

BUILTIN_POLICIES = {
    "DIRECT",
    "REJECT",
    "REJECT-DROP",
    "PASS",
    "COMPATIBLE",
}
ALLOWED_GROUP_TYPES = {
    "select",
    "url-test",
    "fallback",
    "load-balance",
    "relay",  # legacy parser support; do not generate new relay groups.
}


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "y", "on", "aktif"}


def mihomo_version_text(core_path: str | Path) -> str:
    core = str(core_path)
    try:
        proc = subprocess.run(
            [core, "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"gagal menjalankan Mihomo core {core}: {exc}") from exc

    output = (proc.stdout or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(
            f"gagal membaca versi Mihomo core {core}: {output or f'exit={proc.returncode}'}"
        )
    return output


def is_target_mihomo_version(version_text: str) -> bool:
    text = str(version_text or "").lower()
    return "alpha" in text and MIHOMO_TARGET_REVISION in text


def assert_target_mihomo(
    core_path: str | Path,
    *,
    strict: bool = True,
) -> str:
    core = Path(core_path).expanduser()
    if not core.is_file():
        raise RuntimeError(f"Mihomo core tidak ditemukan: {core}")

    version = mihomo_version_text(core)
    if strict and not is_target_mihomo_version(version):
        raise RuntimeError(
            "Mihomo core tidak sesuai target.\n"
            f"  OpenClash target : {OPENCLASH_TARGET_VERSION}\n"
            f"  Mihomo target    : {MIHOMO_TARGET_LABEL}\n"
            f"  Core terdeteksi  : {version}\n"
            "Gunakan binary Mihomo alpha yang dibangun dari commit e183c58."
        )
    return version


def find_existing_core(candidates: Iterable[str | Path]) -> Path | None:
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        if path.is_file():
            return path.resolve()
    return None


def discover_mihomo_core(
    *,
    explicit: str | Path | None = None,
    workdir: str | Path | None = None,
    require_exact: bool = True,
) -> tuple[Path | None, list[str]]:
    """Find a local Mihomo core. Exact target is preferred and required by default."""
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env_core = os.getenv("MIHOMO_PATH", "").strip()
    if env_core:
        candidates.append(Path(env_core).expanduser())
    candidates.append(Path(DEFAULT_ROUTER_CORE))
    if workdir:
        root = Path(workdir)
        candidates.append(root / ".local_bin" / ("mihomo.exe" if os.name == "nt" else "mihomo"))
        candidates.append(root / ("mihomo.exe" if os.name == "nt" else "mihomo"))
    for name in ("mihomo", "clash-meta", "clash_meta"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))

    seen: set[str] = set()
    mismatches: list[str] = []
    first_valid: Path | None = None
    for candidate in candidates:
        key = str(candidate)
        if key in seen or not candidate.is_file():
            continue
        seen.add(key)
        try:
            version = mihomo_version_text(candidate)
        except RuntimeError as exc:
            mismatches.append(f"{candidate}: {exc}")
            continue
        if first_valid is None:
            first_valid = candidate.resolve()
        if is_target_mihomo_version(version):
            return candidate.resolve(), mismatches
        mismatches.append(f"{candidate}: {version}")

    if require_exact:
        return None, mismatches
    return first_valid, mismatches


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _policy_from_rule(rule: str) -> str | None:
    parts = [item.strip() for item in str(rule).split(",")]
    if not parts:
        return None
    rtype = parts[0].upper()
    if rtype in {"MATCH", "FINAL"}:
        return parts[1] if len(parts) >= 2 else None
    if rtype in {"AND", "OR", "NOT", "SUB-RULE"}:
        return None
    if len(parts) < 3:
        return None
    if parts[-1].lower() == "no-resolve" and len(parts) >= 4:
        return parts[-2]
    return parts[-1]


def validate_config_structure(config: Any, *, label: str = "config") -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return [f"{label}: root YAML harus mapping/dict"]

    proxies = config.get("proxies") or []
    groups = config.get("proxy-groups") or []
    rules = config.get("rules") or []
    providers = config.get("rule-providers") or {}

    if not isinstance(proxies, list):
        errors.append(f"{label}: proxies harus list")
        proxies = []
    if not isinstance(groups, list):
        errors.append(f"{label}: proxy-groups harus list")
        groups = []
    if not isinstance(rules, list):
        errors.append(f"{label}: rules harus list")
        rules = []
    if providers is not None and not isinstance(providers, dict):
        errors.append(f"{label}: rule-providers harus mapping")
        providers = {}

    proxy_names = [
        str(item.get("name", "")).strip()
        for item in proxies
        if isinstance(item, dict) and str(item.get("name", "")).strip()
    ]
    group_names = [
        str(item.get("name", "")).strip()
        for item in groups
        if isinstance(item, dict) and str(item.get("name", "")).strip()
    ]

    for duplicate in _duplicates(proxy_names):
        errors.append(f"{label}: nama proxy duplikat: {duplicate}")
    for duplicate in _duplicates(group_names):
        errors.append(f"{label}: nama proxy-group duplikat: {duplicate}")

    # OpenClash v0.47.156 has a reported name-rewrite issue with emoji.
    # Keep proxy/group identifiers printable ASCII to avoid subscription rewrite damage.
    for kind, names in (("proxy", proxy_names), ("proxy-group", group_names)):
        for name in names:
            if not name.isascii() or any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
                errors.append(f"{label}: nama {kind} harus printable ASCII untuk target ini: {name!r}")

    overlap = sorted(set(proxy_names) & set(group_names))
    for name in overlap:
        errors.append(f"{label}: nama dipakai sebagai proxy dan group: {name}")

    known = set(proxy_names) | set(group_names) | BUILTIN_POLICIES
    group_set = set(group_names)
    graph: dict[str, list[str]] = {name: [] for name in group_names}

    for group in groups:
        if not isinstance(group, dict):
            errors.append(f"{label}: proxy-group bukan mapping")
            continue
        name = str(group.get("name", "")).strip()
        gtype = str(group.get("type", "")).strip().lower()
        if not name:
            errors.append(f"{label}: proxy-group tanpa name")
            continue
        if gtype not in ALLOWED_GROUP_TYPES:
            errors.append(f"{label}: group {name} memiliki type tidak dikenal: {gtype or '<kosong>'}")

        refs = group.get("proxies") or []
        if not isinstance(refs, list):
            errors.append(f"{label}: group {name} proxies harus list")
            continue
        if not refs and not group.get("use"):
            errors.append(f"{label}: group {name} kosong")
        for ref in refs:
            ref_name = str(ref).strip()
            if not ref_name:
                continue
            if ref_name not in known:
                errors.append(f"{label}: group {name} mereferensikan target tidak ada: {ref_name}")
            if ref_name in group_set:
                graph[name].append(ref_name)

        if gtype in {"url-test", "fallback", "load-balance"}:
            if not str(group.get("url", "")).strip():
                errors.append(f"{label}: group {name} ({gtype}) tidak memiliki url")
            if "expected-status" in group:
                status = str(group.get("expected-status", "")).strip()
                if status and not re.fullmatch(r"[0-9*/-]+", status):
                    errors.append(f"{label}: expected-status group {name} tidak valid: {status}")

    # Detect group reference cycles.
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in graph.get(node, []):
            if state.get(nxt, 0) == 0:
                visit(nxt)
            elif state.get(nxt) == 1:
                try:
                    start = stack.index(nxt)
                    cycle = stack[start:] + [nxt]
                except ValueError:
                    cycle = [node, nxt]
                errors.append(f"{label}: proxy-group cycle: {' -> '.join(cycle)}")
        stack.pop()
        state[node] = 2

    for name in graph:
        if state.get(name, 0) == 0:
            visit(name)

    provider_names = set(providers.keys()) if isinstance(providers, dict) else set()
    if isinstance(providers, dict):
        for provider_name, provider in providers.items():
            if not isinstance(provider, dict):
                errors.append(f"{label}: rule-provider {provider_name} bukan mapping")
                continue
            ptype = str(provider.get("type", "")).lower()
            fmt = str(provider.get("format", "")).lower()
            behavior = str(provider.get("behavior", "")).lower()
            if ptype == "http":
                path = str(provider.get("path", "")).strip()
                if not path:
                    errors.append(f"{label}: rule-provider {provider_name} tanpa path")
                elif Path(path).is_absolute() or ".." in Path(path).parts:
                    errors.append(f"{label}: rule-provider {provider_name} path tidak portable: {path}")
                if not str(provider.get("url", "")).strip():
                    errors.append(f"{label}: rule-provider {provider_name} tanpa url")
            if fmt == "mrs" and behavior not in {"domain", "ipcidr"}:
                errors.append(
                    f"{label}: MRS provider {provider_name} hanya mendukung behavior domain/ipcidr, didapat {behavior}"
                )

    for raw in rules:
        rule = str(raw).strip()
        if not rule:
            errors.append(f"{label}: rule kosong")
            continue
        parts = [item.strip() for item in rule.split(",")]
        if parts and parts[0].upper() == "RULE-SET":
            if len(parts) < 3:
                errors.append(f"{label}: RULE-SET malformed: {rule}")
                continue
            if parts[1] not in provider_names:
                errors.append(f"{label}: RULE-SET provider tidak ada: {parts[1]}")
        policy = _policy_from_rule(rule)
        if policy and policy not in known:
            errors.append(f"{label}: rule policy tidak ada: {policy} ({rule})")

    if "global-client-fingerprint" in config:
        errors.append(f"{label}: global-client-fingerprint tidak dipakai pada paket target ini")

    return list(dict.fromkeys(errors))


def validate_yaml_text(yaml_text: str, *, label: str = "config") -> list[str]:
    if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in yaml_text):
        return [f"{label}: terdapat control character tersembunyi"]
    try:
        config = yaml.safe_load(yaml_text)
    except Exception as exc:
        return [f"{label}: YAML parse error: {exc}"]
    return validate_config_structure(config, label=label)


def mihomo_config_test(
    core_path: str | Path,
    config_path: str | Path,
    *,
    home_dir: str | Path | None = None,
    timeout: int = 60,
) -> tuple[bool, str]:
    core = str(core_path)
    config = Path(config_path).resolve()
    home = Path(home_dir).resolve() if home_dir else config.parent
    env = os.environ.copy()
    # Matches the safe path used by OpenClash on the target router.
    env.setdefault("SAFE_PATHS", "/usr/share/openclash:/etc/ssl")
    try:
        proc = subprocess.run(
            [core, "-t", "-d", str(home), "-f", str(config)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=max(5, int(timeout)),
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        return False, f"mihomo config test timeout > {timeout}s: {exc}"
    except OSError as exc:
        return False, f"gagal menjalankan mihomo: {exc}"
    output = (proc.stdout or "").strip()
    return proc.returncode == 0, output


def validate_yaml_file(
    path: str | Path,
    *,
    core_path: str | Path | None = None,
    require_exact_core: bool = True,
    parser_test: bool = True,
) -> list[str]:
    file_path = Path(path)
    if not file_path.is_file():
        return [f"file tidak ditemukan: {file_path}"]
    text = file_path.read_text(encoding="utf-8", errors="strict")
    errors = validate_yaml_text(text, label=file_path.name)
    if errors or not parser_test or core_path is None:
        return errors

    try:
        assert_target_mihomo(core_path, strict=require_exact_core)
    except RuntimeError as exc:
        errors.append(str(exc))
        return errors

    ok, output = mihomo_config_test(core_path, file_path, home_dir=file_path.parent)
    if not ok:
        errors.append(
            f"{file_path.name}: ditolak Mihomo {MIHOMO_TARGET_LABEL}: {output[-4000:]}"
        )
    return errors


def validate_generated_text_with_core(
    yaml_text: str,
    *,
    label: str,
    core_path: str | Path,
    require_exact_core: bool = True,
) -> None:
    errors = validate_yaml_text(yaml_text, label=label)
    if errors:
        raise RuntimeError("\n".join(errors))
    assert_target_mihomo(core_path, strict=require_exact_core)
    with tempfile.TemporaryDirectory(prefix="akunyaml-target-") as temp_dir:
        root = Path(temp_dir)
        config_path = root / "config.yaml"
        config_path.write_text(yaml_text, encoding="utf-8")
        ok, output = mihomo_config_test(core_path, config_path, home_dir=root)
        if not ok:
            raise RuntimeError(
                f"{label}: final YAML ditolak Mihomo {MIHOMO_TARGET_LABEL}:\n{output[-4000:]}"
            )
