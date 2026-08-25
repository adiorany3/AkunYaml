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
1. `AKUN-001-UNKNOWN-VLESS-WS-101MS` (url=359ms, status=HTTP 204)
2. `AKUN-002-RUSSIA-VLESS-WS-100MS` (url=1362ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-99MS` (url=349ms, status=HTTP 204)
4. `AKUN-004-AIMALL-VLESS-WS-101MS` (url=362ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-114MS` (url=341ms, status=HTTP 204)
6. `AKUN-006-NOTION-WEB-VLESS-WS-111MS` (url=337ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-110MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-111MS`
9. `AKUN-009-TIME-VLESS-WS-126MS`
10. `AKUN-010-CHATGPT-VLESS-WS-120MS`
11. `AKUN-013-UNKNOWN-VLESS-WS-128MS` (url=353ms, status=HTTP 204)
12. `AKUN-014-MYBB-VLESS-WS-360MS` (url=331ms, status=HTTP 204)
13. `AKUN-015-MEDIUM-VLESS-WS-301MS` (url=326ms, status=HTTP 204)
14. `AKUN-016-MRCLOUDI-VLESS-WS-451MS` (url=1001ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-321MS` (url=345ms, status=HTTP 204)
16. `AKUN-018-ZVC-VLESS-WS-149MS` (url=324ms, status=HTTP 204)
17. `AKUN-019-UNKNOWN-VLESS-WS-317MS` (url=304ms, status=HTTP 204)
18. `AKUN-020-SPEEDTEST-VLESS-WS-359MS` (url=1341ms, status=HTTP 204)
19. `AKUN-021-DEV-VLESS-WS-244MS` (url=360ms, status=HTTP 204)
20. `AKUN-022-UNKNOWN-VLESS-WS-356MS` (url=1361ms, status=HTTP 204)
21. `AKUN-023-UNKNOWN-VLESS-WS-354MS` (url=1354ms, status=HTTP 204)
22. `AKUN-024-UNKNOWN-VLESS-WS-357MS` (url=370ms, status=HTTP 204)
23. `AKUN-025-TIME-VLESS-WS-314MS` (url=334ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-225MS` (url=1319ms, status=HTTP 204)
25. `AKUN-027-UNKNOWN-VLESS-WS-317MS` (url=358ms, status=HTTP 204)
26. `AKUN-029-UNKNOWN-VLESS-WS-299MS` (url=344ms, status=HTTP 204)
27. `AKUN-033-NL-TELEMAGIC-20111109-VLESS-WS-808MS` (url=2406ms, status=HTTP 204)
28. `AKUN-035-UNKNOWN-VLESS-WS-360MS` (url=333ms, status=HTTP 204)
29. `AKUN-036-DEV-VLESS-WS-356MS` (url=1356ms, status=HTTP 204)
30. `AKUN-037-CLOUDFLARE-VLESS-WS-225MS` (url=362ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
