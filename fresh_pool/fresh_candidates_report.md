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
1. `AKUN-006-UNKNOWN-VLESS-WS-126MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-152MS` (url=443ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-159MS` (url=405ms, nekobox=470ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-141MS` (url=436ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-143MS` (url=432ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-117MS` (url=372ms, nekobox=486ms, status=no)
7. `AKUN-004-CLOUDFLARE-VLESS-WS-121MS`
8. `AKUN-009-CLOUDFLARE-VLESS-WS-141MS`
9. `AKUN-009-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-144MS` (url=573ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-142MS` (url=539ms, status=HTTP 204)
11. `AKUN-008-CLOUDFLARE-VLESS-WS-173MS`
12. `AKUN-012-UNKNOWN-VLESS-WS-153MS` (url=461ms, status=HTTP 204)
13. `AKUN-005-CLOUDFLARE-VLESS-WS-181MS`
14. `AKUN-014-UNKNOWN-VLESS-WS-176MS` (url=633ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-213MS` (url=751ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-125MS` (url=453ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-127MS` (url=432ms, status=HTTP 204)
18. `AKUN-001-CLOUDFLARE-VLESS-WS-182MS`
19. `AKUN-019-UNKNOWN-VLESS-WS-142MS` (url=497ms, status=HTTP 204)
20. `AKUN-007-CLOUDFLARE-VLESS-WS-148MS`
21. `AKUN-021-CLOUDFLARE-VLESS-WS-177MS` (url=427ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-133MS` (url=422ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-144MS` (url=438ms, status=HTTP 204)
24. `AKUN-024-UNKNOWN-VLESS-WS-358MS` (url=1425ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-145MS` (url=465ms, status=HTTP 204)
26. `AKUN-026-TENCENT-VLESS-WS-125MS` (url=467ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-142MS` (url=640ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-146MS` (url=425ms, status=HTTP 204)
29. `AKUN-002-CLOUDFLARE-VLESS-WS-143MS`
30. `AKUN-030-SEPPORATED-VLESS-WS-661MS` (url=1862ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
