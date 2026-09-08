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
- Kandidat strict NekoBox-tested: 3
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-225MS` (url=418ms, nekobox=210ms, status=no)
2. `AKUN-001-CLOUDFLARE-VLESS-WS-238MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-227MS` (url=566ms, nekobox=294ms, status=no)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-235MS` (url=415ms, nekobox=5170ms, status=no)
5. `AKUN-005-UNKNOWN-VLESS-WS-257MS` (url=585ms, nekobox=168ms, status=no)
6. `AKUN-003-UNKNOWN-VLESS-WS-257MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-241MS` (url=490ms, nekobox=163ms, status=no)
8. `AKUN-008-RS-RAPIDSEEDBOX-20190717-VLESS-WS-267MS` (url=870ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-262MS` (url=424ms, nekobox=162ms, status=no)
10. `AKUN-002-UNKNOWN-VLESS-WS-251MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-246MS` (url=3361ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-264MS` (url=892ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-264MS` (url=550ms, nekobox=163ms, status=no)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-247MS` (url=738ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-223MS` (url=797ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-258MS` (url=1044ms, status=HTTP 204)
17. `AKUN-017-ORG-VLESS-WS-340MS` (url=1285ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-312MS` (url=829ms, status=HTTP 204)
19. `AKUN-019-NOTION-WEB-VLESS-WS-342MS` (url=935ms, status=HTTP 204)
20. `AKUN-020-RS-RAPIDSEEDBOX-20190717-VLESS-WS-482MS` (url=1433ms, status=HTTP 204)
21. `AKUN-021-BIGCOMMERCE-VLESS-WS-639MS` (url=986ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-340MS` (url=1660ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-359MS` (url=1170ms, status=HTTP 204)
24. `AKUN-024-MEDIUM-VLESS-WS-355MS` (url=1548ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-533MS` (url=1493ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-597MS` (url=4028ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-366MS` (url=1252ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-290MS` (url=1271ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-292MS` (url=696ms, status=HTTP 204)
30. `AKUN-031-CLOUDINARY-VLESS-WS-301MS` (url=835ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
