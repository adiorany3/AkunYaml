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
- Kandidat strict NekoBox-tested: 7
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-92MS` (url=379ms, status=HTTP 204)
2. `AKUN-001-CLOUDFLARE-VLESS-WS-90MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-90MS` (url=367ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-95MS` (url=401ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-82MS` (url=383ms, status=HTTP 204)
6. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-88MS` (url=376ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-89MS` (url=386ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-102MS` (url=353ms, nekobox=271ms, status=no)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-88MS` (url=375ms, status=HTTP 204)
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-88MS` (url=408ms, status=HTTP 204)
11. `AKUN-005-CLOUDFLARE-VLESS-WS-107MS`
12. `AKUN-012-DEV-VLESS-WS-94MS` (url=395ms, status=HTTP 204)
13. `AKUN-014-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-92MS` (url=393ms, status=HTTP 204)
14. `AKUN-015-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-103MS` (url=386ms, status=HTTP 204)
15. `AKUN-016-UNKNOWN-VLESS-WS-82MS` (url=366ms, status=HTTP 204)
16. `AKUN-007-CLOUDFLARE-VLESS-WS-88MS`
17. `AKUN-006-AXIOMED-VLESS-WS-90MS`
18. `AKUN-019-CLOUDFLARE-VLESS-WS-95MS` (url=372ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-93MS` (url=377ms, status=HTTP 204)
20. `AKUN-003-BIGCOMMERCE-VLESS-WS-84MS`
21. `AKUN-022-CLOUDFLARE-VLESS-WS-105MS` (url=407ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-81MS` (url=373ms, status=HTTP 204)
23. `AKUN-024-DEV-VLESS-WS-93MS` (url=384ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-91MS` (url=359ms, nekobox=279ms, status=no)
25. `AKUN-002-MEDIUM-VLESS-WS-97MS`
26. `AKUN-027-CLOUDFLARE-VLESS-WS-96MS` (url=356ms, nekobox=273ms, status=no)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-97MS` (url=376ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-204MS` (url=744ms, status=HTTP 204)
29. `AKUN-032-DEV-VLESS-WS-278MS` (url=956ms, status=HTTP 204)
30. `AKUN-004-CLOUDFLARE-VLESS-WS-88MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
