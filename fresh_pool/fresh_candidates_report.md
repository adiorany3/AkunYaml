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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-113MS` (url=343ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-106MS` (url=519ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-103MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS`
5. `AKUN-005-DEV-VLESS-WS-118MS`
6. `AKUN-006-CHATGPT-VLESS-WS-104MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-117MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-104MS`
9. `AKUN-009-RS-RAPIDSEEDBOX-20190717-VLESS-WS-103MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-121MS`
11. `AKUN-012-DEV-VLESS-WS-115MS` (url=360ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-123MS` (url=1820ms, status=HTTP 204)
13. `AKUN-014-MEDIUM-VLESS-WS-117MS` (url=328ms, status=HTTP 204)
14. `AKUN-015-DEV-VLESS-WS-121MS` (url=629ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-112MS` (url=370ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-111MS` (url=336ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-114MS` (url=353ms, status=HTTP 204)
18. `AKUN-019-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=1347ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-119MS` (url=3100ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-123MS` (url=341ms, status=HTTP 204)
21. `AKUN-022-MYBB-VLESS-WS-124MS` (url=347ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-105MS` (url=371ms, status=HTTP 204)
23. `AKUN-024-7ZZ-VLESS-WS-120MS` (url=371ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-126MS` (url=1368ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-331MS` (url=629ms, status=HTTP 204)
26. `AKUN-027-VISA-VLESS-WS-308MS` (url=629ms, status=HTTP 204)
27. `AKUN-028-PAGM-NET-VLESS-WS-504MS` (url=1219ms, status=HTTP 204)
28. `AKUN-029-PAGM-NET-VLESS-WS-506MS` (url=1421ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-711MS` (url=2358ms, status=HTTP 204)
30. `AKUN-031-UNKNOWN-VLESS-WS-401MS` (url=1560ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
