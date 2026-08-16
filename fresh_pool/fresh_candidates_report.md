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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-106MS` (url=344ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-106MS` (url=326ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-113MS` (url=321ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-118MS` (url=314ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-113MS` (url=1693ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-121MS` (url=1345ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-119MS` (url=330ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-120MS` (url=304ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-119MS` (url=1330ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-112MS` (url=302ms, status=HTTP 204)
11. `AKUN-011-ZVC-VLESS-WS-102MS` (url=335ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-113MS` (url=337ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-119MS` (url=305ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-139MS` (url=326ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-104MS` (url=321ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-142MS` (url=340ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-112MS` (url=323ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-131MS` (url=337ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-120MS` (url=312ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-114MS` (url=318ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-114MS` (url=310ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-97MS` (url=324ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-152MS` (url=341ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-114MS` (url=319ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-151MS` (url=325ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-126MS` (url=327ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-123MS` (url=340ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-123MS` (url=353ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-147MS` (url=303ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-166MS` (url=310ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
