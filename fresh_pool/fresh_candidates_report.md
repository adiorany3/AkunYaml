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
1. `AKUN-001-UNKNOWN-VLESS-WS-256MS` (url=851ms, status=HTTP 204)
2. `AKUN-002-ZVC-VLESS-WS-263MS` (url=735ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-240MS` (url=689ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-243MS` (url=536ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-266MS` (url=571ms, status=HTTP 204)
6. `AKUN-006-MYBB-VLESS-WS-279MS` (url=801ms, status=HTTP 204)
7. `AKUN-007-TIME-VLESS-WS-280MS` (url=548ms, status=HTTP 204)
8. `AKUN-008-EU-VLESS-WS-263MS` (url=761ms, status=HTTP 204)
9. `AKUN-009-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-256MS` (url=807ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-265MS` (url=523ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-270MS` (url=759ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-264MS` (url=769ms, status=HTTP 204)
13. `AKUN-013-DEV-VLESS-WS-256MS` (url=730ms, status=HTTP 204)
14. `AKUN-014-OPENAI-VLESS-WS-278MS` (url=518ms, status=HTTP 204)
15. `AKUN-015-SPEEDTEST-VLESS-WS-262MS` (url=541ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-271MS` (url=658ms, status=HTTP 204)
17. `AKUN-017-DEV-VLESS-WS-256MS` (url=828ms, status=HTTP 204)
18. `AKUN-018-UNKNOWN-VLESS-WS-271MS` (url=761ms, status=HTTP 204)
19. `AKUN-019-DEV-VLESS-WS-275MS` (url=639ms, status=HTTP 204)
20. `AKUN-020-TIME-VLESS-WS-285MS` (url=720ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-276MS` (url=771ms, status=HTTP 204)
22. `AKUN-022-CCWU-VLESS-WS-264MS` (url=811ms, status=HTTP 204)
23. `AKUN-023-NOTION-WEB-VLESS-WS-279MS` (url=587ms, status=HTTP 204)
24. `AKUN-024-SPEEDTEST-VLESS-WS-244MS` (url=613ms, status=HTTP 204)
25. `AKUN-025-DEV-VLESS-WS-271MS` (url=776ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-285MS` (url=759ms, status=HTTP 204)
27. `AKUN-028-RUSSIA-VLESS-WS-271MS` (url=549ms, status=HTTP 204)
28. `AKUN-029-SPEEDTEST-VLESS-WS-286MS` (url=1053ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-261MS` (url=752ms, status=HTTP 204)
30. `AKUN-032-MEDIUM-VLESS-WS-283MS` (url=704ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
