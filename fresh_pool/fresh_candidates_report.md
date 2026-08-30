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
1. `AKUN-001-DEV-VLESS-WS-269MS` (url=1013ms, status=HTTP 204)
2. `AKUN-002-DEV-VLESS-WS-296MS` (url=897ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-261MS` (url=1179ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-292MS` (url=1798ms, status=HTTP 204)
5. `AKUN-005-DEV-VLESS-WS-304MS` (url=801ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-311MS` (url=1936ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-263MS` (url=885ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-309MS` (url=744ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-291MS` (url=762ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-308MS` (url=704ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-261MS` (url=723ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-302MS` (url=661ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-262MS` (url=777ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-248MS` (url=899ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-280MS` (url=795ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-320MS` (url=898ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-562MS` (url=793ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-289MS` (url=1032ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-293MS` (url=1178ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-545MS` (url=630ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-545MS` (url=750ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-266MS` (url=704ms, status=HTTP 204)
23. `AKUN-024-CHATGPT-VLESS-WS-557MS` (url=800ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-546MS` (url=926ms, status=HTTP 204)
25. `AKUN-026-DEV-VLESS-WS-367MS` (url=770ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-444MS` (url=890ms, status=HTTP 204)
27. `AKUN-028-NOTION-WEB-VLESS-WS-406MS` (url=732ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-255MS` (url=1427ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-547MS` (url=795ms, status=HTTP 204)
30. `AKUN-031-DEV-VLESS-WS-562MS` (url=672ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
