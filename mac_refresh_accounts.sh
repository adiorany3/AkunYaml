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
  --max-nodes N         Override jumlah node output.
  --min-nodes N         Override minimum node output.
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
echo "[SETUP] Memastikan dependency Python..."
"$PY" -m pip install --disable-pip-version-check -q -r requirements.txt

# Mac membangun validator exact dari source commit target jika belum ada.
"$ROOT/mac_build_target_core.sh"
CORE="$ROOT/.local_bin/mihomo"

echo "[CORE] $($CORE -v | head -1)"

ARGS=(
  "$PY" local_runner.py
  --config local_config.json
  --mihomo-path "$CORE"
)
[[ -n "$MAX_NODES" ]] && ARGS+=(--max-nodes "$MAX_NODES")
[[ -n "$MIN_NODES" ]] && ARGS+=(--min-nodes "$MIN_NODES")
[[ -n "$CANDIDATE_MIN" ]] && ARGS+=(--candidate-min "$CANDIDATE_MIN")

echo "[RUN] Mencari, mengetes, dan memilih akun baru..."
"${ARGS[@]}"

echo "[ADBLOCK] Audit rule YouTube dan perlindungan playback..."
"$PY" youtube_adblock_audit.py --mode enhanced

echo "[VALIDATE] Memeriksa output final dengan exact core..."
"$PY" validate_openclash_target.py --core "$CORE" \
  openclash_auto.yaml \
  openclash_android.yaml \
  openclash_lite.yaml \
  openclash_fresh_pool.yaml

printf '\n[OK] Refresh akun selesai.\n'
printf '     OpenClash utama: %s/openclash_auto.yaml\n' "$ROOT"
printf '     Akun URI       : %s/akun.txt\n' "$ROOT"
printf '     Fresh pool     : %s/fresh_pool/\n' "$ROOT"

if [[ -d .git ]]; then
  printf '\n[GIT] Perubahan hasil generator:\n'
  git status --short
fi

if [[ "$DO_PUSH" -eq 1 ]]; then
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
