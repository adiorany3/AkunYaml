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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-277MS` (url=723ms, status=HTTP 204)
2. `AKUN-002-EE-WELCOMEHOST-20190515-VLESS-WS-249MS` (url=724ms, status=HTTP 204)
3. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-265MS` (url=499ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-287MS` (url=652ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-285MS` (url=827ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-275MS` (url=739ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-296MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-268MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-282MS`
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-304MS`
11. `AKUN-013-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-243MS` (url=994ms, status=HTTP 204)
12. `AKUN-014-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-308MS` (url=767ms, status=HTTP 204)
13. `AKUN-015-NOTION-WEB-VLESS-WS-296MS` (url=909ms, status=HTTP 204)
14. `AKUN-016-SPEEDTEST-VLESS-WS-315MS` (url=777ms, status=HTTP 204)
15. `AKUN-017-UNKNOWN-VLESS-WS-292MS` (url=651ms, status=HTTP 204)
16. `AKUN-018-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-283MS` (url=629ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-293MS` (url=833ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-354MS` (url=907ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-294MS` (url=669ms, status=HTTP 204)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-294MS` (url=751ms, status=HTTP 204)
21. `AKUN-023-CLOUDFLARE-VLESS-WS-294MS` (url=757ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-285MS` (url=717ms, status=HTTP 204)
23. `AKUN-025-DEV-VLESS-WS-326MS` (url=611ms, status=HTTP 204)
24. `AKUN-026-UNKNOWN-VLESS-WS-308MS` (url=599ms, status=HTTP 204)
25. `AKUN-027-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-314MS` (url=831ms, status=HTTP 204)
26. `AKUN-028-DEV-VLESS-WS-327MS` (url=890ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-327MS` (url=908ms, status=HTTP 204)
28. `AKUN-031-CLOUDFLARE-VLESS-WS-307MS` (url=796ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-305MS` (url=711ms, status=HTTP 204)
30. `AKUN-033-UNKNOWN-VLESS-WS-308MS` (url=947ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
