#!/usr/bin/env python3
"""Compile validated Last-Known-Good domain/ipcidr feeds to MRS when possible.

MRS is never forced. A provider is switched to a local MRS file only after the
configured Mihomo binary successfully converts the corresponding validated feed.
Classical providers are intentionally excluded because MRS supports only domain
and ipcidr behavior.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable


LogFn = Callable[[str], None]


def _enabled() -> bool:
    value = str(os.environ.get("MRS_COMPILE", "auto")).strip().lower()
    return value not in {"0", "false", "no", "off", "disabled"}


def _candidate_core(workdir: Path) -> Path | None:
    raw = str(os.environ.get("MIHOMO_PATH", "")).strip()
    candidates = [Path(raw)] if raw else []
    candidates += [workdir / ".local_bin" / "mihomo", workdir / "mihomo"]
    for path in candidates:
        try:
            resolved = path.expanduser().resolve()
        except Exception:
            continue
        if resolved.is_file() and os.access(resolved, os.X_OK):
            return resolved
    return None


def _can_execute(core: Path) -> bool:
    try:
        proc = subprocess.run([str(core), "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5, check=False)
        return proc.returncode == 0
    except Exception:
        return False


def compile_lkg_to_mrs(
    workdir: Path,
    report: dict[str, dict[str, Any]],
    provider_catalog: dict[str, dict[str, Any]],
    *,
    log: LogFn = print,
) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    if not _enabled():
        return results
    core = _candidate_core(workdir)
    if core is None or not _can_execute(core):
        log("MRS compile: exact/runnable Mihomo unavailable; keep text providers")
        return results

    out_dir = workdir / "rule_providers" / "compiled"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, provider in provider_catalog.items():
        behavior = str(provider.get("behavior") or "").lower()
        fmt = str(provider.get("format") or "").lower()
        item = report.get(name) or {}
        source_rel = str(item.get("path") or "")
        if behavior not in {"domain", "ipcidr"} or fmt != "text" or not source_rel:
            continue
        source = workdir / source_rel
        if not source.exists():
            continue
        target = out_dir / f"{name}.mrs"
        tmpdir = Path(tempfile.mkdtemp(prefix="mrs-compile-", dir=str(out_dir)))
        tmp_target = tmpdir / target.name
        try:
            proc = subprocess.run(
                [str(core), "convert-ruleset", behavior, "text", str(source), str(tmp_target)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=60,
                check=False,
            )
            if proc.returncode != 0 or not tmp_target.exists() or tmp_target.stat().st_size == 0:
                results[name] = {"status": "failed", "detail": (proc.stdout or "")[-400:]}
                continue
            shutil.move(str(tmp_target), target)
            results[name] = {
                "status": "compiled",
                "path": str(target.relative_to(workdir)),
                "size": target.stat().st_size,
                "behavior": behavior,
            }
            log(f"MRS compile {name}: {target.stat().st_size} bytes")
        except Exception as exc:
            results[name] = {"status": "failed", "detail": f"{type(exc).__name__}: {exc}"}
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    return results


def load_compiled_report(workdir: Path) -> dict[str, dict[str, Any]]:
    path = workdir / ".feed_cache" / "mrs_compile_report.json"
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def apply_compiled_mrs(config: dict[str, Any], workdir: Path, compiled: dict[str, dict[str, Any]]) -> int:
    """Switch matching HTTP text providers to local file MRS after successful compile."""
    providers = config.get("rule-providers")
    if not isinstance(providers, dict):
        return 0
    changed = 0
    for name, item in compiled.items():
        if item.get("status") != "compiled" or name not in providers:
            continue
        provider = providers.get(name)
        if not isinstance(provider, dict):
            continue
        behavior = str(provider.get("behavior") or "").lower()
        if behavior not in {"domain", "ipcidr"}:
            continue
        rel = str(item.get("path") or "")
        if not rel or not (workdir / rel).exists():
            continue
        provider.clear()
        provider.update({
            "type": "file",
            "behavior": behavior,
            "format": "mrs",
            "path": "./" + rel.replace("\\", "/"),
        })
        changed += 1
    return changed
