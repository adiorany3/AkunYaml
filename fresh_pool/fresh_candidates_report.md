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
- Kandidat strict NekoBox-tested: 20
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-29MS` (url=281ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-66MS` (url=297ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-65MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-67MS`
5. `AKUN-005-DEV-VLESS-WS-66MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-67MS` (url=384ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-67MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-67MS` (url=283ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-69MS`
10. `AKUN-010-BIGCOMMERCE-VLESS-WS-26MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-68MS`
12. `AKUN-012-CLOUDFLARE-VLESS-WS-69MS`
13. `AKUN-013-CHATGPT-VLESS-WS-72MS`
14. `AKUN-014-CLOUDFLARE-VLESS-WS-38MS`
15. `AKUN-015-CLOUDFLARE-VLESS-WS-65MS`
16. `AKUN-016-CLOUDFLARE-VLESS-WS-68MS`
17. `AKUN-017-UNKNOWN-VLESS-WS-70MS`
18. `AKUN-018-CLOUDFLARE-VLESS-WS-64MS`
19. `AKUN-019-CLOUDFLARE-VLESS-WS-66MS`
20. `AKUN-020-CLOUDFLARE-VLESS-WS-69MS`
21. `AKUN-023-UNKNOWN-VLESS-WS-71MS` (url=884ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-40MS` (url=946ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-65MS` (url=274ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-68MS` (url=295ms, status=HTTP 204)
25. `AKUN-028-CLOUDFLARE-VLESS-WS-70MS` (url=300ms, status=HTTP 204)
26. `AKUN-029-DEV-VLESS-WS-73MS` (url=487ms, status=HTTP 204)
27. `AKUN-030-RS-RAPIDSEEDBOX-20190717-VLESS-WS-68MS` (url=271ms, status=HTTP 204)
28. `AKUN-031-CLOUDFLARE-VLESS-WS-69MS` (url=278ms, status=HTTP 204)
29. `AKUN-032-7ZZ-VLESS-WS-76MS` (url=783ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-73MS` (url=300ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
