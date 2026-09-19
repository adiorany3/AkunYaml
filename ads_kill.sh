#!/usr/bin/env bash
set -euo pipefail

# Update adblock list
python smart_update_adblock.py --candidates adblock_ai_candidates.txt --output suggested_blocklist.txt

# Proxy health check (optional, controlled by config)
if command -v python >/dev/null 2>&1; then
    python proxy_health_check.py || true
fi

# Run fresh pool generator (async URL testing)
python fresh_pool/fresh_pool_generator.py

# Run full audit with HTML report
python ads_audit.py --html-report audit_report.html

# Open HTML report for review
open audit_report.html

# Refresh proxy accounts
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
