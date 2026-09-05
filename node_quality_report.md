# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 13
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 4 node
- STREAMING-FAST: 5 node
- AUTO-FAST: 1 node
- FALLBACK: 13 referensi, manual backup: 3 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-004-CLOUDFLARE-VLESS-WS-105MS
- AKUN-002-CLOUDFLARE-VLESS-WS-107MS
- AKUN-005-CLOUDFLARE-VLESS-WS-108MS
- AKUN-001-CLOUDFLARE-VLESS-WS-113MS

## Tier 1B - WARM-UP-CF
- AKUN-004-CLOUDFLARE-VLESS-WS-105MS
- AKUN-002-CLOUDFLARE-VLESS-WS-107MS
- AKUN-005-CLOUDFLARE-VLESS-WS-108MS
- AKUN-001-CLOUDFLARE-VLESS-WS-113MS

## Streaming Pool
- AKUN-004-CLOUDFLARE-VLESS-WS-105MS
- AKUN-002-CLOUDFLARE-VLESS-WS-107MS
- AKUN-005-CLOUDFLARE-VLESS-WS-108MS
- AKUN-001-CLOUDFLARE-VLESS-WS-113MS
- AKUN-003-CLOUDFLARE-VLESS-WS-114MS

## Node Berisiko dari NekoBox/sing-box Test
- Tes NekoBox/sing-box dinonaktifkan; node tidak diuji.

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
