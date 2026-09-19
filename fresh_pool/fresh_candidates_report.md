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
1. `AKUN-002-UNKNOWN-VLESS-WS-111MS` (url=430ms, status=HTTP 204)
2. `AKUN-003-CLOUDFLARE-VLESS-WS-132MS` (url=418ms, status=HTTP 204)
3. `AKUN-004-NET-147-90-26-0-24-VLESS-WS-137MS` (url=459ms, status=HTTP 204)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-138MS` (url=558ms, status=HTTP 204)
5. `AKUN-006-CLOUDFLARE-VLESS-WS-118MS` (url=369ms, nekobox=352ms, status=no)
6. `AKUN-007-CLOUDFLARE-VLESS-WS-118MS` (url=432ms, status=HTTP 204)
7. `AKUN-008-UNKNOWN-VLESS-WS-146MS` (url=431ms, status=HTTP 204)
8. `AKUN-002-CLOUDFLARE-VLESS-WS-173MS`
9. `AKUN-010-CLOUDFLARE-VLESS-WS-123MS` (url=426ms, status=HTTP 204)
10. `AKUN-011-UNKNOWN-VLESS-WS-211MS` (url=457ms, status=HTTP 204)
11. `AKUN-008-CLOUDFLARE-VLESS-WS-142MS`
12. `AKUN-007-ZUOAI-VLESS-WS-193MS`
13. `AKUN-014-UNKNOWN-VLESS-WS-181MS` (url=425ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-139MS` (url=429ms, status=HTTP 204)
15. `AKUN-001-CLOUDFLARE-VLESS-WS-137MS`
16. `AKUN-017-CLOUDFLARE-VLESS-WS-144MS` (url=432ms, status=HTTP 204)
17. `AKUN-018-DEV-VLESS-WS-127MS` (url=461ms, status=HTTP 204)
18. `AKUN-009-CLOUDFLARE-VLESS-WS-150MS`
19. `AKUN-020-CLOUDFLARE-VLESS-WS-134MS` (url=504ms, status=HTTP 204)
20. `AKUN-003-CLOUDFLARE-VLESS-WS-184MS`
21. `AKUN-004-CLOUDFLARE-VLESS-WS-191MS`
22. `AKUN-023-NASEEJ-VLESS-WS-242MS` (url=456ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-101MS` (url=455ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-190MS` (url=489ms, status=HTTP 204)
25. `AKUN-026-TENCENT-VLESS-WS-115MS` (url=435ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-188MS` (url=431ms, status=HTTP 204)
27. `AKUN-028-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-159MS` (url=421ms, status=HTTP 204)
28. `AKUN-006-CLOUDFLARE-VLESS-WS-192MS`
29. `AKUN-005-UNKNOWN-VLESS-WS-185MS`
30. `AKUN-031-UNKNOWN-VLESS-WS-121MS` (url=421ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
