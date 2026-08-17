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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-105MS` (url=331ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=321ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-106MS`
4. `AKUN-004-ZVC-VLESS-WS-108MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-108MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-110MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-110MS` (url=324ms, status=HTTP 204)
8. `AKUN-008-EDIS-BE-NET-VLESS-WS-138MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-97MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-107MS` (url=340ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-104MS` (url=344ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-106MS` (url=322ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-106MS` (url=1327ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-110MS` (url=1322ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-140MS` (url=1322ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-109MS` (url=327ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-114MS` (url=293ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-115MS` (url=1335ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-97MS` (url=1343ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-111MS` (url=319ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-111MS` (url=338ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-113MS` (url=315ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-106MS` (url=345ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-119MS` (url=325ms, status=HTTP 204)
26. `AKUN-027-NOTION-WEB-VLESS-WS-127MS` (url=329ms, status=HTTP 204)
27. `AKUN-028-NOTION-WEB-VLESS-WS-99MS` (url=318ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-117MS` (url=342ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-99MS` (url=308ms, status=HTTP 204)
30. `AKUN-031-SC-APHRODITEGROUP-201910-VLESS-WS-115MS` (url=339ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
