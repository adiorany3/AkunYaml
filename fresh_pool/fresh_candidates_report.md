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
1. `AKUN-001-UNKNOWN-VLESS-WS-213MS` (url=966ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-205MS` (url=681ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-240MS` (url=648ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-235MS` (url=474ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-241MS` (url=662ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-242MS` (url=555ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-243MS` (url=1009ms, status=HTTP 204)
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-234MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-262MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-258MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-245MS` (url=1170ms, status=HTTP 204)
12. `AKUN-018-CLOUDFLARE-VLESS-WS-211MS` (url=1017ms, status=HTTP 204)
13. `AKUN-019-CLOUDFLARE-VLESS-WS-240MS` (url=1447ms, status=HTTP 204)
14. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-255MS` (url=702ms, status=HTTP 204)
15. `AKUN-023-CLOUDFLARE-VLESS-WS-306MS` (url=1506ms, status=HTTP 204)
16. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-284MS` (url=575ms, status=HTTP 204)
17. `AKUN-025-CLOUDFLARE-VLESS-WS-285MS` (url=632ms, status=HTTP 204)
18. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-220MS` (url=620ms, status=HTTP 204)
19. `AKUN-027-UNKNOWN-VLESS-WS-201MS` (url=1162ms, status=HTTP 204)
20. `AKUN-028-CLOUDFLARE-VLESS-WS-194MS` (url=1236ms, status=HTTP 204)
21. `AKUN-029-CLOUDFLARE-VLESS-WS-244MS` (url=749ms, status=HTTP 204)
22. `AKUN-030-CLOUDFLARE-VLESS-WS-230MS` (url=477ms, status=HTTP 204)
23. `AKUN-031-CLOUDFLARE-VLESS-WS-259MS` (url=776ms, status=HTTP 204)
24. `AKUN-032-CLOUDFLARE-VLESS-WS-235MS` (url=686ms, status=HTTP 204)
25. `AKUN-033-CLOUDFLARE-VLESS-WS-264MS` (url=689ms, status=HTTP 204)
26. `AKUN-034-UNKNOWN-VLESS-WS-252MS` (url=704ms, status=HTTP 204)
27. `AKUN-035-CLOUDFLARE-VLESS-WS-271MS` (url=1251ms, status=HTTP 204)
28. `AKUN-038-CLOUDFLARE-VLESS-WS-254MS` (url=559ms, status=HTTP 204)
29. `AKUN-039-CLOUDFLARE-VLESS-WS-286MS` (url=586ms, status=HTTP 204)
30. `AKUN-040-CLOUDFLARE-VLESS-WS-239MS` (url=1036ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
