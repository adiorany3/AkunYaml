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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-123MS` (url=690ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-139MS` (url=445ms, status=HTTP 204)
3. `AKUN-005-CLOUDFLARE-VLESS-WS-164MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-117MS` (url=489ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-111MS` (url=423ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-161MS` (url=531ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-162MS` (url=481ms, status=HTTP 204)
8. `AKUN-002-MEDIUM-VLESS-WS-143MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-164MS` (url=673ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-217MS` (url=639ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-159MS` (url=406ms, status=HTTP 204)
12. `AKUN-012-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=430ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-113MS` (url=422ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-147MS` (url=447ms, status=HTTP 204)
15. `AKUN-007-UNKNOWN-VLESS-WS-153MS`
16. `AKUN-016-CLOUDFLARE-VLESS-WS-174MS` (url=414ms, status=HTTP 204)
17. `AKUN-017-AIMALL-VLESS-WS-152MS` (url=420ms, status=HTTP 204)
18. `AKUN-018-RS-RAPIDSEEDBOX-20190717-VLESS-WS-161MS` (url=724ms, status=HTTP 204)
19. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-148MS`
20. `AKUN-020-UNKNOWN-VLESS-WS-176MS` (url=415ms, status=HTTP 204)
21. `AKUN-009-UNKNOWN-VLESS-WS-175MS`
22. `AKUN-022-CLOUDFLARE-VLESS-WS-132MS` (url=404ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-179MS` (url=404ms, nekobox=289ms, status=no)
24. `AKUN-003-CLOUDFLARE-VLESS-WS-157MS`
25. `AKUN-008-CLOUDFLARE-VLESS-WS-165MS`
26. `AKUN-026-CLOUDFLARE-VLESS-WS-166MS` (url=420ms, status=HTTP 204)
27. `AKUN-027-BIGCOMMERCE-VLESS-WS-145MS` (url=740ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-177MS` (url=488ms, status=HTTP 204)
29. `AKUN-004-CLOUDFLARE-VLESS-WS-179MS`
30. `AKUN-006-TENCENT-VLESS-WS-179MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
