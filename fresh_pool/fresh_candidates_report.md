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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-44MS` (url=286ms, status=HTTP 204)
2. `AKUN-002-OPENAI-VLESS-WS-52MS` (url=274ms, status=HTTP 204)
3. `AKUN-003-EU-VLESS-WS-67MS` (url=290ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-74MS` (url=286ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-71MS` (url=303ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-42MS` (url=278ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-70MS` (url=299ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-70MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-76MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-43MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-68MS` (url=304ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-69MS` (url=385ms, status=HTTP 204)
13. `AKUN-013-DEV-VLESS-WS-70MS` (url=316ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-72MS` (url=296ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-68MS` (url=297ms, status=HTTP 204)
16. `AKUN-016-ADF-VLESS-WS-72MS` (url=298ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-73MS` (url=272ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-74MS` (url=300ms, status=HTTP 204)
19. `AKUN-019-NOTION-WEB-VLESS-WS-74MS` (url=273ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-70MS` (url=308ms, status=HTTP 204)
21. `AKUN-021-TIME-VLESS-WS-74MS` (url=348ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-67MS` (url=269ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-74MS` (url=309ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-76MS` (url=328ms, status=HTTP 204)
25. `AKUN-025-UNKNOWN-VLESS-WS-70MS` (url=296ms, status=HTTP 204)
26. `AKUN-026-SPEEDTEST-VLESS-WS-73MS` (url=317ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-76MS` (url=285ms, status=HTTP 204)
28. `AKUN-028-SPEEDTEST-VLESS-WS-77MS` (url=349ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-70MS` (url=281ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-73MS` (url=298ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
