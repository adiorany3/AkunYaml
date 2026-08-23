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
1. `AKUN-001-TIME-VLESS-WS-257MS` (url=665ms, status=HTTP 204)
2. `AKUN-002-DEV-VLESS-WS-248MS` (url=558ms, status=HTTP 204)
3. `AKUN-003-SPEEDTEST-VLESS-WS-259MS` (url=439ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-253MS` (url=1024ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-269MS` (url=520ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-263MS` (url=499ms, status=HTTP 204)
7. `AKUN-007-EU-VLESS-WS-266MS` (url=4616ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-263MS` (url=509ms, status=HTTP 204)
9. `AKUN-009-UNKNOWN-VLESS-WS-249MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-260MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-284MS` (url=602ms, status=HTTP 204)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-229MS` (url=550ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-209MS` (url=579ms, status=HTTP 204)
14. `AKUN-016-UNKNOWN-VLESS-WS-274MS` (url=569ms, status=HTTP 204)
15. `AKUN-017-UNKNOWN-VLESS-WS-279MS` (url=468ms, status=HTTP 204)
16. `AKUN-018-DE5-VLESS-WS-267MS` (url=562ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-251MS` (url=577ms, status=HTTP 204)
18. `AKUN-020-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-278MS` (url=492ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-249MS` (url=950ms, status=HTTP 204)
20. `AKUN-023-UNKNOWN-VLESS-WS-253MS` (url=905ms, status=HTTP 204)
21. `AKUN-024-CLOUDFLARE-VLESS-WS-270MS` (url=506ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-284MS` (url=512ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-284MS` (url=561ms, status=HTTP 204)
24. `AKUN-030-UNKNOWN-VLESS-WS-261MS` (url=524ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-246MS` (url=577ms, status=HTTP 204)
26. `AKUN-033-CLOUDFLARE-VLESS-WS-221MS` (url=494ms, status=HTTP 204)
27. `AKUN-034-UNKNOWN-VLESS-WS-270MS` (url=517ms, status=HTTP 204)
28. `AKUN-036-DEV-VLESS-WS-245MS` (url=612ms, status=HTTP 204)
29. `AKUN-038-LEVIKOGJGFDD-VLESS-WS-259MS` (url=559ms, status=HTTP 204)
30. `AKUN-039-EU-VLESS-WS-271MS` (url=780ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
