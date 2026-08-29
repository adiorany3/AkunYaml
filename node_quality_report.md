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
- AKUN-003-CLOUDFLARE-VLESS-WS-239MS
- AKUN-002-CLOUDFLARE-VLESS-WS-249MS
- AKUN-001-CLOUDFLARE-VLESS-WS-255MS
- AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-263MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-239MS
- AKUN-002-CLOUDFLARE-VLESS-WS-249MS
- AKUN-001-CLOUDFLARE-VLESS-WS-255MS
- AKUN-004-CLOUDFLARE-VLESS-WS-264MS

## Streaming Pool
- AKUN-003-CLOUDFLARE-VLESS-WS-239MS
- AKUN-002-CLOUDFLARE-VLESS-WS-249MS
- AKUN-001-CLOUDFLARE-VLESS-WS-255MS
- AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-263MS
- AKUN-004-CLOUDFLARE-VLESS-WS-264MS
- AKUN-007-CLOUDFLARE-VLESS-WS-273MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
