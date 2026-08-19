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
1. `AKUN-001-CHATGPT-VLESS-WS-63MS` (url=308ms, status=HTTP 204)
2. `AKUN-002-OPENAI-VLESS-WS-68MS` (url=301ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-68MS` (url=297ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-70MS` (url=296ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-68MS` (url=329ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-66MS` (url=297ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-64MS` (url=275ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-69MS` (url=341ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-69MS` (url=295ms, status=HTTP 204)
10. `AKUN-010-MEDIUM-VLESS-WS-69MS` (url=306ms, status=HTTP 204)
11. `AKUN-012-UNKNOWN-VLESS-WS-64MS` (url=299ms, status=HTTP 204)
12. `AKUN-013-SPEEDTEST-VLESS-WS-68MS` (url=318ms, status=HTTP 204)
13. `AKUN-014-DEV-VLESS-WS-70MS` (url=684ms, status=HTTP 204)
14. `AKUN-015-SPEEDTEST-VLESS-WS-69MS` (url=323ms, status=HTTP 204)
15. `AKUN-016-CLOUDFLARE-VLESS-WS-70MS` (url=364ms, status=HTTP 204)
16. `AKUN-017-EU-VLESS-WS-73MS` (url=298ms, status=HTTP 204)
17. `AKUN-018-UNKNOWN-VLESS-WS-70MS` (url=292ms, status=HTTP 204)
18. `AKUN-019-UNKNOWN-VLESS-WS-79MS` (url=304ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-77MS` (url=289ms, status=HTTP 204)
20. `AKUN-021-1PASSWORD-VLESS-WS-68MS` (url=317ms, status=HTTP 204)
21. `AKUN-022-DEV-VLESS-WS-71MS` (url=1819ms, status=HTTP 204)
22. `AKUN-023-TIME-VLESS-WS-73MS` (url=289ms, status=HTTP 204)
23. `AKUN-024-UNKNOWN-VLESS-WS-71MS` (url=301ms, status=HTTP 204)
24. `AKUN-025-UNKNOWN-VLESS-WS-74MS` (url=672ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-77MS` (url=285ms, status=HTTP 204)
26. `AKUN-027-TIME-VLESS-WS-79MS` (url=290ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-71MS` (url=299ms, status=HTTP 204)
28. `AKUN-029-CLOUDFLARE-VLESS-WS-73MS` (url=303ms, status=HTTP 204)
29. `AKUN-030-ADF-VLESS-WS-73MS` (url=309ms, status=HTTP 204)
30. `AKUN-031-DEV-VLESS-WS-72MS` (url=326ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
