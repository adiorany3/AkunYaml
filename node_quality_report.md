# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 12
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 4 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 8 node
- FALLBACK: 12 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-007-CLOUDFLARE-VLESS-WS-96MS
- AKUN-005-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS
- AKUN-004-CLOUDFLARE-VLESS-WS-112MS
- AKUN-001-MEDIUM-VLESS-WS-113MS

## Tier 1B - WARM-UP-CF
- AKUN-007-CLOUDFLARE-VLESS-WS-96MS
- AKUN-004-CLOUDFLARE-VLESS-WS-112MS
- AKUN-002-CLOUDFLARE-VLESS-WS-114MS
- AKUN-006-CLOUDFLARE-VLESS-WS-116MS

## Streaming Pool
- AKUN-007-CLOUDFLARE-VLESS-WS-96MS
- AKUN-005-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS
- AKUN-004-CLOUDFLARE-VLESS-WS-112MS
- AKUN-002-CLOUDFLARE-VLESS-WS-114MS
- AKUN-006-CLOUDFLARE-VLESS-WS-116MS

## Node Berisiko dari NekoBox/sing-box Test
- AKUN-010-CLOUDFLARE-VLESS-WS-108MS: ConnectionError: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
- AKUN-001-CLOUDFLARE-VLESS-WS-102MS: ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0)

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
