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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-102MS` (url=321ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
4. `AKUN-004-DEV-VLESS-WS-110MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-115MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-112MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-114MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-114MS` (url=318ms, status=HTTP 204)
9. `AKUN-009-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-105MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-105MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-109MS` (url=1368ms, status=HTTP 204)
12. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-107MS` (url=331ms, status=HTTP 204)
13. `AKUN-016-CLOUDFLARE-VLESS-WS-111MS` (url=1350ms, status=HTTP 204)
14. `AKUN-017-MEDIUM-VLESS-WS-116MS` (url=309ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-104MS` (url=345ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-105MS` (url=306ms, status=HTTP 204)
17. `AKUN-020-CLOUDFLARE-VLESS-WS-116MS` (url=1360ms, status=HTTP 204)
18. `AKUN-021-H2NEXUS-VLESS-WS-126MS` (url=425ms, status=HTTP 204)
19. `AKUN-022-CLOUDFLARE-VLESS-WS-114MS` (url=362ms, status=HTTP 204)
20. `AKUN-023-CLOUDFLARE-VLESS-WS-121MS` (url=347ms, status=HTTP 204)
21. `AKUN-024-CLOUDFLARE-VLESS-WS-112MS` (url=372ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-120MS` (url=1326ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-118MS` (url=352ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-113MS` (url=368ms, status=HTTP 204)
25. `AKUN-028-RESERVED-FOR-TW-VLESS-WS-117MS` (url=330ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-121MS` (url=1344ms, status=HTTP 204)
27. `AKUN-030-CHATGPT-VLESS-WS-122MS` (url=1366ms, status=HTTP 204)
28. `AKUN-031-DEV-VLESS-WS-122MS` (url=328ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-117MS` (url=349ms, status=HTTP 204)
30. `AKUN-034-PAGM-NET-VLESS-WS-525MS` (url=1259ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
