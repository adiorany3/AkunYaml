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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-117MS` (url=1403ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=1332ms, status=HTTP 204)
3. `AKUN-003-ZVC-VLESS-WS-117MS` (url=1358ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-119MS` (url=1365ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-120MS` (url=373ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-127MS` (url=367ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-119MS` (url=315ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-122MS` (url=369ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-128MS` (url=347ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-121MS` (url=349ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-121MS` (url=359ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-115MS` (url=329ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-125MS` (url=368ms, status=HTTP 204)
14. `AKUN-014-NOTION-WEB-VLESS-WS-110MS` (url=349ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-114MS` (url=347ms, status=HTTP 204)
16. `AKUN-016-BIGCOMMERCE-VLESS-WS-127MS` (url=373ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-127MS` (url=1350ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-130MS` (url=373ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-125MS` (url=365ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-118MS` (url=359ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-239MS` (url=450ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-107MS` (url=351ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-119MS` (url=341ms, status=HTTP 204)
24. `AKUN-025-UNKNOWN-VLESS-WS-139MS` (url=916ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-644MS` (url=1216ms, status=HTTP 204)
26. `AKUN-027-UNKNOWN-VLESS-WS-148MS` (url=909ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-125MS` (url=901ms, status=HTTP 204)
28. `AKUN-031-MYBB-VLESS-WS-111MS` (url=330ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-125MS` (url=337ms, status=HTTP 204)
30. `AKUN-033-UNKNOWN-VLESS-WS-118MS` (url=1348ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
