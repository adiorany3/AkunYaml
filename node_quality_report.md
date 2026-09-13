# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 13
- WARM-UP harian: 0 node
- WARM-UP-CF Cloudflare/Worker: 0 node
- STREAMING-FAST: 0 node
- AUTO-FAST: 13 node
- FALLBACK: 13 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- Tidak ada

## Tier 1B - WARM-UP-CF
- Tidak ada

## Streaming Pool
- Tidak ada

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-027-UNKNOWN-VLESS-WS-103MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
