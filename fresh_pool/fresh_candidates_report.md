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
- Proxy di openclash_fresh_pool.yaml: 33

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
1. `AKUN-001-DEV-VLESS-WS-90MS` (url=394ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-87MS` (url=1956ms, status=HTTP 204)
3. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-89MS` (url=386ms, status=HTTP 204)
4. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-86MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-90MS` (url=378ms, status=HTTP 204)
6. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-92MS` (url=412ms, status=HTTP 204)
7. `AKUN-007-DEV-VLESS-WS-94MS` (url=396ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-91MS` (url=400ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-90MS` (url=372ms, nekobox=447ms, status=yes)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-84MS` (url=399ms, status=HTTP 204)
11. `AKUN-005-UNKNOWN-VLESS-WS-87MS`
12. `AKUN-012-AIMALL-VLESS-WS-85MS` (url=383ms, status=HTTP 204)
13. `AKUN-008-CLOUDFLARE-VLESS-WS-99MS`
14. `AKUN-014-UNKNOWN-VLESS-WS-100MS` (url=401ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-90MS` (url=382ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-91MS` (url=383ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-100MS` (url=389ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-85MS` (url=393ms, status=HTTP 204)
19. `AKUN-019-RS-RAPIDSEEDBOX-20190717-VLESS-WS-104MS` (url=376ms, status=HTTP 204)
20. `AKUN-007-AXIOMED-VLESS-WS-86MS`
21. `AKUN-002-BIGCOMMERCE-VLESS-WS-88MS`
22. `AKUN-004-DEV-VLESS-WS-91MS`
23. `AKUN-024-CLOUDFLARE-VLESS-WS-88MS` (url=434ms, status=HTTP 204)
24. `AKUN-001-AXIOMED-VLESS-WS-111MS`
25. `AKUN-026-UNKNOWN-VLESS-WS-85MS` (url=397ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-99MS` (url=379ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-86MS` (url=389ms, status=HTTP 204)
28. `AKUN-010-CLOUDFLARE-VLESS-WS-94MS`
29. `AKUN-003-MEDIUM-VLESS-WS-88MS`
30. `AKUN-031-CLOUDFLARE-VLESS-WS-88MS` (url=374ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
