"""One local check command; full adds real-core checks without running a refresh."""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="Validasi integrasi gameblock lokal dengan core Mihomo/Sing-box")
    args = parser.parse_args()
    commands = [[sys.executable, "-m", "pytest", "-q", "tests"],
                [sys.executable, "-m", "ruff", "check", "domain_policy_tools.py", "singbox_gameblock.py", "release_tools.py", "node_history.py", "check_local.py", "health_report.py", "unified_update.py", "rule_simulation.py", "tests/test_health_report.py", "tests/test_development_tools.py", "adaptive_guard.py", "tests/test_adaptive_guard.py", "tests/test_policy_parity.py"]]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    if args.full:
        import json
        import shutil

        import yaml

        from build_support import PROFILE, validate
        from singbox_gameblock import build

        # Test local-policy integration in throwaway copies, never published output.
        with tempfile.TemporaryDirectory() as temporary:
            stage = Path(temporary) / "gameblock"
            shutil.copytree(ROOT / "local_build/gameblock", stage)
            clash = yaml.safe_load((stage / PROFILE).read_text())
            if any(p.get("type") == "http" for p in clash.get("rule-providers", {}).values()):
                print("[ERROR] Integrasi offline membutuhkan provider lokal")
                return 2
            validate(stage, ROOT / ".local_bin/mihomo")
            config = build(json.loads((ROOT / "local_build/singbox_direct_adblock.json").read_text()), clash, stage, ROOT / ".local_bin/mihomo")
            path = stage / "singbox_gameblock.json"
            path.write_text(json.dumps(config))
            result = subprocess.run([str(ROOT / ".local_bin/sing-box"), "check", "-c", str(path)], cwd=stage, check=False, timeout=120)
            if result.returncode:
                return result.returncode
        print("[OK] Integrasi gameblock Mihomo + Sing-box lulus core lokal")
    print("[OK] Pemeriksaan lokal selesai")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
