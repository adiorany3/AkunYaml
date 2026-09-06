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
- Kandidat strict NekoBox-tested: 5
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS` (url=371ms, status=HTTP 204)
2. `AKUN-002-NOTION-WEB-VLESS-WS-106MS` (url=383ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=346ms, nekobox=6175ms, status=no)
4. `AKUN-004-BIGCOMMERCE-VLESS-WS-115MS` (url=370ms, status=HTTP 204)
5. `AKUN-003-CLOUDFLARE-VLESS-WS-103MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-114MS` (url=340ms, nekobox=267ms, status=no)
7. `AKUN-005-CLOUDFLARE-VLESS-WS-113MS`
8. `AKUN-010-COM-VLESS-WS-117MS` (url=389ms, status=HTTP 204)
9. `AKUN-011-CLOUDFLARE-VLESS-WS-120MS` (url=380ms, status=HTTP 204)
10. `AKUN-012-CLOUDFLARE-VLESS-WS-99MS` (url=349ms, nekobox=6187ms, status=no)
11. `AKUN-013-CLOUDINARY-VLESS-WS-124MS` (url=379ms, status=HTTP 204)
12. `AKUN-004-CLOUDFLARE-VLESS-WS-106MS`
13. `AKUN-015-DEV-VLESS-WS-123MS` (url=359ms, nekobox=263ms, status=no)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-126MS` (url=440ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-122MS` (url=1123ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-174MS` (url=949ms, status=HTTP 204)
17. `AKUN-020-CLOUDFLARE-VLESS-WS-787MS` (url=2509ms, status=HTTP 204)
18. `AKUN-023-CLOUDFLARE-VLESS-WS-863MS` (url=1895ms, status=HTTP 204)
19. `AKUN-030-CLOUDFLARE-VLESS-WS-114MS` (url=372ms, status=HTTP 204)
20. `AKUN-031-CLOUDFLARE-VLESS-WS-146MS` (url=361ms, nekobox=6186ms, status=no)
21. `AKUN-032-CLOUDFLARE-VLESS-WS-117MS` (url=1388ms, status=HTTP 204)
22. `AKUN-033-CLOUDFLARE-VLESS-WS-125MS` (url=1357ms, status=HTTP 204)
23. `AKUN-034-CLOUDFLARE-VLESS-WS-135MS` (url=1352ms, status=HTTP 204)
24. `AKUN-035-CLOUDFLARE-VLESS-WS-652MS` (url=919ms, status=HTTP 204)
25. `AKUN-037-PAI50288-VLESS-WS-1194MS` (url=2029ms, status=HTTP 204)
26. `AKUN-040-DEV-VLESS-WS-116MS` (url=2724ms, status=HTTP 204)
27. `AKUN-043-CLOUDFLARE-VLESS-WS-737MS` (url=2292ms, status=HTTP 204)
28. `AKUN-045-SOFT10-VLESS-WS-959MS` (url=3503ms, status=HTTP 204)
29. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS`
30. `AKUN-001-CLOUDFLARE-VLESS-WS-116MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
