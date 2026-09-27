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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-117MS` (url=428ms, status=HTTP 204)
2. `AKUN-002-UNKNOWN-VLESS-WS-119MS` (url=1171ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-120MS` (url=437ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-126MS` (url=443ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-131MS` (url=421ms, status=HTTP 204)
6. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-132MS` (url=446ms, status=HTTP 204)
7. `AKUN-002-UNKNOWN-VLESS-WS-125MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-127MS` (url=390ms, nekobox=302ms, status=no)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-144MS` (url=418ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-123MS` (url=466ms, status=HTTP 204)
11. `AKUN-011-DEV-VLESS-WS-137MS` (url=413ms, status=HTTP 204)
12. `AKUN-008-CLOUDFLARE-VLESS-WS-113MS`
13. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-122MS`
14. `AKUN-014-CLOUDFLARE-VLESS-WS-130MS` (url=400ms, nekobox=6180ms, status=no)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-137MS` (url=437ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-130MS` (url=426ms, status=HTTP 204)
17. `AKUN-004-UNKNOWN-VLESS-WS-110MS`
18. `AKUN-018-CLOUDFLARE-VLESS-WS-127MS` (url=422ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-137MS` (url=413ms, status=HTTP 204)
20. `AKUN-005-CLOUDFLARE-VLESS-WS-134MS`
21. `AKUN-006-CLOUDFLARE-VLESS-WS-145MS`
22. `AKUN-022-BIGCOMMERCE-VLESS-WS-134MS` (url=412ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-149MS` (url=457ms, status=HTTP 204)
24. `AKUN-024-UNKNOWN-VLESS-WS-127MS` (url=433ms, status=HTTP 204)
25. `AKUN-001-AXIOMED-VLESS-WS-130MS`
26. `AKUN-026-AIMALL-VLESS-WS-119MS` (url=467ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-130MS` (url=431ms, status=HTTP 204)
28. `AKUN-029-MEDIUM-VLESS-WS-139MS` (url=413ms, status=HTTP 204)
29. `AKUN-007-CLOUDFLARE-VLESS-WS-110MS`
30. `AKUN-031-CLOUDFLARE-VLESS-WS-118MS` (url=537ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
