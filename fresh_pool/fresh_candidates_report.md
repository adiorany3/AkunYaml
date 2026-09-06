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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-102MS` (url=360ms, nekobox=6202ms, status=no)
2. `AKUN-002-SPEEDTEST-VLESS-WS-110MS` (url=363ms, status=HTTP 204)
3. `AKUN-007-CLOUDFLARE-VLESS-WS-96MS`
4. `AKUN-004-BIGCOMMERCE-VLESS-WS-106MS` (url=360ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-104MS` (url=367ms, status=HTTP 204)
6. `AKUN-005-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-107MS` (url=1000ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-112MS` (url=370ms, status=HTTP 204)
9. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-108MS` (url=337ms, nekobox=274ms, status=no)
11. `AKUN-011-COM-VLESS-WS-111MS` (url=1381ms, status=HTTP 204)
12. `AKUN-012-NOTION-WEB-VLESS-WS-115MS` (url=368ms, status=HTTP 204)
13. `AKUN-013-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=370ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-115MS` (url=381ms, status=HTTP 204)
15. `AKUN-002-CLOUDFLARE-VLESS-WS-114MS`
16. `AKUN-017-CLOUDFLARE-VLESS-WS-120MS` (url=678ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-105MS` (url=370ms, status=HTTP 204)
18. `AKUN-001-MEDIUM-VLESS-WS-113MS`
19. `AKUN-003-CLOUDFLARE-VLESS-WS-141MS`
20. `AKUN-021-UNKNOWN-VLESS-WS-134MS` (url=371ms, status=HTTP 204)
21. `AKUN-006-CLOUDFLARE-VLESS-WS-116MS`
22. `AKUN-024-CLOUDINARY-VLESS-WS-129MS` (url=383ms, status=HTTP 204)
23. `AKUN-008-090227-VLESS-WS-122MS`
24. `AKUN-026-CLOUDFLARE-VLESS-WS-143MS` (url=420ms, status=HTTP 204)
25. `AKUN-027-DIGITALOCEAN-VLESS-WS-113MS` (url=398ms, status=HTTP 204)
26. `AKUN-028-CLOUDFLARE-VLESS-WS-115MS` (url=461ms, status=HTTP 204)
27. `AKUN-029-CLOUDFLARE-VLESS-WS-383MS` (url=809ms, status=HTTP 204)
28. `AKUN-030-CLOUDFLARE-VLESS-WS-120MS` (url=1059ms, status=HTTP 204)
29. `AKUN-031-UNKNOWN-VLESS-WS-123MS` (url=741ms, status=HTTP 204)
30. `AKUN-036-UNKNOWN-VLESS-WS-875MS` (url=1665ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
