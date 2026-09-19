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
1. `AKUN-001-DEV-VLESS-WS-117MS` (url=468ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-107MS` (url=403ms, status=HTTP 204)
3. `AKUN-003-VULTR-VLESS-WS-130MS` (url=448ms, status=HTTP 204)
4. `AKUN-010-CLOUDFLARE-VLESS-WS-138MS`
5. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS` (url=567ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-150MS` (url=406ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-194MS` (url=464ms, status=HTTP 204)
8. `AKUN-007-CLOUDFLARE-VLESS-WS-126MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS-34aa55b2`
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-200MS` (url=450ms, status=HTTP 204)
11. `AKUN-011-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=411ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-138MS` (url=420ms, status=HTTP 204)
13. `AKUN-002-MEDIUM-VLESS-WS-131MS`
14. `AKUN-014-CLOUDFLARE-VLESS-WS-149MS` (url=449ms, status=HTTP 204)
15. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-123MS`
16. `AKUN-016-CLOUDFLARE-VLESS-WS-167MS` (url=430ms, status=HTTP 204)
17. `AKUN-017-UNKNOWN-VLESS-WS-125MS` (url=453ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-136MS` (url=479ms, status=HTTP 204)
19. `AKUN-019-NASEEJ-VLESS-WS-249MS` (url=403ms, status=HTTP 204)
20. `AKUN-020-ZUOAI-VLESS-WS-262MS` (url=406ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-138MS` (url=403ms, status=HTTP 204)
22. `AKUN-022-BIGCOMMERCE-VLESS-WS-136MS` (url=508ms, status=HTTP 204)
23. `AKUN-006-CLOUDFLARE-VLESS-WS-207MS`
24. `AKUN-008-UNKNOWN-VLESS-WS-237MS`
25. `AKUN-025-DEV-VLESS-WS-134MS` (url=413ms, status=HTTP 204)
26. `AKUN-026-RS-RAPIDSEEDBOX-20190717-VLESS-WS-136MS` (url=421ms, status=HTTP 204)
27. `AKUN-004-TENCENT-VLESS-WS-153MS`
28. `AKUN-001-CLOUDFLARE-VLESS-WS-164MS`
29. `AKUN-030-CLOUDFLARE-VLESS-WS-207MS` (url=1879ms, status=HTTP 204)
30. `AKUN-003-CLOUDFLARE-VLESS-WS-200MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
