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
1. `AKUN-001-GO-DADDY-COM-LLC-VLESS-WS-89MS` (url=340ms, status=HTTP 204)
2. `AKUN-002-RS-RAPIDSEEDBOX-20190717-VLESS-WS-86MS` (url=337ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-90MS` (url=302ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-95MS` (url=1322ms, status=HTTP 204)
5. `AKUN-005-SPEEDTEST-VLESS-WS-89MS` (url=296ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-94MS` (url=326ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-95MS` (url=327ms, status=HTTP 204)
8. `AKUN-008-SPEEDTEST-VLESS-WS-93MS` (url=322ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-94MS` (url=1341ms, status=HTTP 204)
10. `AKUN-010-DK-WEBDOCK-20190903-VLESS-WS-97MS` (url=327ms, status=HTTP 204)
11. `AKUN-011-DEV-VLESS-WS-93MS` (url=1353ms, status=HTTP 204)
12. `AKUN-012-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-94MS` (url=1329ms, status=HTTP 204)
13. `AKUN-013-DEV-VLESS-WS-95MS` (url=1343ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-98MS` (url=325ms, status=HTTP 204)
15. `AKUN-015-SPEEDTEST-VLESS-WS-92MS` (url=335ms, status=HTTP 204)
16. `AKUN-017-SPEEDTEST-VLESS-WS-96MS` (url=1353ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-97MS` (url=352ms, status=HTTP 204)
18. `AKUN-019-DEV-VLESS-WS-102MS` (url=326ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-96MS` (url=334ms, status=HTTP 204)
20. `AKUN-021-MEDIUM-VLESS-WS-98MS` (url=328ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-97MS` (url=1525ms, status=HTTP 204)
22. `AKUN-023-RS-RAPIDSEEDBOX-20190717-VLESS-WS-94MS` (url=334ms, status=HTTP 204)
23. `AKUN-024-CHATGPT-VLESS-WS-104MS` (url=343ms, status=HTTP 204)
24. `AKUN-025-PAGM-NET-VLESS-WS-90MS` (url=327ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-90MS` (url=327ms, status=HTTP 204)
26. `AKUN-027-SPEEDTEST-VLESS-WS-95MS` (url=348ms, status=HTTP 204)
27. `AKUN-028-MYBB-VLESS-WS-98MS` (url=312ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-96MS` (url=324ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-98MS` (url=311ms, status=HTTP 204)
30. `AKUN-031-TIME-VLESS-WS-100MS` (url=322ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
