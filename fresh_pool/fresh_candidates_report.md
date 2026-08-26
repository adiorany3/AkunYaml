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
1. `AKUN-001-ALPHAVPS-VLESS-WS-95MS` (url=340ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-93MS` (url=317ms, status=HTTP 204)
3. `AKUN-003-SPEEDTEST-VLESS-WS-94MS` (url=1356ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-95MS` (url=335ms, status=HTTP 204)
5. `AKUN-005-SPEEDTEST-VLESS-WS-92MS` (url=1360ms, status=HTTP 204)
6. `AKUN-006-PAGM-NET-VLESS-WS-93MS` (url=1343ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-96MS` (url=353ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-96MS` (url=337ms, status=HTTP 204)
9. `AKUN-009-SPEEDTEST-VLESS-WS-97MS` (url=312ms, status=HTTP 204)
10. `AKUN-010-TIME-VLESS-WS-92MS` (url=323ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-95MS` (url=336ms, status=HTTP 204)
12. `AKUN-012-CCWU-VLESS-WS-99MS` (url=328ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-99MS` (url=354ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-94MS` (url=297ms, status=HTTP 204)
15. `AKUN-015-MEDIUM-VLESS-WS-92MS` (url=336ms, status=HTTP 204)
16. `AKUN-016-DEV-VLESS-WS-93MS` (url=341ms, status=HTTP 204)
17. `AKUN-017-DEV-VLESS-WS-95MS` (url=330ms, status=HTTP 204)
18. `AKUN-018-MYBB-VLESS-WS-93MS` (url=306ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-97MS` (url=353ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-99MS` (url=324ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-97MS` (url=1357ms, status=HTTP 204)
22. `AKUN-022-DEV-VLESS-WS-100MS` (url=360ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-103MS` (url=344ms, status=HTTP 204)
24. `AKUN-024-ZVC-VLESS-WS-91MS` (url=330ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-100MS` (url=1320ms, status=HTTP 204)
26. `AKUN-026-TIME-VLESS-WS-92MS` (url=311ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-94MS` (url=1341ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-100MS` (url=1322ms, status=HTTP 204)
29. `AKUN-029-UNKNOWN-VLESS-WS-91MS` (url=336ms, status=HTTP 204)
30. `AKUN-030-DEV-VLESS-WS-101MS` (url=355ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
