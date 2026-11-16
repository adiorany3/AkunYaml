#!/usr/bin/env bash

# Full-refresh entry point. Forces every cache to revalidate so accounts,
# proxies, rule providers, and security feeds are as fresh as the network allows.
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PY" ]] || PY="${PYTHON:-python3}"

# Only successful updates refresh the suggested commit summary.
if [[ "${1:-}" != "--offline" && "${1:-}" != "--security-only" ]]; then
  export SUBSCRIPTION_CACHE_TTL_SEC=0
  export PROVIDER_CACHE_TTL_SEC=3600
  export FEED_REFRESH_TTL_SEC=0
  export REFRESH_SECURITY_FEEDS=true
  export ADAPTIVE_CANDIDATES=true
fi

"$PY" "$ROOT/unified_update.py" "$@"
status=$?
if [[ $status -ne 0 ]]; then
  exit "$status"
fi

if [[ -d "$ROOT/.git" ]]; then
  printf 'Update AkunYaml %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" > "$ROOT/.git/COMMIT_EDITMSG"
  printf '[OK] Suggested GitHub Desktop summary: Update AkunYaml %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
fi

