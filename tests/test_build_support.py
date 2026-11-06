from pathlib import Path

import pytest

from build_support import fetch, publish, validate


def test_publish_replaces_previous(tmp_path):
    target, stage = tmp_path / "output", tmp_path / "stage"
    target.mkdir()
    stage.mkdir()
    (target / "old").touch()
    (stage / "new").touch()
    publish(stage, target)
    assert (target / "new").exists()
    assert not (target / "old").exists()
    assert not (tmp_path / "output.previous").exists()


def test_publish_rolls_back(tmp_path, monkeypatch):
    target, stage = tmp_path / "output", tmp_path / "stage"
    target.mkdir()
    stage.mkdir()
    (target / "old").touch()
    rename = Path.rename

    def fail_stage(self, destination):
        if self == stage:
            raise OSError("simulated failure")
        return rename(self, destination)

    monkeypatch.setattr(Path, "rename", fail_stage)
    with pytest.raises(OSError):
        publish(stage, target)
    assert (target / "old").exists()


def test_download_rejects_untrusted_host():
    with pytest.raises(ValueError):
        fetch("https://example.com/feed")


def test_missing_validator(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate(tmp_path, tmp_path / "missing")


def test_backup_cleanup_failure_reports_publication_success(tmp_path, monkeypatch):
    import build_support
    target, stage = tmp_path / "output", tmp_path / "stage"
    target.mkdir()
    stage.mkdir()
    (stage / "new").touch()

    def fail_cleanup(path):
        raise OSError("busy")

    monkeypatch.setattr(build_support.shutil, "rmtree", fail_cleanup)
    with pytest.warns(RuntimeWarning, match="sudah diterbitkan"):
        publish(stage, target)
    assert (target / "new").exists()