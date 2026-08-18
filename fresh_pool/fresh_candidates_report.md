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
1. `AKUN-001-UNKNOWN-VLESS-WS-246MS` (url=510ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-242MS` (url=655ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-251MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-242MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-264MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-216MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-244MS`
8. `AKUN-008-EU-VLESS-WS-267MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-262MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-251MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-264MS` (url=635ms, status=HTTP 204)
12. `AKUN-016-CLOUDFLARE-VLESS-WS-256MS` (url=567ms, status=HTTP 204)
13. `AKUN-017-UNKNOWN-VLESS-WS-244MS` (url=1918ms, status=HTTP 204)
14. `AKUN-018-UNKNOWN-VLESS-WS-266MS` (url=537ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-252MS` (url=582ms, status=HTTP 204)
16. `AKUN-024-CLOUDFLARE-VLESS-WS-222MS` (url=531ms, status=HTTP 204)
17. `AKUN-025-UNKNOWN-VLESS-WS-244MS` (url=783ms, status=HTTP 204)
18. `AKUN-026-UNKNOWN-VLESS-WS-260MS` (url=533ms, status=HTTP 204)
19. `AKUN-028-UNKNOWN-VLESS-WS-262MS` (url=510ms, status=HTTP 204)
20. `AKUN-032-CLOUDFLARE-VLESS-WS-256MS` (url=546ms, status=HTTP 204)
21. `AKUN-033-CLOUDFLARE-VLESS-WS-243MS` (url=591ms, status=HTTP 204)
22. `AKUN-035-UNKNOWN-VLESS-WS-278MS` (url=731ms, status=HTTP 204)
23. `AKUN-039-CLOUDFLARE-VLESS-WS-288MS` (url=3989ms, status=HTTP 204)
24. `AKUN-041-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-808MS` (url=1788ms, status=HTTP 204)
25. `AKUN-044-CLOUDFLARE-VLESS-WS-315MS` (url=731ms, status=HTTP 204)
26. `AKUN-047-LOCALIP-VLESS-WS-994MS` (url=1648ms, status=HTTP 204)
27. `AKUN-051-CLOUDFLARE-VLESS-WS-447MS` (url=1479ms, status=HTTP 204)
28. `AKUN-052-UNKNOWN-VLESS-WS-260MS` (url=624ms, status=HTTP 204)
29. `AKUN-053-UNKNOWN-VLESS-WS-941MS` (url=1564ms, status=HTTP 204)
30. `AKUN-054-UNKNOWN-VLESS-WS-937MS` (url=1492ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
