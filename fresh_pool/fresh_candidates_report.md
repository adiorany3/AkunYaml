# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 21
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 25

## Cara Pakai di OpenWrt
Jalankan manual saat node mulai mati:

```sh
sh /etc/mihomo-autopilot/openwrt_pull_fresh_pool.sh
```

Atau aktifkan guard otomatis:

```sh
sh /etc/mihomo-autopilot/openwrt_fresh_guard.sh
```

## Kandidat Fresh Teratas
1. `AKUN-001-CLOUDFLARE-VLESS-WS-133MS` (url=377ms, status=HTTP 204)
2. `AKUN-002-DEV-VLESS-WS-115MS`
3. `AKUN-003-RESERVED-FOR-TW-VLESS-WS-154MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-168MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-335MS`
6. `AKUN-006-NETCRAFTERS-VLESS-WS-484MS`
7. `AKUN-007-PAGM-NET-VLESS-WS-535MS`
8. `AKUN-008-NET-151-242-2-0-24-VLESS-WS-706MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-808MS`
10. `AKUN-010-IQIRAQ-VLESS-WS-834MS`
11. `AKUN-020-CLOUDFLARE-VLESS-WS-857MS` (url=1664ms, status=HTTP 204)
12. `AKUN-022-CLOUDFLARE-VLESS-WS-137MS` (url=350ms, status=HTTP 204)
13. `AKUN-023-CLOUDFLARE-VLESS-WS-132MS` (url=1352ms, status=HTTP 204)
14. `AKUN-026-CLOUDFLARE-VLESS-WS-855MS` (url=1563ms, status=HTTP 204)
15. `AKUN-028-UNKNOWN-VLESS-WS-1155MS` (url=2952ms, status=HTTP 204)
16. `AKUN-029-UNKNOWN-VLESS-WS-404MS` (url=1790ms, status=HTTP 204)
17. `AKUN-031-PAGM-NET-VLESS-WS-570MS` (url=1294ms, status=HTTP 204)
18. `AKUN-036-H2NEXUS-VLESS-WS-764MS` (url=1633ms, status=HTTP 204)
19. `AKUN-039-UNKNOWN-VLESS-WS-867MS` (url=1432ms, status=HTTP 204)
20. `AKUN-042-JIKECLOUD-VLESS-WS-1235MS` (url=2263ms, status=HTTP 204)
21. `AKUN-044-JIKECLOUD-VLESS-WS-523MS` (url=1342ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
