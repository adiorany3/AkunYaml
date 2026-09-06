#!/bin/sh
# Offline regression check: sh openwrt_update_selftest.sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TEST_DIR="$(mktemp -d /tmp/akunyaml-update-test.XXXXXX)"
trap 'rm -rf "$TEST_DIR"' EXIT
trap 'exit 1' HUP INT TERM
mkdir -p "$TEST_DIR/bin" "$TEST_DIR/repo/.git" "$TEST_DIR/repo/rule_providers" "$TEST_DIR/config"
cat > "$TEST_DIR/bin/git" <<'EOF'
#!/bin/sh
exit 0
EOF
cat > "$TEST_DIR/bin/core" <<'EOF'
#!/bin/sh
set -eu
if [ "$1" = -v ]; then echo 'Mihomo alpha-ge183c58'; exit 0; fi
[ "$1" = -t ] && [ "$2" = -d ] && [ "$4" = -f ]
[ -s "$3/rule_providers/test.yaml" ]
grep -F "path: $3/rule_providers/test.yaml" "$5" >/dev/null
[ "${FAIL_VALIDATION:-0}" = 0 ]
EOF
chmod +x "$TEST_DIR/bin/git" "$TEST_DIR/bin/core"
export PATH="$TEST_DIR/bin:$PATH"
export REPO_DIR="$TEST_DIR/repo"
export MIHOMO_PATH="$TEST_DIR/bin/core"
export OPENCLASH_CONFIG_DIR="$TEST_DIR/config"
export OPENCLASH_DATA_DIR="$TEST_DIR/data"
export CONFIG_NAME=openclash_auto.yaml
printf 'path: ./rule_providers/test.yaml\n' > "$REPO_DIR/$CONFIG_NAME"
printf 'payload: [example.com]\n' > "$REPO_DIR/rule_providers/test.yaml"
printf 'old config\n' > "$OPENCLASH_CONFIG_DIR/$CONFIG_NAME"
# Relative repository paths must survive staging.
(cd "$TEST_DIR" && REPO_DIR=repo sh "$ROOT/openwrt_git_pull_update.sh")
grep -q 'old config' "$OPENCLASH_CONFIG_DIR/$CONFIG_NAME.bak"
cp "$OPENCLASH_CONFIG_DIR/$CONFIG_NAME" "$TEST_DIR/accepted.yaml"
PROVIDER="$(sed 's/^path: //' "$TEST_DIR/accepted.yaml")"
cmp "$PROVIDER" "$REPO_DIR/rule_providers/test.yaml"
printf 'payload: [changed.example]\n' > "$REPO_DIR/rule_providers/test.yaml"
if FAIL_VALIDATION=1 sh "$ROOT/openwrt_git_pull_update.sh"; then
  echo 'FAIL: invalid config accepted'; exit 1
fi
cmp "$TEST_DIR/accepted.yaml" "$OPENCLASH_CONFIG_DIR/$CONFIG_NAME"
grep -q 'example.com' "$PROVIDER"
[ "$(find "$OPENCLASH_DATA_DIR" -type d -name 'akunyaml-release.*' | wc -l | tr -d ' ')" = 1 ]
sh "$ROOT/openwrt_git_pull_update.sh"
cmp "$TEST_DIR/accepted.yaml" "$OPENCLASH_CONFIG_DIR/$CONFIG_NAME.bak"
[ -f "$PROVIDER" ]
if CONFIG_NAME=../escape.yaml sh "$ROOT/openwrt_git_pull_update.sh"; then
  echo 'FAIL: path traversal accepted'; exit 1
fi
echo 'PASS: deployment, backup, rejected update, provider isolation, path validation'