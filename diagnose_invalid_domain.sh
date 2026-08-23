#!/bin/sh
BASE="/etc/openclash"
NAME="${1:-AkunBaru}"

echo "=== Config files ==="
find "$BASE" -maxdepth 2 -type f \( -iname "*$NAME*.yaml" -o -iname "*$NAME*.yml" \) -print 2>/dev/null

echo
echo "=== Legacy providers that must be gone ==="
grep -RnsE \
'security-tif-mini|popup-ads|hagezi-pro-mini|awavenue-ads|GEOSITE,[[:space:]]*tracker|geosite:category-ads-all,tracker' \
"$BASE/config" "$BASE"/*.yaml 2>/dev/null || echo "tidak ditemukan"

echo
echo "=== Safe security rules ==="
grep -RnsE \
'GEOSITE,[[:space:]]*category-ads-all|tracker-domain|tracker\.mrs' \
"$BASE/config" "$BASE"/*.yaml 2>/dev/null || true
