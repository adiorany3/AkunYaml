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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-68MS` (url=315ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-65MS` (url=314ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-68MS` (url=265ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-65MS` (url=300ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-65MS` (url=313ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-65MS` (url=275ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-66MS` (url=330ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-72MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-72MS` (url=277ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-64MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-63MS` (url=280ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-65MS` (url=279ms, status=HTTP 204)
13. `AKUN-014-UNKNOWN-VLESS-WS-69MS` (url=958ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-70MS` (url=291ms, status=HTTP 204)
15. `AKUN-016-DEV-VLESS-WS-70MS` (url=3257ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-67MS` (url=308ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-71MS` (url=290ms, status=HTTP 204)
18. `AKUN-020-CHATGPT-VLESS-WS-69MS` (url=313ms, status=HTTP 204)
19. `AKUN-021-DEV-VLESS-WS-68MS` (url=380ms, status=HTTP 204)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-72MS` (url=742ms, status=HTTP 204)
21. `AKUN-023-CLOUDFLARE-VLESS-WS-77MS` (url=313ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-71MS` (url=989ms, status=HTTP 204)
23. `AKUN-026-RS-RAPIDSEEDBOX-20190717-VLESS-WS-71MS` (url=278ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-71MS` (url=861ms, status=HTTP 204)
25. `AKUN-028-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-69MS` (url=315ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-67MS` (url=333ms, status=HTTP 204)
27. `AKUN-030-BIGCOMMERCE-VLESS-WS-72MS` (url=286ms, status=HTTP 204)
28. `AKUN-031-UNKNOWN-VLESS-WS-81MS` (url=314ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-66MS` (url=284ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-82MS` (url=323ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
