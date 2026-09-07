"""Run with Python; no network or Mihomo binary required."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import openclash_target as target


def main():
    with TemporaryDirectory() as directory:
        source = Path(directory)
        asset = source / "geoip.metadb"
        asset.write_bytes(b"test database")

        def check_core(core, config, *, home_dir):
            staged = Path(home_dir) / asset.name
            assert Path(config).is_file()
            if asset.exists():
                assert staged.read_bytes() == asset.read_bytes()
                staged.write_bytes(b"core changed staged copy")
                assert asset.read_bytes() == b"test database"
            else:
                assert not staged.exists()
            return True, ""

        with (
            patch.object(target, "__file__", str(source / "openclash_target.py")),
            patch.object(target, "validate_yaml_text", return_value=[]),
            patch.object(target, "assert_target_mihomo") as version_check,
            patch.object(target, "mihomo_config_test", side_effect=check_core) as core_test,
        ):
            target.validate_generated_text_with_core("{}", label="test", core_path="mihomo")
            asset.unlink()
            target.validate_generated_text_with_core("{}", label="test", core_path="mihomo")
            core_test.side_effect = None
            core_test.return_value = (False, "invalid database")
            try:
                target.validate_generated_text_with_core("{}", label="test", core_path="mihomo")
            except RuntimeError as exc:
                assert "invalid database" in str(exc)
            else:
                raise AssertionError("Core validation failure must propagate")
            assert version_check.call_count == 3
    print("PASS: local GeoIP staging, isolated copy, missing asset, core rejection")


if __name__ == "__main__":
    main()