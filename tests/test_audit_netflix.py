# tests/test_audit_netflix.py
import sys
from pathlib import Path
import yaml

# Ensure repository root is on sys.path for imports
repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root))

from ads_audit import audit_netflix, FILES, NETFLIX_PLAYBACK, BROAD_MEDIA_BLOCKS


def test_audit_netflix_no_rules(tmp_path, monkeypatch):
    # Create empty yaml files for each expected file name
    for name in FILES:
        (tmp_path / name).write_text("rules: []", encoding="utf-8")
    # Run audit on the temporary directory
    result = audit_netflix(tmp_path)
    assert result is False


def test_audit_netflix_with_broad_block(tmp_path, monkeypatch):
    # Create a yaml file that contains a broad block rule for netflix.com
    for name in FILES:
        (tmp_path / name).write_text("rules: []", encoding="utf-8")
    # Inject a problematic rule into the first file
    first = tmp_path / FILES[0]
    first.write_text(f"rules: [{list(BROAD_MEDIA_BLOCKS)[0] if BROAD_MEDIA_BLOCKS else 'DOMAIN-SUFFIX,netflix.com,REJECT'}]", encoding="utf-8")
    result = audit_netflix(tmp_path)
    assert result is True
