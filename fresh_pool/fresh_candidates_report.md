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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-65MS` (url=310ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-63MS` (url=276ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-65MS` (url=279ms, status=HTTP 204)
4. `AKUN-004-MEDIUM-VLESS-WS-67MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-69MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-70MS`
7. `AKUN-007-MYBB-VLESS-WS-65MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-67MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-68MS`
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-70MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-66MS` (url=491ms, status=HTTP 204)
12. `AKUN-016-BIGCOMMERCE-VLESS-WS-67MS` (url=282ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-67MS` (url=302ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-71MS` (url=1089ms, status=HTTP 204)
15. `AKUN-020-CLOUDFLARE-VLESS-WS-65MS` (url=318ms, status=HTTP 204)
16. `AKUN-021-CLOUDFLARE-VLESS-WS-68MS` (url=305ms, status=HTTP 204)
17. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-64MS` (url=281ms, status=HTTP 204)
18. `AKUN-023-CLOUDFLARE-VLESS-WS-66MS` (url=285ms, status=HTTP 204)
19. `AKUN-024-CLOUDFLARE-VLESS-WS-67MS` (url=308ms, status=HTTP 204)
20. `AKUN-025-CLOUDFLARE-VLESS-WS-66MS` (url=278ms, status=HTTP 204)
21. `AKUN-026-CHATGPT-VLESS-WS-68MS` (url=287ms, status=HTTP 204)
22. `AKUN-027-COM-VLESS-WS-69MS` (url=287ms, status=HTTP 204)
23. `AKUN-028-DEV-VLESS-WS-69MS` (url=285ms, status=HTTP 204)
24. `AKUN-029-RS-RAPIDSEEDBOX-20190717-VLESS-WS-68MS` (url=280ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-70MS` (url=282ms, status=HTTP 204)
26. `AKUN-032-CLOUDFLARE-VLESS-WS-71MS` (url=725ms, status=HTTP 204)
27. `AKUN-033-CLOUDFLARE-VLESS-WS-65MS` (url=282ms, status=HTTP 204)
28. `AKUN-034-CLOUDFLARE-VLESS-WS-71MS` (url=301ms, status=HTTP 204)
29. `AKUN-035-GOV-VLESS-WS-63MS` (url=314ms, status=HTTP 204)
30. `AKUN-036-CLOUDFLARE-VLESS-WS-73MS` (url=283ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
