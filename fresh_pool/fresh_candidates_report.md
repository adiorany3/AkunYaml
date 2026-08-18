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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-94MS` (url=331ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-103MS` (url=325ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-88MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-103MS` (url=319ms, status=HTTP 204)
5. `AKUN-005-EU-VLESS-WS-105MS` (url=335ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-104MS` (url=332ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-107MS` (url=1338ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-106MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-128MS` (url=1323ms, status=HTTP 204)
11. `AKUN-012-UNKNOWN-VLESS-WS-96MS` (url=328ms, status=HTTP 204)
12. `AKUN-013-UNKNOWN-VLESS-WS-103MS` (url=298ms, status=HTTP 204)
13. `AKUN-014-UNKNOWN-VLESS-WS-96MS` (url=301ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-105MS` (url=322ms, status=HTTP 204)
15. `AKUN-016-UNKNOWN-VLESS-WS-104MS` (url=324ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-88MS` (url=317ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-111MS` (url=328ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-112MS` (url=324ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-87MS` (url=327ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-91MS` (url=320ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-97MS` (url=324ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-97MS` (url=303ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-132MS` (url=306ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-133MS` (url=291ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-91MS` (url=1337ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-103MS` (url=304ms, status=HTTP 204)
27. `AKUN-028-EU-VLESS-WS-107MS` (url=321ms, status=HTTP 204)
28. `AKUN-029-CHATGPT-VLESS-WS-118MS` (url=330ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-115MS` (url=325ms, status=HTTP 204)
30. `AKUN-031-UNKNOWN-VLESS-WS-113MS` (url=332ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
