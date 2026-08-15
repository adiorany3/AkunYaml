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
- Kandidat strict NekoBox-tested: 20
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-148MS` (url=360ms, nekobox=309ms, status=no)
2. `AKUN-001-CLOUDFLARE-VLESS-WS-168MS`
3. `AKUN-002-CLOUDFLARE-VLESS-WS-162MS`
4. `AKUN-003-CLOUDFLARE-VLESS-WS-192MS`
5. `AKUN-004-CLOUDFLARE-VLESS-WS-183MS`
6. `AKUN-005-ZVC-VLESS-WS-207MS`
7. `AKUN-006-CLOUDFLARE-VLESS-WS-210MS`
8. `AKUN-007-CLOUDFLARE-VLESS-WS-212MS`
9. `AKUN-008-CLOUDFLARE-VLESS-WS-205MS`
10. `AKUN-009-CLOUDFLARE-VLESS-WS-206MS`
11. `AKUN-010-CLOUDFLARE-VLESS-WS-197MS`
12. `AKUN-011-CLOUDFLARE-VLESS-WS-204MS`
13. `AKUN-012-CLOUDFLARE-VLESS-WS-224MS`
14. `AKUN-013-CLOUDFLARE-VLESS-WS-193MS`
15. `AKUN-014-NOTION-WEB-VLESS-WS-188MS`
16. `AKUN-015-NOTION-WEB-VLESS-WS-202MS`
17. `AKUN-016-CLOUDFLARE-VLESS-WS-178MS`
18. `AKUN-017-BIGCOMMERCE-VLESS-WS-203MS`
19. `AKUN-018-CLOUDFLARE-VLESS-WS-202MS`
20. `AKUN-019-CLOUDFLARE-VLESS-WS-172MS`
21. `AKUN-020-CLOUDFLARE-VLESS-WS-203MS`
22. `AKUN-023-CLOUDFLARE-VLESS-WS-187MS` (url=375ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-165MS` (url=358ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-185MS` (url=361ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-210MS` (url=359ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-225MS` (url=348ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-225MS` (url=386ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-228MS` (url=349ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-194MS` (url=345ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-196MS` (url=1378ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
