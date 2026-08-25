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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-99MS` (url=341ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-102MS` (url=547ms, status=HTTP 204)
3. `AKUN-003-EU-VLESS-WS-103MS` (url=684ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-113MS` (url=565ms, status=HTTP 204)
5. `AKUN-005-MEDIUM-VLESS-WS-109MS` (url=319ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-114MS` (url=636ms, status=HTTP 204)
7. `AKUN-007-RUSSIA-VLESS-WS-118MS` (url=540ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-105MS` (url=578ms, status=HTTP 204)
9. `AKUN-009-NOTION-WEB-VLESS-WS-117MS`
10. `AKUN-010-SPEEDTEST-VLESS-WS-116MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-103MS` (url=670ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-111MS` (url=546ms, status=HTTP 204)
13. `AKUN-014-RS-RAPIDSEEDBOX-20190717-VLESS-WS-111MS` (url=654ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-105MS` (url=341ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-114MS` (url=391ms, status=HTTP 204)
16. `AKUN-017-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-121MS` (url=568ms, status=HTTP 204)
17. `AKUN-018-DE5-VLESS-WS-122MS` (url=391ms, status=HTTP 204)
18. `AKUN-019-SPEEDTEST-VLESS-WS-109MS` (url=666ms, status=HTTP 204)
19. `AKUN-021-MYBB-VLESS-WS-104MS` (url=349ms, status=HTTP 204)
20. `AKUN-022-UNKNOWN-VLESS-WS-115MS` (url=333ms, status=HTTP 204)
21. `AKUN-023-EU-VLESS-WS-103MS` (url=561ms, status=HTTP 204)
22. `AKUN-025-CLOUDFLARE-VLESS-WS-115MS` (url=348ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-114MS` (url=547ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-115MS` (url=564ms, status=HTTP 204)
25. `AKUN-028-UNKNOWN-VLESS-WS-117MS` (url=549ms, status=HTTP 204)
26. `AKUN-029-DEV-VLESS-WS-125MS` (url=557ms, status=HTTP 204)
27. `AKUN-030-CLOUDFLARE-VLESS-WS-117MS` (url=638ms, status=HTTP 204)
28. `AKUN-031-DEV-VLESS-WS-134MS` (url=543ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-124MS` (url=338ms, status=HTTP 204)
30. `AKUN-033-UNKNOWN-VLESS-WS-119MS` (url=351ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
