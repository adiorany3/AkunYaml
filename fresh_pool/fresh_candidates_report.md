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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-66MS`
2. `AKUN-002-MYBB-VLESS-WS-68MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-70MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-69MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-36MS`
6. `AKUN-006-MEDIUM-VLESS-WS-68MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-70MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-71MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-73MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-66MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-73MS` (url=278ms, status=HTTP 204)
12. `AKUN-015-CLOUDFLARE-VLESS-WS-71MS` (url=294ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-70MS` (url=264ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-74MS` (url=327ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-65MS` (url=275ms, status=HTTP 204)
16. `AKUN-020-RS-RAPIDSEEDBOX-20190717-VLESS-WS-67MS` (url=283ms, status=HTTP 204)
17. `AKUN-022-CLOUDFLARE-VLESS-WS-70MS` (url=746ms, status=HTTP 204)
18. `AKUN-023-CLOUDFLARE-VLESS-WS-72MS` (url=295ms, status=HTTP 204)
19. `AKUN-024-CLOUDFLARE-VLESS-WS-67MS` (url=268ms, status=HTTP 204)
20. `AKUN-025-CHATGPT-VLESS-WS-65MS` (url=276ms, status=HTTP 204)
21. `AKUN-027-GOV-VLESS-WS-72MS` (url=301ms, status=HTTP 204)
22. `AKUN-028-CLOUDFLARE-VLESS-WS-67MS` (url=299ms, status=HTTP 204)
23. `AKUN-029-CLOUDFLARE-VLESS-WS-67MS` (url=1072ms, status=HTTP 204)
24. `AKUN-030-RS-RAPIDSEEDBOX-20190717-VLESS-WS-69MS` (url=310ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-70MS` (url=585ms, status=HTTP 204)
26. `AKUN-032-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-75MS` (url=275ms, status=HTTP 204)
27. `AKUN-033-BIGCOMMERCE-VLESS-WS-72MS` (url=314ms, status=HTTP 204)
28. `AKUN-034-COM-VLESS-WS-73MS` (url=276ms, status=HTTP 204)
29. `AKUN-035-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-74MS` (url=310ms, status=HTTP 204)
30. `AKUN-036-CLOUDFLARE-VLESS-WS-74MS` (url=274ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
