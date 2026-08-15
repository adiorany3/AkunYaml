#!/usr/bin/env python3
from __future__ import annotations

import copy
import re
import shutil
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path

import yaml

REFERENCE_URL = (
    "https://raw.githubusercontent.com/adiorany3/ConvertYAML/"
    "refs/heads/main/openclash_auto.yaml"
)
TARGET = "openclash_auto.yaml"


def fetch_reference() -> dict:
    req = urllib.request.Request(
        REFERENCE_URL,
        headers={"User-Agent": "ConvertYAML-Reference-Fix/2.3"},
    )
    with urllib.request.urlopen(
        req,
        timeout=60,
        context=ssl.create_default_context(),
    ) as response:
        cfg = yaml.safe_load(response.read().decode("utf-8")) or {}
    if not isinstance(cfg, dict):
        raise RuntimeError("Reference YAML invalid")
    return cfg


def main() -> int:
    workdir = Path(__file__).resolve().parent
    target = workdir / TARGET

    if not target.exists():
        print(f"[ERROR] {TARGET} tidak ditemukan")
        return 1

    generated = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    if not isinstance(generated, dict):
        print("[ERROR] YAML target invalid")
        return 2

    reference = fetch_reference()

    backup_dir = workdir / "backup_reference_lock"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = backup_dir / f"{TARGET}.{stamp}.bak"
    shutil.copy2(target, backup)
    print(f"[BACKUP] {backup}")

    merged = copy.deepcopy(generated)

    for key in ("profile", "sniffer", "dns", "rule-providers", "rules"):
        if key in reference:
            merged[key] = copy.deepcopy(reference[key])

    merged.pop("global-client-fingerprint", None)

    providers = merged.get("rule-providers")
    if isinstance(providers, dict):
        for name in (
            "tracker-domain",
            "security-tif-mini",
            "popup-ads",
            "hagezi-pro-mini",
            "awavenue-ads",
        ):
            providers.pop(name, None)

    if isinstance(merged.get("rules"), list):
        merged["rules"] = [
            str(raw).strip()
            for raw in merged["rules"]
            if not re.match(
                r"(?i)^GEOSITE\s*,\s*(tracker|category-ads-all)\s*,",
                str(raw).strip(),
            )
            and not re.match(
                r"(?i)^RULE-SET\s*,\s*"
                r"(tracker-domain|security-tif-mini|popup-ads|hagezi-pro-mini|awavenue-ads)"
                r"\s*,",
                str(raw).strip(),
            )
        ]

    proxy_names = {
        str(p.get("name"))
        for p in merged.get("proxies", []) or []
        if isinstance(p, dict) and p.get("name")
    }
    group_names = {
        str(g.get("name"))
        for g in merged.get("proxy-groups", []) or []
        if isinstance(g, dict) and g.get("name")
    }
    valid_refs = proxy_names | group_names | {
        "DIRECT", "REJECT", "PASS", "COMPATIBLE"
    }

    for group in merged.get("proxy-groups", []) or []:
        if not isinstance(group, dict):
            continue
        refs = group.get("proxies")
        if isinstance(refs, list):
            group["proxies"] = [
                str(ref) for ref in refs if str(ref) in valid_refs
            ]

    target.write_text(
        yaml.safe_dump(
            merged,
            allow_unicode=True,
            sort_keys=False,
            width=160,
        ),
        encoding="utf-8",
    )

    print("[OK] Reference-locked profile diterapkan.")
    print("[OK] Proxy dan proxy-group hasil pencarian dipertahankan.")
    print("[OK] DNS/sniffer/providers/rules kembali ke baseline proven.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
