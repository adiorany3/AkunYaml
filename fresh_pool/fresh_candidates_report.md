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
- Kandidat strict NekoBox-tested: 0
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
1. `AKUN-001-CHATGPT-VLESS-WS-109MS` (url=388ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-107MS` (url=349ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-108MS` (url=350ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-109MS` (url=381ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-103MS` (url=370ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-105MS` (url=358ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-108MS` (url=350ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-116MS` (url=370ms, status=HTTP 204)
9. `AKUN-009-NOTION-WEB-VLESS-WS-110MS` (url=362ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-105MS` (url=337ms, status=HTTP 204)
11. `AKUN-011-MYBB-VLESS-WS-110MS` (url=319ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-113MS` (url=1330ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-115MS` (url=329ms, status=HTTP 204)
14. `AKUN-014-MEDIUM-VLESS-WS-112MS` (url=329ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-117MS` (url=369ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-117MS` (url=391ms, status=HTTP 204)
17. `AKUN-017-DEV-VLESS-WS-103MS` (url=1982ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-118MS` (url=1364ms, status=HTTP 204)
19. `AKUN-019-UNKNOWN-VLESS-WS-127MS` (url=1004ms, status=HTTP 204)
20. `AKUN-020-CLOUDINARY-VLESS-WS-116MS` (url=1367ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-112MS` (url=709ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-112MS` (url=1319ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-114MS` (url=349ms, status=HTTP 204)
24. `AKUN-025-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-108MS` (url=1400ms, status=HTTP 204)
25. `AKUN-026-BIGCOMMERCE-VLESS-WS-132MS` (url=359ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-113MS` (url=360ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-115MS` (url=350ms, status=HTTP 204)
28. `AKUN-030-DEV-VLESS-WS-108MS` (url=1622ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-125MS` (url=355ms, status=HTTP 204)
30. `AKUN-032-SINGAPORE-VLESS-WS-127MS` (url=2374ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
