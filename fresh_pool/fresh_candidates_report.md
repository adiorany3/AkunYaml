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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-114MS` (url=342ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-109MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-113MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-118MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-114MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-114MS` (url=1739ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-122MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-120MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-109MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-112MS` (url=1610ms, status=HTTP 204)
12. `AKUN-014-DEV-VLESS-WS-114MS` (url=1480ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-116MS` (url=389ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-110MS` (url=330ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-118MS` (url=378ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-119MS` (url=362ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-125MS` (url=387ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-127MS` (url=400ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-110MS` (url=369ms, status=HTTP 204)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-115MS` (url=337ms, status=HTTP 204)
21. `AKUN-023-CLOUDFLARE-VLESS-WS-116MS` (url=342ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-117MS` (url=369ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-108MS` (url=367ms, status=HTTP 204)
24. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=350ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-113MS` (url=332ms, status=HTTP 204)
26. `AKUN-028-UNKNOWN-VLESS-WS-116MS` (url=1380ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-125MS` (url=361ms, status=HTTP 204)
28. `AKUN-031-UK-GB-DCL-01-20191003-VLESS-WS-150MS` (url=1412ms, status=HTTP 204)
29. `AKUN-032-UNKNOWN-VLESS-WS-124MS` (url=460ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-313MS` (url=2729ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
