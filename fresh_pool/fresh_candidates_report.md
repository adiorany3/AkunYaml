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
- Kandidat strict NekoBox-tested: 7
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-85MS` (url=2044ms, status=HTTP 204)
2. `AKUN-003-CLOUDFLARE-VLESS-WS-105MS` (url=666ms, status=HTTP 204)
3. `AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-116MS` (url=694ms, status=HTTP 204)
4. `AKUN-003-CLOUDFLARE-VLESS-WS-90MS`
5. `AKUN-006-CLOUDFLARE-VLESS-WS-128MS` (url=677ms, status=HTTP 204)
6. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-157MS`
7. `AKUN-004-CLOUDFLARE-VLESS-WS-91MS`
8. `AKUN-009-UNKNOWN-VLESS-WS-90MS` (url=664ms, status=HTTP 204)
9. `AKUN-010-CLOUDFLARE-VLESS-WS-107MS` (url=654ms, status=HTTP 204)
10. `AKUN-011-CLOUDFLARE-VLESS-WS-91MS` (url=656ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-131MS` (url=550ms, nekobox=1274ms, status=no)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-84MS` (url=665ms, status=HTTP 204)
13. `AKUN-016-CLOUDFLARE-VLESS-WS-83MS` (url=650ms, status=HTTP 204)
14. `AKUN-017-TENCENT-VLESS-WS-86MS` (url=662ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-90MS` (url=654ms, status=HTTP 204)
16. `AKUN-006-CLOUDFLARE-VLESS-WS-86MS`
17. `AKUN-002-CLOUDFLARE-VLESS-WS-86MS`
18. `AKUN-005-MEDIUM-VLESS-WS-110MS`
19. `AKUN-022-CLOUDFLARE-VLESS-WS-115MS` (url=750ms, status=HTTP 204)
20. `AKUN-023-CLOUDFLARE-VLESS-WS-99MS` (url=731ms, status=HTTP 204)
21. `AKUN-024-CLOUDFLARE-VLESS-WS-92MS` (url=691ms, status=HTTP 204)
22. `AKUN-025-UNKNOWN-VLESS-WS-94MS` (url=655ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-323MS` (url=652ms, status=HTTP 204)
24. `AKUN-027-BIGCOMMERCE-VLESS-WS-315MS` (url=759ms, status=HTTP 204)
25. `AKUN-028-UNKNOWN-VLESS-WS-320MS` (url=367ms, nekobox=6348ms, status=no)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-93MS` (url=643ms, status=HTTP 204)
27. `AKUN-030-CLOUDFLARE-VLESS-WS-97MS` (url=656ms, status=HTTP 204)
28. `AKUN-007-CLOUDFLARE-VLESS-WS-298MS`
29. `AKUN-032-CLOUDFLARE-VLESS-WS-290MS` (url=661ms, status=HTTP 204)
30. `AKUN-034-CLOUDFLARE-VLESS-WS-224MS` (url=634ms, nekobox=267ms, status=no)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
