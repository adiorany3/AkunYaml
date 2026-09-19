#!/usr/bin/env bash
set -euo pipefail

# Install dependencies (if not already installed)
python -m pip install --upgrade pip
pip install -r requirements.txt

# Update adblock rules using the smart update script
python -m akunyaml.smart_update_adblock --candidates adblock_ai_candidates.txt --output suggested_blocklist.txt
# Open the generated suggestions file for quick review
open suggested_blocklist.txt

# Refresh proxy accounts (mac_refresh_accounts.sh)
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh
else
    echo "mac_refresh_accounts.sh not found; skipping proxy refresh."
fi
