# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 14
- WARM-UP harian: 3 node
- WARM-UP-CF Cloudflare/Worker: 2 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 6 node
- FALLBACK: 14 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-001-RESERVED-FOR-TW-VLESS-WS-127MS
- AKUN-003-CLOUDFLARE-VLESS-WS-131MS
- AKUN-002-CLOUDFLARE-VLESS-WS-143MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-131MS
- AKUN-002-CLOUDFLARE-VLESS-WS-143MS

## Streaming Pool
- AKUN-001-RESERVED-FOR-TW-VLESS-WS-127MS
- AKUN-003-CLOUDFLARE-VLESS-WS-131MS
- AKUN-002-CLOUDFLARE-VLESS-WS-143MS
- AKUN-004-NETCRAFTERS-VLESS-WS-465MS
- AKUN-006-PAGM-NET-VLESS-WS-524MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
