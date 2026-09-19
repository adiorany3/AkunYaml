# tests/test_smart_update.py
import sys
from pathlib import Path


def test_smart_update(tmp_path, monkeypatch):
    # Create a dummy blocklist yaml with a rule for example.com
    block_yaml = tmp_path / "openclash_auto.yaml"
    block_yaml.write_text("rules:\n  - DOMAIN-SUFFIX,example.com,REJECT\n", encoding="utf-8")
    # Create a candidates file with example.com (already covered) and newdomain.com
    candidates = tmp_path / "candidates.txt"
    candidates.write_text("example.com\nnewdomain.com\n", encoding="utf-8")
    # Prepare output path
    output = tmp_path / "suggestions.txt"
    # Patch configuration to point to our temporary yaml file
    import yaml
    cfg_path = Path(__file__).parent.parent / "config.yaml"
    # If config exists, backup and replace temporarily
    if cfg_path.is_file():
        original = cfg_path.read_text()
        yaml.safe_load(cfg_path.read_text())
    # Monkeypatch FILES in smart_update_adblock module
    import smart_update_adblock as su
    monkeypatch.setattr(su, "FILES", (block_yaml.name,))
    # Run main with arguments
    monkeypatch.setattr(sys, "argv", ["smart_update_adblock.py", "--candidates", str(candidates), "--output", str(output)])
    # Ensure the script looks for files in the temporary directory
    monkeypatch.setattr(su.Path, "cwd", lambda: tmp_path)
    exit_code = su.main()
    assert exit_code == 0
    # Verify output contains only newdomain.com rule
    content = output.read_text().splitlines()
    assert len(content) == 1
    assert content[0] == "DOMAIN-SUFFIX,newdomain.com,REJECT"
