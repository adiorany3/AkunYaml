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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-496MS` (url=969ms, status=HTTP 204)
2. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-489MS` (url=1392ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-544MS` (url=1090ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-545MS` (url=1016ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-545MS` (url=1122ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-514MS` (url=1399ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-518MS` (url=940ms, status=HTTP 204)
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-494MS` (url=1271ms, status=HTTP 204)
9. `AKUN-009-PAGM-NET-VLESS-WS-548MS` (url=1276ms, status=HTTP 204)
10. `AKUN-010-GO-DADDY-COM-LLC-VLESS-WS-532MS` (url=1885ms, status=HTTP 204)
11. `AKUN-011-SPEEDTEST-VLESS-WS-582MS` (url=1773ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-477MS` (url=2542ms, status=HTTP 204)
13. `AKUN-014-ESA-VLESS-WS-564MS` (url=1462ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-479MS` (url=1649ms, status=HTTP 204)
15. `AKUN-016-SPEEDTEST-VLESS-WS-527MS` (url=1780ms, status=HTTP 204)
16. `AKUN-017-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-552MS` (url=2350ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-500MS` (url=876ms, status=HTTP 204)
18. `AKUN-019-CCWU-VLESS-WS-581MS` (url=890ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-567MS` (url=861ms, status=HTTP 204)
20. `AKUN-022-DEV-VLESS-WS-552MS` (url=1338ms, status=HTTP 204)
21. `AKUN-023-UNKNOWN-VLESS-WS-561MS` (url=2991ms, status=HTTP 204)
22. `AKUN-024-SPEEDTEST-VLESS-WS-574MS` (url=893ms, status=HTTP 204)
23. `AKUN-025-UNKNOWN-VLESS-WS-544MS` (url=997ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-549MS` (url=991ms, status=HTTP 204)
25. `AKUN-027-MEDIUM-VLESS-WS-532MS` (url=1764ms, status=HTTP 204)
26. `AKUN-028-TIME-VLESS-WS-527MS` (url=1042ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-544MS` (url=1048ms, status=HTTP 204)
28. `AKUN-030-DEV-VLESS-WS-614MS` (url=2305ms, status=HTTP 204)
29. `AKUN-031-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-575MS` (url=852ms, status=HTTP 204)
30. `AKUN-032-OVH-VLESS-WS-536MS` (url=1224ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
