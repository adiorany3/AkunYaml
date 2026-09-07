"""Offline per-file publication and YAML transaction rollback checks."""
import tempfile
from pathlib import Path
from unittest.mock import patch

from openclash_target import atomic_write_text
from local_runner import yaml_edit_transaction, _yaml_store_config, _YAML_TX_CACHE, _YAML_TX_DIRTY

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "config.yaml"
    path.write_text("old: true\n", encoding="utf-8")
    path.chmod(0o640)
    for target in ("openclash_target.os.fsync", "pathlib.Path.replace"):
        with patch(target, side_effect=OSError("injected publication failure")):
            try:
                atomic_write_text(path, "new: true\n")
            except OSError:
                pass
            else:
                raise AssertionError("publication failure swallowed")
        assert path.read_text() == "old: true\n"
        assert list(path.parent.iterdir()) == [path]
    atomic_write_text(path, "new: true\n")
    assert path.read_text() == "new: true\n"
    assert path.stat().st_mode & 0o777 == 0o640
    try:
        with yaml_edit_transaction(path):
            _yaml_store_config(path, {"partial": True})
            raise ValueError("abort optimization")
    except ValueError:
        pass
    assert path.read_text() == "new: true\n"
    assert not _YAML_TX_CACHE and not _YAML_TX_DIRTY
    fresh = Path(tmp) / "new.yaml"
    atomic_write_text(fresh, "new: true\n")
    assert fresh.stat().st_mode & 0o777 == 0o600
print("PASS: replacement, permissions, failure preservation, cleanup, YAML rollback")