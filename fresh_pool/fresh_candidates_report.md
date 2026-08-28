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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-71MS` (url=322ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-57MS` (url=289ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-82MS` (url=304ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-81MS` (url=303ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-76MS`
6. `AKUN-006-MEDIUM-VLESS-WS-68MS`
7. `AKUN-007-SS-SYSTEC-VLESS-WS-81MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-78MS`
9. `AKUN-009-DEV-VLESS-WS-85MS`
10. `AKUN-010-DEV-VLESS-WS-84MS`
11. `AKUN-014-NOTION-WEB-VLESS-WS-93MS` (url=332ms, status=HTTP 204)
12. `AKUN-015-CCWU-VLESS-WS-96MS` (url=331ms, status=HTTP 204)
13. `AKUN-016-SPEEDTEST-VLESS-WS-82MS` (url=316ms, status=HTTP 204)
14. `AKUN-017-CLOUDFLARE-VLESS-WS-91MS` (url=346ms, status=HTTP 204)
15. `AKUN-018-DEV-VLESS-WS-80MS` (url=972ms, status=HTTP 204)
16. `AKUN-020-UNKNOWN-VLESS-WS-96MS` (url=884ms, status=HTTP 204)
17. `AKUN-021-TIME-VLESS-WS-90MS` (url=303ms, status=HTTP 204)
18. `AKUN-022-CLOUDFLARE-VLESS-WS-106MS` (url=1165ms, status=HTTP 204)
19. `AKUN-023-DEV-VLESS-WS-84MS` (url=347ms, status=HTTP 204)
20. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-78MS` (url=296ms, status=HTTP 204)
21. `AKUN-025-UNKNOWN-VLESS-WS-93MS` (url=494ms, status=HTTP 204)
22. `AKUN-026-CLOUDFLARE-VLESS-WS-76MS` (url=274ms, status=HTTP 204)
23. `AKUN-027-CLOUDFLARE-VLESS-WS-88MS` (url=295ms, status=HTTP 204)
24. `AKUN-028-UNKNOWN-VLESS-WS-109MS` (url=887ms, status=HTTP 204)
25. `AKUN-029-UNKNOWN-VLESS-WS-113MS` (url=335ms, status=HTTP 204)
26. `AKUN-030-CLOUDFLARE-VLESS-WS-97MS` (url=366ms, status=HTTP 204)
27. `AKUN-031-SPEEDTEST-VLESS-WS-98MS` (url=319ms, status=HTTP 204)
28. `AKUN-032-UNKNOWN-VLESS-WS-116MS` (url=384ms, status=HTTP 204)
29. `AKUN-034-CLOUDFLARE-VLESS-WS-129MS` (url=349ms, status=HTTP 204)
30. `AKUN-035-CLOUDFLARE-VLESS-WS-124MS` (url=287ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
