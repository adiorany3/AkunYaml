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
- Kandidat strict NekoBox-tested: 6
- Proxy di openclash_fresh_pool.yaml: 33

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
1. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-378MS` (url=4502ms, status=HTTP 204)
2. `AKUN-003-UNKNOWN-VLESS-WS-157MS` (url=2486ms, status=HTTP 204)
3. `AKUN-004-UNKNOWN-VLESS-WS-440MS` (url=2380ms, status=HTTP 204)
4. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-174MS`
5. `AKUN-006-TENCENT-VLESS-WS-154MS` (url=1701ms, nekobox=6176ms, status=no)
6. `AKUN-007-CLOUDFLARE-VLESS-WS-191MS` (url=4438ms, status=HTTP 204)
7. `AKUN-008-CLOUDFLARE-VLESS-WS-136MS` (url=2439ms, status=HTTP 204)
8. `AKUN-002-CLOUDFLARE-VLESS-WS-457MS`
9. `AKUN-011-CLOUDFLARE-VLESS-WS-137MS` (url=495ms, nekobox=6332ms, status=no)
10. `AKUN-014-CLOUDFLARE-VLESS-WS-133MS` (url=917ms, nekobox=2120ms, status=no)
11. `AKUN-019-CLOUDFLARE-VLESS-WS-371MS` (url=2007ms, status=HTTP 204)
12. `AKUN-022-NET-147-90-26-0-24-VLESS-WS-458MS` (url=3070ms, status=HTTP 204)
13. `AKUN-005-TENCENT-VLESS-WS-664MS`
14. `AKUN-024-CLOUDFLARE-VLESS-WS-649MS` (url=3455ms, status=HTTP 204)
15. `AKUN-004-UNKNOWN-VLESS-WS-777MS`
16. `AKUN-027-CLOUDFLARE-VLESS-WS-421MS` (url=4131ms, status=HTTP 204)
17. `AKUN-029-CLOUDFLARE-VLESS-WS-915MS` (url=2868ms, status=HTTP 204)
18. `AKUN-031-CLOUDFLARE-VLESS-WS-174MS` (url=4623ms, status=HTTP 204)
19. `AKUN-001-UNKNOWN-VLESS-WS-173MS`
20. `AKUN-033-CLOUDFLARE-VLESS-WS-647MS` (url=4485ms, status=HTTP 204)
21. `AKUN-034-NASEEJ-VLESS-WS-236MS` (url=4164ms, status=HTTP 204)
22. `AKUN-035-UNKNOWN-VLESS-WS-1126MS` (url=4520ms, status=HTTP 204)
23. `AKUN-036-CLOUDFLARE-VLESS-WS-411MS` (url=739ms, nekobox=6175ms, status=no)
24. `AKUN-037-CLOUDFLARE-VLESS-WS-753MS` (url=1864ms, status=HTTP 204)
25. `AKUN-039-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-423MS` (url=2425ms, status=HTTP 204)
26. `AKUN-042-CLOUDFLARE-VLESS-WS-890MS` (url=3189ms, status=HTTP 204)
27. `AKUN-043-CLOUDFLARE-VLESS-WS-501MS` (url=2868ms, status=HTTP 204)
28. `AKUN-045-CLOUDFLARE-VLESS-WS-145MS` (url=1782ms, status=HTTP 204)
29. `AKUN-046-UNKNOWN-VLESS-WS-995MS` (url=2672ms, status=HTTP 204)
30. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-185MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
