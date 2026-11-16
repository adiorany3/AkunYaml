#!/usr/bin/env bash
# Full-refresh entry point. Forces every cache to revalidate so accounts,
# proxies, rule providers, and security feeds are as fresh as the network allows.
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PY" ]] || PY="${PYTHON:-python3}"

if [[ "${1:-}" == "--offline" || "${1:-}" == "--security-only" ]]; then
  exec "$PY" "$ROOT/unified_update.py" "$@"
fi

# Force refresh: subscription, provider, and security feed caches revalidate now.
export SUBSCRIPTION_CACHE_TTL_SEC=0
export PROVIDER_CACHE_TTL_SEC=3600
export FEED_REFRESH_TTL_SEC=0
export REFRESH_SECURITY_FEEDS=true
export ADAPTIVE_CANDIDATES=true

exec "$PY" "$ROOT/unified_update.py" "$@"
