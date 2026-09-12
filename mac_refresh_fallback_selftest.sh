#!/bin/bash
# Offline regression check: bash mac_refresh_fallback_selftest.sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT
cd "$TEST_DIR"

# Bootstrap imports before runner startup; stub Python to avoid package/network changes.
BOOTSTRAP="$(awk '/^if ! "\$PY" -c/{copy=1} copy{print} copy && /^fi$/{exit}' "$ROOT/mac_refresh_accounts.sh")"
[[ -n "$BOOTSTRAP" ]]
fake_python() {
  printf '%s\n' "$*" >> "$TEST_DIR/python.log"
  if [[ "$1" == '-c' ]]; then return "$IMPORT_EXIT"; fi
  return "$INSTALL_EXIT"
}
PY=fake_python
for IMPORT_EXIT in 0 1; do
  INSTALL_EXIT=0
  : > "$TEST_DIR/python.log"
  eval "$BOOTSTRAP"
  [[ "$(wc -l < "$TEST_DIR/python.log")" -eq "$((IMPORT_EXIT + 1))" ]]
done
grep -q -- '-m pip install --disable-pip-version-check requests>=2.31 PyYAML>=6.0 certifi>=2024.2.2' "$TEST_DIR/python.log"
IMPORT_EXIT=1
INSTALL_EXIT=23
set +e
(set -e; eval "$BOOTSTRAP")
result=$?
set -e
[[ "$result" -eq 23 ]]
printf 'PASS: dependency bootstrap, installed fast path, pip failure stops startup\n'

# ponytail: test extracted gates only; add full script stubs for orchestration changes.
GATE="$(awk '/^if \[\[ "\$GENERATOR_EXIT" -ne 0 \]\]; then/{copy=1} copy{print} copy && /^fi$/{exit}' "$ROOT/mac_refresh_accounts.sh")"
[[ -n "$GATE" ]]
GENERATOR_LOG="$TEST_DIR/generator.log"
OUTPUTS=(openclash_auto.yaml openclash_android.yaml singbox_android.json openclash_lite.yaml openclash_fresh_pool.yaml akun.txt)
for file in "${OUTPUTS[@]}"; do printf 'fixture\n' > "$file"; done

check() {
  local expected="$1" generator_exit="$2" result
  : > "$GENERATOR_LOG"
  set +e
  (
    set -e
    GENERATOR_EXIT="$generator_exit"
    STALE_FALLBACK=0
    eval "$GATE"
    [[ "$STALE_FALLBACK" -eq 1 ]]
  ) > /dev/null 2>&1
  result=$?
  set -e
  if [[ "$result" -ne "$expected" ]]; then
    printf 'FAIL: expected %s, got %s: generator exit %s\n' "$expected" "$result" "$generator_exit"
    exit 1
  fi
}

check 0 3
check 23 23
for file in "${OUTPUTS[@]}"; do
  : > "$file"
  check 3 3
  rm "$file"
  check 3 3
  printf 'fixture\n' > "$file"
done
printf 'PASS: fallback exit-code contract, unrelated errors, missing/empty outputs\n'