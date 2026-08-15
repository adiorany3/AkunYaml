#!/bin/sh
# ConvertYAML/OpenClash router audit and fixer v2.0
# Audit: sh openclash_router_fix.sh
# Fix:   sh openclash_router_fix.sh --fix

set -u

MODE="${1:-audit}"
BASE="/etc/openclash"
CORE="$BASE/core/clash_meta"
INIT="/etc/init.d/openclash"
SAFE_PATHS_VALUE="/usr/share/openclash:/etc/ssl"
STAMP="$(date +%Y%m%d-%H%M%S 2>/dev/null || echo backup)"

say() { printf '%s\n' "$*"; }
sep() { say "------------------------------------------------------------"; }

get_raw_config() {
  P=""
  if command -v uci >/dev/null 2>&1; then
    P="$(uci -q get openclash.config.config_path 2>/dev/null || true)"
  fi
  [ -n "$P" ] || P="$BASE/config/config.yaml"
  printf '%s' "$P"
}

RAW_CONFIG="$(get_raw_config)"
RAW_NAME="$(basename "$RAW_CONFIG")"
START_CONFIG="$BASE/$RAW_NAME"

if [ -f "$BASE/config.yaml" ]; then
  FINAL_CONFIG="$BASE/config.yaml"
elif [ -f "$START_CONFIG" ]; then
  FINAL_CONFIG="$START_CONFIG"
else
  FINAL_CONFIG="$RAW_CONFIG"
fi

say "OpenClash Router Audit/Fix v2.0"
sep
say "Mode           : $MODE"
say "Raw config     : $RAW_CONFIG"
say "Startup config : $START_CONFIG"
say "Final config   : $FINAL_CONFIG"
say "Core           : $CORE"
say "SAFE_PATHS     : $SAFE_PATHS_VALUE"
sep

say ""
say "[OpenClash package]"
if command -v opkg >/dev/null 2>&1; then
  opkg list-installed 2>/dev/null | grep -i openclash || true
elif command -v apk >/dev/null 2>&1; then
  apk info 2>/dev/null | grep -i openclash || true
fi

say ""
say "[Core version]"
if [ -x "$CORE" ]; then
  "$CORE" -v 2>/dev/null || "$CORE" version 2>/dev/null || true
else
  say "core tidak ditemukan"
fi

say ""
say "[Init SAFE_PATHS]"
if [ -f "$INIT" ]; then
  grep -n 'SAFE_PATHS' "$INIT" 2>/dev/null || say "TIDAK DITEMUKAN"
else
  say "init tidak ditemukan"
fi

scan() {
  PAT="$1"
  TITLE="$2"
  say ""
  say "[$TITLE]"
  FOUND=0

  if [ -d "$BASE/config" ]; then
    grep -RnsE "$PAT" "$BASE/config" 2>/dev/null && FOUND=1
  fi
  for f in "$BASE"/*.yaml "$BASE"/config.yaml; do
    [ -f "$f" ] || continue
    grep -nE "$PAT" "$f" 2>/dev/null | sed "s#^#$f:#" && FOUND=1
  done
  if [ -d "$BASE/custom" ]; then
    grep -RnsE "$PAT" "$BASE/custom" 2>/dev/null && FOUND=1
  fi
  [ "$FOUND" -eq 1 ] || say "tidak ditemukan"
}

scan 'GEOSITE,[[:space:]]*tracker([[:space:]]*,|$)' "GEOSITE tracker"
scan 'global-client-fingerprint[[:space:]]*:' "global-client-fingerprint"
scan 'geosite:category-ads-all,tracker' "stale DNS ads+tracker key"
scan 'external-ui.*\/usr\/share\/openclash\/ui' "external-ui OpenClash"

fix_yaml() {
  F="$1"
  [ -f "$F" ] || return 0

  if ! grep -Eq 'GEOSITE,[[:space:]]*tracker([[:space:]]*,|$)|global-client-fingerprint[[:space:]]*:|geosite:category-ads-all,tracker' "$F" 2>/dev/null; then
    return 0
  fi

  BAK="$F.pre-convertyaml-v2-$STAMP.bak"
  cp -p "$F" "$BAK" || return 1
  say "[BACKUP] $BAK"

  TMP="$F.tmp.$$"
  sed -E \
    -e '/GEOSITE,[[:space:]]*tracker,[[:space:]]*REJECT/d' \
    -e '/^[[:space:]]*global-client-fingerprint[[:space:]]*:/d' \
    -e '/geosite:category-ads-all,tracker[[:space:]]*:/d' \
    "$F" > "$TMP" || {
      rm -f "$TMP"
      return 1
    }
  mv "$TMP" "$F"
  say "[FIXED] $F"
}

fix_custom_list() {
  F="$1"
  [ -f "$F" ] || return 0

  case "$F" in
    *.sh|*.rb)
      if grep -Eq 'GEOSITE,[[:space:]]*tracker|global-client-fingerprint|geosite:category-ads-all,tracker' "$F" 2>/dev/null; then
        say "[MANUAL] injector script masih memuat pola lama: $F"
      fi
      return 0
      ;;
  esac

  if ! grep -Eq 'GEOSITE,[[:space:]]*tracker([[:space:]]*,|$)' "$F" 2>/dev/null; then
    return 0
  fi

  BAK="$F.pre-convertyaml-v2-$STAMP.bak"
  cp -p "$F" "$BAK" || return 1
  TMP="$F.tmp.$$"
  sed -E \
    -e '/GEOSITE,[[:space:]]*tracker,[[:space:]]*REJECT/d' \
    "$F" > "$TMP" || {
      rm -f "$TMP"
      return 1
    }
  mv "$TMP" "$F"
  say "[FIXED] $F"
}

if [ "$MODE" = "--fix" ] || [ "$MODE" = "fix" ]; then
  say ""
  sep
  say "APPLY FIX"

  fix_yaml "$RAW_CONFIG"
  fix_yaml "$START_CONFIG"
  fix_yaml "$BASE/config.yaml"

  if [ -d "$BASE/config" ]; then
    find "$BASE/config" -type f \( -name '*.yaml' -o -name '*.yml' \) 2>/dev/null |
    while IFS= read -r f; do fix_yaml "$f"; done
  fi

  if [ -d "$BASE/custom" ]; then
    find "$BASE/custom" -type f 2>/dev/null |
    while IFS= read -r f; do fix_custom_list "$f"; done
  fi
fi

say ""
sep
say "VALIDATION WITH OPENCLASH SAFE_PATHS"
if [ -x "$CORE" ] && [ -f "$FINAL_CONFIG" ]; then
  SAFE_PATHS="$SAFE_PATHS_VALUE" "$CORE" -t -d "$BASE" -f "$FINAL_CONFIG"
  RC=$?
else
  say "Core atau final config tidak tersedia"
  RC=2
fi
say "Exit code: $RC"

say ""
sep
if [ "$RC" -eq 0 ]; then
  say "CONFIG VALID."
else
  say "CONFIG MASIH GAGAL."
  say "Error tepat di atas adalah penyebab aktif berikutnya."
fi

if [ -f "$INIT" ] && ! grep -q 'SAFE_PATHS' "$INIT" 2>/dev/null; then
  say ""
  say "PERINGATAN: /etc/init.d/openclash tidak terlihat menyetel SAFE_PATHS."
  say "Jangan patch init otomatis. Update OpenClash atau sesuaikan service secara manual."
fi

say ""
say "Catatan: external-ui /usr/share/openclash/ui valid saat core dijalankan"
say "dengan SAFE_PATHS=/usr/share/openclash:/etc/ssl."

exit "$RC"
