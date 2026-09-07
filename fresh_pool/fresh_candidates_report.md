# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 23
- Kandidat strict NekoBox-tested: 5
- Proxy di openclash_fresh_pool.yaml: 27

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-101MS` (url=365ms, nekobox=6179ms, status=no)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-101MS` (url=347ms, nekobox=6179ms, status=no)
3. `AKUN-003-GTHOST-VLESS-WS-110MS` (url=641ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-109MS` (url=363ms, nekobox=377ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-112MS` (url=396ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-114MS` (url=330ms, nekobox=431ms, status=no)
7. `AKUN-007-UNKNOWN-VLESS-WS-111MS` (url=396ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-111MS` (url=1572ms, status=HTTP 204)
9. `AKUN-010-DEV-VLESS-WS-114MS` (url=361ms, nekobox=282ms, status=no)
10. `AKUN-011-UNKNOWN-VLESS-WS-115MS` (url=370ms, status=HTTP 204)
11. `AKUN-002-CLOUDFLARE-VLESS-WS-126MS`
12. `AKUN-015-NOTION-WEB-VLESS-WS-115MS` (url=347ms, nekobox=6179ms, status=no)
13. `AKUN-016-ORG-VLESS-WS-115MS` (url=394ms, status=HTTP 204)
14. `AKUN-017-CLOUDFLARE-VLESS-WS-285MS` (url=1296ms, status=HTTP 204)
15. `AKUN-019-UNKNOWN-VLESS-WS-376MS` (url=997ms, status=HTTP 204)
16. `AKUN-020-CLOUDFLARE-VLESS-WS-128MS` (url=776ms, status=HTTP 204)
17. `AKUN-005-CLOUDFLARE-VLESS-WS-114MS`
18. `AKUN-001-CLOUDFLARE-VLESS-WS-165MS`
19. `AKUN-032-CLOUDFLARE-VLESS-WS-105MS` (url=377ms, status=HTTP 204)
20. `AKUN-033-CLOUDFLARE-VLESS-WS-129MS` (url=1369ms, status=HTTP 204)
21. `AKUN-034-UNKNOWN-VLESS-WS-875MS` (url=2621ms, status=HTTP 204)
22. `AKUN-046-RTXCONFIGZ-VLESS-WS-1043MS` (url=5033ms, status=HTTP 204)
23. `AKUN-003-CLOUDFLARE-VLESS-WS-130MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
