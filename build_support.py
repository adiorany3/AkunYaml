"""Shared download, validation, and staged publication helpers."""
import shutil
import subprocess
import urllib.request
import warnings
from pathlib import Path

PROFILE = "openclash_noproxy_gameblock.yaml"


def seed_geodata(directory: Path, root: Path) -> None:
    """Reuse installed databases in temporary core homes; never alter sources."""
    locations = (root, root / ".runtime_cache/independent_gameblock", root / "local_build")
    for name in ("GeoSite.dat", "GeoIP.dat", "geoip.metadb", "Country.mmdb"):
        target = directory / name
        if target.exists():
            continue
        for location in locations:
            source = location / name
            if source.is_file() and source.stat().st_size:
                shutil.copy2(source, target)
                break


def fetch(url: str) -> bytes:
    if not url.startswith("https://raw.githubusercontent.com/"):
        raise ValueError("Provider harus berasal dari raw.githubusercontent.com HTTPS")
    with urllib.request.urlopen(url, timeout=90) as response:
        data = response.read(40 * 1024 * 1024 + 1)
    if not data or len(data) > 40 * 1024 * 1024:
        raise ValueError("Provider kosong atau melebihi batas 40 MiB")
    return data


def validate(directory: Path, core: Path) -> None:
    if not core.is_file():
        raise FileNotFoundError("Validator Mihomo lokal tidak tersedia")
    seed_geodata(directory, core.resolve().parent.parent)
    result = subprocess.run(
        [str(core), "-t", "-d", str(directory), "-f", str(directory / PROFILE)],
        capture_output=True, text=True, timeout=120, check=False,
    )
    if result.returncode:
        raise RuntimeError("Validasi Mihomo gagal:\n" + (result.stdout + result.stderr)[-4000:])


def publish(stage: Path, target: Path) -> None:
    """Keep the previous release until directory replacement succeeds."""
    backup = target.with_name(target.name + ".previous")
    if backup.exists():
        raise FileExistsError(f"Backup belum ditangani: {backup}")
    existed = target.exists()
    if existed:
        target.rename(backup)
    try:
        stage.rename(target)
    except OSError:
        if existed:
            backup.rename(target)
        raise
    if existed:
        try:
            shutil.rmtree(backup)
        except OSError:
            warnings.warn(f"Hasil baru sudah diterbitkan; backup belum dapat dibersihkan: {backup}", RuntimeWarning, stacklevel=2)