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
- AKUN-002-CLOUDFLARE-VLESS-WS-140MS
- AKUN-007-CLOUDFLARE-VLESS-WS-141MS
- AKUN-003-CLOUDFLARE-VLESS-WS-145MS
- AKUN-006-CLOUDFLARE-VLESS-WS-146MS
- AKUN-005-CLOUDFLARE-VLESS-WS-146MS
- AKUN-001-CLOUDFLARE-VLESS-WS-152MS
- AKUN-004-CLOUD-NETWORK-HK-VLESS-WS-174MS

## Tier 1B - WARM-UP-CF
- AKUN-002-CLOUDFLARE-VLESS-WS-140MS
- AKUN-003-CLOUDFLARE-VLESS-WS-145MS
- AKUN-006-CLOUDFLARE-VLESS-WS-146MS
- AKUN-005-CLOUDFLARE-VLESS-WS-146MS
- AKUN-001-CLOUDFLARE-VLESS-WS-152MS

## Streaming Pool
- AKUN-008-CLOUDFLARE-VLESS-WS-134MS
- AKUN-002-CLOUDFLARE-VLESS-WS-140MS
- AKUN-007-CLOUDFLARE-VLESS-WS-141MS
- AKUN-003-CLOUDFLARE-VLESS-WS-145MS
- AKUN-006-CLOUDFLARE-VLESS-WS-146MS
- AKUN-005-CLOUDFLARE-VLESS-WS-146MS
- AKUN-001-CLOUDFLARE-VLESS-WS-152MS
- AKUN-004-CLOUD-NETWORK-HK-VLESS-WS-174MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
