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
1. `AKUN-001-RS-RAPIDSEEDBOX-20190717-VLESS-WS-114MS` (url=413ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-116MS` (url=388ms, status=HTTP 204)
3. `AKUN-005-CLOUDFLARE-VLESS-WS-128MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-121MS` (url=394ms, status=HTTP 204)
5. `AKUN-005-NOTION-WEB-VLESS-WS-126MS` (url=397ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-125MS` (url=1422ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-124MS` (url=1377ms, status=HTTP 204)
8. `AKUN-008-MEDIUM-VLESS-WS-122MS` (url=1382ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-132MS` (url=1408ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-132MS` (url=1397ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-121MS` (url=413ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-131MS` (url=388ms, status=HTTP 204)
13. `AKUN-004-CLOUDFLARE-VLESS-WS-127MS`
14. `AKUN-014-CLOUDFLARE-VLESS-WS-127MS` (url=949ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-125MS` (url=390ms, status=HTTP 204)
16. `AKUN-006-CLOUDFLARE-VLESS-WS-127MS`
17. `AKUN-017-CLOUDFLARE-VLESS-WS-127MS` (url=397ms, status=HTTP 204)
18. `AKUN-008-CLOUDFLARE-VLESS-WS-137MS`
19. `AKUN-007-ORG-VLESS-WS-145MS`
20. `AKUN-002-CLOUDFLARE-VLESS-WS-134MS`
21. `AKUN-021-CLOUDFLARE-VLESS-WS-134MS` (url=422ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-140MS` (url=1088ms, status=HTTP 204)
23. `AKUN-023-RS-RAPIDSEEDBOX-20190717-VLESS-WS-131MS` (url=400ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-156MS` (url=418ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-124MS` (url=361ms, nekobox=452ms, status=no)
26. `AKUN-026-BIGCOMMERCE-VLESS-WS-127MS` (url=389ms, status=HTTP 204)
27. `AKUN-001-CLOUDFLARE-VLESS-WS-116MS`
28. `AKUN-003-CLOUDFLARE-VLESS-WS-144MS`
29. `AKUN-030-CLOUDFLARE-VLESS-WS-143MS` (url=941ms, status=HTTP 204)
30. `AKUN-009-CLOUDFLARE-VLESS-WS-138MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
