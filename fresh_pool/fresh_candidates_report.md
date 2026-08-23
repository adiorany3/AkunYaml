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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-252MS` (url=705ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-247MS` (url=1022ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-268MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-260MS`
5. `AKUN-005-NOTION-WEB-VLESS-WS-261MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-320MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-343MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-273MS`
9. `AKUN-009-CCWU-VLESS-WS-241MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-281MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-257MS` (url=1035ms, status=HTTP 204)
12. `AKUN-016-CLOUDFLARE-VLESS-WS-252MS` (url=739ms, status=HTTP 204)
13. `AKUN-017-NOTION-WEB-VLESS-WS-297MS` (url=639ms, status=HTTP 204)
14. `AKUN-018-UNKNOWN-VLESS-WS-279MS` (url=820ms, status=HTTP 204)
15. `AKUN-019-UNKNOWN-VLESS-WS-279MS` (url=1739ms, status=HTTP 204)
16. `AKUN-020-UNKNOWN-VLESS-WS-284MS` (url=640ms, status=HTTP 204)
17. `AKUN-022-CLOUDFLARE-VLESS-WS-253MS` (url=542ms, status=HTTP 204)
18. `AKUN-024-SPEEDTEST-VLESS-WS-301MS` (url=461ms, status=HTTP 204)
19. `AKUN-025-CLOUDFLARE-VLESS-WS-225MS` (url=487ms, status=HTTP 204)
20. `AKUN-029-CLOUDFLARE-VLESS-WS-264MS` (url=652ms, status=HTTP 204)
21. `AKUN-030-CLOUDFLARE-VLESS-WS-295MS` (url=610ms, status=HTTP 204)
22. `AKUN-031-CLOUDFLARE-VLESS-WS-268MS` (url=768ms, status=HTTP 204)
23. `AKUN-032-CHATGPT-VLESS-WS-316MS` (url=791ms, status=HTTP 204)
24. `AKUN-033-CLOUDFLARE-VLESS-WS-285MS` (url=529ms, status=HTTP 204)
25. `AKUN-034-CLOUDFLARE-VLESS-WS-337MS` (url=2043ms, status=HTTP 204)
26. `AKUN-035-CLOUDFLARE-VLESS-WS-267MS` (url=1026ms, status=HTTP 204)
27. `AKUN-036-CLOUDFLARE-VLESS-WS-291MS` (url=569ms, status=HTTP 204)
28. `AKUN-037-CLOUDFLARE-VLESS-WS-326MS` (url=709ms, status=HTTP 204)
29. `AKUN-038-UNKNOWN-VLESS-WS-272MS` (url=558ms, status=HTTP 204)
30. `AKUN-039-CLOUDFLARE-VLESS-WS-235MS` (url=511ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
