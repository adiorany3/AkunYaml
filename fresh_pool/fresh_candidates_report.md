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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-99MS` (url=325ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=367ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-108MS` (url=369ms, status=HTTP 204)
4. `AKUN-004-NOTION-WEB-VLESS-WS-103MS` (url=332ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-109MS` (url=322ms, status=HTTP 204)
6. `AKUN-006-CHATGPT-VLESS-WS-101MS` (url=371ms, status=HTTP 204)
7. `AKUN-007-DEV-VLESS-WS-106MS` (url=340ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-105MS` (url=368ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-115MS` (url=379ms, status=HTTP 204)
10. `AKUN-010-CLOUDINARY-VLESS-WS-121MS` (url=370ms, status=HTTP 204)
11. `AKUN-011-CHATGPT-VLESS-WS-111MS` (url=319ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-107MS` (url=371ms, status=HTTP 204)
13. `AKUN-013-UNKNOWN-VLESS-WS-116MS` (url=359ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-117MS` (url=378ms, status=HTTP 204)
15. `AKUN-015-UNKNOWN-VLESS-WS-121MS` (url=367ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-128MS` (url=390ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-173MS` (url=342ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-354MS` (url=1168ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-199MS` (url=513ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-115MS` (url=890ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-125MS` (url=2019ms, status=HTTP 204)
22. `AKUN-026-CLOUDFLARE-VLESS-WS-837MS` (url=1452ms, status=HTTP 204)
23. `AKUN-047-BIGCOMMERCE-VLESS-WS-105MS` (url=1373ms, status=HTTP 204)
24. `AKUN-048-CLOUDFLARE-VLESS-WS-118MS` (url=1371ms, status=HTTP 204)
25. `AKUN-049-UNKNOWN-VLESS-WS-111MS` (url=328ms, status=HTTP 204)
26. `AKUN-050-CLOUDFLARE-VLESS-WS-109MS` (url=340ms, status=HTTP 204)
27. `AKUN-051-CLOUDFLARE-VLESS-WS-125MS` (url=1358ms, status=HTTP 204)
28. `AKUN-052-CLOUDFLARE-VLESS-WS-830MS` (url=919ms, status=HTTP 204)
29. `AKUN-053-CLOUDFLARE-VLESS-WS-141MS` (url=448ms, status=HTTP 204)
30. `AKUN-056-CLOUDFLARE-VLESS-WS-722MS` (url=3392ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
