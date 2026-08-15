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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-267MS` (url=575ms, status=HTTP 204)
2. `AKUN-002-UNKNOWN-VLESS-WS-288MS` (url=538ms, status=HTTP 204)
3. `AKUN-003-EE-WELCOMEHOST-20190515-VLESS-WS-300MS` (url=540ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-297MS`
5. `AKUN-005-DEV-VLESS-WS-401MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-319MS`
7. `AKUN-007-NOTION-WEB-VLESS-WS-263MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-422MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-464MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-262MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-364MS`
12. `AKUN-012-U1HOST-FRA-VLESS-WS-516MS`
13. `AKUN-013-UNKNOWN-VLESS-WS-297MS`
14. `AKUN-014-ZVC-VLESS-WS-357MS`
15. `AKUN-015-CLOUDFLARE-VLESS-WS-279MS`
16. `AKUN-016-UNKNOWN-VLESS-WS-252MS`
17. `AKUN-017-CLOUDFLARE-VLESS-WS-264MS`
18. `AKUN-018-DEV-VLESS-WS-279MS`
19. `AKUN-019-CLOUDFLARE-VLESS-WS-310MS`
20. `AKUN-020-UNKNOWN-VLESS-WS-319MS`
21. `AKUN-026-PUBLICDOMAINREGISTRY-NET-VLESS-WS-294MS` (url=877ms, status=HTTP 204)
22. `AKUN-027-UNKNOWN-VLESS-WS-347MS` (url=2797ms, status=HTTP 204)
23. `AKUN-028-UNKNOWN-VLESS-WS-306MS` (url=1027ms, status=HTTP 204)
24. `AKUN-030-UNKNOWN-VLESS-WS-294MS` (url=578ms, status=HTTP 204)
25. `AKUN-031-CLOUDFLARE-VLESS-WS-290MS` (url=1919ms, status=HTTP 204)
26. `AKUN-032-CLOUDFLARE-VLESS-WS-260MS` (url=719ms, status=HTTP 204)
27. `AKUN-033-CLOUDFLARE-VLESS-WS-329MS` (url=1140ms, status=HTTP 204)
28. `AKUN-034-MEDIUM-VLESS-WS-369MS` (url=493ms, status=HTTP 204)
29. `AKUN-035-CLOUDFLARE-VLESS-WS-237MS` (url=493ms, status=HTTP 204)
30. `AKUN-036-CLOUDFLARE-VLESS-WS-350MS` (url=646ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
