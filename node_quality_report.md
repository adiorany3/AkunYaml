# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 14
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 4 node
- STREAMING-FAST: 6 node
- AUTO-FAST: 8 node
- FALLBACK: 14 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-009-CCWU-VLESS-WS-241MS
- AKUN-002-CLOUDFLARE-VLESS-WS-247MS
- AKUN-001-CLOUDFLARE-VLESS-WS-252MS
- AKUN-004-CLOUDFLARE-VLESS-WS-260MS

## Tier 1B - WARM-UP-CF
- AKUN-002-CLOUDFLARE-VLESS-WS-247MS
- AKUN-001-CLOUDFLARE-VLESS-WS-252MS
- AKUN-004-CLOUDFLARE-VLESS-WS-260MS
- AKUN-003-CLOUDFLARE-VLESS-WS-268MS

## Streaming Pool
- AKUN-009-CCWU-VLESS-WS-241MS
- AKUN-002-CLOUDFLARE-VLESS-WS-247MS
- AKUN-001-CLOUDFLARE-VLESS-WS-252MS
- AKUN-004-CLOUDFLARE-VLESS-WS-260MS
- AKUN-005-NOTION-WEB-VLESS-WS-261MS
- AKUN-003-CLOUDFLARE-VLESS-WS-268MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
