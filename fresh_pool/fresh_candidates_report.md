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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-008-UNKNOWN-VLESS-WS-100MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-93MS` (url=614ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-94MS` (url=587ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-93MS` (url=619ms, status=HTTP 204)
5. `AKUN-003-CLOUDFLARE-VLESS-WS-91MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-99MS` (url=1594ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-97MS` (url=972ms, status=HTTP 204)
8. `AKUN-004-CLOUDFLARE-VLESS-WS-98MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-98MS` (url=614ms, status=HTTP 204)
10. `AKUN-009-CLOUDFLARE-VLESS-WS-99MS`
11. `AKUN-011-BIGCOMMERCE-VLESS-WS-100MS` (url=613ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-103MS` (url=632ms, status=HTTP 204)
13. `AKUN-006-CLOUDFLARE-VLESS-WS-102MS`
14. `AKUN-015-MEDIUM-VLESS-WS-103MS` (url=600ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-102MS` (url=615ms, status=HTTP 204)
16. `AKUN-017-UNKNOWN-VLESS-WS-94MS` (url=634ms, status=HTTP 204)
17. `AKUN-018-EE-WELCOMEHOST-20190515-VLESS-WS-95MS` (url=1625ms, status=HTTP 204)
18. `AKUN-020-GOV-VLESS-WS-94MS` (url=618ms, status=HTTP 204)
19. `AKUN-021-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-109MS` (url=1647ms, status=HTTP 204)
20. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-99MS` (url=1627ms, status=HTTP 204)
21. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-105MS`
22. `AKUN-001-CLOUDFLARE-VLESS-WS-100MS`
23. `AKUN-025-CLOUDFLARE-VLESS-WS-99MS` (url=1104ms, status=HTTP 204)
24. `AKUN-007-RS-RAPIDSEEDBOX-20190717-VLESS-WS-97MS`
25. `AKUN-027-UNKNOWN-VLESS-WS-103MS` (url=337ms, nekobox=6181ms, status=no)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-114MS` (url=1687ms, status=HTTP 204)
27. `AKUN-029-TENCENT-VLESS-WS-91MS` (url=611ms, status=HTTP 204)
28. `AKUN-005-RETZOR-VLESS-WS-97MS`
29. `AKUN-031-UNKNOWN-VLESS-WS-110MS` (url=628ms, status=HTTP 204)
30. `AKUN-032-CLOUDFLARE-VLESS-WS-102MS` (url=617ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
