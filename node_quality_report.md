# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 9
- WARM-UP harian: 5 node
- WARM-UP-CF Cloudflare/Worker: 2 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 5 node
- FALLBACK: 9 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-001-UNKNOWN-VLESS-WS-260MS
- AKUN-002-CLOUDFLARE-VLESS-WS-261MS
- AKUN-003-LEVIKOGJGFDD-VLESS-WS-322MS
- AKUN-005-CLOUDFLARE-VLESS-WS-333MS
- AKUN-004-UNKNOWN-VLESS-WS-392MS

## Tier 1B - WARM-UP-CF
- AKUN-002-CLOUDFLARE-VLESS-WS-261MS
- AKUN-005-CLOUDFLARE-VLESS-WS-333MS

## Streaming Pool
- AKUN-001-UNKNOWN-VLESS-WS-260MS
- AKUN-002-CLOUDFLARE-VLESS-WS-261MS
- AKUN-003-LEVIKOGJGFDD-VLESS-WS-322MS
- AKUN-005-CLOUDFLARE-VLESS-WS-333MS
- AKUN-004-UNKNOWN-VLESS-WS-392MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-003-UNKNOWN-VLESS-WS-244MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-004-UNKNOWN-VLESS-WS-305MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-005-CLOUDFLARE-VLESS-WS-262MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-006-SPEEDTEST-VLESS-WS-291MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-008-CLOUDFLARE-VLESS-WS-292MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-009-UNKNOWN-VLESS-WS-271MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-013-SPEEDTEST-VLESS-WS-292MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-014-SPEEDTEST-VLESS-WS-355MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-015-NOTION-WEB-VLESS-WS-231MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-019-UNKNOWN-VLESS-WS-256MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-022-CLOUDFLARE-VLESS-WS-288MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-238MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-027-UNKNOWN-VLESS-WS-262MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-028-LEVIKOGJGFDD-VLESS-WS-270MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-029-SPEEDTEST-VLESS-WS-247MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-030-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-291MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-031-NOTION-WEB-VLESS-WS-333MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-032-UNKNOWN-VLESS-WS-255MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-034-UNKNOWN-VLESS-WS-303MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-035-SPEEDTEST-VLESS-WS-283MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-037-BIGCOMMERCE-VLESS-WS-364MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)
- AKUN-038-CLOUDFLARE-VLESS-WS-330MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-042-DIGITALOCEAN-VLESS-WS-419MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-044-UNKNOWN-VLESS-WS-304MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-052-UNKNOWN-VLESS-WS-657MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=8.0)

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
