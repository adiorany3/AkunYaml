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
1. `AKUN-001-UNKNOWN-VLESS-WS-245MS`
2. `AKUN-002-UNKNOWN-VLESS-WS-248MS` (url=457ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-258MS` (url=986ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-266MS` (url=540ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-253MS` (url=584ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-261MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-256MS`
8. `AKUN-008-LEVIKOGJGFDD-VLESS-WS-311MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-266MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-268MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-253MS` (url=513ms, status=HTTP 204)
12. `AKUN-017-UNKNOWN-VLESS-WS-242MS` (url=836ms, status=HTTP 204)
13. `AKUN-018-CLOUDFLARE-VLESS-WS-244MS` (url=625ms, status=HTTP 204)
14. `AKUN-019-UNKNOWN-VLESS-WS-249MS` (url=934ms, status=HTTP 204)
15. `AKUN-020-CLOUDFLARE-VLESS-WS-245MS` (url=753ms, status=HTTP 204)
16. `AKUN-021-CLOUDFLARE-VLESS-WS-257MS` (url=1227ms, status=HTTP 204)
17. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-235MS` (url=1127ms, status=HTTP 204)
18. `AKUN-023-UNKNOWN-VLESS-WS-256MS` (url=542ms, status=HTTP 204)
19. `AKUN-027-UNKNOWN-VLESS-WS-321MS` (url=524ms, status=HTTP 204)
20. `AKUN-028-CLOUDFLARE-VLESS-WS-261MS` (url=678ms, status=HTTP 204)
21. `AKUN-029-CLOUDFLARE-VLESS-WS-264MS` (url=1718ms, status=HTTP 204)
22. `AKUN-030-CLOUDFLARE-VLESS-WS-345MS` (url=774ms, status=HTTP 204)
23. `AKUN-031-UNKNOWN-VLESS-WS-327MS` (url=634ms, status=HTTP 204)
24. `AKUN-032-CLOUDFLARE-VLESS-WS-249MS` (url=1206ms, status=HTTP 204)
25. `AKUN-033-UNKNOWN-VLESS-WS-830MS` (url=4672ms, status=HTTP 204)
26. `AKUN-035-CLOUDFLARE-VLESS-WS-296MS` (url=1579ms, status=HTTP 204)
27. `AKUN-036-CLOUDFLARE-VLESS-WS-284MS` (url=1065ms, status=HTTP 204)
28. `AKUN-037-TANG-NET-VLESS-WS-895MS` (url=1585ms, status=HTTP 204)
29. `AKUN-038-UNKNOWN-VLESS-WS-245MS` (url=785ms, status=HTTP 204)
30. `AKUN-039-UNKNOWN-VLESS-WS-403MS` (url=673ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
