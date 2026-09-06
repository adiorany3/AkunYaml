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
1. `AKUN-001-CHATGPT-VLESS-WS-104MS` (url=359ms, nekobox=401ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-103MS` (url=341ms, nekobox=371ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-105MS` (url=350ms, nekobox=393ms, status=yes)
4. `AKUN-004-SINGAPORE-VLESS-WS-110MS` (url=372ms, nekobox=377ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-120MS` (url=316ms, nekobox=1372ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-112MS` (url=350ms, nekobox=389ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-115MS` (url=1392ms, nekobox=1366ms, status=yes)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-107MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-111MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-113MS` (url=365ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-97MS` (url=310ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-115MS` (url=372ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-116MS` (url=1338ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-107MS` (url=310ms, status=HTTP 204)
16. `AKUN-017-UNKNOWN-VLESS-WS-105MS` (url=358ms, status=HTTP 204)
17. `AKUN-018-MEDIUM-VLESS-WS-108MS` (url=330ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-116MS` (url=350ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-112MS` (url=1362ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-132MS` (url=348ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-111MS` (url=368ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-113MS` (url=359ms, status=HTTP 204)
23. `AKUN-024-CLOUDINARY-VLESS-WS-129MS` (url=1372ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-121MS` (url=1369ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-119MS` (url=329ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-119MS` (url=349ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-122MS` (url=351ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-116MS` (url=377ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-101MS` (url=343ms, status=HTTP 204)
30. `AKUN-032-CLOUDFLARE-VLESS-WS-114MS` (url=350ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
