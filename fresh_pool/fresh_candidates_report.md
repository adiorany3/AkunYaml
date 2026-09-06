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
- Kandidat strict NekoBox-tested: 5
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
1. `AKUN-005-CLOUDFLARE-VLESS-WS-96MS`
2. `AKUN-001-CLOUDFLARE-VLESS-WS-104MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-111MS` (url=346ms, nekobox=6182ms, status=no)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-105MS` (url=313ms, nekobox=445ms, status=no)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-108MS` (url=319ms, nekobox=270ms, status=no)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-111MS` (url=358ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-116MS` (url=360ms, status=HTTP 204)
8. `AKUN-008-CLOUDINARY-VLESS-WS-113MS` (url=379ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS` (url=368ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-101MS` (url=344ms, nekobox=288ms, status=no)
11. `AKUN-012-BIGCOMMERCE-VLESS-WS-112MS` (url=373ms, status=HTTP 204)
12. `AKUN-002-CLOUDFLARE-VLESS-WS-119MS`
13. `AKUN-003-CLOUDFLARE-VLESS-WS-121MS`
14. `AKUN-015-COM-VLESS-WS-118MS` (url=371ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-110MS` (url=378ms, status=HTTP 204)
16. `AKUN-017-CLOUDFLARE-VLESS-WS-131MS` (url=348ms, nekobox=433ms, status=no)
17. `AKUN-018-NOTION-WEB-VLESS-WS-104MS` (url=370ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-120MS` (url=370ms, status=HTTP 204)
19. `AKUN-020-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS` (url=356ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-115MS` (url=362ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-113MS` (url=360ms, status=HTTP 204)
22. `AKUN-023-CLOUDFLARE-VLESS-WS-111MS` (url=358ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-131MS` (url=373ms, status=HTTP 204)
24. `AKUN-026-CLOUDFLARE-VLESS-WS-126MS` (url=439ms, status=HTTP 204)
25. `AKUN-027-CLOUDFLARE-VLESS-WS-115MS` (url=440ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-118MS` (url=1109ms, status=HTTP 204)
27. `AKUN-030-UNKNOWN-VLESS-WS-124MS` (url=951ms, status=HTTP 204)
28. `AKUN-033-CLOUDFLARE-VLESS-WS-367MS` (url=1452ms, status=HTTP 204)
29. `AKUN-038-CLOUDFLARE-VLESS-WS-844MS` (url=1465ms, status=HTTP 204)
30. `AKUN-004-CLOUDFLARE-VLESS-WS-115MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
