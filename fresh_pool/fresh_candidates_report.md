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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-113MS` (url=371ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-117MS` (url=329ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-119MS` (url=357ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-114MS` (url=1362ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-115MS` (url=369ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-116MS` (url=358ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS` (url=1341ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-120MS` (url=1352ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-117MS` (url=336ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-122MS` (url=347ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-124MS` (url=350ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-122MS` (url=334ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-124MS` (url=339ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-116MS` (url=368ms, status=HTTP 204)
15. `AKUN-016-NOTION-WEB-VLESS-WS-117MS` (url=358ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-120MS` (url=1350ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-122MS` (url=325ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-128MS` (url=393ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-115MS` (url=1360ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-114MS` (url=368ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-115MS` (url=1388ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-128MS` (url=1387ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-145MS` (url=341ms, status=HTTP 204)
24. `AKUN-025-AMAZON-VLESS-WS-184MS` (url=378ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-121MS` (url=453ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-169MS` (url=484ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-589MS` (url=1341ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-659MS` (url=1194ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-129MS` (url=889ms, status=HTTP 204)
30. `AKUN-032-CLOUDFLARE-VLESS-WS-435MS` (url=1482ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
