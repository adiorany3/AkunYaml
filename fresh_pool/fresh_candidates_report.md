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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS` (url=373ms, status=HTTP 204)
2. `AKUN-003-BIGCOMMERCE-VLESS-WS-104MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-106MS` (url=361ms, status=HTTP 204)
4. `AKUN-004-TIME-VLESS-WS-110MS` (url=361ms, status=HTTP 204)
5. `AKUN-005-DEV-VLESS-WS-101MS` (url=436ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-104MS` (url=400ms, status=HTTP 204)
7. `AKUN-005-CLOUDFLARE-VLESS-WS-107MS`
8. `AKUN-008-NOTION-WEB-VLESS-WS-110MS` (url=340ms, nekobox=6173ms, status=no)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-113MS` (url=364ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-103MS` (url=315ms, nekobox=1432ms, status=no)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-105MS` (url=373ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-105MS` (url=370ms, status=HTTP 204)
13. `AKUN-014-DEV-VLESS-WS-112MS` (url=323ms, nekobox=273ms, status=no)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-116MS` (url=375ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-106MS` (url=373ms, status=HTTP 204)
16. `AKUN-002-ORG-VLESS-WS-116MS`
17. `AKUN-018-CLOUDFLARE-VLESS-WS-126MS` (url=1517ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-108MS` (url=360ms, nekobox=261ms, status=no)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-115MS` (url=1353ms, status=HTTP 204)
20. `AKUN-004-CLOUDFLARE-VLESS-WS-118MS`
21. `AKUN-023-CLOUDFLARE-VLESS-WS-116MS` (url=1341ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-112MS` (url=376ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-113MS` (url=1353ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-127MS` (url=367ms, status=HTTP 204)
25. `AKUN-027-UNKNOWN-VLESS-WS-111MS` (url=358ms, nekobox=6177ms, status=no)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-386MS` (url=719ms, status=HTTP 204)
27. `AKUN-032-DEV-VLESS-WS-114MS` (url=920ms, status=HTTP 204)
28. `AKUN-033-CLOUDFLARE-VLESS-WS-124MS` (url=1970ms, status=HTTP 204)
29. `AKUN-001-CLOUDFLARE-VLESS-WS-120MS`
30. `AKUN-045-UNKNOWN-VLESS-WS-119MS` (url=371ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
