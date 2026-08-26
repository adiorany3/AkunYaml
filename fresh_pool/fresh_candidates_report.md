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
1. `AKUN-001-GO-DADDY-COM-LLC-VLESS-WS-86MS` (url=329ms, status=HTTP 204)
2. `AKUN-002-DEV-VLESS-WS-91MS` (url=1325ms, status=HTTP 204)
3. `AKUN-003-ZVC-VLESS-WS-90MS` (url=322ms, status=HTTP 204)
4. `AKUN-004-RS-RAPIDSEEDBOX-20190717-VLESS-WS-93MS` (url=327ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-93MS` (url=337ms, status=HTTP 204)
6. `AKUN-006-MEDIUM-VLESS-WS-94MS` (url=316ms, status=HTTP 204)
7. `AKUN-007-COGENT-VLESS-WS-94MS` (url=343ms, status=HTTP 204)
8. `AKUN-008-MYBB-VLESS-WS-90MS` (url=300ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-92MS` (url=346ms, status=HTTP 204)
10. `AKUN-010-DEV-VLESS-WS-94MS` (url=341ms, status=HTTP 204)
11. `AKUN-011-SPEEDTEST-VLESS-WS-90MS` (url=334ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-91MS` (url=343ms, status=HTTP 204)
13. `AKUN-013-TWO-E-TELEKOM-VLESS-WS-96MS` (url=335ms, status=HTTP 204)
14. `AKUN-014-DEV-VLESS-WS-97MS` (url=1328ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-94MS` (url=316ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-93MS` (url=332ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-95MS` (url=342ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-96MS` (url=342ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-99MS` (url=348ms, status=HTTP 204)
20. `AKUN-020-CHATGPT-VLESS-WS-92MS` (url=334ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-90MS` (url=1334ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-99MS` (url=328ms, status=HTTP 204)
23. `AKUN-024-SPEEDTEST-VLESS-WS-90MS` (url=333ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-92MS` (url=330ms, status=HTTP 204)
25. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-110MS` (url=341ms, status=HTTP 204)
26. `AKUN-027-SPEEDTEST-VLESS-WS-94MS` (url=347ms, status=HTTP 204)
27. `AKUN-028-DEV-VLESS-WS-96MS` (url=330ms, status=HTTP 204)
28. `AKUN-029-DEV-VLESS-WS-104MS` (url=345ms, status=HTTP 204)
29. `AKUN-030-SPEEDTEST-VLESS-WS-91MS` (url=325ms, status=HTTP 204)
30. `AKUN-031-CCWU-VLESS-WS-96MS` (url=1344ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
