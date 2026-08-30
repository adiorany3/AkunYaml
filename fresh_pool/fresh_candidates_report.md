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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-110MS` (url=368ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-111MS` (url=324ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-107MS` (url=340ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS` (url=345ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-105MS` (url=368ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-105MS` (url=360ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-110MS` (url=340ms, status=HTTP 204)
8. `AKUN-008-MEDIUM-VLESS-WS-116MS` (url=333ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-106MS` (url=394ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-109MS` (url=731ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-104MS` (url=369ms, status=HTTP 204)
12. `AKUN-012-UNKNOWN-VLESS-WS-118MS` (url=369ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-126MS` (url=359ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-117MS` (url=341ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-110MS` (url=349ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-116MS` (url=1368ms, status=HTTP 204)
17. `AKUN-021-CHATGPT-VLESS-WS-155MS` (url=360ms, status=HTTP 204)
18. `AKUN-022-CLOUDFLARE-VLESS-WS-122MS` (url=388ms, status=HTTP 204)
19. `AKUN-023-CLOUDFLARE-VLESS-WS-167MS` (url=370ms, status=HTTP 204)
20. `AKUN-024-CLOUDFLARE-VLESS-WS-341MS` (url=1661ms, status=HTTP 204)
21. `AKUN-025-PAGM-NET-VLESS-WS-510MS` (url=1426ms, status=HTTP 204)
22. `AKUN-026-PAGM-NET-VLESS-WS-547MS` (url=2272ms, status=HTTP 204)
23. `AKUN-027-NETCRAFTERS-VLESS-WS-480MS` (url=1000ms, status=HTTP 204)
24. `AKUN-033-UNKNOWN-VLESS-WS-804MS` (url=2140ms, status=HTTP 204)
25. `AKUN-034-DEV-VLESS-WS-126MS` (url=1146ms, status=HTTP 204)
26. `AKUN-038-UNKNOWN-VLESS-WS-394MS` (url=1754ms, status=HTTP 204)
27. `AKUN-039-CLOUDFLARE-VLESS-WS-114MS` (url=1377ms, status=HTTP 204)
28. `AKUN-040-CLOUDFLARE-VLESS-WS-105MS` (url=358ms, status=HTTP 204)
29. `AKUN-041-TYCHRON-02-VLESS-WS-108MS` (url=324ms, status=HTTP 204)
30. `AKUN-042-CLOUDFLARE-VLESS-WS-110MS` (url=359ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
