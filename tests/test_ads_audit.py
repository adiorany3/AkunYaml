# Simple test for ads_audit module
import sys
from pathlib import Path

# Ensure the repository root is on sys.path for imports
repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root))

from ads_audit import audit_netflix

def test_audit_netflix_no_files(tmp_path, monkeypatch):
    # Create a temporary directory without any of the expected YAML files
    # Monkeypatch Path(__file__) used inside audit_netflix to point to tmp_path
    monkeypatch.setattr('ads_audit.Path', lambda *args, **kwargs: tmp_path)
    # Since the function expects a Path argument, we pass the temporary directory
    result = audit_netflix(tmp_path)
    assert result is False
