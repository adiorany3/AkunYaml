# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 20
- WARM-UP harian: 7 node
- WARM-UP-CF Cloudflare/Worker: 5 node
- STREAMING-FAST: 8 node
- AUTO-FAST: 12 node
- FALLBACK: 20 referensi, manual backup: 0 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-CLOUDFLARE-VLESS-WS-106MS
- AKUN-001-CLOUDFLARE-VLESS-WS-124MS
- AKUN-006-CLOUDFLARE-VLESS-WS-132MS
- AKUN-002-CLOUDFLARE-VLESS-WS-132MS
- AKUN-005-CLOUDFLARE-VLESS-WS-137MS
- AKUN-004-CLOUDFLARE-VLESS-WS-157MS
- AKUN-007-CLOUDFLARE-VLESS-WS-170MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-106MS
- AKUN-001-CLOUDFLARE-VLESS-WS-124MS
- AKUN-002-CLOUDFLARE-VLESS-WS-132MS
- AKUN-005-CLOUDFLARE-VLESS-WS-137MS
- AKUN-004-CLOUDFLARE-VLESS-WS-157MS

## Streaming Pool
- AKUN-003-CLOUDFLARE-VLESS-WS-106MS
- AKUN-001-CLOUDFLARE-VLESS-WS-124MS
- AKUN-006-CLOUDFLARE-VLESS-WS-132MS
- AKUN-002-CLOUDFLARE-VLESS-WS-132MS
- AKUN-005-CLOUDFLARE-VLESS-WS-137MS
- AKUN-004-CLOUDFLARE-VLESS-WS-157MS
- AKUN-007-CLOUDFLARE-VLESS-WS-170MS
- AKUN-008-BIGCOMMERCE-VLESS-WS-179MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-007-CLOUDFLARE-VLESS-WS-193MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-011-CLOUDFLARE-VLESS-WS-156MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-014-CLOUDFLARE-VLESS-WS-170MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-020-CLOUDFLARE-VLESS-WS-156MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-026-CLOUDFLARE-VLESS-WS-201MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
