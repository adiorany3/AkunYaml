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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-135MS` (url=402ms, nekobox=296ms, status=no)
2. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-125MS` (url=431ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-151MS` (url=2184ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-144MS` (url=488ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-128MS` (url=441ms, status=HTTP 204)
6. `AKUN-006-ZUOAI-VLESS-WS-158MS` (url=428ms, status=HTTP 204)
7. `AKUN-007-OLOIN-1-VLESS-WS-195MS` (url=416ms, status=HTTP 204)
8. `AKUN-008-OLOIN-1-VLESS-WS-196MS` (url=434ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-125MS` (url=439ms, status=HTTP 204)
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-146MS` (url=438ms, status=HTTP 204)
11. `AKUN-011-PMBET-NET-VLESS-WS-187MS` (url=416ms, status=HTTP 204)
12. `AKUN-005-CLOUDFLARE-VLESS-WS-128MS-954ea4e4`
13. `AKUN-013-CLOUDFLARE-VLESS-WS-134MS` (url=433ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-136MS` (url=475ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-128MS` (url=443ms, status=HTTP 204)
16. `AKUN-002-CLOUDFLARE-VLESS-WS-155MS`
17. `AKUN-001-CLOUDFLARE-VLESS-WS-145MS`
18. `AKUN-003-TENCENT-VLESS-WS-151MS`
19. `AKUN-004-BIGCOMMERCE-VLESS-WS-121MS`
20. `AKUN-020-UNKNOWN-VLESS-WS-119MS` (url=431ms, status=HTTP 204)
21. `AKUN-007-CLOUDFLARE-VLESS-WS-121MS`
22. `AKUN-022-CLOUDFLARE-VLESS-WS-133MS` (url=438ms, status=HTTP 204)
23. `AKUN-008-CLOUDFLARE-VLESS-WS-177MS`
24. `AKUN-009-CLOUDFLARE-VLESS-WS-160MS`
25. `AKUN-025-CLOUDFLARE-VLESS-WS-150MS` (url=454ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-150MS` (url=710ms, status=HTTP 204)
27. `AKUN-027-NASEEJ-VLESS-WS-237MS` (url=464ms, status=HTTP 204)
28. `AKUN-006-CLOUDFLARE-VLESS-WS-164MS`
29. `AKUN-029-TYCHRON-02-VLESS-WS-239MS` (url=419ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-161MS` (url=417ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
