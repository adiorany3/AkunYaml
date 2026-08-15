#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 tidak ditemukan."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "[SETUP] Membuat virtual environment..."
  "$PYTHON" -m venv .venv
fi

".venv/bin/python" local_runner.py --config local_config.json
