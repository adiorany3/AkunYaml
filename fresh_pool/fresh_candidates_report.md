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
- Kandidat strict NekoBox-tested: 6
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-103MS` (url=748ms, status=HTTP 204)
2. `AKUN-006-UNKNOWN-VLESS-WS-105MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-105MS` (url=346ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-95MS` (url=359ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-101MS` (url=1350ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-104MS` (url=358ms, status=HTTP 204)
7. `AKUN-007-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-103MS` (url=319ms, nekobox=286ms, status=no)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-105MS` (url=381ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-106MS` (url=1778ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-100MS` (url=350ms, status=HTTP 204)
11. `AKUN-011-DEV-VLESS-WS-118MS` (url=320ms, nekobox=245ms, status=no)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-114MS` (url=409ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-108MS` (url=370ms, status=HTTP 204)
14. `AKUN-014-NOTION-WEB-VLESS-WS-125MS` (url=368ms, status=HTTP 204)
15. `AKUN-015-GTHOST-VLESS-WS-121MS` (url=1740ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-101MS` (url=357ms, status=HTTP 204)
17. `AKUN-005-ORG-VLESS-WS-121MS`
18. `AKUN-001-CLOUDFLARE-VLESS-WS-101MS`
19. `AKUN-020-UNKNOWN-VLESS-WS-118MS` (url=368ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-120MS` (url=331ms, nekobox=6180ms, status=no)
21. `AKUN-022-UNKNOWN-VLESS-WS-110MS` (url=328ms, nekobox=293ms, status=no)
22. `AKUN-003-CLOUDFLARE-VLESS-WS-99MS`
23. `AKUN-002-CLOUDFLARE-VLESS-WS-99MS`
24. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS`
25. `AKUN-026-CLOUDFLARE-VLESS-WS-113MS` (url=361ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-103MS` (url=359ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-109MS` (url=350ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-119MS` (url=349ms, status=HTTP 204)
29. `AKUN-031-UNKNOWN-VLESS-WS-127MS` (url=372ms, status=HTTP 204)
30. `AKUN-032-CLOUDFLARE-VLESS-WS-105MS` (url=438ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
