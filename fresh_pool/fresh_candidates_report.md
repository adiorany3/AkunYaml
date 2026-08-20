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
1. `AKUN-001-UNKNOWN-VLESS-WS-67MS`
2. `AKUN-002-1PASSWORD-VLESS-WS-65MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-66MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-37MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-64MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-70MS`
7. `AKUN-007-MEDIUM-VLESS-WS-68MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-68MS`
9. `AKUN-009-DEV-VLESS-WS-74MS`
10. `AKUN-010-DEV-VLESS-WS-74MS` (url=700ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-47MS` (url=286ms, status=HTTP 204)
12. `AKUN-013-UNKNOWN-VLESS-WS-74MS` (url=310ms, status=HTTP 204)
13. `AKUN-014-ADF-VLESS-WS-76MS` (url=286ms, status=HTTP 204)
14. `AKUN-015-TIME-VLESS-WS-79MS` (url=310ms, status=HTTP 204)
15. `AKUN-016-OPENAI-VLESS-WS-58MS` (url=307ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-66MS` (url=307ms, status=HTTP 204)
17. `AKUN-018-RS-RAPIDSEEDBOX-20190717-VLESS-WS-73MS` (url=307ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-76MS` (url=313ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-73MS` (url=284ms, status=HTTP 204)
20. `AKUN-021-CCWU-VLESS-WS-78MS` (url=313ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-82MS` (url=309ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-66MS` (url=301ms, status=HTTP 204)
23. `AKUN-024-UNKNOWN-VLESS-WS-67MS` (url=278ms, status=HTTP 204)
24. `AKUN-025-SPEEDTEST-VLESS-WS-69MS` (url=316ms, status=HTTP 204)
25. `AKUN-026-SPEEDTEST-VLESS-WS-75MS` (url=275ms, status=HTTP 204)
26. `AKUN-027-DEV-VLESS-WS-68MS` (url=276ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-72MS` (url=311ms, status=HTTP 204)
28. `AKUN-029-SPEEDTEST-VLESS-WS-50MS` (url=295ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-64MS` (url=309ms, status=HTTP 204)
30. `AKUN-031-UNKNOWN-VLESS-WS-66MS` (url=315ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
