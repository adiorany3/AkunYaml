#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Pada macOS gunakan workflow khusus yang melakukan git pull, exact-core build,
# pencarian akun, generate, dan validasi.
if [[ "$(uname -s)" == "Darwin" ]]; then
  exec ./mac_refresh_accounts.sh "$@"
fi

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 tidak ditemukan."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "[SETUP] Membuat virtual environment..."
  "$PYTHON" -m venv .venv
fi

".venv/bin/python" -m pip install --disable-pip-version-check -q -r requirements.txt
".venv/bin/python" local_runner.py --config local_config.json "$@"
