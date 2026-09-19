# tests/test_main_report.py
import sys
from pathlib import Path
import json


def test_main_json_report(tmp_path, monkeypatch):
    # Ensure repository root is on sys.path for imports
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    # Prepare a temporary report path
    report_path = tmp_path / "audit_report.json"
    # Mock command‑line arguments
    monkeypatch.setattr(sys, "argv", ["ads_audit.py", "--report", str(report_path)])
    # Mock audit_netflix to return False (no failures)
    import ads_audit as audit_mod
    monkeypatch.setattr(audit_mod, "audit_netflix", lambda root: False)
    # Mock subprocess.run to simulate successful audit scripts
    class DummyResult:
        def __init__(self):
            self.returncode = 0
    monkeypatch.setattr(audit_mod.subprocess, "run", lambda *args, **kwargs: DummyResult())
    # Run the main function
    from ads_audit import main
    exit_code = main()
    assert exit_code == 0
    # Verify JSON report was created and contains expected keys
    data = json.loads(report_path.read_text())
    assert "failed" in data
    assert data["failed"] is False
    assert "audits" in data
    # There should be at least one audit entry (the default audits list)
    assert isinstance(data["audits"], list)
    assert len(data["audits"]) > 0
