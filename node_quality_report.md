# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 42
- WARM-UP harian: 5 node
- WARM-UP-CF Cloudflare/Worker: 3 node
- STREAMING-FAST: 8 node
- AUTO-FAST: 12 node
- FALLBACK: 42 referensi, manual backup: 12 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST1
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST2
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST3
- AKUN-002-UNKNOWN-VLESS-WS-230MS-HOST1
- AKUN-002-UNKNOWN-VLESS-WS-230MS-HOST2

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST1
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST2
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST3

## Streaming Pool
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST1
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST2
- AKUN-001-UNKNOWN-VLESS-WS-215MS-HOST3
- AKUN-002-UNKNOWN-VLESS-WS-230MS-HOST1
- AKUN-002-UNKNOWN-VLESS-WS-230MS-HOST2
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST1
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST2
- AKUN-005-CLOUDFLARE-VLESS-WS-242MS-HOST3

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
