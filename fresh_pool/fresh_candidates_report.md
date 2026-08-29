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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-255MS` (url=1355ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-249MS` (url=713ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-239MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-264MS`
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-294MS`
6. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-263MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-273MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-284MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-300MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-283MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-254MS` (url=939ms, status=HTTP 204)
12. `AKUN-013-UNKNOWN-VLESS-WS-263MS` (url=581ms, status=HTTP 204)
13. `AKUN-014-NOTION-WEB-VLESS-WS-295MS` (url=669ms, status=HTTP 204)
14. `AKUN-015-008500-VLESS-WS-284MS` (url=749ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-306MS` (url=829ms, status=HTTP 204)
16. `AKUN-018-UNKNOWN-VLESS-WS-301MS` (url=1130ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-257MS` (url=610ms, status=HTTP 204)
18. `AKUN-020-UNKNOWN-VLESS-WS-295MS` (url=629ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-300MS` (url=621ms, status=HTTP 204)
20. `AKUN-022-SPEEDTEST-VLESS-WS-291MS` (url=600ms, status=HTTP 204)
21. `AKUN-023-CLOUDFLARE-VLESS-WS-293MS` (url=747ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-304MS` (url=3740ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-306MS` (url=692ms, status=HTTP 204)
24. `AKUN-027-UNKNOWN-VLESS-WS-312MS` (url=570ms, status=HTTP 204)
25. `AKUN-028-CLOUDFLARE-VLESS-WS-293MS` (url=729ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-275MS` (url=730ms, status=HTTP 204)
27. `AKUN-030-CLOUDFLARE-VLESS-WS-280MS` (url=731ms, status=HTTP 204)
28. `AKUN-031-RS-RAPIDSEEDBOX-20190717-VLESS-WS-275MS` (url=787ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-300MS` (url=510ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-356MS` (url=4020ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
