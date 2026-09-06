# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 10
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 1 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 1 node
- FALLBACK: 10 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS
- AKUN-004-CHATGPT-VLESS-WS-106MS
- AKUN-003-BIGCOMMERCE-VLESS-WS-108MS
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS

## Streaming Pool
- AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS
- AKUN-004-CHATGPT-VLESS-WS-106MS
- AKUN-003-BIGCOMMERCE-VLESS-WS-108MS
- AKUN-005-CLOUDFLARE-VLESS-WS-111MS
- AKUN-001-008500-VLESS-WS-114MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-048-CLOUDFLARE-VLESS-WS-124MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-009-CLOUDFLARE-VLESS-WS-112MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-011-NOTION-WEB-VLESS-WS-106MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)
- AKUN-001-CLOUDFLARE-VLESS-WS-108MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
