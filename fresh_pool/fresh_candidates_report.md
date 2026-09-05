# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 27
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 30

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-102MS` (url=335ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-103MS` (url=329ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-103MS` (url=319ms, status=HTTP 204)
4. `AKUN-004-CHATGPT-VLESS-WS-120MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-106MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-106MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-110MS`
8. `AKUN-008-BIGCOMMERCE-VLESS-WS-114MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-120MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-123MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-129MS` (url=367ms, status=HTTP 204)
12. `AKUN-016-CHATGPT-VLESS-WS-104MS` (url=358ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-128MS` (url=340ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-103MS` (url=361ms, status=HTTP 204)
15. `AKUN-019-NOTION-WEB-VLESS-WS-111MS` (url=352ms, status=HTTP 204)
16. `AKUN-020-CLOUDFLARE-VLESS-WS-120MS` (url=735ms, status=HTTP 204)
17. `AKUN-021-CLOUDFLARE-VLESS-WS-118MS` (url=390ms, status=HTTP 204)
18. `AKUN-022-CLOUDFLARE-VLESS-WS-109MS` (url=1369ms, status=HTTP 204)
19. `AKUN-024-CLOUDFLARE-VLESS-WS-132MS` (url=382ms, status=HTTP 204)
20. `AKUN-025-CLOUDFLARE-VLESS-WS-116MS` (url=348ms, status=HTTP 204)
21. `AKUN-026-UNKNOWN-VLESS-WS-343MS` (url=1270ms, status=HTTP 204)
22. `AKUN-028-CLOUDFLARE-VLESS-WS-108MS` (url=978ms, status=HTTP 204)
23. `AKUN-029-CLOUDFLARE-VLESS-WS-157MS` (url=1020ms, status=HTTP 204)
24. `AKUN-036-CLOUDFLARE-VLESS-WS-868MS` (url=1432ms, status=HTTP 204)
25. `AKUN-051-CLOUDFLARE-VLESS-WS-117MS` (url=1363ms, status=HTTP 204)
26. `AKUN-053-CLOUDFLARE-VLESS-WS-668MS` (url=1969ms, status=HTTP 204)
27. `AKUN-054-CLOUDFLARE-VLESS-WS-1122MS` (url=369ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
