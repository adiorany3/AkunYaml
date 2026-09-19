# tests/test_audit_config.py
import sys
from pathlib import Path

# Ensure repository root is on sys.path for imports
repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root))

from ads_audit import _cfg, AUDITS, FILES, NETFLIX_PLAYBACK, BROAD_MEDIA_BLOCKS


def test_default_config_values():
    # Verify that defaults from config.yaml are loaded correctly.
    assert isinstance(FILES, tuple) and len(FILES) > 0
    assert isinstance(NETFLIX_PLAYBACK, set) and len(NETFLIX_PLAYBACK) > 0
    # BROAD_MEDIA_BLOCKS is empty by default (can be overridden)
    assert isinstance(BROAD_MEDIA_BLOCKS, set)
    assert len(BROAD_MEDIA_BLOCKS) == 0
    # AUDITS should be a tuple with at least one entry
    assert isinstance(AUDITS, tuple) and len(AUDITS) > 0


def test_cfg_helper_fallback():
    # When a key is missing, _cfg should return the provided default.
    assert _cfg("nonexistent_key", "default") == "default"
