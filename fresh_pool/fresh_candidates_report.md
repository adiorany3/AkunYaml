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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-106MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-109MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-113MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-114MS`
7. `AKUN-007-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-116MS`
8. `AKUN-008-RS-RAPIDSEEDBOX-20190717-VLESS-WS-121MS`
9. `AKUN-009-DEV-VLESS-WS-107MS`
10. `AKUN-010-CHATGPT-VLESS-WS-114MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-113MS` (url=350ms, status=HTTP 204)
12. `AKUN-015-UNKNOWN-VLESS-WS-107MS` (url=1552ms, status=HTTP 204)
13. `AKUN-016-RESERVED-FOR-TW-VLESS-WS-107MS` (url=1319ms, status=HTTP 204)
14. `AKUN-017-BIGCOMMERCE-VLESS-WS-116MS` (url=360ms, status=HTTP 204)
15. `AKUN-018-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=339ms, status=HTTP 204)
16. `AKUN-019-RS-RAPIDSEEDBOX-20190717-VLESS-WS-116MS` (url=361ms, status=HTTP 204)
17. `AKUN-020-DEV-VLESS-WS-113MS` (url=360ms, status=HTTP 204)
18. `AKUN-021-CLOUDFLARE-VLESS-WS-116MS` (url=357ms, status=HTTP 204)
19. `AKUN-022-CLOUDFLARE-VLESS-WS-126MS` (url=1372ms, status=HTTP 204)
20. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-114MS` (url=332ms, status=HTTP 204)
21. `AKUN-025-UNKNOWN-VLESS-WS-110MS` (url=360ms, status=HTTP 204)
22. `AKUN-026-CLOUDFLARE-VLESS-WS-101MS` (url=340ms, status=HTTP 204)
23. `AKUN-027-7ZZ-VLESS-WS-120MS` (url=889ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-337MS` (url=1051ms, status=HTTP 204)
25. `AKUN-029-UNKNOWN-VLESS-WS-375MS` (url=1809ms, status=HTTP 204)
26. `AKUN-030-NETCRAFTERS-VLESS-WS-465MS` (url=2229ms, status=HTTP 204)
27. `AKUN-034-DEV-VLESS-WS-130MS` (url=2122ms, status=HTTP 204)
28. `AKUN-035-CLOUDFLARE-VLESS-WS-114MS` (url=2170ms, status=HTTP 204)
29. `AKUN-036-MEDIUM-VLESS-WS-102MS` (url=1359ms, status=HTTP 204)
30. `AKUN-037-CLOUDFLARE-VLESS-WS-107MS` (url=359ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
