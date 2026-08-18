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
1. `AKUN-001-NOTION-WEB-VLESS-WS-247MS` (url=645ms, status=HTTP 204)
2. `AKUN-002-NOTION-WEB-VLESS-WS-269MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-267MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-275MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-282MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-240MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-274MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-322MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-252MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-270MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-266MS` (url=1101ms, status=HTTP 204)
12. `AKUN-016-UNKNOWN-VLESS-WS-260MS` (url=646ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-259MS` (url=511ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-264MS` (url=864ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-238MS` (url=2049ms, status=HTTP 204)
16. `AKUN-020-CLOUDFLARE-VLESS-WS-258MS` (url=626ms, status=HTTP 204)
17. `AKUN-022-UNKNOWN-VLESS-WS-279MS` (url=3230ms, status=HTTP 204)
18. `AKUN-024-CLOUDFLARE-VLESS-WS-313MS` (url=736ms, status=HTTP 204)
19. `AKUN-025-CLOUDFLARE-VLESS-WS-444MS` (url=538ms, status=HTTP 204)
20. `AKUN-027-CLOUDFLARE-VLESS-WS-612MS` (url=1396ms, status=HTTP 204)
21. `AKUN-028-CLOUDFLARE-VLESS-WS-260MS` (url=1132ms, status=HTTP 204)
22. `AKUN-029-UNKNOWN-VLESS-WS-287MS` (url=765ms, status=HTTP 204)
23. `AKUN-030-CLOUDFLARE-VLESS-WS-717MS` (url=753ms, status=HTTP 204)
24. `AKUN-031-CLOUDFLARE-VLESS-WS-292MS` (url=481ms, status=HTTP 204)
25. `AKUN-034-UNKNOWN-VLESS-WS-665MS` (url=692ms, status=HTTP 204)
26. `AKUN-035-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-299MS` (url=1825ms, status=HTTP 204)
27. `AKUN-037-UNKNOWN-VLESS-WS-809MS` (url=1531ms, status=HTTP 204)
28. `AKUN-041-CLOUDFLARE-VLESS-WS-927MS` (url=1175ms, status=HTTP 204)
29. `AKUN-048-UNKNOWN-VLESS-WS-1036MS` (url=4112ms, status=HTTP 204)
30. `AKUN-050-DPDNS-VLESS-WS-1107MS` (url=1831ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
