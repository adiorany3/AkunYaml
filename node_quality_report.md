# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 14
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 1 node
- STREAMING-FAST: 6 node
- AUTO-FAST: 8 node
- FALLBACK: 14 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-005-CLOUDFLARE-VLESS-WS-86MS
- AKUN-009-UNKNOWN-VLESS-WS-87MS
- AKUN-002-MYBB-VLESS-WS-88MS
- AKUN-001-UNKNOWN-VLESS-WS-89MS

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-86MS

## Streaming Pool
- AKUN-005-CLOUDFLARE-VLESS-WS-86MS
- AKUN-009-UNKNOWN-VLESS-WS-87MS
- AKUN-002-MYBB-VLESS-WS-88MS
- AKUN-006-UNKNOWN-VLESS-WS-89MS
- AKUN-001-UNKNOWN-VLESS-WS-89MS
- AKUN-003-ZVC-VLESS-WS-91MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
