# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 8
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 4 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 5 node
- FALLBACK: 8 referensi, manual backup: 3 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-002-CLOUDFLARE-VLESS-WS-101MS
- AKUN-001-CLOUDFLARE-VLESS-WS-104MS
- AKUN-005-CLOUDFLARE-VLESS-WS-106MS
- AKUN-003-CLOUDFLARE-VLESS-WS-122MS

## Tier 1B - WARM-UP-CF
- AKUN-002-CLOUDFLARE-VLESS-WS-101MS
- AKUN-001-CLOUDFLARE-VLESS-WS-104MS
- AKUN-005-CLOUDFLARE-VLESS-WS-106MS
- AKUN-003-CLOUDFLARE-VLESS-WS-122MS

## Streaming Pool
- AKUN-002-CLOUDFLARE-VLESS-WS-101MS
- AKUN-001-CLOUDFLARE-VLESS-WS-104MS
- AKUN-005-CLOUDFLARE-VLESS-WS-106MS
- AKUN-003-CLOUDFLARE-VLESS-WS-122MS
- AKUN-004-UNKNOWN-VLESS-WS-159MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-003-CLOUDFLARE-VLESS-WS-104MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-021-UNKNOWN-VLESS-WS-118MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-026-DEV-VLESS-WS-111MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-020-UNKNOWN-VLESS-WS-114MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-017-CLOUDFLARE-VLESS-WS-114MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
