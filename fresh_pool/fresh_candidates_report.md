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
1. `AKUN-001-DEV-VLESS-WS-531MS` (url=1663ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-494MS` (url=1250ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-482MS` (url=1109ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-553MS` (url=1099ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-524MS` (url=1057ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-578MS` (url=1972ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-502MS` (url=1611ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-562MS` (url=1114ms, status=HTTP 204)
9. `AKUN-009-PAGM-NET-VLESS-WS-468MS` (url=1074ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-551MS` (url=4288ms, status=HTTP 204)
11. `AKUN-011-SPEEDTEST-VLESS-WS-526MS` (url=1400ms, status=HTTP 204)
12. `AKUN-012-VEESP-SIA-VLESS-WS-505MS` (url=849ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-580MS` (url=1569ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-530MS` (url=929ms, status=HTTP 204)
15. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-616MS` (url=1139ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-548MS` (url=1048ms, status=HTTP 204)
17. `AKUN-017-CHATGPT-VLESS-WS-627MS` (url=1077ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-528MS` (url=2273ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-546MS` (url=1070ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-564MS` (url=3402ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-576MS` (url=1473ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-503MS` (url=4691ms, status=HTTP 204)
23. `AKUN-024-MEDIUM-VLESS-WS-632MS` (url=1107ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-538MS` (url=1368ms, status=HTTP 204)
25. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-574MS` (url=1155ms, status=HTTP 204)
26. `AKUN-027-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-457MS` (url=1283ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-544MS` (url=1860ms, status=HTTP 204)
28. `AKUN-029-SPEEDTEST-VLESS-WS-471MS` (url=931ms, status=HTTP 204)
29. `AKUN-030-TIME-VLESS-WS-509MS` (url=1337ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-631MS` (url=1071ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
