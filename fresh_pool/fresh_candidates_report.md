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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-110MS` (url=361ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS` (url=359ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-102MS` (url=328ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-109MS` (url=335ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-104MS` (url=365ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-119MS` (url=347ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-121MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-119MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-101MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-97MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-112MS` (url=322ms, status=HTTP 204)
12. `AKUN-016-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-106MS` (url=375ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-114MS` (url=318ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-117MS` (url=367ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-110MS` (url=347ms, status=HTTP 204)
16. `AKUN-020-CLOUDFLARE-VLESS-WS-114MS` (url=380ms, status=HTTP 204)
17. `AKUN-021-CLOUDFLARE-VLESS-WS-119MS` (url=339ms, status=HTTP 204)
18. `AKUN-022-NOTION-WEB-VLESS-WS-120MS` (url=366ms, status=HTTP 204)
19. `AKUN-023-CLOUDFLARE-VLESS-WS-117MS` (url=1711ms, status=HTTP 204)
20. `AKUN-024-CLOUDFLARE-VLESS-WS-122MS` (url=371ms, status=HTTP 204)
21. `AKUN-025-CLOUDFLARE-VLESS-WS-110MS` (url=381ms, status=HTTP 204)
22. `AKUN-026-CLOUDFLARE-VLESS-WS-116MS` (url=365ms, status=HTTP 204)
23. `AKUN-027-CLOUDFLARE-VLESS-WS-126MS` (url=336ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-128MS` (url=353ms, status=HTTP 204)
25. `AKUN-029-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-103MS` (url=1692ms, status=HTTP 204)
26. `AKUN-030-CLOUDFLARE-VLESS-WS-127MS` (url=351ms, status=HTTP 204)
27. `AKUN-031-CLOUDFLARE-VLESS-WS-112MS` (url=357ms, status=HTTP 204)
28. `AKUN-032-CLOUDFLARE-VLESS-WS-117MS` (url=327ms, status=HTTP 204)
29. `AKUN-034-CLOUDFLARE-VLESS-WS-319MS` (url=1271ms, status=HTTP 204)
30. `AKUN-035-CLOUDFLARE-VLESS-WS-411MS` (url=2988ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
