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
1. `AKUN-001-MEDIUM-VLESS-WS-102MS` (url=1347ms, status=HTTP 204)
2. `AKUN-002-SINGAPORE-VLESS-WS-108MS` (url=350ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-109MS` (url=1380ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-111MS` (url=330ms, status=HTTP 204)
5. `AKUN-005-CHATGPT-VLESS-WS-117MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-103MS`
7. `AKUN-007-ORACLE-VLESS-WS-126MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-114MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-114MS` (url=338ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-126MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-120MS` (url=337ms, status=HTTP 204)
12. `AKUN-013-COM-VLESS-WS-114MS` (url=360ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-117MS` (url=360ms, status=HTTP 204)
14. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-118MS` (url=362ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-130MS` (url=357ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-111MS` (url=319ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-119MS` (url=340ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-106MS` (url=350ms, status=HTTP 204)
19. `AKUN-020-RESERVED-FOR-TW-VLESS-WS-113MS` (url=329ms, status=HTTP 204)
20. `AKUN-021-OVH-VLESS-WS-156MS` (url=389ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-128MS` (url=342ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-343MS` (url=733ms, status=HTTP 204)
23. `AKUN-025-UNKNOWN-VLESS-WS-348MS` (url=759ms, status=HTTP 204)
24. `AKUN-026-NETCRAFTERS-VLESS-WS-456MS` (url=1089ms, status=HTTP 204)
25. `AKUN-027-PAGM-NET-VLESS-WS-516MS` (url=1380ms, status=HTTP 204)
26. `AKUN-030-CLOUDFLARE-VLESS-WS-692MS` (url=1303ms, status=HTTP 204)
27. `AKUN-033-CLOUDFLARE-VLESS-WS-791MS` (url=1637ms, status=HTTP 204)
28. `AKUN-036-UNKNOWN-VLESS-WS-778MS` (url=1639ms, status=HTTP 204)
29. `AKUN-038-INTERLIR-CUSTOMER-VLESS-WS-864MS` (url=2371ms, status=HTTP 204)
30. `AKUN-039-CLOUDFLARE-VLESS-WS-119MS` (url=1238ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
