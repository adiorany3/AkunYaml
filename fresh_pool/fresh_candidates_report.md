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
1. `AKUN-001-RUSSIA-VLESS-WS-108MS` (url=378ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-104MS` (url=343ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-107MS` (url=336ms, status=HTTP 204)
4. `AKUN-004-TIME-VLESS-WS-107MS` (url=325ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-112MS` (url=358ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-108MS` (url=346ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-102MS` (url=357ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-104MS` (url=353ms, status=HTTP 204)
9. `AKUN-009-UNKNOWN-VLESS-WS-116MS` (url=329ms, status=HTTP 204)
10. `AKUN-010-UNKNOWN-VLESS-WS-99MS` (url=361ms, status=HTTP 204)
11. `AKUN-011-UNKNOWN-VLESS-WS-104MS` (url=348ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-114MS` (url=356ms, status=HTTP 204)
13. `AKUN-013-TIME-VLESS-WS-122MS` (url=343ms, status=HTTP 204)
14. `AKUN-014-NOTION-WEB-VLESS-WS-108MS` (url=342ms, status=HTTP 204)
15. `AKUN-015-SPEEDTEST-VLESS-WS-117MS` (url=372ms, status=HTTP 204)
16. `AKUN-016-DE5-VLESS-WS-118MS` (url=369ms, status=HTTP 204)
17. `AKUN-017-DE5-VLESS-WS-120MS` (url=374ms, status=HTTP 204)
18. `AKUN-018-UNKNOWN-VLESS-WS-103MS` (url=372ms, status=HTTP 204)
19. `AKUN-019-UNKNOWN-VLESS-WS-116MS` (url=362ms, status=HTTP 204)
20. `AKUN-020-ZVC-VLESS-WS-118MS` (url=362ms, status=HTTP 204)
21. `AKUN-021-DIGITALOCEAN-VLESS-WS-122MS` (url=416ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-109MS` (url=334ms, status=HTTP 204)
23. `AKUN-025-UNKNOWN-VLESS-WS-110MS` (url=345ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-121MS` (url=1365ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-113MS` (url=334ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-120MS` (url=344ms, status=HTTP 204)
27. `AKUN-029-DE5-VLESS-WS-119MS` (url=367ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-122MS` (url=367ms, status=HTTP 204)
29. `AKUN-031-CLOUDFLARE-VLESS-WS-104MS` (url=353ms, status=HTTP 204)
30. `AKUN-032-CCWU-VLESS-WS-118MS` (url=345ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
