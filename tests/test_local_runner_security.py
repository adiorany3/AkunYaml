import tarfile

import pytest

from local_runner import extract_binary


def test_extract_binary_rejects_tar_path_traversal(tmp_path):
    archive = tmp_path / "malicious.tar.gz"
    output = tmp_path / "bin" / "core"
    with tarfile.open(archive, "w:gz") as tf:
        info = tarfile.TarInfo("../core")
        info.size = 4
        import io
        tf.addfile(info, io.BytesIO(b"evil"))

    with pytest.raises(RuntimeError, match="Path archive tidak aman"):
        extract_binary(archive, "core", output)

    assert not output.exists()
