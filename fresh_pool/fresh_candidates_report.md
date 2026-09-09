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
- Kandidat strict NekoBox-tested: 7
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
1. `AKUN-003-CLOUDFLARE-VLESS-WS-125MS` (url=340ms, nekobox=599ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-116MS` (url=417ms, status=HTTP 204)
3. `AKUN-001-CLOUDFLARE-VLESS-WS-125MS` (url=364ms, nekobox=445ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-124MS` (url=404ms, status=HTTP 204)
5. `AKUN-002-CLOUDFLARE-VLESS-WS-129MS`
6. `AKUN-006-NOTION-WEB-VLESS-WS-131MS` (url=390ms, nekobox=6191ms, status=no)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-125MS` (url=398ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-134MS` (url=411ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-130MS` (url=410ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-130MS` (url=2310ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-133MS` (url=1389ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-128MS` (url=409ms, status=HTTP 204)
13. `AKUN-013-EE-WELCOMEHOST-20190515-VLESS-WS-138MS` (url=403ms, status=HTTP 204)
14. `AKUN-014-MEDIUM-VLESS-WS-136MS` (url=396ms, status=HTTP 204)
15. `AKUN-004-CLOUDFLARE-VLESS-WS-131MS`
16. `AKUN-016-CLOUDFLARE-VLESS-WS-138MS` (url=392ms, status=HTTP 204)
17. `AKUN-017-ORG-VLESS-WS-126MS` (url=399ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-116MS` (url=411ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-127MS` (url=395ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-132MS` (url=392ms, status=HTTP 204)
21. `AKUN-006-090227-VLESS-WS-144MS`
22. `AKUN-022-CLOUDFLARE-VLESS-WS-131MS` (url=371ms, nekobox=304ms, status=no)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-124MS` (url=1388ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-131MS` (url=1419ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-132MS` (url=399ms, status=HTTP 204)
26. `AKUN-005-CLOUDFLARE-VLESS-WS-163MS`
27. `AKUN-007-BIGCOMMERCE-VLESS-WS-143MS`
28. `AKUN-029-CLOUDFLARE-VLESS-WS-136MS` (url=389ms, nekobox=6191ms, status=no)
29. `AKUN-030-RS-RAPIDSEEDBOX-20190717-VLESS-WS-134MS` (url=419ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-140MS` (url=391ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
