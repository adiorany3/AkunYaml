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
1. `AKUN-001-VULTR-VLESS-WS-153MS` (url=484ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-133MS` (url=439ms, status=HTTP 204)
3. `AKUN-003-NET-147-90-26-0-24-VLESS-WS-141MS` (url=410ms, status=HTTP 204)
4. `AKUN-010-CLOUDFLARE-VLESS-WS-113MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-112MS` (url=444ms, status=HTTP 204)
6. `AKUN-009-CLOUDFLARE-VLESS-WS-111MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-119MS` (url=434ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-108MS` (url=428ms, status=HTTP 204)
9. `AKUN-009-DEV-VLESS-WS-149MS` (url=414ms, status=HTTP 204)
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-221MS` (url=425ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-201MS` (url=413ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-131MS` (url=407ms, status=HTTP 204)
13. `AKUN-013-UNKNOWN-VLESS-WS-134MS` (url=431ms, status=HTTP 204)
14. `AKUN-006-ZUOAI-VLESS-WS-214MS`
15. `AKUN-015-NASEEJ-VLESS-WS-216MS` (url=442ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-257MS` (url=419ms, status=HTTP 204)
17. `AKUN-018-DEV-VLESS-WS-172MS` (url=395ms, status=HTTP 204)
18. `AKUN-007-CLOUDFLARE-VLESS-WS-178MS`
19. `AKUN-020-CLOUDFLARE-VLESS-WS-174MS` (url=447ms, status=HTTP 204)
20. `AKUN-001-TENCENT-VLESS-WS-169MS`
21. `AKUN-005-UNKNOWN-VLESS-WS-254MS`
22. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-256MS`
23. `AKUN-002-CLOUDFLARE-VLESS-WS-185MS`
24. `AKUN-025-UNKNOWN-VLESS-WS-234MS` (url=439ms, status=HTTP 204)
25. `AKUN-027-UNKNOWN-VLESS-WS-332MS` (url=438ms, status=HTTP 204)
26. `AKUN-008-CLOUDFLARE-VLESS-WS-239MS`
27. `AKUN-004-CLOUDFLARE-VLESS-WS-231MS`
28. `AKUN-030-CLOUDFLARE-VLESS-WS-249MS` (url=3065ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-160MS` (url=414ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-165MS` (url=395ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
