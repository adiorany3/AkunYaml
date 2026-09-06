#!/usr/bin/env bash
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

# local_runner hanya memasang dependency jika import belum tersedia.
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

STALE_FALLBACK=0
GENERATOR_LOG="$(mktemp -t akunyaml-generator.XXXXXX)"
trap 'rm -f "$GENERATOR_LOG"' EXIT

echo "[RUN] Mencari, mengetes, dan memilih akun baru..."
set +e
"${ARGS[@]}" >"$GENERATOR_LOG" 2>&1
GENERATOR_EXIT=$?
set -e
cat "$GENERATOR_LOG"
if [[ "$GENERATOR_EXIT" -ne 0 ]]; then
  REQUIRED_OUTPUTS=(openclash_auto.yaml openclash_android.yaml singbox_android.json openclash_lite.yaml openclash_fresh_pool.yaml akun.txt)
  MISSING_OUTPUTS=()
  for f in "${REQUIRED_OUTPUTS[@]}"; do
    [[ -s "$f" ]] || MISSING_OUTPUTS+=("$f")
  done
  if grep -q "Node otomatis hidup hanya" "$GENERATOR_LOG" \
      && grep -q "output lama dipertahankan" "$GENERATOR_LOG" \
      && [[ ${#MISSING_OUTPUTS[@]} -eq 0 ]]; then
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
"$PY" adblock_provider_audit.py
"$PY" app_ad_audit.py
"$PY" cctv_app_audit.py
"$PY" dns_speed_policy_audit.py
"$PY" dns_leak_audit.py
"$PY" popup_game_ad_audit.py
"$PY" youtube_adblock_audit.py --mode enhanced --dedup lean
"$PY" youtube_gambling_sponsor_audit.py
"$PY" threat_safe_audit.py
"$PY" security_hardening_audit.py
"$PY" openwrt_adblock_audit.py
"$PY" performance_budget_audit.py
"$PY" load_balance_policy_audit.py
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
"$SINGBOX" check -c singbox_android.json

if [[ "$STALE_FALLBACK" -eq 1 ]]; then
  printf '\n[OK] Output known-good lama lolos seluruh audit; refresh akun ditunda.\n'
else
  printf '\n[OK] Refresh akun selesai.\n'
fi
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
