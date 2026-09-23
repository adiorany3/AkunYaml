#!/usr/bin/env bash
# This script uses Bash arrays and PIPESTATUS, including when invoked via zsh.
if [ -z "${BASH_VERSION:-}" ]; then
    exec /bin/bash "$0" "$@"
fi
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$PWD"
DO_PULL=1
DO_PUSH=0
MAX_NODES=""
MIN_NODES=""
CANDIDATE_MIN=""

usage() {
  cat <<'TXT'
AkunYaml macOS refresh

Pemakaian:
  ./mac_refresh_accounts.sh
  ./mac_refresh_accounts.sh --push
  ./mac_refresh_accounts.sh --no-pull
  ./mac_refresh_accounts.sh --max-nodes 10 --min-nodes 6

Opsi:
  --push                Commit + push hasil generator ke branch aktif GitHub.
  --no-pull             Jangan git pull sebelum pencarian akun.
  --max-nodes N         Override baseline minimum node otomatis (nama opsi kompatibel lama).
  --min-nodes N         Override minimum total node output (otomatis + manual).
  --candidate-min N     Override minimum kandidat yang diperiksa.
  -h, --help            Bantuan.
TXT
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --push) DO_PUSH=1; shift ;;
    --no-pull) DO_PULL=0; shift ;;
    --max-nodes) MAX_NODES="${2:-}"; shift 2 ;;
    --min-nodes) MIN_NODES="${2:-}"; shift 2 ;;
    --candidate-min) CANDIDATE_MIN="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERROR] Opsi tidak dikenal: $1"; usage; exit 2 ;;
  esac
done

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[ERROR] Script ini khusus macOS."
  exit 2
fi

if ! command -v git >/dev/null 2>&1; then
  echo "[ERROR] git tidak tersedia. Jalankan: xcode-select --install"
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 tidak tersedia. Instal Python 3 terlebih dahulu."
  exit 2
fi

if [[ -d .git ]]; then
  BRANCH="$(git branch --show-current)"
  [[ -n "$BRANCH" ]] || BRANCH="main"

  if [[ "$DO_PULL" -eq 1 ]]; then
    echo "[GIT] Sinkronisasi branch $BRANCH dari GitHub..."
    # Autostash menjaga perubahan lokal sementara jika ada output lama yang belum dicommit.
    git pull --rebase --autostash origin "$BRANCH"
  fi
else
  echo "[WARN] Folder ini bukan hasil git clone. Pencarian akun tetap dijalankan,"
  echo "       tetapi git pull/push tidak tersedia. Untuk workflow GitHub gunakan:"
  echo "       git clone https://github.com/adiorany3/AkunYaml.git"
fi

if [[ ! -x .venv/bin/python ]]; then
  echo "[SETUP] Membuat Python virtual environment..."
  python3 -m venv .venv
fi

PY="$ROOT/.venv/bin/python"

# Bootstrap before local_runner imports modules that require PyYAML.
if ! "$PY" -c 'import requests, yaml, certifi'; then
  "$PY" -m pip install --disable-pip-version-check 'requests>=2.31' 'PyYAML>=6.0' 'certifi>=2024.2.2'
fi
# Mac membangun validator exact dari source commit target jika belum ada.
"$ROOT/mac_build_target_core.sh"
CORE="$ROOT/.local_bin/mihomo"

CORE_VERSION="$($CORE -v)"
echo "[CORE] ${CORE_VERSION%%$'\n'*}"

ARGS=(
  "$PY" local_runner.py
  --config local_config.json
  --mihomo-path "$CORE"
)
[[ -n "$MAX_NODES" ]] && ARGS+=(--max-nodes "$MAX_NODES")
[[ -n "$MIN_NODES" ]] && ARGS+=(--min-nodes "$MIN_NODES")
[[ -n "$CANDIDATE_MIN" ]] && ARGS+=(--candidate-min "$CANDIDATE_MIN")

# Explicit refresh checks every subscription/feed now; HTTP validators still avoid
# downloading unchanged content, stale cache remains available on network failure.
export SUBSCRIPTION_CACHE_TTL_SEC=0
export FEED_REFRESH_TTL_SEC=0
export REFRESH_SECURITY_FEEDS=true

