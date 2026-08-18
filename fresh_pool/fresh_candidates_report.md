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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-208MS` (url=4521ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-186MS` (url=509ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-245MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-257MS`
5. `AKUN-005-UNKNOWN-VLESS-WS-258MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-258MS` (url=733ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-204MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-275MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-401MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-267MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-285MS` (url=719ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-204MS` (url=525ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-262MS` (url=683ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-236MS` (url=723ms, status=HTTP 204)
15. `AKUN-017-NOTION-WEB-VLESS-WS-245MS` (url=742ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-242MS` (url=730ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-212MS` (url=463ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-264MS` (url=869ms, status=HTTP 204)
19. `AKUN-022-AMAZON-VLESS-WS-282MS` (url=593ms, status=HTTP 204)
20. `AKUN-023-CLOUDFLARE-VLESS-WS-249MS` (url=422ms, status=HTTP 204)
21. `AKUN-024-NOTION-WEB-VLESS-WS-259MS` (url=2493ms, status=HTTP 204)
22. `AKUN-025-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-257MS` (url=789ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-328MS` (url=1435ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-261MS` (url=1540ms, status=HTTP 204)
25. `AKUN-029-CLOUDFLARE-VLESS-WS-250MS` (url=651ms, status=HTTP 204)
26. `AKUN-030-CLOUDFLARE-VLESS-WS-260MS` (url=2536ms, status=HTTP 204)
27. `AKUN-031-CLOUDFLARE-VLESS-WS-254MS` (url=715ms, status=HTTP 204)
28. `AKUN-032-UNKNOWN-VLESS-WS-309MS` (url=668ms, status=HTTP 204)
29. `AKUN-034-CLOUDFLARE-VLESS-WS-254MS` (url=1619ms, status=HTTP 204)
30. `AKUN-035-CLOUDFLARE-VLESS-WS-257MS` (url=422ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
