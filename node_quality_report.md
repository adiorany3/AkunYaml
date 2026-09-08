# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 7
- WARM-UP harian: 3 node
- WARM-UP-CF Cloudflare/Worker: 1 node
- STREAMING-FAST: 3 node
- AUTO-FAST: 3 node
- FALLBACK: 7 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-001-CLOUDFLARE-VLESS-WS-238MS
- AKUN-002-UNKNOWN-VLESS-WS-251MS
- AKUN-003-UNKNOWN-VLESS-WS-257MS

## Tier 1B - WARM-UP-CF
- AKUN-001-CLOUDFLARE-VLESS-WS-238MS

## Streaming Pool
- AKUN-001-CLOUDFLARE-VLESS-WS-238MS
- AKUN-002-UNKNOWN-VLESS-WS-251MS
- AKUN-003-UNKNOWN-VLESS-WS-257MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-004-CLOUDFLARE-VLESS-WS-235MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-001-CLOUDFLARE-VLESS-WS-225MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))
- AKUN-009-CLOUDFLARE-VLESS-WS-262MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))
- AKUN-007-CLOUDFLARE-VLESS-WS-241MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))
- AKUN-013-CLOUDFLARE-VLESS-WS-264MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))
- AKUN-003-UNKNOWN-VLESS-WS-227MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))
- AKUN-005-UNKNOWN-VLESS-WS-257MS: ConnectionError: ('Connection aborted.', OSError(22, 'Invalid argument'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
