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
- Proxy di openclash_fresh_pool.yaml: 33

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-99MS` (url=368ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=366ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-104MS` (url=313ms, nekobox=435ms, status=no)
4. `AKUN-002-CLOUDFLARE-VLESS-WS-101MS`
5. `AKUN-005-NOTION-WEB-VLESS-WS-115MS` (url=390ms, status=HTTP 204)
6. `AKUN-007-CLOUDFLARE-VLESS-WS-108MS` (url=374ms, status=HTTP 204)
7. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS` (url=383ms, status=HTTP 204)
8. `AKUN-010-CLOUDFLARE-VLESS-WS-107MS` (url=379ms, status=HTTP 204)
9. `AKUN-011-CLOUDFLARE-VLESS-WS-116MS` (url=370ms, status=HTTP 204)
10. `AKUN-012-ALIBABA-VLESS-WS-118MS` (url=378ms, status=HTTP 204)
11. `AKUN-014-CLOUDFLARE-VLESS-WS-119MS` (url=1539ms, status=HTTP 204)
12. `AKUN-003-CLOUDFLARE-VLESS-WS-122MS`
13. `AKUN-017-CLOUDFLARE-VLESS-WS-114MS` (url=350ms, nekobox=1272ms, status=no)
14. `AKUN-019-CLOUDFLARE-VLESS-WS-118MS` (url=361ms, status=HTTP 204)
15. `AKUN-020-UNKNOWN-VLESS-WS-114MS` (url=348ms, nekobox=6181ms, status=no)
16. `AKUN-021-UNKNOWN-VLESS-WS-118MS` (url=329ms, nekobox=269ms, status=no)
17. `AKUN-001-CLOUDFLARE-VLESS-WS-104MS`
18. `AKUN-023-CLOUDFLARE-VLESS-WS-107MS` (url=390ms, status=HTTP 204)
19. `AKUN-024-CLOUDFLARE-VLESS-WS-107MS` (url=369ms, status=HTTP 204)
20. `AKUN-025-BIGCOMMERCE-VLESS-WS-110MS` (url=359ms, status=HTTP 204)
21. `AKUN-026-DEV-VLESS-WS-111MS` (url=330ms, nekobox=269ms, status=no)
22. `AKUN-027-UNKNOWN-VLESS-WS-126MS` (url=356ms, status=HTTP 204)
23. `AKUN-028-CLOUDFLARE-VLESS-WS-120MS` (url=363ms, status=HTTP 204)
24. `AKUN-029-CLOUDFLARE-VLESS-WS-135MS` (url=399ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-114MS` (url=1826ms, status=HTTP 204)
26. `AKUN-033-CLOUDFLARE-VLESS-WS-124MS` (url=1921ms, status=HTTP 204)
27. `AKUN-005-CLOUDFLARE-VLESS-WS-106MS`
28. `AKUN-041-CLOUDFLARE-VLESS-WS-120MS` (url=360ms, status=HTTP 204)
29. `AKUN-042-UNKNOWN-VLESS-WS-114MS` (url=358ms, status=HTTP 204)
30. `AKUN-004-UNKNOWN-VLESS-WS-159MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
