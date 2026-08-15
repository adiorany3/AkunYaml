#!/bin/sh
# Exact OpenClash/Mihomo validator for the router.
#
# Uses the exact core installed on this router. This is the final source of
# truth for subscription compatibility.
#
# Commands:
#   sh openclash_exact_core_filter.sh test
#   sh openclash_exact_core_filter.sh isolate
#   sh openclash_exact_core_filter.sh watch
#
# Optional source URL:
#   SOURCE_URL=https://... sh openclash_exact_core_filter.sh test

set -u

MODE="${1:-test}"
SOURCE_URL="${SOURCE_URL:-https://raw.githubusercontent.com/adiorany3/AkunYaml/main/openclash_auto.yaml}"
REFERENCE_URL="${REFERENCE_URL:-https://raw.githubusercontent.com/adiorany3/ConvertYAML/main/openclash_auto.yaml}"
BASE="/etc/openclash"
CORE="$BASE/core/clash_meta"
SAFE_PATHS_VALUE="/usr/share/openclash:/etc/ssl"
WORK="/tmp/openclash-exact-filter"
SOURCE="$WORK/source.yaml"
REFERENCE="$WORK/reference.yaml"
CAPTURED="/root/AkunBaru_CAPTURED_BAD.yaml"
FILTERED="/root/openclash_auto_exact_filtered.yaml"

say() { printf '%s\n' "$*"; }
sep() { say "------------------------------------------------------------"; }

