# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 7
- WARM-UP harian: 3 node
- WARM-UP-CF Cloudflare/Worker: 2 node
- STREAMING-FAST: 3 node
- AUTO-FAST: 3 node
- FALLBACK: 7 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-US-VLESS-WS-985MS
- AKUN-001-CLOUDFLARE-VLESS-WS-992MS
- AKUN-002-CLOUDFLARE-VLESS-WS-994MS

## Tier 1B - WARM-UP-CF
- AKUN-001-CLOUDFLARE-VLESS-WS-992MS
- AKUN-002-CLOUDFLARE-VLESS-WS-994MS

## Streaming Pool
- AKUN-003-US-VLESS-WS-985MS
- AKUN-001-CLOUDFLARE-VLESS-WS-992MS
- AKUN-002-CLOUDFLARE-VLESS-WS-994MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
