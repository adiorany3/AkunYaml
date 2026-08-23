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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-215MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-215MS` (url=541ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-251MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-269MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-283MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-274MS`
7. `AKUN-007-DEV-VLESS-WS-262MS`
8. `AKUN-008-FMN5-RENTED-NET2-VLESS-WS-289MS`
9. `AKUN-009-DEV-VLESS-WS-232MS`
10. `AKUN-010-CONFLU-VLESS-WS-293MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-263MS` (url=484ms, status=HTTP 204)
12. `AKUN-015-UNKNOWN-VLESS-WS-275MS` (url=590ms, status=HTTP 204)
13. `AKUN-016-CLOUDFLARE-VLESS-WS-204MS` (url=559ms, status=HTTP 204)
14. `AKUN-017-UNKNOWN-VLESS-WS-274MS` (url=529ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-293MS` (url=518ms, status=HTTP 204)
16. `AKUN-019-UNKNOWN-VLESS-WS-266MS` (url=602ms, status=HTTP 204)
17. `AKUN-020-UNKNOWN-VLESS-WS-255MS` (url=489ms, status=HTTP 204)
18. `AKUN-021-TIME-VLESS-WS-280MS` (url=747ms, status=HTTP 204)
19. `AKUN-022-UNKNOWN-VLESS-WS-230MS` (url=542ms, status=HTTP 204)
20. `AKUN-023-UNKNOWN-VLESS-WS-305MS` (url=610ms, status=HTTP 204)
21. `AKUN-024-CLOUDFLARE-VLESS-WS-252MS` (url=1026ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-281MS` (url=531ms, status=HTTP 204)
23. `AKUN-027-SPEEDTEST-VLESS-WS-286MS` (url=612ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-202MS` (url=489ms, status=HTTP 204)
25. `AKUN-031-LEVIKOGJGFDD-VLESS-WS-228MS` (url=569ms, status=HTTP 204)
26. `AKUN-032-CLOUDFLARE-VLESS-WS-240MS` (url=500ms, status=HTTP 204)
27. `AKUN-033-SPEEDTEST-VLESS-WS-248MS` (url=567ms, status=HTTP 204)
28. `AKUN-036-CLOUDFLARE-VLESS-WS-288MS` (url=569ms, status=HTTP 204)
29. `AKUN-038-CLOUDFLARE-VLESS-WS-250MS` (url=665ms, status=HTTP 204)
30. `AKUN-039-CLOUDFLARE-VLESS-WS-284MS` (url=809ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
