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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-004-UNKNOWN-VLESS-WS-140MS` (url=394ms, nekobox=300ms, status=no)
2. `AKUN-005-UNKNOWN-VLESS-WS-152MS` (url=436ms, status=HTTP 204)
3. `AKUN-009-UNKNOWN-VLESS-WS-116MS`
4. `AKUN-003-CLOUDFLARE-VLESS-WS-129MS`
5. `AKUN-008-CLOUDFLARE-VLESS-WS-119MS` (url=471ms, status=HTTP 204)
6. `AKUN-002-CLOUDFLARE-VLESS-WS-134MS`
7. `AKUN-010-NET-147-90-26-0-24-VLESS-WS-138MS` (url=422ms, status=HTTP 204)
8. `AKUN-004-CLOUDFLARE-VLESS-WS-167MS`
9. `AKUN-012-CLOUDFLARE-VLESS-WS-161MS` (url=475ms, status=HTTP 204)
10. `AKUN-013-CLOUDFLARE-VLESS-WS-162MS` (url=426ms, status=HTTP 204)
11. `AKUN-014-DEV-VLESS-WS-142MS` (url=437ms, status=HTTP 204)
12. `AKUN-006-CLOUDFLARE-VLESS-WS-144MS`
13. `AKUN-016-CLOUDFLARE-VLESS-WS-142MS` (url=453ms, status=HTTP 204)
14. `AKUN-017-RS-RAPIDSEEDBOX-20190717-VLESS-WS-119MS` (url=450ms, status=HTTP 204)
15. `AKUN-001-MEDIUM-VLESS-WS-150MS`
16. `AKUN-007-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-165MS`
17. `AKUN-020-CLOUDFLARE-VLESS-WS-197MS` (url=418ms, status=HTTP 204)
18. `AKUN-021-CLOUDFLARE-VLESS-WS-150MS` (url=446ms, status=HTTP 204)
19. `AKUN-022-CLOUDFLARE-VLESS-WS-163MS` (url=440ms, status=HTTP 204)
20. `AKUN-023-BIGCOMMERCE-VLESS-WS-123MS` (url=453ms, status=HTTP 204)
21. `AKUN-024-UNKNOWN-VLESS-WS-150MS` (url=433ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-136MS` (url=487ms, status=HTTP 204)
23. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-239MS` (url=436ms, status=HTTP 204)
24. `AKUN-005-UNKNOWN-VLESS-WS-185MS`
25. `AKUN-008-ZUOAI-VLESS-WS-277MS`
26. `AKUN-030-UNKNOWN-VLESS-WS-123MS` (url=438ms, status=HTTP 204)
27. `AKUN-031-CLOUDFLARE-VLESS-WS-190MS` (url=426ms, status=HTTP 204)
28. `AKUN-032-CLOUDFLARE-VLESS-WS-133MS` (url=417ms, status=HTTP 204)
29. `AKUN-033-CLOUDFLARE-VLESS-WS-200MS` (url=426ms, status=HTTP 204)
30. `AKUN-034-CLOUDFLARE-VLESS-WS-191MS` (url=2507ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
