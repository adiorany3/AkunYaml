#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
./mac_refresh_accounts.sh --push
printf '\nSelesai. Tekan Enter untuk menutup...'
read -r _
