import json
from datetime import UTC, datetime

import pytest

from health_report import render

NOW = datetime(2026, 11, 10, 12, tzinfo=UTC)


def write(root, name, data):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def test_summary_is_conservative_and_excludes_secrets(tmp_path):
    write(tmp_path, "local_build/build_report.json", {"remote_providers_at_runtime": ["ads", "ads"]})
    write(tmp_path, "local_build/gameblock/build_report.json", {
        "assets": [{"fetched_at": "2026-11-10T10:00:00+00:00", "url": "SECRET"}],
    })
    manifest = {
        "mode": "security-refresh-retained-accounts",
        "account_refresh": "retained-old",
        "adaptive_guard": "fresh",
        "packaged_at": "2026-11-10T11:00:00+00:00",
        "validation": {"profiles": 13},
        "sources": [{"modified_at": "2026-11-08T12:00:00+00:00", "path": "SECRET"}],
        "warning": "SECRET",
    }
    text = render(tmp_path, manifest, now=NOW)
    assert "13 profil lulus" in text
    assert "48.0 jam" in text
    assert "2.0 jam" in text
    assert "runtime: 1" in text
    assert "akun lama dipertahankan" in text
    assert "Node aktif saat ini: tidak diketahui" in text
    assert "SECRET" not in text


@pytest.mark.parametrize("timestamp", [None, "bad", "2026-11-10T13:00:00+00:00", "2026-11-10T10:00:00"])
def test_invalid_timestamps_and_legacy_manifest(tmp_path, timestamp):
    write(tmp_path, "local_build/build_report.json", {})
    write(tmp_path, "local_build/gameblock/build_report.json", {"assets": [{"fetched_at": timestamp}]})
    text = render(tmp_path, {"packaged_at": timestamp, "sources": [{"modified_at": timestamp}]}, now=NOW)
    assert "belum mencatat bukti validasi" in text
    assert "waktu feed gameblock tidak diketahui" in text
    assert "Waktu packaging tidak diketahui" in text


@pytest.mark.parametrize("data", ["{", "[]", '{"mode": [], "account_refresh": {}, "adaptive_guard": []}'])
def test_missing_or_malformed_reports_do_not_crash(tmp_path, data):
    path = tmp_path / "output/manifest.json"
    path.parent.mkdir()
    path.write_text(data)
    text = render(tmp_path, now=NOW)
    assert "tidak diketahui" in text
    assert "Laporan tidak tersedia/rusak" in text


def test_collect_publishes_health_only_after_validation(tmp_path, monkeypatch):
    import unified_update

    for name in ["openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml",
                 "local_build/openclash_noproxy.yaml", "local_build/gameblock/openclash_noproxy_gameblock.yaml"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("rules: [MATCH,DIRECT]\n")
    for name in ["singbox_android.json", "local_build/singbox_direct_adblock.json"]:
        write(tmp_path, name, {})
    (tmp_path / "akun.txt").write_text("SECRET")
    monkeypatch.setattr(unified_update, "hako_singbox", lambda config: config)
    monkeypatch.setattr(unified_update, "build_singbox_gameblock", lambda *args: {})
    monkeypatch.setattr(unified_update, "apply_adaptive_guard", lambda stage, root: "unavailable")
    monkeypatch.setattr(unified_update, "export_openwrt", lambda stage: None)

    def validate(stage, root):
        assert not (stage / "health_report.md").exists()
        return list(stage.glob("**/*.yaml")) + list(stage.glob("sing-box/*.json"))

    monkeypatch.setattr(unified_update, "validate_bundle", validate)
    output = unified_update.collect(tmp_path, "offline-snapshot")
    text = (output / "health_report.md").read_text()
    assert "14 profil lulus" in text
    assert "SECRET" not in text
    assert json.loads((output / "manifest.json").read_text())["validation"]["profiles"] == 14
    assert (output / "changes.json").is_file()

    def fail(stage, root):
        raise RuntimeError("validation failed")

    monkeypatch.setattr(unified_update, "validate_bundle", fail)
    with pytest.raises(RuntimeError, match="validation failed"):
        unified_update.collect(tmp_path, "online-refresh")
    assert (output / "health_report.md").read_text() == text
