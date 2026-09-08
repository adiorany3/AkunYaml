#!/usr/bin/env python3
"""Run one conservative ad audit across YouTube, Netflix, apps, and providers."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

FILES = ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml")
NETFLIX_PLAYBACK = {
    "netflix.com",
    "netflix.net",
    "nflxvideo.net",
    "nflximg.net",
    "nflxso.net",
    "nflxext.com",
}
BROAD_MEDIA_BLOCKS = {
    "DOMAIN-SUFFIX,netflix.com,REJECT",
    "DOMAIN-SUFFIX,netflix.net,REJECT",
    "DOMAIN-SUFFIX,nflxvideo.net,REJECT",
    "DOMAIN-SUFFIX,nflximg.net,REJECT",
    "DOMAIN-SUFFIX,nflxso.net,REJECT",
    "DOMAIN-SUFFIX,nflxext.com,REJECT",
}
AUDITS = (
    ("provider", "adblock_provider_audit.py"),
    ("YouTube", "youtube_adblock_audit.py", "--mode", "enhanced", "--dedup", "lean"),
    ("apps", "app_ad_audit.py"),
    ("streaming", "streaming_ad_audit.py"),
    ("popup/game", "popup_game_ad_audit.py"),
    ("YouTube gambling sponsor", "youtube_gambling_sponsor_audit.py"),
)


def audit_netflix(root: Path) -> bool:
    failed = False
    for name in FILES:
        path = root / name
        if not path.exists():
            print(f"[SKIP] Netflix: {name} tidak ditemukan")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rules = {str(rule) for rule in data.get("rules", []) or []}
        broad = sorted(BROAD_MEDIA_BLOCKS & rules)
        if broad:
            failed = True
            print(f"[FAIL] Netflix playback safety: {name}")
            print("  broad media blocks: " + ", ".join(broad))
        else:
            print(f"[OK] Netflix playback safety: {name}; shared CDN tidak diblokir luas")
            print("  [WARN] Netflix ads tidak dapat dipisahkan aman dari content/CDN pada DNS level")
    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="cek URL provider upstream")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    failed = audit_netflix(root)
    for label, script, *script_args in AUDITS:
        command = [sys.executable, script, *script_args]
        if args.network and label == "provider":
            command.append("--network")
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode:
            failed = True
            print(f"[FAIL] {label} audit exit={result.returncode}")
    print("[FAIL] Ads audit selesai dengan error" if failed else "[OK] Ads audit lengkap selesai")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())

# Self-check: Netflix control domains must never be broad-blocked.
assert not (NETFLIX_PLAYBACK & {rule.split(",", 2)[1] for rule in BROAD_MEDIA_BLOCKS})

# ponytail: DNS cannot isolate Netflix ads from licensed content; add app/browser telemetry only when a safe API exists.
