# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 9
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 4 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 5 node
- FALLBACK: 9 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-CLOUDFLARE-VLESS-WS-103MS
- AKUN-004-CLOUDFLARE-VLESS-WS-106MS
- AKUN-005-CLOUDFLARE-VLESS-WS-113MS
- AKUN-002-CLOUDFLARE-VLESS-WS-114MS

## Tier 1B - WARM-UP-CF
- AKUN-003-CLOUDFLARE-VLESS-WS-103MS
- AKUN-004-CLOUDFLARE-VLESS-WS-106MS
- AKUN-005-CLOUDFLARE-VLESS-WS-113MS
- AKUN-002-CLOUDFLARE-VLESS-WS-114MS

## Streaming Pool
- AKUN-003-CLOUDFLARE-VLESS-WS-103MS
- AKUN-004-CLOUDFLARE-VLESS-WS-106MS
- AKUN-005-CLOUDFLARE-VLESS-WS-113MS
- AKUN-002-CLOUDFLARE-VLESS-WS-114MS
- AKUN-001-CLOUDFLARE-VLESS-WS-116MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-006-CLOUDFLARE-VLESS-WS-114MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-003-CLOUDFLARE-VLESS-WS-114MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-012-CLOUDFLARE-VLESS-WS-99MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-015-DEV-VLESS-WS-123MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-031-CLOUDFLARE-VLESS-WS-146MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
