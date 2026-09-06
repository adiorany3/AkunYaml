#!/bin/sh
set -eu

REPO_DIR="${REPO_DIR:-$(pwd)}"
BRANCH="${BRANCH:-main}"
CONFIG_NAME="${CONFIG_NAME:-openclash_auto.yaml}"
CORE="${MIHOMO_PATH:-/etc/openclash/core/clash_meta}"
DEST_DIR="${OPENCLASH_CONFIG_DIR:-/etc/openclash/config}"
DATA_DIR="${OPENCLASH_DATA_DIR:-/etc/openclash}"

case "$CONFIG_NAME" in
  ''|.*|*[!A-Za-z0-9_.-]*) echo "[ERROR] CONFIG_NAME harus nama file YAML, bukan path."; exit 2 ;;
esac

cd "$REPO_DIR"
REPO_DIR="$(pwd -P)"

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

VERSION="$("$CORE" -v 2>/dev/null || true)"
case "$VERSION" in
  *alpha*e183c58*) ;;
  *)
    echo "[ERROR] Core router bukan alpha-ge183c58."
    echo "        $VERSION"
    exit 4
    ;;
esac

echo "[CORE] $VERSION"

# Versi provider terpisah: kegagalan update tidak menyentuh provider aktif.
mkdir -p "$DATA_DIR" "$DEST_DIR"
DATA_DIR="$(cd "$DATA_DIR" && pwd -P)"
case "$DATA_DIR" in
  *[!A-Za-z0-9_./-]*) echo "[ERROR] Path data mengandung karakter tidak didukung."; exit 2 ;;
esac
STAGE="$(mktemp -d "$DATA_DIR/akunyaml-release.XXXXXX")"
TMP_CONFIG=""
KEEP_STAGE=0
cleanup() {
  if [ -n "$TMP_CONFIG" ]; then rm -f "$TMP_CONFIG"; fi
  if [ "$KEEP_STAGE" -eq 0 ]; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT
trap 'exit 1' HUP INT TERM
cp -R "$REPO_DIR/rule_providers" "$STAGE/rule_providers"
sed "s|\./rule_providers/|$STAGE/rule_providers/|g" "$CONFIG_NAME" > "$STAGE/config.yaml"
if ! "$CORE" -t -d "$STAGE" -f "$STAGE/config.yaml"; then
  echo "[ERROR] YAML/provider ditolak core. Konfigurasi aktif tidak diganti."
  exit 5
fi

# Rename dalam filesystem tujuan menjaga YAML lama sampai salinan lengkap siap.
TMP_CONFIG="$(mktemp "$DEST_DIR/.akunyaml-config.XXXXXX")"
cp "$STAGE/config.yaml" "$TMP_CONFIG"
# Simpan versi lama agar rollback tetap memiliki seluruh provider.
if [ -f "$DEST_DIR/$CONFIG_NAME" ]; then
  cp -p "$DEST_DIR/$CONFIG_NAME" "$DEST_DIR/$CONFIG_NAME.bak"
fi
KEEP_STAGE=1
mv -f "$TMP_CONFIG" "$DEST_DIR/$CONFIG_NAME"
echo "[OK] Disalin ke $DEST_DIR/$CONFIG_NAME"
echo "[OK] Provider versi ini: $STAGE/rule_providers"
echo "[INFO] Restart OpenClash tidak dilakukan otomatis. Terapkan/restart dari LuCI setelah pemeriksaan."
