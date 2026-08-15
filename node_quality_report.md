# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 24
- WARM-UP harian: 7 node
- WARM-UP-CF Cloudflare/Worker: 5 node
- STREAMING-FAST: 8 node
- AUTO-FAST: 12 node
- FALLBACK: 24 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS
- AKUN-007-CLOUDFLARE-VLESS-WS-111MS
- AKUN-003-CLOUDFLARE-VLESS-WS-115MS
- AKUN-002-CLOUDFLARE-VLESS-WS-122MS
- AKUN-001-CLOUDFLARE-VLESS-WS-123MS
- AKUN-006-CLOUDFLARE-VLESS-WS-127MS
- AKUN-004-CLOUDFLARE-VLESS-WS-134MS

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS
- AKUN-003-CLOUDFLARE-VLESS-WS-115MS
- AKUN-002-CLOUDFLARE-VLESS-WS-122MS
- AKUN-001-CLOUDFLARE-VLESS-WS-123MS
- AKUN-004-CLOUDFLARE-VLESS-WS-134MS

## Streaming Pool
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS
- AKUN-007-CLOUDFLARE-VLESS-WS-111MS
- AKUN-003-CLOUDFLARE-VLESS-WS-115MS
- AKUN-002-CLOUDFLARE-VLESS-WS-122MS
- AKUN-001-CLOUDFLARE-VLESS-WS-123MS
- AKUN-008-CLOUDFLARE-VLESS-WS-125MS
- AKUN-006-CLOUDFLARE-VLESS-WS-127MS
- AKUN-004-CLOUDFLARE-VLESS-WS-134MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
