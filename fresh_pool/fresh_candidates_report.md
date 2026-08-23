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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-87MS` (url=345ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-87MS` (url=342ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-90MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-86MS` (url=1319ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-87MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-84MS` (url=323ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-89MS` (url=323ms, status=HTTP 204)
8. `AKUN-008-OPENAI-VLESS-WS-90MS` (url=345ms, status=HTTP 204)
9. `AKUN-009-UNKNOWN-VLESS-WS-90MS` (url=323ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-92MS` (url=328ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-88MS` (url=310ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-87MS` (url=306ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-91MS` (url=304ms, status=HTTP 204)
14. `AKUN-014-SPEEDTEST-VLESS-WS-95MS` (url=338ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-95MS` (url=328ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-96MS` (url=340ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-97MS` (url=309ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-89MS` (url=328ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-91MS` (url=334ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-91MS` (url=1324ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-92MS` (url=320ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-93MS` (url=319ms, status=HTTP 204)
23. `AKUN-023-SPEEDTEST-VLESS-WS-98MS` (url=323ms, status=HTTP 204)
24. `AKUN-024-RUSSIA-VLESS-WS-90MS` (url=352ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-85MS` (url=323ms, status=HTTP 204)
26. `AKUN-026-DEV-VLESS-WS-99MS` (url=365ms, status=HTTP 204)
27. `AKUN-027-ADF-VLESS-WS-100MS` (url=310ms, status=HTTP 204)
28. `AKUN-028-FMN5-RENTED-NET2-VLESS-WS-90MS` (url=331ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-92MS` (url=314ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-86MS` (url=312ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
