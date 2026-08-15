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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-115MS` (url=370ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-122MS` (url=367ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-116MS` (url=336ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-126MS` (url=380ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-124MS` (url=389ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-112MS` (url=365ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-128MS` (url=377ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-144MS` (url=367ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-139MS` (url=1385ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-184MS` (url=1344ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-125MS` (url=370ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-123MS` (url=367ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-152MS` (url=374ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-125MS` (url=386ms, status=HTTP 204)
15. `AKUN-015-NOTION-WEB-VLESS-WS-164MS` (url=410ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-180MS` (url=1340ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-146MS` (url=383ms, status=HTTP 204)
18. `AKUN-018-NOTION-WEB-VLESS-WS-204MS` (url=1367ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-164MS` (url=383ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-152MS` (url=371ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-156MS` (url=368ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-155MS` (url=349ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-205MS` (url=373ms, status=HTTP 204)
24. `AKUN-024-UNKNOWN-VLESS-WS-154MS` (url=363ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-171MS` (url=364ms, status=HTTP 204)
26. `AKUN-026-CHATGPT-VLESS-WS-219MS` (url=388ms, status=HTTP 204)
27. `AKUN-027-UNKNOWN-VLESS-WS-137MS` (url=381ms, status=HTTP 204)
28. `AKUN-028-UNKNOWN-VLESS-WS-189MS` (url=360ms, status=HTTP 204)
29. `AKUN-029-UNKNOWN-VLESS-WS-210MS` (url=384ms, status=HTTP 204)
30. `AKUN-030-UNKNOWN-VLESS-WS-155MS` (url=372ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
