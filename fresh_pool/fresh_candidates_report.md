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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-106MS` (url=350ms, nekobox=535ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS` (url=369ms, nekobox=1387ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-111MS` (url=471ms, nekobox=392ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-105MS` (url=340ms, nekobox=390ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-115MS` (url=2029ms, nekobox=1424ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-108MS` (url=2080ms, nekobox=408ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-113MS` (url=340ms, nekobox=1409ms, status=yes)
8. `AKUN-008-UNKNOWN-VLESS-WS-115MS` (url=1349ms, nekobox=376ms, status=yes)
9. `AKUN-009-CLOUDINARY-VLESS-WS-118MS` (url=373ms, nekobox=419ms, status=yes)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-116MS` (url=376ms, nekobox=399ms, status=yes)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-125MS` (url=372ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-125MS` (url=356ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-108MS` (url=367ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-108MS` (url=469ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-119MS` (url=374ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-118MS` (url=379ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-124MS` (url=368ms, status=HTTP 204)
18. `AKUN-019-SINGAPORE-VLESS-WS-118MS` (url=368ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-113MS` (url=350ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-107MS` (url=339ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-128MS` (url=359ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-105MS` (url=694ms, status=HTTP 204)
23. `AKUN-024-UNKNOWN-VLESS-WS-112MS` (url=375ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-125MS` (url=359ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-109MS` (url=1354ms, status=HTTP 204)
26. `AKUN-027-MEDIUM-VLESS-WS-105MS` (url=345ms, status=HTTP 204)
27. `AKUN-028-BIGCOMMERCE-VLESS-WS-123MS` (url=1353ms, status=HTTP 204)
28. `AKUN-029-MYBB-VLESS-WS-102MS` (url=326ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-122MS` (url=369ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-144MS` (url=341ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