STALE_FALLBACK=0
GENERATOR_LOG="$(mktemp -t akunyaml-generator.XXXXXX)"
trap 'RUN_EXIT=$?; printf "\n[STATUS] Refresh berakhir: exit=%s; log generator: %s\n" "$RUN_EXIT" "$GENERATOR_LOG"' EXIT

echo "[RUN] Refresh subscription/proxy, akun, adblock, generate, dan pilih node sehat terbaru..."
echo "[INFO] Log langsung: $GENERATOR_LOG"
echo "[INFO] Batch AI ditampilkan saat berjalan; selesai AI belum berarti audit/validasi selesai."
set +e
PYTHONUNBUFFERED=1 "${ARGS[@]}" 2>&1 | tee "$GENERATOR_LOG"
PIPELINE_STATUS=("${PIPESTATUS[@]}")
GENERATOR_EXIT=${PIPELINE_STATUS[0]}
set -e
if [[ ${PIPELINE_STATUS[1]} -ne 0 ]]; then
    echo "[ERROR] Gagal menulis log generator."
    exit "${PIPELINE_STATUS[1]}"
fi
echo "[RUN] Generator berakhir: exit=$GENERATOR_EXIT"

# Keep the standalone no-proxy profile aligned with refreshed manual nodes.
if [[ -s openclash_auto.yaml && -s openclash_noproxy.yaml ]]; then
  "$PY" - <<'PY'
from pathlib import Path
import yaml

auto_path = Path("openclash_auto.yaml")
noproxy_path = Path("openclash_noproxy.yaml")
auto = yaml.safe_load(auto_path.read_text()) or {}
noproxy = yaml.safe_load(noproxy_path.read_text()) or {}
manual_types = {"vmess", "vless", "trojan", "ss", "socks5", "http"}
manual = [
    proxy for proxy in auto.get("proxies", [])
    if isinstance(proxy, dict)
    and str(proxy.get("name", "")).startswith("MANUAL-")
    and str(proxy.get("type", "")).lower() in manual_types
]
if manual:
    existing = [proxy for proxy in noproxy.get("proxies", []) if isinstance(proxy, dict)]
    refreshed_names = {proxy["name"] for proxy in manual}
    noproxy["proxies"] = [proxy for proxy in existing if proxy.get("name") not in refreshed_names] + manual
    groups = noproxy.setdefault("proxy-groups", [])
    group = next((item for item in groups if item.get("name") == "MANUAL"), None)
    if group is None:
        group = {"name": "MANUAL", "type": "select", "proxies": []}
        groups.insert(0, group)
    group["type"] = "select"
    group["proxies"] = ["DIRECT", *[proxy["name"] for proxy in manual]]
    noproxy_path.write_text(yaml.safe_dump(noproxy, sort_keys=False, allow_unicode=True))
    print(f"[SYNC] {noproxy_path}: {len(manual)} manual node(s)")
else:
    print("[SYNC] Tidak ada node MANUAL-* baru; noproxy dipertahankan.")
