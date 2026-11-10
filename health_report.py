"""Ringkasan lokal tanpa jaringan, pembacaan profil, atau kredensial akun."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


def render(root: Path, manifest=None, *, now=None):
    now = now or datetime.now(UTC)
    warnings = []

    def load(relative):
        try:
            data = json.loads((root / relative).read_text())
            if not isinstance(data, dict):
                raise TypeError("Expected object")
            return data
        except (OSError, ValueError, TypeError):
            warnings.append(f"Laporan tidak tersedia/rusak: {relative}.")
            return {}

    def age(value):
        try:
            timestamp = datetime.fromisoformat(value)
            if timestamp.tzinfo is None or timestamp > now:
                raise ValueError("Invalid timestamp")
            return (now - timestamp).total_seconds() / 3600
        except (TypeError, ValueError):
            return None

    manifest = load("output/manifest.json") if manifest is None else manifest

    def label(options, value):
        return options.get(value, "tidak diketahui") if isinstance(value, str) else "tidak diketahui"
    game = load("local_build/gameblock/build_report.json")
    direct = load("local_build/build_report.json")
    modes = {
        "offline-snapshot": "snapshot offline",
        "online-refresh": "refresh online",
        "security-refresh": "refresh keamanan saja",
        "security-refresh-retained-accounts": "refresh keamanan, akun lama dipertahankan",
    }
    accounts = {
        "completed": "refresh selesai (bukan jaminan node masih aktif)",
        "retained-old": "akun lama dipertahankan; refresh baru tidak memenuhi syarat",
        "not-requested": "refresh tidak diminta",
    }
    if manifest.get("account_refresh") == "retained-old":
        warnings.append("Periksa akun lama sebelum dipakai; refresh akun baru tidak memenuhi syarat.")
    validation = manifest.get("validation", {})
    count = validation.get("profiles") if isinstance(validation, dict) else None
    validated = isinstance(count, int) and not isinstance(count, bool) and count > 0
    sources = manifest.get("sources", [])
    sources = sources if isinstance(sources, list) else []
    source_ages = [age(item.get("modified_at")) for item in sources if isinstance(item, dict)]
    assets = game.get("assets", [])
    assets = assets if isinstance(assets, list) else []
    feed_ages = [age(item.get("fetched_at")) for item in assets if isinstance(item, dict)]

    def oldest(values):
        known = [value for value in values if value is not None]
        return f"{max(known):.1f} jam" if known else "tidak diketahui"

    if not validated:
        warnings.append("Manifest belum mencatat bukti validasi; jalankan update untuk merekamnya.")
    if not source_ages or None in source_ages:
        warnings.append("Sebagian/seluruh waktu sumber tidak diketahui atau tidak valid.")
    if not feed_ages or None in feed_ages:
        warnings.append("Sebagian/seluruh waktu feed gameblock tidak diketahui atau tidak valid.")
    adaptive = {"fresh": "segar saat packaging", "expired": "kedaluwarsa saat packaging", "unavailable": "tidak tersedia"}
    adaptive_status = label(adaptive, manifest.get("adaptive_guard"))
    if manifest.get("adaptive_guard") != "fresh":
        warnings.append("Periksa feed adaptif; status packaging bukan fresh.")
    packaged_age = age(manifest.get("packaged_at"))
    runtime = direct.get("remote_providers_at_runtime", [])
    remote_count = len(set(runtime)) if isinstance(runtime, list) and all(isinstance(v, str) for v in runtime) else None
    lines = [
        "# Kesehatan AkunYaml",
        "",
        f"- Mode: {label(modes, manifest.get('mode'))}.",
        f"- Umur packaging: {oldest([packaged_age])}.",
        f"- Akun: {label(accounts, manifest.get('account_refresh'))}.",
        f"- Validasi core saat packaging: {str(count) + ' profil lulus' if validated else 'tidak diketahui'}.",
        f"- Umur sumber tertua: {oldest(source_ages)} (waktu modifikasi, bukan uji node).",
        f"- Feed gameblock: {len(assets)} tercatat; umur unduhan tertua: {oldest(feed_ages)}.",
        f"- Adaptive guard: {adaptive_status}.",
        f"- Provider direct yang memerlukan internet saat runtime: {remote_count if remote_count is not None else 'tidak diketahui'}.",
        "- Node aktif saat ini: tidak diketahui; laporan ini tidak menjalankan health check.",
        "",
        "## Tindakan/peringatan",
    ]
    if packaged_age is None:
        warnings.append("Waktu packaging tidak diketahui atau tidak valid.")
    lines.extend(f"- {warning}" for warning in warnings)
    lines.append("- Umur feed ditampilkan tanpa klaim masih aman/segar; periksa kebutuhan refresh.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(render(args.root), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
