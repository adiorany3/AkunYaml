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
- Kandidat strict NekoBox-tested: 20
- Proxy di openclash_fresh_pool.yaml: 30

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-124MS` (url=400ms, nekobox=392ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-132MS` (url=1348ms, nekobox=1434ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-106MS` (url=367ms, nekobox=411ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-157MS` (url=385ms, nekobox=1414ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-137MS` (url=358ms, nekobox=398ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-132MS` (url=359ms, nekobox=424ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-193MS` (url=1347ms, nekobox=281ms, status=no)
8. `AKUN-007-CLOUDFLARE-VLESS-WS-170MS`
9. `AKUN-008-BIGCOMMERCE-VLESS-WS-179MS`
10. `AKUN-009-FMN5-RENTED-NET-VLESS-WS-114MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-156MS` (url=345ms, nekobox=273ms, status=no)
12. `AKUN-010-CLOUDFLARE-VLESS-WS-185MS`
13. `AKUN-014-CLOUDFLARE-VLESS-WS-170MS` (url=1321ms, nekobox=1274ms, status=no)
14. `AKUN-011-CLOUDFLARE-VLESS-WS-174MS`
15. `AKUN-012-CLOUDFLARE-VLESS-WS-178MS`
16. `AKUN-013-CLOUDFLARE-VLESS-WS-185MS` (url=376ms, nekobox=420ms, status=yes)
17. `AKUN-014-CLOUDFLARE-VLESS-WS-195MS`
18. `AKUN-015-CLOUDFLARE-VLESS-WS-205MS`
19. `AKUN-020-CLOUDFLARE-VLESS-WS-156MS` (url=349ms, nekobox=282ms, status=no)
20. `AKUN-016-CLOUDFLARE-VLESS-WS-187MS`
21. `AKUN-017-CLOUDFLARE-VLESS-WS-232MS`
22. `AKUN-018-NOTION-WEB-VLESS-WS-240MS`
23. `AKUN-019-CLOUDFLARE-VLESS-WS-161MS`
24. `AKUN-026-CLOUDFLARE-VLESS-WS-201MS` (url=355ms, nekobox=293ms, status=no)
25. `AKUN-020-CLOUDFLARE-VLESS-WS-217MS`
26. `AKUN-028-VEESP-VLESS-WS-220MS` (url=452ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-209MS` (url=339ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-184MS` (url=343ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-222MS` (url=377ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-241MS` (url=382ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
