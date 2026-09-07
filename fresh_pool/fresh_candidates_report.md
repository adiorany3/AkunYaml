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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-45MS` (url=320ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-55MS` (url=298ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-65MS` (url=292ms, status=HTTP 204)
4. `AKUN-001-CLOUDFLARE-VLESS-WS-49MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-54MS` (url=279ms, nekobox=312ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-63MS` (url=927ms, status=HTTP 204)
7. `AKUN-008-CLOUDFLARE-VLESS-WS-69MS`
8. `AKUN-006-CLOUDFLARE-VLESS-WS-67MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-68MS` (url=874ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-73MS` (url=304ms, status=HTTP 204)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-67MS` (url=306ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-73MS` (url=291ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-75MS` (url=307ms, status=HTTP 204)
14. `AKUN-003-CLOUDFLARE-VLESS-WS-71MS`
15. `AKUN-016-UNKNOWN-VLESS-WS-68MS` (url=845ms, status=HTTP 204)
16. `AKUN-017-DEV-VLESS-WS-69MS` (url=497ms, status=HTTP 204)
17. `AKUN-004-CLOUDFLARE-VLESS-WS-59MS`
18. `AKUN-020-CLOUDINARY-VLESS-WS-71MS` (url=307ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-73MS` (url=666ms, status=HTTP 204)
20. `AKUN-023-CLOUDFLARE-VLESS-WS-67MS` (url=315ms, status=HTTP 204)
21. `AKUN-024-MEDIUM-VLESS-WS-73MS` (url=314ms, status=HTTP 204)
22. `AKUN-007-UNKNOWN-VLESS-WS-53MS`
23. `AKUN-026-NOTION-WEB-VLESS-WS-59MS` (url=259ms, nekobox=6177ms, status=no)
24. `AKUN-002-CLOUDFLARE-VLESS-WS-77MS`
25. `AKUN-028-CLOUDFLARE-VLESS-WS-72MS` (url=851ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-68MS` (url=2276ms, status=HTTP 204)
27. `AKUN-009-CLOUDFLARE-VLESS-WS-73MS`
28. `AKUN-031-RS-RAPIDSEEDBOX-20190717-VLESS-WS-76MS` (url=300ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-77MS` (url=310ms, status=HTTP 204)
30. `AKUN-034-CLOUDFLARE-VLESS-WS-72MS` (url=306ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
