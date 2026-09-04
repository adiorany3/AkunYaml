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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-30MS` (url=305ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-29MS` (url=298ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-67MS` (url=286ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-65MS` (url=299ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-66MS` (url=282ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-68MS` (url=279ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-68MS` (url=274ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-63MS` (url=293ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-66MS` (url=278ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-70MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-70MS` (url=365ms, status=HTTP 204)
12. `AKUN-014-DEV-VLESS-WS-69MS` (url=379ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-67MS` (url=278ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-68MS` (url=946ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-65MS` (url=276ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-66MS` (url=294ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-71MS` (url=278ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-74MS` (url=870ms, status=HTTP 204)
19. `AKUN-021-CLOUDFLARE-VLESS-WS-65MS` (url=302ms, status=HTTP 204)
20. `AKUN-022-UNKNOWN-VLESS-WS-68MS` (url=1104ms, status=HTTP 204)
21. `AKUN-023-DEV-VLESS-WS-68MS` (url=472ms, status=HTTP 204)
22. `AKUN-024-CLOUDFLARE-VLESS-WS-73MS` (url=682ms, status=HTTP 204)
23. `AKUN-025-CLOUDFLARE-VLESS-WS-68MS` (url=300ms, status=HTTP 204)
24. `AKUN-026-CHATGPT-VLESS-WS-70MS` (url=301ms, status=HTTP 204)
25. `AKUN-028-BIGCOMMERCE-VLESS-WS-67MS` (url=281ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-70MS` (url=304ms, status=HTTP 204)
27. `AKUN-030-UNKNOWN-VLESS-WS-33MS` (url=319ms, status=HTTP 204)
28. `AKUN-031-NOTION-WEB-VLESS-WS-65MS` (url=278ms, status=HTTP 204)
29. `AKUN-032-CLOUDFLARE-VLESS-WS-72MS` (url=275ms, status=HTTP 204)
30. `AKUN-033-CLOUDFLARE-VLESS-WS-74MS` (url=310ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
