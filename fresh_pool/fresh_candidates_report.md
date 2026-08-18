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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-103MS` (url=326ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-105MS` (url=312ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-110MS` (url=330ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-108MS` (url=296ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-109MS` (url=308ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-100MS` (url=6146ms, status=ReadTimeout: HTTPSConnectionPool(host='www.gstatic.com', port=443): Read timed out. (read timeout=6.0))
7. `AKUN-007-CLOUDFLARE-VLESS-WS-114MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-108MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-94MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-110MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-103MS` (url=326ms, status=HTTP 204)
12. `AKUN-013-BIGCOMMERCE-VLESS-WS-104MS` (url=345ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-107MS` (url=343ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-107MS` (url=3331ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-112MS` (url=320ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-79MS` (url=308ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-107MS` (url=321ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-107MS` (url=307ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-109MS` (url=317ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-114MS` (url=1364ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-105MS` (url=307ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-113MS` (url=305ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-110MS` (url=310ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-122MS` (url=310ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-141MS` (url=1307ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-98MS` (url=1331ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-103MS` (url=314ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-136MS` (url=317ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-106MS` (url=325ms, status=HTTP 204)
30. `AKUN-032-CLOUDFLARE-VLESS-WS-108MS` (url=334ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
