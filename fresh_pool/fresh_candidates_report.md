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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-104MS` (url=343ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-98MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-105MS`
6. `AKUN-006-BY-SPRINTHOST-4-VLESS-WS-107MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-114MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-105MS`
9. `AKUN-009-7ZZ-VLESS-WS-113MS`
10. `AKUN-010-MEDIUM-VLESS-WS-118MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-116MS` (url=331ms, status=HTTP 204)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-114MS` (url=339ms, status=HTTP 204)
13. `AKUN-016-RS-RAPIDSEEDBOX-20190717-VLESS-WS-128MS` (url=364ms, status=HTTP 204)
14. `AKUN-017-RESERVED-FOR-TW-VLESS-WS-106MS` (url=327ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-132MS` (url=360ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-124MS` (url=353ms, status=HTTP 204)
17. `AKUN-020-BIGCOMMERCE-VLESS-WS-122MS` (url=375ms, status=HTTP 204)
18. `AKUN-021-CLOUDFLARE-VLESS-WS-103MS` (url=331ms, status=HTTP 204)
19. `AKUN-022-CLOUDFLARE-VLESS-WS-119MS` (url=371ms, status=HTTP 204)
20. `AKUN-023-CLOUDFLARE-VLESS-WS-111MS` (url=347ms, status=HTTP 204)
21. `AKUN-024-CLOUDFLARE-VLESS-WS-116MS` (url=340ms, status=HTTP 204)
22. `AKUN-025-UNKNOWN-VLESS-WS-152MS` (url=369ms, status=HTTP 204)
23. `AKUN-028-CLOUDFLARE-VLESS-WS-181MS` (url=2250ms, status=HTTP 204)
24. `AKUN-029-UNKNOWN-VLESS-WS-347MS` (url=1029ms, status=HTTP 204)
25. `AKUN-030-CLOUDFLARE-VLESS-WS-130MS` (url=372ms, status=HTTP 204)
26. `AKUN-031-PAGM-NET-VLESS-WS-515MS` (url=1278ms, status=HTTP 204)
27. `AKUN-033-UNKNOWN-VLESS-WS-659MS` (url=2524ms, status=HTTP 204)
28. `AKUN-036-UNKNOWN-VLESS-WS-794MS` (url=1143ms, status=HTTP 204)
29. `AKUN-037-CLOUDFLARE-VLESS-WS-734MS` (url=2336ms, status=HTTP 204)
30. `AKUN-039-DEV-VLESS-WS-115MS` (url=1141ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
