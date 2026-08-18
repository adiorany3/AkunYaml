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
1. `AKUN-001-UNKNOWN-VLESS-WS-239MS` (url=455ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-239MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-244MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-245MS`
5. `AKUN-005-NOTION-WEB-VLESS-WS-236MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-228MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-237MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-246MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-265MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-218MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-234MS` (url=520ms, status=HTTP 204)
12. `AKUN-017-NOTION-WEB-VLESS-WS-246MS` (url=552ms, status=HTTP 204)
13. `AKUN-018-CLOUDFLARE-VLESS-WS-249MS` (url=609ms, status=HTTP 204)
14. `AKUN-024-CLOUDFLARE-VLESS-WS-230MS` (url=574ms, status=HTTP 204)
15. `AKUN-025-CLOUDFLARE-VLESS-WS-226MS` (url=506ms, status=HTTP 204)
16. `AKUN-026-CLOUDFLARE-VLESS-WS-219MS` (url=1403ms, status=HTTP 204)
17. `AKUN-029-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-255MS` (url=493ms, status=HTTP 204)
18. `AKUN-030-CLOUDFLARE-VLESS-WS-256MS` (url=568ms, status=HTTP 204)
19. `AKUN-031-CLOUDFLARE-VLESS-WS-225MS` (url=1328ms, status=HTTP 204)
20. `AKUN-032-CLOUDFLARE-VLESS-WS-284MS` (url=1907ms, status=HTTP 204)
21. `AKUN-033-CLOUDFLARE-VLESS-WS-243MS` (url=531ms, status=HTTP 204)
22. `AKUN-035-CLOUDFLARE-VLESS-WS-256MS` (url=1004ms, status=HTTP 204)
23. `AKUN-036-CLOUDFLARE-VLESS-WS-266MS` (url=533ms, status=HTTP 204)
24. `AKUN-037-CLOUDFLARE-VLESS-WS-704MS` (url=1940ms, status=HTTP 204)
25. `AKUN-038-CLOUDFLARE-VLESS-WS-215MS` (url=762ms, status=HTTP 204)
26. `AKUN-040-CLOUDFLARE-VLESS-WS-725MS` (url=1128ms, status=HTTP 204)
27. `AKUN-041-CLOUDFLARE-VLESS-WS-208MS` (url=645ms, status=HTTP 204)
28. `AKUN-042-CLOUDFLARE-VLESS-WS-239MS` (url=728ms, status=HTTP 204)
29. `AKUN-044-UNKNOWN-VLESS-WS-782MS` (url=1658ms, status=HTTP 204)
30. `AKUN-045-NL-TELEMAGIC-20111109-VLESS-WS-902MS` (url=1652ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
