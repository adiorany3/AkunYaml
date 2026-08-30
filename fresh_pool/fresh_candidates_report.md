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
1. `AKUN-001-DEV-VLESS-WS-106MS` (url=368ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=351ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=440ms, status=SSLError: HTTPSConnectionPool(host='www.gstatic.com', port=443): Max retries exceeded with url: /generate_204 (Caused by SSLError()
4. `AKUN-004-CLOUDFLARE-VLESS-WS-114MS` (url=353ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-114MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-117MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-118MS`
8. `AKUN-008-CHATGPT-VLESS-WS-116MS`
9. `AKUN-009-DEV-VLESS-WS-105MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-114MS`
11. `AKUN-014-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-112MS` (url=1362ms, status=HTTP 204)
12. `AKUN-015-CLOUDFLARE-VLESS-WS-105MS` (url=370ms, status=HTTP 204)
13. `AKUN-016-RS-RAPIDSEEDBOX-20190717-VLESS-WS-130MS` (url=356ms, status=HTTP 204)
14. `AKUN-017-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=1331ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-111MS` (url=1378ms, status=HTTP 204)
16. `AKUN-019-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=345ms, status=HTTP 204)
17. `AKUN-020-MYBB-VLESS-WS-125MS` (url=343ms, status=HTTP 204)
18. `AKUN-022-MEDIUM-VLESS-WS-105MS` (url=333ms, status=HTTP 204)
19. `AKUN-023-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-114MS` (url=359ms, status=HTTP 204)
20. `AKUN-024-CLOUDFLARE-VLESS-WS-114MS` (url=1359ms, status=HTTP 204)
21. `AKUN-025-UNKNOWN-VLESS-WS-117MS` (url=360ms, status=HTTP 204)
22. `AKUN-026-CLOUDFLARE-VLESS-WS-114MS` (url=370ms, status=HTTP 204)
23. `AKUN-027-CLOUDFLARE-VLESS-WS-122MS` (url=1358ms, status=HTTP 204)
24. `AKUN-028-RESERVED-FOR-TW-VLESS-WS-135MS` (url=1340ms, status=HTTP 204)
25. `AKUN-029-CLOUDFLARE-VLESS-WS-124MS` (url=350ms, status=HTTP 204)
26. `AKUN-030-7ZZ-VLESS-WS-125MS` (url=749ms, status=HTTP 204)
27. `AKUN-031-CLOUDFLARE-VLESS-WS-350MS` (url=1920ms, status=HTTP 204)
28. `AKUN-032-VISA-VLESS-WS-284MS` (url=707ms, status=HTTP 204)
29. `AKUN-033-NETCRAFTERS-VLESS-WS-480MS` (url=1074ms, status=HTTP 204)
30. `AKUN-034-PAGM-NET-VLESS-WS-508MS` (url=1285ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
