# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 25
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 29

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
1. `AKUN-001-NOTION-WEB-VLESS-WS-333MS` (url=575ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-260MS` (url=705ms, status=HTTP 204)
3. `AKUN-003-PAGM-NET-VLESS-WS-735MS` (url=1550ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-547MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-341MS`
6. `AKUN-006-DEV-VLESS-WS-328MS`
7. `AKUN-007-NETCRAFTERS-VLESS-WS-789MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-337MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-424MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-365MS`
11. `AKUN-023-DEV-VLESS-WS-367MS` (url=634ms, status=HTTP 204)
12. `AKUN-025-CLOUDFLARE-VLESS-WS-375MS` (url=631ms, status=HTTP 204)
13. `AKUN-026-INTERLIR-CUSTOMER-VLESS-WS-1059MS` (url=1869ms, status=HTTP 204)
14. `AKUN-028-UNKNOWN-VLESS-WS-1060MS` (url=1993ms, status=HTTP 204)
15. `AKUN-029-CLOUDFLARE-VLESS-WS-354MS` (url=1034ms, status=HTTP 204)
16. `AKUN-032-CLOUDFLARE-VLESS-WS-324MS` (url=594ms, status=HTTP 204)
17. `AKUN-033-CLOUDFLARE-VLESS-WS-348MS` (url=661ms, status=HTTP 204)
18. `AKUN-034-DEV-VLESS-WS-342MS` (url=609ms, status=HTTP 204)
19. `AKUN-035-JIKECLOUD-VLESS-WS-415MS` (url=837ms, status=HTTP 204)
20. `AKUN-038-090227-VLESS-WS-1230MS` (url=1894ms, status=HTTP 204)
21. `AKUN-039-CLOUDFLARE-VLESS-WS-1554MS` (url=6108ms, status=HTTP 204)
22. `AKUN-040-CLOUDFLARE-VLESS-WS-1118MS` (url=3658ms, status=HTTP 204)
23. `AKUN-041-UNKNOWN-VLESS-WS-1736MS` (url=2560ms, status=HTTP 204)
24. `AKUN-043-CLOUDFLARE-VLESS-WS-1479MS` (url=1816ms, status=HTTP 204)
25. `AKUN-044-UNKNOWN-VLESS-WS-533MS` (url=752ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
