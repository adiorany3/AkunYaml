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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-248MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-241MS` (url=4632ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-244MS` (url=4608ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-228MS` (url=932ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-254MS` (url=719ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-200MS` (url=699ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-248MS` (url=531ms, status=HTTP 204)
8. `AKUN-008-EU-VLESS-WS-272MS` (url=860ms, status=HTTP 204)
9. `AKUN-009-DEV-VLESS-WS-275MS` (url=591ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-237MS` (url=547ms, status=HTTP 204)
11. `AKUN-011-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-283MS` (url=959ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-237MS` (url=1489ms, status=HTTP 204)
13. `AKUN-013-UNKNOWN-VLESS-WS-244MS` (url=540ms, status=HTTP 204)
14. `AKUN-014-UNKNOWN-VLESS-WS-276MS` (url=700ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-262MS` (url=640ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-249MS` (url=561ms, status=HTTP 204)
17. `AKUN-017-CHATGPT-VLESS-WS-283MS` (url=667ms, status=HTTP 204)
18. `AKUN-018-DE5-VLESS-WS-305MS` (url=769ms, status=HTTP 204)
19. `AKUN-019-UNKNOWN-VLESS-WS-254MS` (url=521ms, status=HTTP 204)
20. `AKUN-020-CLOUDFLARE-VLESS-WS-274MS` (url=1059ms, status=HTTP 204)
21. `AKUN-021-UNKNOWN-VLESS-WS-240MS` (url=797ms, status=HTTP 204)
22. `AKUN-022-DE5-VLESS-WS-290MS` (url=3793ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-249MS` (url=859ms, status=HTTP 204)
24. `AKUN-024-CCWU-VLESS-WS-240MS` (url=562ms, status=HTTP 204)
25. `AKUN-025-UNKNOWN-VLESS-WS-222MS` (url=1059ms, status=HTTP 204)
26. `AKUN-026-UNKNOWN-VLESS-WS-266MS` (url=519ms, status=HTTP 204)
27. `AKUN-027-UNKNOWN-VLESS-WS-286MS` (url=600ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-239MS` (url=502ms, status=HTTP 204)
29. `AKUN-029-UNKNOWN-VLESS-WS-320MS` (url=977ms, status=HTTP 204)
30. `AKUN-030-UNKNOWN-VLESS-WS-250MS` (url=528ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
