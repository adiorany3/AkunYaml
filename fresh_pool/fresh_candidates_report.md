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
1. `AKUN-001-UNKNOWN-VLESS-WS-102MS` (url=384ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-105MS` (url=340ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-117MS` (url=333ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS` (url=371ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-116MS` (url=364ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-117MS` (url=336ms, status=HTTP 204)
7. `AKUN-007-RS-RAPIDSEEDBOX-20190717-VLESS-WS-101MS` (url=409ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-111MS` (url=324ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-117MS` (url=351ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-116MS` (url=383ms, status=HTTP 204)
11. `AKUN-011-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-118MS` (url=1637ms, status=HTTP 204)
12. `AKUN-012-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-119MS` (url=320ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-118MS` (url=372ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-119MS` (url=373ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-120MS` (url=375ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-120MS` (url=343ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-120MS` (url=377ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-102MS` (url=337ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-117MS` (url=327ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-106MS` (url=344ms, status=HTTP 204)
21. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-101MS` (url=361ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-121MS` (url=350ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-121MS` (url=364ms, status=HTTP 204)
24. `AKUN-027-NOTION-WEB-VLESS-WS-110MS` (url=368ms, status=HTTP 204)
25. `AKUN-028-CLOUDFLARE-VLESS-WS-113MS` (url=371ms, status=HTTP 204)
26. `AKUN-029-UNKNOWN-VLESS-WS-118MS` (url=360ms, status=HTTP 204)
27. `AKUN-030-SPEEDTEST-VLESS-WS-121MS` (url=338ms, status=HTTP 204)
28. `AKUN-031-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-105MS` (url=1376ms, status=HTTP 204)
29. `AKUN-033-CLOUDFLARE-VLESS-WS-114MS` (url=351ms, status=HTTP 204)
30. `AKUN-034-CLOUDFLARE-VLESS-WS-110MS` (url=380ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
