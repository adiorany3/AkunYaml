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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-123MS` (url=426ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-149MS` (url=363ms, nekobox=309ms, status=no)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-148MS` (url=435ms, status=HTTP 204)
4. `AKUN-006-FI-HOXHUNT-19981229-VLESS-WS-166MS`
5. `AKUN-005-OLOIN-1-VLESS-WS-145MS` (url=407ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-133MS` (url=455ms, status=HTTP 204)
7. `AKUN-002-CLOUDFLARE-VLESS-WS-155MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-158MS` (url=437ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-135MS` (url=461ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-154MS` (url=415ms, status=HTTP 204)
11. `AKUN-011-NASEEJ-VLESS-WS-242MS` (url=437ms, status=HTTP 204)
12. `AKUN-012-OLOIN-1-VLESS-WS-176MS` (url=439ms, status=HTTP 204)
13. `AKUN-013-PMBET-NET-VLESS-WS-172MS` (url=427ms, status=HTTP 204)
14. `AKUN-014-NASEEJ-VLESS-WS-231MS` (url=451ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-151MS` (url=531ms, status=HTTP 204)
16. `AKUN-016-BIGCOMMERCE-VLESS-WS-144MS` (url=418ms, status=HTTP 204)
17. `AKUN-017-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-145MS` (url=409ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-114MS` (url=393ms, nekobox=330ms, status=no)
19. `AKUN-019-UNKNOWN-VLESS-WS-138MS` (url=484ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-123MS` (url=448ms, status=HTTP 204)
21. `AKUN-005-CLOUDFLARE-VLESS-WS-121MS`
22. `AKUN-001-CLOUDFLARE-VLESS-WS-172MS`
23. `AKUN-023-CLOUDFLARE-VLESS-WS-152MS` (url=449ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-178MS` (url=3510ms, status=HTTP 204)
25. `AKUN-003-CLOUDFLARE-VLESS-WS-135MS`
26. `AKUN-007-CLOUDFLARE-VLESS-WS-185MS`
27. `AKUN-008-TENCENT-VLESS-WS-130MS`
28. `AKUN-028-CLOUDFLARE-VLESS-WS-127MS` (url=430ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-179MS` (url=448ms, status=HTTP 204)
30. `AKUN-004-CLOUDFLARE-VLESS-WS-181MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
