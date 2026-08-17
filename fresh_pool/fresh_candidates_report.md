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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-100MS` (url=1345ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-117MS` (url=327ms, status=HTTP 204)
3. `AKUN-003-ZVC-VLESS-WS-115MS` (url=332ms, status=HTTP 204)
4. `AKUN-004-SC-APHRODITEGROUP-201910-VLESS-WS-118MS` (url=351ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-96MS` (url=1327ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-98MS` (url=344ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-106MS` (url=1348ms, status=HTTP 204)
8. `AKUN-008-NOTION-WEB-VLESS-WS-124MS` (url=326ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-91MS` (url=340ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-116MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-108MS` (url=1322ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-115MS` (url=1326ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-102MS` (url=1334ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-102MS` (url=339ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-148MS` (url=327ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-96MS` (url=320ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-99MS` (url=325ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-111MS` (url=346ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-132MS` (url=333ms, status=HTTP 204)
20. `AKUN-021-NETCUP-VLESS-WS-104MS` (url=357ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-127MS` (url=327ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-126MS` (url=354ms, status=HTTP 204)
23. `AKUN-024-CLOUDFLARE-VLESS-WS-106MS` (url=346ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-108MS` (url=334ms, status=HTTP 204)
25. `AKUN-026-CLOUDFLARE-VLESS-WS-124MS` (url=304ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-153MS` (url=1308ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-101MS` (url=331ms, status=HTTP 204)
28. `AKUN-029-VEESP-VLESS-WS-200MS` (url=360ms, status=HTTP 204)
29. `AKUN-030-CLOUDFLARE-VLESS-WS-308MS` (url=617ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-469MS` (url=1818ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
