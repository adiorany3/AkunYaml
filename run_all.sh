#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "[ERROR] python3 tidak tersedia." >&2
  exit 2
}

case "${1:-}" in
  -h|--help) exec ./mac_refresh_accounts.sh "$@" ;;
esac

PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY=python3
"$PY" -m pytest -q
"$PY" ads_audit.py --html-report audit_report.html

if command -v open >/dev/null 2>&1 && [ -f audit_report.html ]; then
  open audit_report.html
fi

exit 0
