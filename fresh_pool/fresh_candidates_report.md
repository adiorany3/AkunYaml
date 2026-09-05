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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-98MS` (url=1385ms, status=HTTP 204)
2. `AKUN-002-BIGCOMMERCE-VLESS-WS-100MS` (url=375ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-96MS` (url=380ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-96MS` (url=368ms, status=HTTP 204)
5. `AKUN-005-MEDIUM-VLESS-WS-104MS` (url=339ms, status=HTTP 204)
6. `AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-102MS` (url=353ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-103MS` (url=363ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-102MS` (url=1367ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-101MS` (url=361ms, status=HTTP 204)
10. `AKUN-010-UNKNOWN-VLESS-WS-107MS` (url=372ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-104MS` (url=380ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-113MS` (url=392ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-107MS` (url=337ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-115MS` (url=347ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-103MS` (url=339ms, status=HTTP 204)
16. `AKUN-016-CLOUDINARY-VLESS-WS-114MS` (url=371ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-106MS` (url=368ms, status=HTTP 204)
18. `AKUN-019-CHATGPT-VLESS-WS-115MS` (url=358ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-108MS` (url=369ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-117MS` (url=1031ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-102MS` (url=1380ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-114MS` (url=1388ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-122MS` (url=538ms, status=HTTP 204)
24. `AKUN-025-DEV-VLESS-WS-112MS` (url=921ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-105MS` (url=369ms, status=HTTP 204)
26. `AKUN-027-CHATGPT-VLESS-WS-110MS` (url=360ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-107MS` (url=354ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-126MS` (url=1377ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-107MS` (url=371ms, status=HTTP 204)
30. `AKUN-032-NOTION-WEB-VLESS-WS-117MS` (url=359ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
