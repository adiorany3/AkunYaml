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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-67MS` (url=291ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-37MS` (url=285ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-34MS` (url=299ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-68MS` (url=333ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-73MS` (url=306ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-73MS` (url=313ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-71MS` (url=410ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-72MS` (url=974ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-68MS` (url=297ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-71MS` (url=297ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-76MS` (url=378ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-67MS` (url=319ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-68MS` (url=299ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-75MS` (url=1063ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-62MS` (url=306ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-67MS` (url=323ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-71MS` (url=297ms, status=HTTP 204)
18. `AKUN-018-DEV-VLESS-WS-72MS` (url=522ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-74MS` (url=700ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-67MS` (url=307ms, status=HTTP 204)
21. `AKUN-021-DEV-VLESS-WS-70MS` (url=310ms, status=HTTP 204)
22. `AKUN-022-DEV-VLESS-WS-74MS` (url=399ms, status=HTTP 204)
23. `AKUN-023-RS-RAPIDSEEDBOX-20190717-VLESS-WS-73MS` (url=313ms, status=HTTP 204)
24. `AKUN-024-MEDIUM-VLESS-WS-75MS` (url=293ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-76MS` (url=307ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-63MS` (url=306ms, status=HTTP 204)
27. `AKUN-027-UNKNOWN-VLESS-WS-75MS` (url=283ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-84MS` (url=314ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-72MS` (url=304ms, status=HTTP 204)
30. `AKUN-031-UNKNOWN-VLESS-WS-81MS` (url=316ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
