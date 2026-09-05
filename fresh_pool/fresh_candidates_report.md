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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-99MS` (url=355ms, status=HTTP 204)
2. `AKUN-002-CLOUDINARY-VLESS-WS-102MS` (url=377ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-102MS` (url=1354ms, status=HTTP 204)
4. `AKUN-004-CHATGPT-VLESS-WS-110MS` (url=368ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-107MS` (url=382ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-110MS` (url=372ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS` (url=385ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-115MS` (url=1012ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-115MS` (url=347ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-115MS` (url=381ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-95MS` (url=359ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-124MS` (url=1400ms, status=HTTP 204)
13. `AKUN-013-RS-RAPIDSEEDBOX-20190717-VLESS-WS-106MS` (url=379ms, status=HTTP 204)
14. `AKUN-014-DEV-VLESS-WS-109MS` (url=910ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-100MS` (url=367ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-106MS` (url=337ms, status=HTTP 204)
17. `AKUN-018-NOTION-WEB-VLESS-WS-103MS` (url=359ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-115MS` (url=347ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-114MS` (url=342ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-115MS` (url=1359ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-115MS` (url=1339ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-130MS` (url=461ms, status=HTTP 204)
23. `AKUN-025-UNKNOWN-VLESS-WS-125MS` (url=991ms, status=HTTP 204)
24. `AKUN-026-CHATGPT-VLESS-WS-118MS` (url=321ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-107MS` (url=345ms, status=HTTP 204)
26. `AKUN-028-DEV-VLESS-WS-117MS` (url=1903ms, status=HTTP 204)
27. `AKUN-029-UNKNOWN-VLESS-WS-365MS` (url=579ms, status=HTTP 204)
28. `AKUN-041-INTERLIR-CUSTOMER-VLESS-WS-855MS` (url=1637ms, status=HTTP 204)
29. `AKUN-042-CLOUDFLARE-VLESS-WS-114MS` (url=350ms, status=HTTP 204)
30. `AKUN-043-CLOUDFLARE-VLESS-WS-106MS` (url=382ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
