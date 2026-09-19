#!/usr/bin/env python3
"""Run one conservative ad audit across YouTube, Netflix, apps, and providers."""
from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

import yaml
import hashlib
import json
import os
from pathlib import Path

# Load optional configuration file (config.yaml) to allow overriding defaults.
# If the file does not exist, fall back to the hard‑coded defaults defined below.
CONFIG_PATH = Path(__file__).with_name("config.yaml")
if CONFIG_PATH.is_file():
    try:
        _config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    except Exception as e:
        logger = logging.getLogger(__name__)  # temporary logger before full setup
        logger.error("Failed to load configuration file %s: %s", CONFIG_PATH, e)
        _config = {}
else:
    _config = {}

# Helper to fetch a config value with a fallback.
def _cfg(key: str, default):
    return _config.get(key, default)

# Configure basic logging (will be reconfigured after parsing args)
logger = logging.getLogger(__name__)

FILES = tuple(_cfg("files", ["openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml"]))
NETFLIX_PLAYBACK = set(_cfg("netflix_playback", [
    "netflix.com",
    "netflix.net",
    "nflxvideo.net",
    "nflximg.net",
    "nflxso.net",
    "nflxext.com",
]))
BROAD_MEDIA_BLOCKS = set(_cfg("broad_media_blocks", []))
AUDITS = tuple(tuple(audit) for audit in _cfg("audits", [
    ("provider", "adblock_provider_audit.py"),
    ("YouTube", "youtube_adblock_audit.py", "--mode", "enhanced", "--dedup", "lean"),
    ("apps", "app_ad_audit.py"),
    ("streaming", "streaming_ad_audit.py"),
    ("popup/game", "popup_game_ad_audit.py"),
    ("YouTube gambling sponsor", "youtube_gambling_sponsor_audit.py"),
]))


def audit_netflix(root: Path) -> bool:
    """Audit Netflix configuration files.

    Checks each YAML file listed in ``FILES`` for broad‑block rules that
    would affect Netflix playback domains. Returns ``True`` if any
    problematic rules are found, otherwise ``False``.
    """
    failed = False
    for name in FILES:
        path = root / name
        if not path.exists():
            logger.info(f"[SKIP] Netflix: {name} tidak ditemukan")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rules = {str(rule) for rule in data.get("rules", []) or []}
        # Only reject rules targeting Netflix playback domains are unsafe.
        broad = set(BROAD_MEDIA_BLOCKS & rules)
        for rule in rules:
            parts = [part.strip() for part in rule.split(",")]
            if len(parts) < 3 or parts[2] not in {"REJECT", "REJECT-DROP"}:
                continue
            kind, domain = parts[:2]
            domain = domain.lower().rstrip(".")
            if kind == "DOMAIN" and domain in NETFLIX_PLAYBACK:
                broad.add(rule)
            elif kind == "DOMAIN-SUFFIX" and any(
                d == domain or d.endswith("." + domain) for d in NETFLIX_PLAYBACK
            ):
                broad.add(rule)
            elif kind == "DOMAIN-KEYWORD" and any(domain in d for d in NETFLIX_PLAYBACK):
                broad.add(rule)
        broad = sorted(broad)
        if broad:
            failed = True
            logger.error(f"[FAIL] Netflix playback safety: {name}")
            logger.debug("  broad media blocks: " + ", ".join(broad))
        else:
            logger.info(f"[OK] Netflix playback safety: {name}; shared CDN tidak diblokir luas")
            logger.warning("  [WARN] Netflix ads tidak dapat dipisahkan aman dari content/CDN pada DNS level")
    return failed


def main() -> int:
    """Entry point for the ad‑audit suite.

    Parses command‑line arguments, configures logging, runs the Netflix
    audit and then iterates over the other audit scripts defined in
    ``AUDITS``. Returns ``0`` on success or ``1`` if any audit reports a
    failure.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="cek URL provider upstream")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--log-file", type=str, help="Path to file log file")
    parser.add_argument("--report", type=str, help="Path to write JSON report")
    parser.add_argument("--html-report", type=str, help="Path to write HTML report")
    args = parser.parse_args()
    # Configure logging based on CLI arguments
    # Reset any existing handlers to avoid duplicate logs when the script is imported multiple times
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # Optional file handler
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    root = Path(__file__).resolve().parent
    failed = audit_netflix(root)
    results: list[dict[str, object]] = [{
        "label": "Netflix playback safety",
        "script": "ads_audit.py",
        "status": "fail" if failed else "pass",
        "exit_code": int(failed),
    }]
    for label, script, *script_args in AUDITS:
        command = [sys.executable, script, *script_args]
        if args.network and label == "provider":
            command.append("--network")
        try:
            result = subprocess.run(command, cwd=root, check=False, timeout=300)
        except subprocess.TimeoutExpired:
            failed = True
            logger.error(f"[FAIL] {label} audit timeout setelah 300 detik")
            results.append({"label": label, "script": script, "status": "timeout"})
            continue
        except (OSError, subprocess.SubprocessError) as exc:
            failed = True
            logger.error(f"[FAIL] {label} audit gagal dijalankan: {exc}")
            results.append({"label": label, "script": script, "status": "error", "error": str(exc)})
            continue
        status = "fail" if result.returncode else "pass"
        if result.returncode:
            failed = True
            logger.error(f"[FAIL] {label} audit exit={result.returncode}")
        results.append({"label": label, "script": script, "status": status, "exit_code": result.returncode})
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps({"failed": failed, "audits": results}, indent=2), encoding="utf-8")
        logger.info(f"[OK] Laporan audit ditulis ke {report_path}")

    if args.html_report:
        try:
            from jinja2 import Template
        except ImportError:
            logger.error("Jinja2 is required for HTML report generation")
            raise
        html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Audit Report</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 20px;}
        table {border-collapse: collapse; width: 100%;}
        th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
        th {background-color: #f2f2f2;}
        .pass {color: green;}
        .fail {color: red;}
        .timeout {color: orange;}
    </style>
</head>
<body>
    <h1>Audit Report</h1>
    <p>Status: {% if failed %}<span class="fail">FAIL</span>{% else %}<span class="pass">PASS</span>{% endif %}</p>
    <table>
        <tr><th>Label</th><th>Script</th><th>Status</th><th>Exit Code</th></tr>
        {% for r in audits %}
        <tr>
            <td>{{ r.label }}</td>
            <td>{{ r.script }}</td>
            <td class="{{ r.status }}">{{ r.status|capitalize }}</td>
            <td>{{ r.exit_code | default('') }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>"""
        tmpl = Template(html_template)
        html_content = tmpl.render(failed=failed, audits=results)
        html_path = Path(args.html_report)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html_content, encoding="utf-8")
        logger.info(f"[OK] HTML report written to {html_path}")
    # Print concise summary table to console
    logger.info("\nAudit Summary:\nLabel\tScript\tStatus\tExitCode")
    for r in results:
        logger.info(f"{r.get('label','')}\t{r.get('script','')}\t{r.get('status','')}\t{r.get('exit_code','')}" )
    if failed:
        logger.error(f"[FAIL] Ads audit selesai dengan error: {failed} failures")
    else:
        logger.info("[OK] Ads audit lengkap selesai")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())

# Self-check: Netflix control domains must never be broad-blocked.
assert not (NETFLIX_PLAYBACK & {rule.split(",", 2)[1] for rule in BROAD_MEDIA_BLOCKS})

# ponytail: DNS cannot isolate Netflix ads from licensed content; add app/browser telemetry only when a safe API exists.
