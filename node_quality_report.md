# Node Quality Report - Smart Stable

## Ringkasan
- Total proxy di YAML: 12
- WARM-UP harian: 4 node
- WARM-UP-CF Cloudflare/Worker: 1 node
- STREAMING-FAST: 6 node
- AUTO-FAST: 6 node
- FALLBACK: 12 referensi, manual backup: 4 node

## Rekomendasi Pakai
- Harian/browsing: pilih `WARM-UP` atau `AUTO-FAST`.
- Cloudflare/Worker dan streaming: pilih `WARM-UP-CF` atau `STREAMING-FAST`.
- Kalau koneksi putus-putus: pilih `FALLBACK`, karena urutannya sudah automatic strict dulu lalu manual backup.
- Router RAM kecil: pakai `openclash_lite.yaml`.

## Tier 1 - WARM-UP
- AKUN-003-GO-DADDY-COM-LLC-VLESS-WS-267MS
- AKUN-005-CLOUDFLARE-VLESS-WS-268MS
- AKUN-001-RS-RAPIDSEEDBOX-20190717-VLESS-WS-271MS
- AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-271MS

## Tier 1B - WARM-UP-CF
- AKUN-005-CLOUDFLARE-VLESS-WS-268MS

## Streaming Pool
- AKUN-003-GO-DADDY-COM-LLC-VLESS-WS-267MS
- AKUN-005-CLOUDFLARE-VLESS-WS-268MS
- AKUN-001-RS-RAPIDSEEDBOX-20190717-VLESS-WS-271MS
- AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-271MS
- AKUN-002-VEESP-SIA-VLESS-WS-275MS
- AKUN-006-CLOUDFLARE-VLESS-WS-623MS

## Node Berisiko dari NekoBox/sing-box Test
- Tidak ada yang gagal pada laporan terakhir

## Catatan Smart Mode
- Health-check cepat hanya untuk pool kecil, bukan semua node.
- Cloudflare/Worker punya endpoint test sendiri: `https://cp.cloudflare.com`.
- `fake-ip-filter` diperluas untuk domain LAN, NTP, connectivity check, router, dan perbankan.
