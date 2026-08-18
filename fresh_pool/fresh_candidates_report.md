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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-242MS`
2. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-243MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-247MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-289MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-296MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-264MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-282MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-253MS`
9. `AKUN-009-NOTION-WEB-VLESS-WS-293MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-263MS`
11. `AKUN-017-NOTION-WEB-VLESS-WS-250MS` (url=994ms, status=HTTP 204)
12. `AKUN-018-UNKNOWN-VLESS-WS-248MS` (url=748ms, status=HTTP 204)
13. `AKUN-020-UNKNOWN-VLESS-WS-247MS` (url=550ms, status=HTTP 204)
14. `AKUN-021-UNKNOWN-VLESS-WS-237MS` (url=1081ms, status=HTTP 204)
15. `AKUN-022-UNKNOWN-VLESS-WS-232MS` (url=854ms, status=HTTP 204)
16. `AKUN-023-UNKNOWN-VLESS-WS-247MS` (url=560ms, status=HTTP 204)
17. `AKUN-024-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-249MS` (url=714ms, status=HTTP 204)
18. `AKUN-025-UNKNOWN-VLESS-WS-249MS` (url=498ms, status=HTTP 204)
19. `AKUN-026-UNKNOWN-VLESS-WS-256MS` (url=867ms, status=HTTP 204)
20. `AKUN-027-UNKNOWN-VLESS-WS-270MS` (url=576ms, status=HTTP 204)
21. `AKUN-028-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-288MS` (url=577ms, status=HTTP 204)
22. `AKUN-029-UNKNOWN-VLESS-WS-249MS` (url=575ms, status=HTTP 204)
23. `AKUN-030-UNKNOWN-VLESS-WS-288MS` (url=963ms, status=HTTP 204)
24. `AKUN-031-CLOUDFLARE-VLESS-WS-329MS` (url=600ms, status=HTTP 204)
25. `AKUN-032-CLOUDFLARE-VLESS-WS-274MS` (url=543ms, status=HTTP 204)
26. `AKUN-033-UNKNOWN-VLESS-WS-286MS` (url=603ms, status=HTTP 204)
27. `AKUN-034-UNKNOWN-VLESS-WS-276MS` (url=674ms, status=HTTP 204)
28. `AKUN-035-UNKNOWN-VLESS-WS-336MS` (url=675ms, status=HTTP 204)
29. `AKUN-036-CLOUDFLARE-VLESS-WS-770MS` (url=1667ms, status=HTTP 204)
30. `AKUN-037-CLOUDFLARE-VLESS-WS-282MS` (url=1339ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
