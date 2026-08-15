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
- AKUN-001-CLOUDFLARE-VLESS-WS-86MS
- AKUN-004-NOTION-WEB-VLESS-WS-86MS
- AKUN-002-NOTION-WEB-VLESS-WS-87MS
- AKUN-006-CLOUDFLARE-VLESS-WS-88MS
- AKUN-005-CLOUDFLARE-VLESS-WS-89MS
- AKUN-003-CLOUDFLARE-VLESS-WS-90MS
- AKUN-007-CLOUDFLARE-VLESS-WS-92MS

## Tier 1B - WARM-UP-CF
- AKUN-001-CLOUDFLARE-VLESS-WS-86MS
- AKUN-006-CLOUDFLARE-VLESS-WS-88MS
- AKUN-005-CLOUDFLARE-VLESS-WS-89MS
- AKUN-003-CLOUDFLARE-VLESS-WS-90MS
- AKUN-007-CLOUDFLARE-VLESS-WS-92MS

## Streaming Pool
- AKUN-001-CLOUDFLARE-VLESS-WS-86MS
- AKUN-004-NOTION-WEB-VLESS-WS-86MS
- AKUN-002-NOTION-WEB-VLESS-WS-87MS
- AKUN-006-CLOUDFLARE-VLESS-WS-88MS
- AKUN-005-CLOUDFLARE-VLESS-WS-89MS
- AKUN-003-CLOUDFLARE-VLESS-WS-90MS
- AKUN-008-CLOUDFLARE-VLESS-WS-90MS
- AKUN-007-CLOUDFLARE-VLESS-WS-92MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-015-CLOUDFLARE-VLESS-WS-93MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
