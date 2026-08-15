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
- AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-232MS
- AKUN-004-UNKNOWN-VLESS-WS-237MS
- AKUN-002-AIMALL-VLESS-WS-250MS
- AKUN-003-CLOUDFLARE-VLESS-WS-257MS
- AKUN-005-UNKNOWN-VLESS-WS-271MS
- AKUN-006-CLOUDFLARE-VLESS-WS-279MS
- AKUN-007-CLOUDFLARE-VLESS-WS-298MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-257MS
- AKUN-008-CLOUDFLARE-VLESS-WS-272MS
- AKUN-006-CLOUDFLARE-VLESS-WS-279MS
- AKUN-011-CLOUDFLARE-VLESS-WS-294MS
- AKUN-007-CLOUDFLARE-VLESS-WS-298MS

## Streaming Pool
- AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-232MS
- AKUN-004-UNKNOWN-VLESS-WS-237MS
- AKUN-002-AIMALL-VLESS-WS-250MS
- AKUN-003-CLOUDFLARE-VLESS-WS-257MS
- AKUN-008-CLOUDFLARE-VLESS-WS-272MS
- AKUN-006-CLOUDFLARE-VLESS-WS-279MS
- AKUN-011-CLOUDFLARE-VLESS-WS-294MS
- AKUN-007-CLOUDFLARE-VLESS-WS-298MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-012-CLOUDFLARE-VLESS-WS-276MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-013-SPEEDTEST-VLESS-WS-325MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-014-SPEEDTEST-VLESS-WS-307MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-018-CLOUDFLARE-VLESS-WS-270MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-019-CLOUDFLARE-VLESS-WS-285MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-020-UNKNOWN-VLESS-WS-311MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-021-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-279MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-022-CLOUDFLARE-VLESS-WS-275MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
