# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 14
- WARM-UP harian: 5 node
- WARM-UP-CF Cloudflare/Worker: 5 node
- STREAMING-FAST: 8 node
- AUTO-FAST: 10 node
- FALLBACK: 14 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-UNKNOWN-VLESS-WS-88MS
- AKUN-001-CLOUDFLARE-VLESS-WS-94MS
- AKUN-004-UNKNOWN-VLESS-WS-103MS
- AKUN-002-CLOUDFLARE-VLESS-WS-103MS
- AKUN-006-CLOUDFLARE-VLESS-WS-104MS

## Tier 1B - WARM-UP-CF
- AKUN-001-CLOUDFLARE-VLESS-WS-94MS
- AKUN-002-CLOUDFLARE-VLESS-WS-103MS
- AKUN-006-CLOUDFLARE-VLESS-WS-104MS
- AKUN-009-CLOUDFLARE-VLESS-WS-105MS
- AKUN-008-CLOUDFLARE-VLESS-WS-106MS

## Streaming Pool
- AKUN-003-UNKNOWN-VLESS-WS-88MS
- AKUN-001-CLOUDFLARE-VLESS-WS-94MS
- AKUN-004-UNKNOWN-VLESS-WS-103MS
- AKUN-002-CLOUDFLARE-VLESS-WS-103MS
- AKUN-006-CLOUDFLARE-VLESS-WS-104MS
- AKUN-005-EU-VLESS-WS-105MS
- AKUN-009-CLOUDFLARE-VLESS-WS-105MS
- AKUN-008-CLOUDFLARE-VLESS-WS-106MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
