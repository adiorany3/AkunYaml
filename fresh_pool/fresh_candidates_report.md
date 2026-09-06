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
- Kandidat strict NekoBox-tested: 8
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-100MS` (url=381ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-102MS` (url=359ms, status=HTTP 204)
3. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-110MS` (url=357ms, status=HTTP 204)
5. `AKUN-006-CLOUDFLARE-VLESS-WS-107MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-109MS` (url=374ms, status=HTTP 204)
7. `AKUN-007-DEV-VLESS-WS-110MS` (url=357ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-110MS` (url=353ms, nekobox=6176ms, status=no)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-112MS` (url=377ms, status=HTTP 204)
10. `AKUN-004-UNKNOWN-VLESS-WS-117MS`
11. `AKUN-011-MEDIUM-VLESS-WS-111MS` (url=360ms, status=HTTP 204)
12. `AKUN-012-COM-VLESS-WS-111MS` (url=1389ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-117MS` (url=390ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-118MS` (url=719ms, status=HTTP 204)
15. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-119MS` (url=356ms, status=HTTP 204)
16. `AKUN-008-DIGITALOCEAN-VLESS-WS-114MS`
17. `AKUN-018-CLOUDFLARE-VLESS-WS-111MS` (url=368ms, status=HTTP 204)
18. `AKUN-019-RS-RAPIDSEEDBOX-20190717-VLESS-WS-122MS` (url=368ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-130MS` (url=337ms, nekobox=6188ms, status=no)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-107MS` (url=1012ms, status=HTTP 204)
21. `AKUN-003-CLOUDFLARE-VLESS-WS-126MS`
22. `AKUN-005-CLOUDFLARE-VLESS-WS-110MS`
23. `AKUN-001-CLOUDFLARE-VLESS-WS-112MS`
24. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS`
25. `AKUN-027-CLOUDFLARE-VLESS-WS-143MS` (url=399ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-122MS` (url=1350ms, status=HTTP 204)
27. `AKUN-029-CLOUDINARY-VLESS-WS-117MS` (url=369ms, status=HTTP 204)
28. `AKUN-030-UNKNOWN-VLESS-WS-139MS` (url=390ms, status=HTTP 204)
29. `AKUN-031-BIGCOMMERCE-VLESS-WS-114MS` (url=1399ms, status=HTTP 204)
30. `AKUN-033-NOTION-WEB-VLESS-WS-120MS` (url=355ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
