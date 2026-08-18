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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-250MS` (url=941ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-251MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-254MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-262MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-275MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-240MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-233MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-302MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-295MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-260MS`
11. `AKUN-017-CLOUDFLARE-VLESS-WS-257MS` (url=559ms, status=HTTP 204)
12. `AKUN-018-CLOUDFLARE-VLESS-WS-240MS` (url=589ms, status=HTTP 204)
13. `AKUN-020-CLOUDFLARE-VLESS-WS-235MS` (url=4993ms, status=HTTP 204)
14. `AKUN-021-CLOUDFLARE-VLESS-WS-264MS` (url=750ms, status=HTTP 204)
15. `AKUN-022-NOTION-WEB-VLESS-WS-264MS` (url=4085ms, status=HTTP 204)
16. `AKUN-023-CLOUDFLARE-VLESS-WS-223MS` (url=882ms, status=HTTP 204)
17. `AKUN-025-CLOUDFLARE-VLESS-WS-249MS` (url=514ms, status=HTTP 204)
18. `AKUN-026-CLOUDFLARE-VLESS-WS-264MS` (url=697ms, status=HTTP 204)
19. `AKUN-027-CLOUDFLARE-VLESS-WS-253MS` (url=650ms, status=HTTP 204)
20. `AKUN-028-CLOUDFLARE-VLESS-WS-261MS` (url=601ms, status=HTTP 204)
21. `AKUN-029-CLOUDFLARE-VLESS-WS-243MS` (url=1495ms, status=HTTP 204)
22. `AKUN-030-CLOUDFLARE-VLESS-WS-258MS` (url=673ms, status=HTTP 204)
23. `AKUN-032-CLOUDFLARE-VLESS-WS-293MS` (url=473ms, status=HTTP 204)
24. `AKUN-034-CLOUDFLARE-VLESS-WS-229MS` (url=570ms, status=HTTP 204)
25. `AKUN-038-CLOUDFLARE-VLESS-WS-327MS` (url=585ms, status=HTTP 204)
26. `AKUN-039-CLOUDFLARE-VLESS-WS-246MS` (url=586ms, status=HTTP 204)
27. `AKUN-040-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-260MS` (url=714ms, status=HTTP 204)
28. `AKUN-041-CLOUDFLARE-VLESS-WS-297MS` (url=4248ms, status=HTTP 204)
29. `AKUN-043-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-289MS` (url=597ms, status=HTTP 204)
30. `AKUN-049-CLOUDFLARE-VLESS-WS-950MS` (url=2257ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
