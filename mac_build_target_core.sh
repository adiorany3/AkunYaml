#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

TARGET_COMMIT="e183c58"
TARGET_BRANCH="Alpha"
TARGET_LABEL="alpha-ge183c58"
CORE_OUT="${MIHOMO_PATH:-$PWD/.local_bin/mihomo}"
SRC_DIR="$PWD/.build/mihomo-e183c58"
REPO_URL="https://github.com/MetaCubeX/mihomo.git"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[ERROR] Script ini khusus macOS (Darwin)."
  exit 2
fi

mkdir -p "$(dirname "$CORE_OUT")" "$PWD/.build"

if [[ -x "$CORE_OUT" ]]; then
  VERSION="$($CORE_OUT -v 2>/dev/null || true)"
  if [[ "$VERSION" == *"alpha"* && "$VERSION" == *"$TARGET_COMMIT"* ]]; then
    echo "[OK] Mihomo exact target sudah tersedia: $CORE_OUT"
    echo "     $VERSION"
    exit 0
  fi
fi

for cmd in git go; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] '$cmd' belum tersedia di Mac."
    if [[ "$cmd" == "git" ]]; then
      echo "        Instal Xcode Command Line Tools: xcode-select --install"
    else
      echo "        Instal Go terlebih dahulu, lalu jalankan script ini lagi."
    fi
    exit 2
  fi
done

if [[ ! -d "$SRC_DIR/.git" ]]; then
  echo "[SETUP] Clone source Mihomo..."
  rm -rf "$SRC_DIR"
  git clone --filter=blob:none "$REPO_URL" "$SRC_DIR"
fi

cd "$SRC_DIR"
echo "[SETUP] Mengambil branch $TARGET_BRANCH agar commit $TARGET_COMMIT tersedia..."
# Short commit SHA bukan remote ref, jadi jangan menjalankan `git fetch origin e183c58`.
# Fetch branch Alpha terlebih dahulu, kemudian checkout commit target dari object database lokal.
git fetch --force --prune origin "+refs/heads/${TARGET_BRANCH}:refs/remotes/origin/${TARGET_BRANCH}"

if ! git cat-file -e "${TARGET_COMMIT}^{commit}" 2>/dev/null; then
  echo "[WARN] Commit $TARGET_COMMIT belum ditemukan setelah fetch $TARGET_BRANCH. Fetch seluruh heads..."
  git fetch --force --prune origin '+refs/heads/*:refs/remotes/origin/*'
fi

if ! git cat-file -e "${TARGET_COMMIT}^{commit}" 2>/dev/null; then
  echo "[ERROR] Commit target $TARGET_COMMIT tidak ditemukan di repository Mihomo."
  exit 3
fi

git checkout --detach "$TARGET_COMMIT"

# Pastikan commit yang dibangun tepat.
ACTUAL="$(git rev-parse --short=7 HEAD)"
if [[ "$ACTUAL" != "$TARGET_COMMIT" ]]; then
  echo "[ERROR] Commit Mihomo tidak sesuai. Target=$TARGET_COMMIT aktual=$ACTUAL"
  exit 3
fi

MACHINE="$(uname -m)"
case "$MACHINE" in
  arm64|aarch64)
    GOARCH="arm64"
    GOAMD64=""
    ;;
  x86_64|amd64)
    GOARCH="amd64"
    GOAMD64="v1"
    ;;
  *)
    echo "[ERROR] Arsitektur Mac tidak didukung: $MACHINE"
    exit 2
    ;;
esac

BUILD_TIME="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "[BUILD] Mihomo $TARGET_LABEL untuk macOS/$GOARCH..."

BUILD_ENV=(env CGO_ENABLED=0 GOOS=darwin GOARCH="$GOARCH")
if [[ -n "$GOAMD64" ]]; then
  BUILD_ENV+=(GOAMD64="$GOAMD64")
fi

"${BUILD_ENV[@]}" go build \
  -tags with_gvisor \
  -trimpath \
  -ldflags "-X github.com/metacubex/mihomo/constant.Version=$TARGET_LABEL -X github.com/metacubex/mihomo/constant.BuildTime=$BUILD_TIME -w -s -buildid=" \
  -o "$CORE_OUT" .

chmod +x "$CORE_OUT"
VERSION="$($CORE_OUT -v 2>/dev/null || true)"

if [[ "$VERSION" != *"alpha"* || "$VERSION" != *"$TARGET_COMMIT"* ]]; then
  echo "[ERROR] Binary hasil build tidak melaporkan target exact."
  echo "        $VERSION"
  exit 4
fi

echo "[OK] Exact core berhasil dibuat: $CORE_OUT"
echo "     $VERSION"
