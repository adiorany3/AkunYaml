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
1. `AKUN-001-UNKNOWN-VLESS-WS-89MS` (url=362ms, status=HTTP 204)
2. `AKUN-002-MYBB-VLESS-WS-88MS` (url=316ms, status=HTTP 204)
3. `AKUN-003-ZVC-VLESS-WS-91MS` (url=322ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-92MS` (url=343ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-86MS` (url=315ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-89MS` (url=327ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-94MS` (url=337ms, status=HTTP 204)
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-92MS` (url=322ms, status=HTTP 204)
9. `AKUN-009-UNKNOWN-VLESS-WS-87MS` (url=328ms, status=HTTP 204)
10. `AKUN-010-CHATGPT-VLESS-WS-94MS` (url=342ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-86MS` (url=332ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-94MS` (url=694ms, status=HTTP 204)
13. `AKUN-013-UNKNOWN-VLESS-WS-89MS` (url=325ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-91MS` (url=321ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-90MS` (url=331ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-91MS` (url=336ms, status=HTTP 204)
17. `AKUN-017-UNKNOWN-VLESS-WS-91MS` (url=325ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-92MS` (url=324ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-92MS` (url=337ms, status=HTTP 204)
20. `AKUN-020-TIME-VLESS-WS-93MS` (url=331ms, status=HTTP 204)
21. `AKUN-021-UNKNOWN-VLESS-WS-93MS` (url=342ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-91MS` (url=328ms, status=HTTP 204)
23. `AKUN-023-DEV-VLESS-WS-94MS` (url=325ms, status=HTTP 204)
24. `AKUN-024-UNKNOWN-VLESS-WS-96MS` (url=320ms, status=HTTP 204)
25. `AKUN-025-UNKNOWN-VLESS-WS-89MS` (url=345ms, status=HTTP 204)
26. `AKUN-026-UNKNOWN-VLESS-WS-98MS` (url=340ms, status=HTTP 204)
27. `AKUN-027-UNKNOWN-VLESS-WS-93MS` (url=337ms, status=HTTP 204)
28. `AKUN-028-UNKNOWN-VLESS-WS-94MS` (url=325ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-86MS` (url=330ms, status=HTTP 204)
30. `AKUN-030-UNKNOWN-VLESS-WS-92MS` (url=334ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
