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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-110MS` (url=974ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS` (url=310ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-115MS` (url=323ms, status=HTTP 204)
4. `AKUN-004-SC-APHRODITEGROUP-201910-VLESS-WS-122MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-123MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-104MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS`
8. `AKUN-008-DIGITALOCEAN-VLESS-WS-110MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-119MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-129MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-132MS` (url=364ms, status=HTTP 204)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-124MS` (url=324ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-113MS` (url=337ms, status=HTTP 204)
14. `AKUN-016-GF-RO-BUC-VLESS-WS-116MS` (url=387ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-104MS` (url=341ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-130MS` (url=330ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-133MS` (url=357ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-113MS` (url=1093ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-118MS` (url=339ms, status=HTTP 204)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-142MS` (url=308ms, status=HTTP 204)
21. `AKUN-024-AKAMAI-VLESS-WS-176MS` (url=376ms, status=HTTP 204)
22. `AKUN-025-AKAMAI-VLESS-WS-179MS` (url=318ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-122MS` (url=504ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-257MS` (url=734ms, status=HTTP 204)
25. `AKUN-029-CLOUDFLARE-VLESS-WS-504MS` (url=1130ms, status=HTTP 204)
26. `AKUN-033-GCS-SER-NET-VLESS-WS-434MS` (url=1795ms, status=HTTP 204)
27. `AKUN-035-CLOUDFLARE-VLESS-WS-805MS` (url=1318ms, status=HTTP 204)
28. `AKUN-038-CLOUDFLARE-VLESS-WS-814MS` (url=1317ms, status=HTTP 204)
29. `AKUN-043-CLOUDFLARE-VLESS-WS-854MS` (url=1501ms, status=HTTP 204)
30. `AKUN-044-CLOUDFLARE-VLESS-WS-871MS` (url=1788ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
