# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 14
- WARM-UP harian: 1 node
- WARM-UP-CF Cloudflare/Worker: 2 node
- STREAMING-FAST: 6 node
- AUTO-FAST: 6 node
- FALLBACK: 14 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-001-RESERVED-FOR-TW-VLESS-WS-145MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-193MS
- AKUN-002-DEV-VLESS-WS-199MS

## Streaming Pool
- AKUN-001-RESERVED-FOR-TW-VLESS-WS-145MS
- AKUN-003-CLOUDFLARE-VLESS-WS-193MS
- AKUN-002-DEV-VLESS-WS-199MS
- AKUN-004-UNKNOWN-VLESS-WS-220MS
- AKUN-008-UNKNOWN-VLESS-WS-442MS
- AKUN-005-NETCRAFTERS-VLESS-WS-495MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
