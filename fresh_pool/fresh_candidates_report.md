# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 24
- Kandidat strict NekoBox-tested: 6
- Proxy di openclash_fresh_pool.yaml: 28

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS` (url=370ms, nekobox=6174ms, status=no)
2. `AKUN-003-BIGCOMMERCE-VLESS-WS-108MS` (url=352ms, nekobox=1431ms, status=yes)
3. `AKUN-004-CLOUDFLARE-VLESS-WS-102MS` (url=373ms, status=HTTP 204)
4. `AKUN-006-CLOUDFLARE-VLESS-WS-108MS` (url=372ms, status=HTTP 204)
5. `AKUN-007-CLOUDFLARE-VLESS-WS-117MS` (url=639ms, status=HTTP 204)
6. `AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-105MS`
7. `AKUN-009-CLOUDFLARE-VLESS-WS-112MS` (url=349ms, nekobox=264ms, status=no)
8. `AKUN-004-CHATGPT-VLESS-WS-106MS`
9. `AKUN-011-NOTION-WEB-VLESS-WS-106MS` (url=350ms, nekobox=6185ms, status=no)
10. `AKUN-002-MEDIUM-VLESS-WS-121MS`
11. `AKUN-005-CLOUDFLARE-VLESS-WS-111MS`
12. `AKUN-014-CLOUDINARY-VLESS-WS-123MS` (url=379ms, status=HTTP 204)
13. `AKUN-001-008500-VLESS-WS-114MS`
14. `AKUN-016-CLOUDFLARE-VLESS-WS-117MS` (url=439ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-122MS` (url=1999ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-395MS` (url=800ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-123MS` (url=1973ms, status=HTTP 204)
18. `AKUN-023-CLOUDFLARE-VLESS-WS-826MS` (url=1442ms, status=HTTP 204)
19. `AKUN-025-CLOUDFLARE-VLESS-WS-738MS` (url=4232ms, status=HTTP 204)
20. `AKUN-048-CLOUDFLARE-VLESS-WS-124MS` (url=322ms, nekobox=276ms, status=no)
21. `AKUN-049-ALIBABA-VLESS-WS-126MS` (url=1400ms, status=HTTP 204)
22. `AKUN-051-CLOUDFLARE-VLESS-WS-128MS` (url=377ms, status=HTTP 204)
23. `AKUN-054-PAI50288-VLESS-WS-1138MS` (url=3061ms, status=HTTP 204)
24. `AKUN-058-SOFT10-VLESS-WS-986MS` (url=3107ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
