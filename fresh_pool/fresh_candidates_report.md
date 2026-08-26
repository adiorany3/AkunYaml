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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-88MS` (url=349ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-91MS` (url=342ms, status=HTTP 204)
3. `AKUN-003-VEESP-VLESS-WS-94MS` (url=313ms, status=HTTP 204)
4. `AKUN-004-PAGM-NET-VLESS-WS-93MS` (url=324ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-90MS` (url=341ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-93MS` (url=420ms, status=SSLError: HTTPSConnectionPool(host='www.gstatic.com', port=443): Max retries exceeded with url: /generate_204 (Caused by SSLError()
7. `AKUN-007-TIME-VLESS-WS-92MS`
8. `AKUN-008-CHATGPT-VLESS-WS-92MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-94MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-96MS`
11. `AKUN-012-SPEEDTEST-VLESS-WS-98MS` (url=329ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-98MS` (url=355ms, status=HTTP 204)
13. `AKUN-014-AIMALL-VLESS-WS-96MS` (url=361ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-95MS` (url=338ms, status=HTTP 204)
15. `AKUN-016-DPDNS-VLESS-WS-102MS` (url=350ms, status=HTTP 204)
16. `AKUN-017-UNKNOWN-VLESS-WS-98MS` (url=311ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-99MS` (url=328ms, status=HTTP 204)
18. `AKUN-019-SPEEDTEST-VLESS-WS-98MS` (url=302ms, status=HTTP 204)
19. `AKUN-020-DEV-VLESS-WS-107MS` (url=1358ms, status=HTTP 204)
20. `AKUN-021-PAGM-NET-VLESS-WS-92MS` (url=335ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-97MS` (url=348ms, status=HTTP 204)
22. `AKUN-023-DEV-VLESS-WS-95MS` (url=305ms, status=HTTP 204)
23. `AKUN-024-UNKNOWN-VLESS-WS-96MS` (url=325ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-101MS` (url=348ms, status=HTTP 204)
25. `AKUN-026-VEESP-SIA-VLESS-WS-101MS` (url=334ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-96MS` (url=319ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-103MS` (url=1325ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-93MS` (url=343ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-100MS` (url=310ms, status=HTTP 204)
30. `AKUN-032-UNKNOWN-VLESS-WS-94MS` (url=409ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