mkdir -p "$WORK/proxy-tests"
rm -f "$WORK/proxy-tests"/*.yaml "$WORK/failing_names.txt" 2>/dev/null || true

if [ ! -x "$CORE" ]; then
  say "[ERROR] Core tidak ditemukan: $CORE"
  exit 2
fi

if ! command -v ruby >/dev/null 2>&1; then
  say "[ERROR] Ruby tidak ditemukan. OpenClash biasanya memasang Ruby."
  exit 2
fi

fetch() {
  URL="$1"
  OUT="$2"
  curl -fL --connect-timeout 15 --max-time 60 \
    -A "Clash.meta" \
    "$URL" -o "$OUT"
}

test_cfg() {
  FILE="$1"
  LABEL="$2"
  OUT="$WORK/${LABEL}.log"
  SAFE_PATHS="$SAFE_PATHS_VALUE" \
    "$CORE" -t -d "$BASE" -f "$FILE" >"$OUT" 2>&1
  RC=$?
  say ""
  say "[$LABEL] exit=$RC"
  cat "$OUT"
  return "$RC"
}

direct_test() {
  sep
  say "DOWNLOAD SOURCE"
  say "$SOURCE_URL"
  fetch "$SOURCE_URL" "$SOURCE" || {
    say "[ERROR] source download gagal"
    return 10
  }

  say ""
  say "DOWNLOAD KNOWN-GOOD REFERENCE"
  fetch "$REFERENCE_URL" "$REFERENCE" || {
    say "[ERROR] reference download gagal"
    return 11
  }

  sep
  say "TEST KNOWN-GOOD REFERENCE"
  if ! test_cfg "$REFERENCE" "known_good"; then
    say "[STOP] Known-good juga gagal di core ini."
    say "Masalah bukan node AkunYaml. Periksa environment/cache/OpenClash."
    return 12
  fi

  sep
  say "TEST AKUNYAML SOURCE DIRECTLY"
  if test_cfg "$SOURCE" "source_direct"; then
    say ""
    say "[RESULT] SOURCE GITHUB VALID di exact core router."
    say "Jadi invalid domain dibuat pada proses subscription/overwrite OpenClash."
    say "Jalankan:"
    say "  sh openclash_exact_core_filter.sh watch"
    return 0
  fi

  say ""
  say "[RESULT] SOURCE GITHUB SENDIRI INVALID."
  say "Lanjutkan dengan mode isolate."
  return 1
}

build_proxy_tests() {
  INPUT="$1"
  rm -f "$WORK/proxy-tests"/*.yaml "$WORK/proxy_names.tsv" 2>/dev/null || true

  ruby - "$INPUT" "$WORK/proxy-tests" "$WORK/proxy_names.tsv" <<'RUBY'
require 'yaml'
require 'fileutils'

input, outdir, manifest = ARGV
cfg = YAML.load_file(input) || {}
proxies = cfg['proxies'].is_a?(Array) ? cfg['proxies'] : []
FileUtils.mkdir_p(outdir)

File.open(manifest, 'w') do |mf|
  proxies.each_with_index do |proxy, idx|
    next unless proxy.is_a?(Hash)
    name = proxy['name'].to_s
    safe = format('%03d', idx + 1)
    minimal = {
      'mixed-port' => 7890,
      'mode' => 'rule',
      'log-level' => 'warning',
      'proxies' => [proxy],
      'proxy-groups' => [
        {
          'name' => 'EXACT-TEST',
          'type' => 'select',
          'proxies' => [name],
        }
      ],
      'rules' => ['MATCH,EXACT-TEST'],
    }
    path = File.join(outdir, "#{safe}.yaml")
    File.write(path, YAML.dump(minimal))
    mf.puts "#{safe}\t#{name}"
  end
end
RUBY
}

isolate_file() {
  INPUT="$1"

  sep
  say "ISOLATE EXACT PROXY PARSER"
  build_proxy_tests "$INPUT"

  : > "$WORK/failing_names.txt"
  TOTAL=0
  FAIL=0

  while IFS="$(printf '\t')" read -r ID NAME; do
    [ -n "$ID" ] || continue
    TOTAL=$((TOTAL + 1))
    TESTFILE="$WORK/proxy-tests/$ID.yaml"
    SAFE_PATHS="$SAFE_PATHS_VALUE" \
      "$CORE" -t -d "$BASE" -f "$TESTFILE" \
      >"$WORK/proxy-$ID.log" 2>&1
    RC=$?
    if [ "$RC" -eq 0 ]; then
      say "[PASS] $ID $NAME"
    else
      FAIL=$((FAIL + 1))
      say "[FAIL] $ID $NAME"
      tail -n 8 "$WORK/proxy-$ID.log"
      printf '%s\n' "$NAME" >> "$WORK/failing_names.txt"
    fi
  done < "$WORK/proxy_names.tsv"

  say ""
  say "Proxy result: pass=$((TOTAL - FAIL)) fail=$FAIL total=$TOTAL"

  if [ "$FAIL" -gt 0 ]; then
    sep
    say "BUILD FILTERED YAML"
    ruby - "$INPUT" "$WORK/failing_names.txt" "$FILTERED" <<'RUBY'
require 'yaml'

input, bad_file, output = ARGV
cfg = YAML.load_file(input) || {}
bad = File.readlines(bad_file, chomp: true).to_h { |x| [x, true] }

if cfg['proxies'].is_a?(Array)
  cfg['proxies'] = cfg['proxies'].reject do |p|
    p.is_a?(Hash) && bad[p['name'].to_s]
  end
end

proxy_names = (cfg['proxies'] || []).filter_map do |p|
  p['name'].to_s if p.is_a?(Hash) && p['name']
end
group_names = (cfg['proxy-groups'] || []).filter_map do |g|
  g['name'].to_s if g.is_a?(Hash) && g['name']
end

valid = {}
(proxy_names + group_names + %w[DIRECT REJECT PASS COMPATIBLE]).each { |x| valid[x] = true }
fallback = proxy_names.first || 'DIRECT'

(cfg['proxy-groups'] || []).each do |g|
  next unless g.is_a?(Hash) && g['proxies'].is_a?(Array)
  g['proxies'] = g['proxies'].map(&:to_s).select { |x| valid[x] }
  g['proxies'] = [fallback] if g['proxies'].empty?
end

cfg.delete('global-client-fingerprint')
File.write(output, YAML.dump(cfg))
RUBY

    if test_cfg "$FILTERED" "filtered"; then
      say ""
      say "[OK] FILTERED YAML VALID:"
      say "  $FILTERED"
      say "Node yang dibuang:"
      cat "$WORK/failing_names.txt"
      return 0
    fi

    say "[WARN] Node gagal sudah dibuang tetapi full config masih invalid."
  else
    say ""
    say "Semua proxy lolos exact proxy parser."
  fi

  sep
  say "SECTION ISOLATION"

  # Remove DNS.
  ruby - "$INPUT" "$WORK/no_dns.yaml" <<'RUBY'
require 'yaml'
a,b=ARGV
c=YAML.load_file(a)||{}
c.delete('dns')
File.write(b,YAML.dump(c))
RUBY
  if test_cfg "$WORK/no_dns.yaml" "no_dns"; then
    say "[CAUSE] dns section / injected fake-ip-filter / nameserver policy."
    return 20
  fi

  # Remove sniffer.
  ruby - "$INPUT" "$WORK/no_sniffer.yaml" <<'RUBY'
require 'yaml'
a,b=ARGV
c=YAML.load_file(a)||{}
c.delete('sniffer')
File.write(b,YAML.dump(c))
RUBY
  if test_cfg "$WORK/no_sniffer.yaml" "no_sniffer"; then
    say "[CAUSE] sniffer domain list."
    return 21
  fi

  # Remove rule providers and use only MATCH.
  ruby - "$INPUT" "$WORK/no_rule_data.yaml" <<'RUBY'
require 'yaml'
a,b=ARGV
c=YAML.load_file(a)||{}
c.delete('rule-providers')
groups=(c['proxy-groups']||[])
target=groups.first.is_a?(Hash) ? groups.first['name'].to_s : 'DIRECT'
c['rules']=["MATCH,#{target}"]
File.write(b,YAML.dump(c))
RUBY
  if test_cfg "$WORK/no_rule_data.yaml" "no_rule_data"; then
    say "[CAUSE] rules or rule-providers."
    return 22
  fi

  say "[CAUSE] Tidak terisolasi ke proxy/dns/sniffer/rule-provider."
  say "Periksa proxy-groups/top-level options dari captured config."
  return 23
}

watch_tmp() {
  sep
  say "WATCHING /tmp/yaml_sub_tmp_config.yaml"
  say "Sekarang tekan Update AkunBaru di LuCI."
  say "Script berhenti otomatis saat menangkap config INVALID."
  say "Timeout 120 detik."

  TMP="/tmp/yaml_sub_tmp_config.yaml"
  LAST_SIG=""
  I=0
  while [ "$I" -lt 120 ]; do
    I=$((I + 1))
    if [ -s "$TMP" ]; then
      SIG="$(wc -c < "$TMP" 2>/dev/null)-$(cksum "$TMP" 2>/dev/null | awk '{print $1}')"
      if [ "$SIG" != "$LAST_SIG" ]; then
        LAST_SIG="$SIG"
        cp "$TMP" "$WORK/captured.yaml"
        say "[CAPTURE] $SIG"
        if ! test_cfg "$WORK/captured.yaml" "captured"; then
          cp "$WORK/captured.yaml" "$CAPTURED"
          say ""
          say "[FOUND] Invalid subscription temp config disimpan:"
          say "  $CAPTURED"
          isolate_file "$CAPTURED"
          return $?
        fi
      fi
    fi
    sleep 1
  done

  say "[TIMEOUT] Tidak menangkap config invalid."
  return 30
}

case "$MODE" in
  test)
    direct_test
    RC=$?
    if [ "$RC" -eq 1 ]; then
      isolate_file "$SOURCE"
      exit $?
    fi
    exit "$RC"
    ;;
  isolate)
    fetch "$SOURCE_URL" "$SOURCE" || exit 10
    isolate_file "$SOURCE"
    ;;
  watch)
    watch_tmp
    ;;
  *)
    say "Usage:"
    say "  sh openclash_exact_core_filter.sh test"
    say "  sh openclash_exact_core_filter.sh isolate"
    say "  sh openclash_exact_core_filter.sh watch"
    exit 1
    ;;
esac
