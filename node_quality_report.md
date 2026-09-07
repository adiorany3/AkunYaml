# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 9
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 3 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 5 node
- FALLBACK: 9 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-BIGCOMMERCE-VLESS-WS-104MS
- AKUN-005-CLOUDFLARE-VLESS-WS-107MS
- AKUN-002-ORG-VLESS-WS-116MS
- AKUN-004-CLOUDFLARE-VLESS-WS-118MS

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-107MS
- AKUN-004-CLOUDFLARE-VLESS-WS-118MS
- AKUN-001-CLOUDFLARE-VLESS-WS-120MS

## Streaming Pool
- AKUN-003-BIGCOMMERCE-VLESS-WS-104MS
- AKUN-005-CLOUDFLARE-VLESS-WS-107MS
- AKUN-002-ORG-VLESS-WS-116MS
- AKUN-004-CLOUDFLARE-VLESS-WS-118MS
- AKUN-001-CLOUDFLARE-VLESS-WS-120MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-010-CLOUDFLARE-VLESS-WS-103MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-014-DEV-VLESS-WS-112MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-008-NOTION-WEB-VLESS-WS-110MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-027-UNKNOWN-VLESS-WS-111MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-019-CLOUDFLARE-VLESS-WS-108MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
