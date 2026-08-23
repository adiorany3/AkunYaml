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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-236MS` (url=752ms, status=HTTP 204)
2. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-257MS` (url=527ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-275MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-276MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-291MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-275MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-261MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-292MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-247MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-218MS`
11. `AKUN-019-CLOUDFLARE-VLESS-WS-277MS` (url=1701ms, status=HTTP 204)
12. `AKUN-020-CLOUDFLARE-VLESS-WS-272MS` (url=1840ms, status=HTTP 204)
13. `AKUN-021-CHATGPT-VLESS-WS-274MS` (url=535ms, status=HTTP 204)
14. `AKUN-022-CLOUDFLARE-VLESS-WS-278MS` (url=431ms, status=HTTP 204)
15. `AKUN-023-CLOUDFLARE-VLESS-WS-323MS` (url=1143ms, status=HTTP 204)
16. `AKUN-024-CLOUDFLARE-VLESS-WS-266MS` (url=771ms, status=HTTP 204)
17. `AKUN-025-UNKNOWN-VLESS-WS-297MS` (url=1028ms, status=HTTP 204)
18. `AKUN-026-CLOUDFLARE-VLESS-WS-280MS` (url=552ms, status=HTTP 204)
19. `AKUN-028-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-454MS` (url=1328ms, status=HTTP 204)
20. `AKUN-032-CLOUDFLARE-VLESS-WS-399MS` (url=522ms, status=HTTP 204)
21. `AKUN-033-CLOUDFLARE-VLESS-WS-286MS` (url=549ms, status=HTTP 204)
22. `AKUN-034-NL-TELEMAGIC-20111109-VLESS-WS-896MS` (url=1642ms, status=HTTP 204)
23. `AKUN-038-CLOUDFLARE-VLESS-WS-276MS` (url=5183ms, status=HTTP 204)
24. `AKUN-041-LOCALIP-VLESS-WS-1049MS` (url=1832ms, status=HTTP 204)
25. `AKUN-043-EU-VLESS-WS-279MS` (url=791ms, status=HTTP 204)
26. `AKUN-044-CLOUDFLARE-VLESS-WS-985MS` (url=1562ms, status=HTTP 204)
27. `AKUN-045-CLOUDFLARE-VLESS-WS-273MS` (url=938ms, status=HTTP 204)
28. `AKUN-048-CLOUDFLARE-VLESS-WS-927MS` (url=1517ms, status=HTTP 204)
29. `AKUN-049-AS199785-DE-IPV4-VLESS-WS-1079MS` (url=3669ms, status=HTTP 204)
30. `AKUN-050-UNKNOWN-VLESS-WS-815MS` (url=1911ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
