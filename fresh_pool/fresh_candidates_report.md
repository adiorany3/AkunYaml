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
- Kandidat strict NekoBox-tested: 8
- Proxy di openclash_fresh_pool.yaml: 32

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
1. `AKUN-001-UNKNOWN-VLESS-WS-84MS` (url=963ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-92MS` (url=365ms, status=HTTP 204)
3. `AKUN-003-AIMALL-VLESS-WS-97MS` (url=345ms, nekobox=413ms, status=yes)
4. `AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-103MS`
5. `AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-95MS`
6. `AKUN-001-BIGCOMMERCE-VLESS-WS-105MS`
7. `AKUN-008-CLOUDFLARE-VLESS-WS-112MS` (url=366ms, status=HTTP 204)
8. `AKUN-009-CLOUDFLARE-VLESS-WS-95MS` (url=345ms, nekobox=6186ms, status=no)
9. `AKUN-010-CLOUDFLARE-VLESS-WS-87MS` (url=376ms, status=HTTP 204)
10. `AKUN-011-CLOUDFLARE-VLESS-WS-101MS` (url=375ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-102MS` (url=381ms, status=HTTP 204)
12. `AKUN-013-DEV-VLESS-WS-91MS` (url=374ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-84MS` (url=406ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-95MS` (url=377ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-90MS` (url=383ms, status=HTTP 204)
16. `AKUN-007-MEDIUM-VLESS-WS-90MS`
17. `AKUN-018-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-93MS` (url=356ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-95MS` (url=358ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-92MS` (url=383ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-100MS` (url=389ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-93MS` (url=373ms, status=HTTP 204)
22. `AKUN-008-UNKNOWN-VLESS-WS-100MS`
23. `AKUN-024-CLOUDFLARE-VLESS-WS-96MS` (url=358ms, status=HTTP 204)
24. `AKUN-005-CLOUDFLARE-VLESS-WS-98MS`
25. `AKUN-002-CLOUDFLARE-VLESS-WS-100MS`
26. `AKUN-027-CLOUDFLARE-VLESS-WS-101MS` (url=405ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-92MS` (url=351ms, nekobox=5182ms, status=no)
28. `AKUN-029-UNKNOWN-VLESS-WS-91MS` (url=353ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-90MS` (url=364ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-206MS` (url=590ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
