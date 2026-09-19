#!/usr/bin/env bash
set -euo pipefail

# Update adblock list
python -m akunyaml.smart_update_adblock --candidates adblock_ai_candidates.txt --output suggested_blocklist.txt

# Run fresh pool generator (async URL testing)
python -m akunyaml.fresh_pool.fresh_pool_generator

# Run full audit with HTML report
python -m akunyaml.ads_audit --html-report audit_report.html

# Open HTML report for review
open audit_report.html

# Refresh proxy accounts
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