PY
fi
if [[ "$GENERATOR_EXIT" -ne 0 ]]; then
  REQUIRED_OUTPUTS=(openclash_auto.yaml openclash_android.yaml singbox_android.json openclash_lite.yaml openclash_fresh_pool.yaml akun.txt)
  MISSING_OUTPUTS=()
  for f in "${REQUIRED_OUTPUTS[@]}"; do
    [[ -s "$f" ]] || MISSING_OUTPUTS+=("$f")
  done
  if [[ "$GENERATOR_EXIT" -eq 3 && ${#MISSING_OUTPUTS[@]} -eq 0 ]]; then
    STALE_FALLBACK=1
    echo "[WARN] Feed tidak memberi minimum node sehat; memakai output known-good lama."
    echo "[WARN] Audit penuh tetap wajib; --push akan ditolak."
  else
    echo "[ERROR] Pipeline generator gagal, exit=$GENERATOR_EXIT"
    if [[ ${#MISSING_OUTPUTS[@]} -gt 0 ]]; then
      echo "[ERROR] Output fallback hilang: ${MISSING_OUTPUTS[*]}"
    fi
    exit "$GENERATOR_EXIT"
  fi
fi

echo "[AUDIT] Memeriksa keamanan, adblock, kategori judi, dan budget performa..."
"$PY" ads_audit.py
"$PY" cctv_app_audit.py
"$PY" child_safe_search_audit.py
"$PY" dns_speed_policy_audit.py
"$PY" dns_leak_audit.py
"$PY" threat_safe_audit.py
"$PY" security_hardening_audit.py
"$PY" openwrt_adblock_audit.py
"$PY" performance_budget_audit.py
"$PY" load_balance_policy_audit.py
"$PY" android_marketplace_live_audit.py
"$PY" test_android_gambling_adblock.py
"$PY" semantic_rule_audit.py \
  openclash_auto.yaml \
  openclash_android.yaml \
  openclash_lite.yaml \
  openclash_fresh_pool.yaml

echo "[VALIDATE] Memeriksa output final dengan exact core..."
"$PY" validate_openclash_target.py --core "$CORE" \
  openclash_auto.yaml \
  openclash_android.yaml \
  openclash_lite.yaml \
  openclash_fresh_pool.yaml

echo "[VALIDATE] Memeriksa profil sing-box Android..."
SINGBOX="${SINGBOX_PATH:-}"
if [[ -z "$SINGBOX" || ! -x "$SINGBOX" ]]; then
  SINGBOX="$(command -v sing-box || true)"
fi
if [[ -z "$SINGBOX" || ! -x "$SINGBOX" ]]; then
  SINGBOX="$ROOT/.local_bin/sing-box"
fi
if [[ ! -x "$SINGBOX" ]]; then
  echo "[ERROR] sing-box binary tidak ditemukan. Set SINGBOX_PATH atau instal sing-box."
  exit 7
fi
SINGBOX_VERSION="$($PY -c 'from openclash_target import assert_target_singbox; import sys; print(assert_target_singbox(sys.argv[1]))' "$SINGBOX")"
echo "[SINGBOX] ${SINGBOX_VERSION%%$'\n'*}"
"$SINGBOX" check -c singbox_android.json

if [[ "$STALE_FALLBACK" -eq 1 ]]; then
  printf '\n[OK] Output known-good lama lolos seluruh audit; refresh akun ditunda.\n'
else
  printf '\n[OK] Refresh akun selesai.\n'
fi
printf '[INFO] Blocklist iklan berhasil diperbarui.\n'
printf '     OpenClash utama: %s/openclash_auto.yaml\n' "$ROOT"
printf '     sing-box Android: %s/singbox_android.json\n' "$ROOT"
printf '     Akun URI       : %s/akun.txt\n' "$ROOT"
printf '     Fresh pool     : %s/fresh_pool/\n' "$ROOT"

if [[ -d .git ]]; then
  printf '\n[GIT] Perubahan hasil generator:\n'
  git status --short
fi

if [[ "$DO_PUSH" -eq 1 ]]; then
  if [[ "$STALE_FALLBACK" -eq 1 ]]; then
    echo "[ERROR] --push ditolak: refresh memakai output known-good lama."
    exit 6
  fi
  if [[ ! -d .git ]]; then
    echo "[ERROR] --push membutuhkan repository hasil git clone."
    exit 5
  fi

  BRANCH="$(git branch --show-current)"
  [[ -n "$BRANCH" ]] || BRANCH="main"

  # Commit hanya output dan laporan yang memang berubah karena refresh.
  FILES=(
    openclash_auto.yaml
    openclash_android.yaml
    rule_providers/popup-ads_android.yaml
    openclash_lite.yaml
    openclash_fresh_pool.yaml
    singbox_android.json
    akun.txt
    akun_manual.txt
    last_update.txt
    openclash_auto_report.csv
    openclash_compat_report.csv
    urltest_report.csv
    nekobox_test_report.csv
    node_quality_report.md
    fresh_pool/fresh_candidates.txt
    fresh_pool/fresh_candidates_strict.txt
    fresh_pool/fresh_candidates.json
    fresh_pool/fresh_candidates_report.md
  )

  EXISTING=()
  for f in "${FILES[@]}"; do
    [[ -e "$f" ]] && EXISTING+=("$f")
  done
  if [[ ${#EXISTING[@]} -gt 0 ]]; then
    git add -- "${EXISTING[@]}"
  fi

  if git diff --cached --quiet; then
    echo "[GIT] Tidak ada perubahan output untuk dipush."
  else
    STAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
    git commit -m "refresh accounts: $STAMP"
    git push origin "$BRANCH"
    echo "[GIT] Hasil terbaru sudah dipush ke origin/$BRANCH."
  fi
fi
