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
1. `AKUN-001-DEV-VLESS-WS-137MS` (url=451ms, status=HTTP 204)
2. `AKUN-002-VULTR-VLESS-WS-137MS` (url=463ms, status=HTTP 204)
3. `AKUN-005-NET-147-90-26-0-24-VLESS-WS-139MS`
4. `AKUN-002-CLOUDFLARE-VLESS-WS-140MS`
5. `AKUN-006-CLOUDFLARE-VLESS-WS-136MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-139MS` (url=378ms, nekobox=322ms, status=no)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-159MS` (url=466ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-132MS` (url=435ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-122MS` (url=483ms, status=HTTP 204)
10. `AKUN-010-UNKNOWN-VLESS-WS-154MS` (url=469ms, status=HTTP 204)
11. `AKUN-008-CLOUDFLARE-VLESS-WS-163MS`
12. `AKUN-012-CLOUDFLARE-VLESS-WS-140MS` (url=578ms, status=HTTP 204)
13. `AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-210MS`
14. `AKUN-014-CLOUDFLARE-VLESS-WS-158MS` (url=427ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-150MS` (url=448ms, status=HTTP 204)
16. `AKUN-016-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-143MS` (url=421ms, status=HTTP 204)
17. `AKUN-001-MEDIUM-VLESS-WS-133MS`
18. `AKUN-018-CLOUDFLARE-VLESS-WS-143MS` (url=434ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-120MS` (url=460ms, status=HTTP 204)
20. `AKUN-020-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-128MS` (url=455ms, status=HTTP 204)
21. `AKUN-021-UNKNOWN-VLESS-WS-125MS` (url=457ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-157MS` (url=501ms, status=HTTP 204)
23. `AKUN-003-BIGCOMMERCE-VLESS-WS-145MS`
24. `AKUN-007-CLOUDFLARE-VLESS-WS-122MS`
25. `AKUN-025-CLOUDFLARE-VLESS-WS-260MS` (url=433ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-153MS` (url=463ms, status=HTTP 204)
27. `AKUN-027-ZUOAI-VLESS-WS-238MS` (url=439ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-158MS` (url=427ms, status=HTTP 204)
29. `AKUN-029-UNKNOWN-VLESS-WS-129MS` (url=433ms, status=HTTP 204)
30. `AKUN-009-UNKNOWN-VLESS-WS-214MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
