#!/usr/bin/env python3
"""Smart update for adblock lists.

Scans candidate domains and suggests those not already present in any
existing blocklist YAML files defined in the configuration.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import yaml

# Module-level logger
logger = logging.getLogger(__name__)

# Load configuration (reuse logic from ads_audit if possible)
CONFIG_PATH = Path(__file__).with_name("config.yaml")
if CONFIG_PATH.is_file():
    _config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
else:
    _config = {}

def _cfg(key: str, default):
    return _config.get(key, default)

# Default files list – can be overridden via config.yaml
FILES = tuple(_cfg("files", ["openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml"]))


def load_rules_from_yaml(path: Path) -> set[str]:
    """Return a set of rule strings from a blocklist YAML file."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:  # ruff: noqa: BLE001
        logging.getLogger(__name__).error("Failed to read %s: %s", path, e)  # ruff: noqa: LOG015
        return set()
    # The YAML structure used in this repo stores rules under the key "rules"
    return {str(rule) for rule in data.get("rules", [])}


def main() -> int:
    parser = argparse.ArgumentParser(description="Smart adblock update")
    parser.add_argument("--candidates", type=Path, default=Path("adblock_ai_candidates.txt"), help="File with candidate domains, one per line")
    parser.add_argument("--output", type=Path, default=Path("suggested_blocklist.txt"), help="Where to write the suggested new rules")
    parser.add_argument("--log-file", type=Path, help="Optional log file")
    args = parser.parse_args()

    # Configure logging
    logger = logging.getLogger("smart_update")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Load all existing rules
    existing_rules: set[str] = set()
    for name in FILES:
        yaml_path = Path.cwd() / name
        if yaml_path.is_file():
            existing_rules.update(load_rules_from_yaml(yaml_path))
        else:
            logging.getLogger(__name__).warning("Blocklist file %s not found", yaml_path)

    # Load candidates (ignore comment lines and empty lines)
    candidates = []
    try:
        for line in args.candidates.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            candidates.append(line)
    except Exception as e:
        logging.getLogger(__name__).error("Failed to read candidates %s: %s", args.candidates, e)
        return 1

    # Determine which candidates are not already covered
    suggestions = []
    for domain in candidates:
        # Simple heuristic: if any existing rule contains the domain, we consider it covered.
        if any(domain in rule for rule in existing_rules):
            continue
        suggestions.append(f"DOMAIN-SUFFIX,{domain},REJECT")

    # Write suggestions
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(suggestions), encoding="utf-8")
        logging.getLogger(__name__).info("Wrote %d suggestions to %s", len(suggestions), args.output)
    except Exception as e:
        logging.getLogger(__name__).error("Failed to write suggestions: %s", e)
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
