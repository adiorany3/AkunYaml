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
- Proxy di openclash_fresh_pool.yaml: 102

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
1. `AKUN-001-UNKNOWN-VLESS-WS-215MS`
2. `AKUN-002-UNKNOWN-VLESS-WS-230MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-241MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-252MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-242MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-242MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-250MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-235MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-254MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-289MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-254MS` (url=415ms, status=HTTP 204)
12. `AKUN-017-CLOUDFLARE-VLESS-WS-219MS` (url=859ms, status=HTTP 204)
13. `AKUN-018-CLOUDFLARE-VLESS-WS-218MS` (url=733ms, status=HTTP 204)
14. `AKUN-019-CLOUDFLARE-VLESS-WS-234MS` (url=1475ms, status=HTTP 204)
15. `AKUN-020-CLOUDFLARE-VLESS-WS-233MS` (url=696ms, status=HTTP 204)
16. `AKUN-021-CLOUDFLARE-VLESS-WS-249MS` (url=531ms, status=HTTP 204)
17. `AKUN-023-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-233MS` (url=535ms, status=HTTP 204)
18. `AKUN-024-CLOUDFLARE-VLESS-WS-236MS` (url=600ms, status=HTTP 204)
19. `AKUN-025-CLOUDFLARE-VLESS-WS-240MS` (url=780ms, status=HTTP 204)
20. `AKUN-026-CLOUDFLARE-VLESS-WS-233MS` (url=495ms, status=HTTP 204)
21. `AKUN-027-CLOUDFLARE-VLESS-WS-248MS` (url=467ms, status=HTTP 204)
22. `AKUN-028-CLOUDFLARE-VLESS-WS-214MS` (url=552ms, status=HTTP 204)
23. `AKUN-029-UNKNOWN-VLESS-WS-275MS` (url=520ms, status=HTTP 204)
24. `AKUN-030-NODE2-VLESS-WS-247MS` (url=706ms, status=HTTP 204)
25. `AKUN-034-CLOUDFLARE-VLESS-WS-261MS` (url=540ms, status=HTTP 204)
26. `AKUN-035-NOTION-WEB-VLESS-WS-264MS` (url=1235ms, status=HTTP 204)
27. `AKUN-036-UNKNOWN-VLESS-WS-459MS` (url=1572ms, status=HTTP 204)
28. `AKUN-041-UNKNOWN-VLESS-WS-271MS` (url=474ms, status=HTTP 204)
29. `AKUN-042-CLOUDFLARE-VLESS-WS-284MS` (url=496ms, status=HTTP 204)
30. `AKUN-048-LOCALIP-VLESS-WS-1017MS` (url=1681ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
