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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-160MS` (url=419ms, nekobox=391ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-166MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-149MS`
4. `AKUN-005-CLOUDFLARE-VLESS-WS-180MS` (url=373ms, nekobox=273ms, status=no)
5. `AKUN-004-CLOUDFLARE-VLESS-WS-175MS`
6. `AKUN-005-CLOUDFLARE-VLESS-WS-178MS`
7. `AKUN-006-CLOUDFLARE-VLESS-WS-137MS`
8. `AKUN-007-CLOUDFLARE-VLESS-WS-124MS`
9. `AKUN-008-CLOUDFLARE-VLESS-WS-249MS`
10. `AKUN-009-CLOUDFLARE-VLESS-WS-183MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-183MS` (url=353ms, nekobox=283ms, status=no)
12. `AKUN-010-CLOUDFLARE-VLESS-WS-175MS`
13. `AKUN-011-CLOUD-NETWORK-HK-VLESS-WS-256MS`
14. `AKUN-012-CLOUDFLARE-VLESS-WS-248MS`
15. `AKUN-013-CLOUDFLARE-VLESS-WS-233MS`
16. `AKUN-014-CLOUDFLARE-VLESS-WS-157MS`
17. `AKUN-015-CLOUDFLARE-VLESS-WS-151MS`
18. `AKUN-016-CLOUDFLARE-VLESS-WS-148MS`
19. `AKUN-017-CLOUDFLARE-VLESS-WS-211MS`
20. `AKUN-018-CLOUDFLARE-VLESS-WS-157MS`
21. `AKUN-019-MINEDU-BLK-NZ-VLESS-WS-202MS`
22. `AKUN-020-CLOUDFLARE-VLESS-WS-211MS`
23. `AKUN-025-CLOUDFLARE-VLESS-WS-205MS` (url=371ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-204MS` (url=355ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-216MS` (url=388ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-218MS` (url=389ms, status=HTTP 204)
27. `AKUN-029-UNKNOWN-VLESS-WS-208MS` (url=376ms, status=HTTP 204)
28. `AKUN-030-UNKNOWN-VLESS-WS-196MS` (url=349ms, status=HTTP 204)
29. `AKUN-031-DEV-VLESS-WS-151MS` (url=359ms, status=HTTP 204)
30. `AKUN-032-UNKNOWN-VLESS-WS-283MS` (url=369ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
