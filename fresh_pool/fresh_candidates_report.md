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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-109MS` (url=343ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-101MS` (url=369ms, status=HTTP 204)
3. `AKUN-003-BIGCOMMERCE-VLESS-WS-112MS` (url=342ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-111MS` (url=374ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-112MS` (url=373ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-113MS` (url=353ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS` (url=364ms, status=HTTP 204)
8. `AKUN-008-EE-WELCOMEHOST-20190515-VLESS-WS-112MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-116MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-116MS` (url=339ms, status=HTTP 204)
11. `AKUN-013-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=370ms, status=HTTP 204)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-120MS` (url=367ms, status=HTTP 204)
13. `AKUN-015-UNKNOWN-VLESS-WS-115MS` (url=377ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-115MS` (url=372ms, status=HTTP 204)
15. `AKUN-017-UNKNOWN-VLESS-WS-109MS` (url=362ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-98MS` (url=351ms, status=HTTP 204)
17. `AKUN-020-CLOUDFLARE-VLESS-WS-109MS` (url=324ms, status=HTTP 204)
18. `AKUN-021-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=372ms, status=HTTP 204)
19. `AKUN-023-CLOUDFLARE-VLESS-WS-118MS` (url=378ms, status=HTTP 204)
20. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-124MS` (url=334ms, status=HTTP 204)
21. `AKUN-025-CLOUDFLARE-VLESS-WS-119MS` (url=1694ms, status=HTTP 204)
22. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=358ms, status=HTTP 204)
23. `AKUN-027-CLOUDFLARE-VLESS-WS-119MS` (url=361ms, status=HTTP 204)
24. `AKUN-028-CLOUDFLARE-VLESS-WS-125MS` (url=364ms, status=HTTP 204)
25. `AKUN-030-UNKNOWN-VLESS-WS-121MS` (url=390ms, status=HTTP 204)
26. `AKUN-031-CLOUDFLARE-VLESS-WS-122MS` (url=513ms, status=HTTP 204)
27. `AKUN-032-CLOUDFLARE-VLESS-WS-115MS` (url=1375ms, status=HTTP 204)
28. `AKUN-034-UNKNOWN-VLESS-WS-122MS` (url=978ms, status=HTTP 204)
29. `AKUN-038-UNKNOWN-VLESS-WS-374MS` (url=1192ms, status=HTTP 204)
30. `AKUN-041-UNKNOWN-VLESS-WS-820MS` (url=1879ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
