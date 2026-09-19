#!/usr/bin/env bash
set -euo pipefail

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Lint (disabled)
pip install ruff
# ruff check . (disabled)

# Type check (disabled)
pip install mypy
# mypy . (disabled)

# Run tests
pip install pytest
pytest -q

# Run ads audit HTML report
python ads_audit.py --html-report audit_report.html || true
# Open HTML report
open audit_report.html || true

# Refresh proxy accounts
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
set -euo pipefail

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Lint (disabled)
pip install ruff
# ruff check . (disabled)

# Type check (disabled)
pip install mypy
# mypy . (disabled)

# Run tests
pip install pytest
pytest -q

# Run ads audit HTML report
python ads_audit.py --html-report audit_report.html || true
# Open HTML report
open audit_report.html || true

# Refresh proxy accounts
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
# END_OF_SCRIPT
set -euo pipefail

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Lint (disabled)
pip install ruff
# ruff check . (disabled)

# Type check (disabled)
pip install mypy
# mypy . (disabled)

# Run tests
pip install pytest
pytest -q

# Run ads audit HTML report
python ads_audit.py --html-report audit_report.html || true
# Open HTML report
open audit_report.html || true

# Refresh proxy accounts
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
set -euo pipefail

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Lint
pip install ruff
# ruff check . (disabled)

# Type check
pip install mypy
# mypy . (disabled)

# Run tests
pip install pytest
pytest -q
pip install pytest
pytest -q

# Run ads audit with HTML report
python ads_audit.py --html-report audit_report.html || true
# Open HTML report
open audit_report.html || true

# Refresh accounts using mac_refresh_accounts.sh
if [[ -f ./mac_refresh_accounts.sh ]]; then
    chmod +x ./mac_refresh_accounts.sh
    ./mac_refresh_accounts.sh || true
else
    echo "mac_refresh_accounts.sh not found"
fi
