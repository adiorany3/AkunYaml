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
- Kandidat strict NekoBox-tested: 20
- Proxy di openclash_fresh_pool.yaml: 30

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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-232MS` (url=389ms, nekobox=3967ms, status=yes)
2. `AKUN-002-AIMALL-VLESS-WS-250MS` (url=381ms, nekobox=428ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-257MS` (url=3685ms, nekobox=4004ms, status=yes)
4. `AKUN-004-UNKNOWN-VLESS-WS-237MS` (url=326ms, nekobox=423ms, status=yes)
5. `AKUN-005-UNKNOWN-VLESS-WS-271MS` (url=1380ms, nekobox=401ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-279MS` (url=1391ms, nekobox=419ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-298MS` (url=355ms, nekobox=377ms, status=yes)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-272MS` (url=456ms, nekobox=495ms, status=yes)
9. `AKUN-009-UNKNOWN-VLESS-WS-265MS` (url=344ms, nekobox=415ms, status=yes)
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-295MS` (url=356ms, nekobox=481ms, status=yes)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-294MS` (url=366ms, nekobox=384ms, status=yes)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-276MS` (url=333ms, nekobox=270ms, status=no)
13. `AKUN-013-SPEEDTEST-VLESS-WS-325MS` (url=420ms, nekobox=343ms, status=no)
14. `AKUN-014-SPEEDTEST-VLESS-WS-307MS` (url=1335ms, nekobox=250ms, status=no)
15. `AKUN-012-SPEEDTEST-VLESS-WS-223MS`
16. `AKUN-013-UNKNOWN-VLESS-WS-272MS`
17. `AKUN-014-UNKNOWN-VLESS-WS-284MS`
18. `AKUN-018-CLOUDFLARE-VLESS-WS-270MS` (url=336ms, nekobox=1266ms, status=no)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-285MS` (url=367ms, nekobox=269ms, status=no)
20. `AKUN-020-UNKNOWN-VLESS-WS-311MS` (url=391ms, nekobox=253ms, status=no)
21. `AKUN-021-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-279MS` (url=346ms, nekobox=263ms, status=no)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-275MS` (url=337ms, nekobox=266ms, status=no)
23. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-297MS`
24. `AKUN-016-CLOUDFLARE-VLESS-WS-281MS`
25. `AKUN-017-CLOUDFLARE-VLESS-WS-256MS`
26. `AKUN-018-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-261MS`
27. `AKUN-019-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-783MS`
28. `AKUN-020-CLOUDFLARE-VLESS-WS-264MS`
29. `AKUN-029-CLOUDFLARE-VLESS-WS-256MS` (url=903ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-251MS` (url=370ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
