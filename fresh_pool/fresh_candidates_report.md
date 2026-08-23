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
1. `AKUN-001-UNKNOWN-VLESS-WS-255MS`
2. `AKUN-002-UNKNOWN-VLESS-WS-258MS` (url=488ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-227MS` (url=485ms, status=HTTP 204)
4. `AKUN-004-MEDIUM-VLESS-WS-231MS` (url=469ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-265MS` (url=598ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-249MS` (url=680ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-257MS` (url=839ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-247MS` (url=700ms, status=HTTP 204)
9. `AKUN-009-DEV-VLESS-WS-220MS` (url=589ms, status=HTTP 204)
10. `AKUN-010-UNKNOWN-VLESS-WS-271MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-254MS` (url=750ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-263MS` (url=529ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-250MS` (url=541ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-217MS` (url=549ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-269MS` (url=529ms, status=HTTP 204)
16. `AKUN-016-DEV-VLESS-WS-243MS` (url=550ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-246MS` (url=538ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-280MS` (url=780ms, status=HTTP 204)
19. `AKUN-019-DE5-VLESS-WS-268MS` (url=949ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-236MS` (url=498ms, status=HTTP 204)
21. `AKUN-021-UNKNOWN-VLESS-WS-212MS` (url=690ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-243MS` (url=661ms, status=HTTP 204)
23. `AKUN-023-UNKNOWN-VLESS-WS-255MS` (url=3897ms, status=HTTP 204)
24. `AKUN-024-UNKNOWN-VLESS-WS-257MS` (url=874ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-253MS` (url=655ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-285MS` (url=741ms, status=HTTP 204)
27. `AKUN-027-SPEEDTEST-VLESS-WS-249MS` (url=1517ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-257MS` (url=560ms, status=HTTP 204)
29. `AKUN-029-SPEEDTEST-VLESS-WS-278MS` (url=499ms, status=HTTP 204)
30. `AKUN-030-UNKNOWN-VLESS-WS-239MS` (url=519ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
