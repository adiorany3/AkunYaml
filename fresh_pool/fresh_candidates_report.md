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
1. `AKUN-001-UNKNOWN-VLESS-WS-102MS` (url=371ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-106MS` (url=369ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-109MS` (url=331ms, status=HTTP 204)
4. `AKUN-004-NOTION-WEB-VLESS-WS-106MS` (url=349ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-110MS` (url=382ms, status=HTTP 204)
6. `AKUN-006-MYBB-VLESS-WS-108MS` (url=337ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS` (url=370ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-108MS` (url=719ms, status=HTTP 204)
9. `AKUN-009-MEDIUM-VLESS-WS-110MS` (url=319ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-117MS` (url=379ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-112MS` (url=1360ms, status=HTTP 204)
12. `AKUN-012-DEV-VLESS-WS-118MS` (url=908ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-109MS` (url=350ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-126MS` (url=363ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-108MS` (url=372ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-114MS` (url=349ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-106MS` (url=340ms, status=HTTP 204)
18. `AKUN-019-BIGCOMMERCE-VLESS-WS-115MS` (url=348ms, status=HTTP 204)
19. `AKUN-020-CLOUDINARY-VLESS-WS-108MS` (url=1370ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-116MS` (url=350ms, status=HTTP 204)
21. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-114MS` (url=370ms, status=HTTP 204)
22. `AKUN-023-SINGAPORE-VLESS-WS-105MS` (url=379ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-123MS` (url=349ms, status=HTTP 204)
24. `AKUN-025-CHATGPT-VLESS-WS-105MS` (url=1350ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-122MS` (url=348ms, status=HTTP 204)
26. `AKUN-027-RS-RAPIDSEEDBOX-20190717-VLESS-WS-116MS` (url=350ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-120MS` (url=435ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-372MS` (url=686ms, status=HTTP 204)
29. `AKUN-033-CLOUDFLARE-VLESS-WS-117MS` (url=2066ms, status=HTTP 204)
30. `AKUN-034-DEV-VLESS-WS-116MS` (url=894ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
