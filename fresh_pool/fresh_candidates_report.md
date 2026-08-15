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
- Kandidat strict NekoBox-tested: 20
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-86MS` (url=321ms, nekobox=336ms, status=yes)
2. `AKUN-002-NOTION-WEB-VLESS-WS-87MS` (url=1309ms, nekobox=338ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-90MS` (url=335ms, nekobox=342ms, status=yes)
4. `AKUN-004-NOTION-WEB-VLESS-WS-86MS` (url=306ms, nekobox=339ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-89MS` (url=291ms, nekobox=361ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-88MS` (url=329ms, nekobox=355ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-92MS` (url=316ms, nekobox=359ms, status=yes)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-90MS` (url=330ms, nekobox=364ms, status=yes)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-90MS` (url=331ms, nekobox=385ms, status=yes)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-86MS` (url=317ms, nekobox=360ms, status=yes)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-88MS` (url=307ms, nekobox=364ms, status=yes)
12. `AKUN-012-BIGCOMMERCE-VLESS-WS-93MS` (url=315ms, nekobox=358ms, status=yes)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-95MS` (url=2250ms, nekobox=2333ms, status=yes)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-91MS` (url=323ms, nekobox=358ms, status=yes)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-93MS` (url=1284ms, nekobox=1258ms, status=no)
16. `AKUN-015-CLOUDFLARE-VLESS-WS-91MS`
17. `AKUN-016-CLOUDFLARE-VLESS-WS-92MS`
18. `AKUN-017-CLOUDFLARE-VLESS-WS-80MS`
19. `AKUN-018-CLOUDFLARE-VLESS-WS-82MS`
20. `AKUN-019-CLOUDFLARE-VLESS-WS-89MS`
21. `AKUN-020-CLOUDFLARE-VLESS-WS-91MS`
22. `AKUN-022-CLOUDFLARE-VLESS-WS-90MS` (url=345ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-94MS` (url=321ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-91MS` (url=299ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-93MS` (url=309ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-86MS` (url=319ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-94MS` (url=321ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-96MS` (url=339ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-86MS` (url=307ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-90MS` (url=314ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
