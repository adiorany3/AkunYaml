#!/bin/sh
set -eu

REPO_DIR="${REPO_DIR:-$(pwd)}"
BRANCH="${BRANCH:-main}"
CONFIG_NAME="${CONFIG_NAME:-openclash_auto.yaml}"
CORE="${MIHOMO_PATH:-/etc/openclash/core/clash_meta}"
DEST_DIR="${OPENCLASH_CONFIG_DIR:-/etc/openclash/config}"

cd "$REPO_DIR"

if [ ! -d .git ]; then
  echo "[ERROR] $REPO_DIR bukan repository git clone."
  exit 2
fi

if ! command -v git >/dev/null 2>&1; then
  echo "[ERROR] git belum terpasang di OpenWrt."
  exit 2
fi

echo "[GIT] Pull origin/$BRANCH..."
git pull --ff-only origin "$BRANCH"

if [ ! -f "$CONFIG_NAME" ]; then
  echo "[ERROR] YAML tidak ditemukan: $CONFIG_NAME"
  exit 3
fi

if [ ! -x "$CORE" ]; then
  echo "[ERROR] Core OpenClash tidak ditemukan/executable: $CORE"
  exit 4
fi

VERSION="$($CORE -v 2>/dev/null || true)"
case "$VERSION" in
  *alpha*e183c58*) ;;
  *)
    echo "[ERROR] Core router bukan alpha-ge183c58."
    echo "        $VERSION"
    exit 4
    ;;
esac

echo "[CORE] $VERSION"

# Parser test langsung dengan core router. Tidak membutuhkan Python.
TMP_HOME="/tmp/akunyaml-openclash-test"
rm -rf "$TMP_HOME"
mkdir -p "$TMP_HOME"
if ! "$CORE" -t -d "$TMP_HOME" -f "$REPO_DIR/$CONFIG_NAME"; then
  echo "[ERROR] YAML terbaru ditolak oleh core target. File OpenClash tidak diganti."
  rm -rf "$TMP_HOME"
  exit 5
fi
rm -rf "$TMP_HOME"

echo "[OK] YAML lolos parser target."
mkdir -p "$DEST_DIR"
cp "$CONFIG_NAME" "$DEST_DIR/$CONFIG_NAME"
echo "[OK] Disalin ke $DEST_DIR/$CONFIG_NAME"
echo "[INFO] Restart OpenClash tidak dilakukan otomatis. Terapkan/restart dari LuCI setelah pemeriksaan."
