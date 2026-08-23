# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 30
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 34

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
1. `AKUN-001-UNKNOWN-VLESS-WS-102MS` (url=342ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-97MS` (url=864ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-152MS` (url=319ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS` (url=359ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-140MS` (url=313ms, status=HTTP 204)
6. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-132MS` (url=336ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-116MS` (url=338ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-162MS`
9. `AKUN-009-SPEEDTEST-VLESS-WS-101MS`
10. `AKUN-010-SPEEDTEST-VLESS-WS-111MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-125MS` (url=1318ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-108MS` (url=344ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-149MS` (url=292ms, status=HTTP 204)
14. `AKUN-015-7ZZ-VLESS-WS-168MS` (url=324ms, status=HTTP 204)
15. `AKUN-016-UNKNOWN-VLESS-WS-116MS` (url=341ms, status=HTTP 204)
16. `AKUN-017-UNKNOWN-VLESS-WS-236MS` (url=682ms, status=HTTP 204)
17. `AKUN-018-UNKNOWN-VLESS-WS-110MS` (url=335ms, status=HTTP 204)
18. `AKUN-019-ZVC-VLESS-WS-93MS` (url=344ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-145MS` (url=312ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-162MS` (url=326ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-150MS` (url=725ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-114MS` (url=326ms, status=HTTP 204)
23. `AKUN-024-SPEEDTEST-VLESS-WS-114MS` (url=322ms, status=HTTP 204)
24. `AKUN-025-UNKNOWN-VLESS-WS-104MS` (url=766ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-143MS` (url=337ms, status=HTTP 204)
26. `AKUN-027-UNKNOWN-VLESS-WS-148MS` (url=360ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-177MS` (url=336ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-127MS` (url=324ms, status=HTTP 204)
29. `AKUN-030-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-141MS` (url=356ms, status=HTTP 204)
30. `AKUN-031-DEV-VLESS-WS-96MS` (url=315ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
