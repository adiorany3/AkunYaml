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
1. `AKUN-001-UNKNOWN-VLESS-WS-98MS` (url=345ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-95MS` (url=315ms, status=HTTP 204)
3. `AKUN-003-EU-VLESS-WS-105MS` (url=312ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-96MS` (url=341ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-102MS` (url=313ms, status=HTTP 204)
6. `AKUN-006-NOTION-WEB-VLESS-WS-112MS` (url=345ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS` (url=334ms, status=HTTP 204)
8. `AKUN-008-LEVIKOGJGFDD-VLESS-WS-105MS` (url=329ms, status=HTTP 204)
9. `AKUN-009-UNKNOWN-VLESS-WS-127MS` (url=325ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-142MS`
11. `AKUN-011-UNKNOWN-VLESS-WS-112MS` (url=338ms, status=HTTP 204)
12. `AKUN-012-UNKNOWN-VLESS-WS-101MS` (url=329ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-103MS` (url=320ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-109MS` (url=290ms, status=HTTP 204)
15. `AKUN-015-UNKNOWN-VLESS-WS-111MS` (url=325ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-115MS` (url=331ms, status=HTTP 204)
17. `AKUN-017-UNKNOWN-VLESS-WS-122MS` (url=321ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-139MS` (url=327ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-144MS` (url=332ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-145MS` (url=317ms, status=HTTP 204)
21. `AKUN-022-UNKNOWN-VLESS-WS-114MS` (url=312ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-111MS` (url=311ms, status=HTTP 204)
23. `AKUN-024-UNKNOWN-VLESS-WS-119MS` (url=1316ms, status=HTTP 204)
24. `AKUN-025-UNKNOWN-VLESS-WS-143MS` (url=320ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-136MS` (url=341ms, status=HTTP 204)
26. `AKUN-027-UNKNOWN-VLESS-WS-116MS` (url=324ms, status=HTTP 204)
27. `AKUN-028-UNKNOWN-VLESS-WS-110MS` (url=323ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-115MS` (url=1340ms, status=HTTP 204)
29. `AKUN-030-UNKNOWN-VLESS-WS-103MS` (url=331ms, status=HTTP 204)
30. `AKUN-031-UNKNOWN-VLESS-WS-121MS` (url=343ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
