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
1. `AKUN-001-UNKNOWN-VLESS-WS-87MS` (url=1364ms, status=HTTP 204)
2. `AKUN-002-SPEEDTEST-VLESS-WS-92MS` (url=333ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-90MS` (url=331ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-96MS` (url=341ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-96MS` (url=318ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-93MS` (url=357ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-92MS` (url=1346ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-93MS` (url=1079ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-96MS` (url=321ms, status=HTTP 204)
10. `AKUN-010-DK-WEBDOCK-20190903-VLESS-WS-97MS` (url=344ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-98MS` (url=757ms, status=HTTP 204)
12. `AKUN-012-UNKNOWN-VLESS-WS-94MS` (url=324ms, status=HTTP 204)
13. `AKUN-013-DEV-VLESS-WS-97MS` (url=323ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-96MS` (url=1344ms, status=HTTP 204)
15. `AKUN-015-UNKNOWN-VLESS-WS-98MS` (url=340ms, status=HTTP 204)
16. `AKUN-016-DEV-VLESS-WS-97MS` (url=364ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-102MS` (url=1352ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-97MS` (url=370ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-98MS` (url=336ms, status=HTTP 204)
20. `AKUN-020-DEV-VLESS-WS-101MS` (url=359ms, status=HTTP 204)
21. `AKUN-021-TIME-VLESS-WS-101MS` (url=339ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-93MS` (url=737ms, status=HTTP 204)
23. `AKUN-023-GO-DADDY-COM-LLC-VLESS-WS-87MS` (url=362ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-96MS` (url=330ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-97MS` (url=335ms, status=HTTP 204)
26. `AKUN-026-RS-RAPIDSEEDBOX-20190717-VLESS-WS-94MS` (url=347ms, status=HTTP 204)
27. `AKUN-027-NOTION-WEB-VLESS-WS-99MS` (url=1335ms, status=HTTP 204)
28. `AKUN-028-DEV-VLESS-WS-99MS` (url=336ms, status=HTTP 204)
29. `AKUN-029-SPEEDTEST-VLESS-WS-93MS` (url=310ms, status=HTTP 204)
30. `AKUN-030-MYBB-VLESS-WS-95MS` (url=308ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
