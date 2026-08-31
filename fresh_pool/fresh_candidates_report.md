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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-46MS` (url=292ms, status=HTTP 204)
2. `AKUN-002-RS-RAPIDSEEDBOX-20190717-VLESS-WS-39MS` (url=308ms, status=HTTP 204)
3. `AKUN-003-MEDIUM-VLESS-WS-65MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-65MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-66MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-64MS` (url=426ms, status=SSLError: HTTPSConnectionPool(host='www.gstatic.com', port=443): Max retries exceeded with url: /generate_204 (Caused by SSLError()
7. `AKUN-007-CLOUDFLARE-VLESS-WS-65MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-66MS`
9. `AKUN-009-GOV-VLESS-WS-68MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-66MS` (url=593ms, status=HTTP 204)
11. `AKUN-013-BIGCOMMERCE-VLESS-WS-68MS` (url=285ms, status=HTTP 204)
12. `AKUN-015-CHATGPT-VLESS-WS-69MS` (url=282ms, status=HTTP 204)
13. `AKUN-016-CLOUDFLARE-VLESS-WS-68MS` (url=309ms, status=HTTP 204)
14. `AKUN-019-CLOUDFLARE-VLESS-WS-73MS` (url=1094ms, status=HTTP 204)
15. `AKUN-021-CLOUDFLARE-VLESS-WS-69MS` (url=311ms, status=HTTP 204)
16. `AKUN-022-CLOUDFLARE-VLESS-WS-64MS` (url=286ms, status=HTTP 204)
17. `AKUN-023-CLOUDFLARE-VLESS-WS-67MS` (url=311ms, status=HTTP 204)
18. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-67MS` (url=308ms, status=HTTP 204)
19. `AKUN-025-COM-VLESS-WS-72MS` (url=293ms, status=HTTP 204)
20. `AKUN-026-CLOUDFLARE-VLESS-WS-74MS` (url=280ms, status=HTTP 204)
21. `AKUN-027-CLOUDFLARE-VLESS-WS-70MS` (url=288ms, status=HTTP 204)
22. `AKUN-028-CLOUDFLARE-VLESS-WS-67MS` (url=278ms, status=HTTP 204)
23. `AKUN-029-CLOUDFLARE-VLESS-WS-71MS` (url=291ms, status=HTTP 204)
24. `AKUN-030-CLOUDFLARE-VLESS-WS-72MS` (url=282ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-75MS` (url=610ms, status=HTTP 204)
26. `AKUN-032-CLOUDFLARE-VLESS-WS-70MS` (url=308ms, status=HTTP 204)
27. `AKUN-033-CLOUDFLARE-VLESS-WS-68MS` (url=305ms, status=HTTP 204)
28. `AKUN-034-CLOUDFLARE-VLESS-WS-73MS` (url=287ms, status=HTTP 204)
29. `AKUN-035-CLOUDFLARE-VLESS-WS-76MS` (url=676ms, status=HTTP 204)
30. `AKUN-036-CLOUDFLARE-VLESS-WS-77MS` (url=287ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
