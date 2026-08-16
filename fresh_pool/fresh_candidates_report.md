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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-110MS` (url=376ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-98MS` (url=328ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-93MS` (url=311ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-111MS` (url=680ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-110MS` (url=514ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-112MS` (url=1341ms, status=HTTP 204)
7. `AKUN-007-MINEDU-BLK-NZ-VLESS-WS-107MS` (url=1353ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-120MS` (url=336ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-102MS` (url=342ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-110MS` (url=348ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-106MS` (url=334ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-146MS` (url=349ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-152MS` (url=337ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-106MS` (url=322ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-116MS` (url=346ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-144MS` (url=1346ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-102MS` (url=354ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-150MS` (url=340ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-224MS` (url=422ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-130MS` (url=389ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-125MS` (url=346ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-169MS` (url=306ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-120MS` (url=388ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-158MS` (url=321ms, status=HTTP 204)
25. `AKUN-027-NOTION-WEB-VLESS-WS-133MS` (url=340ms, status=HTTP 204)
26. `AKUN-028-VEESP-VLESS-WS-200MS` (url=384ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-470MS` (url=1111ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-145MS` (url=331ms, status=HTTP 204)
29. `AKUN-034-CLOUDFLARE-VLESS-WS-168MS` (url=1092ms, status=HTTP 204)
30. `AKUN-035-ZVC-VLESS-WS-827MS` (url=1313ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
