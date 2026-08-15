# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 24
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 28

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
1. `AKUN-001-UNKNOWN-VLESS-WS-412MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-303MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-356MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-292MS`
5. `AKUN-005-NOTION-WEB-VLESS-WS-314MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-492MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-342MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-327MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-322MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-861MS`
11. `AKUN-029-CLOUDFLARE-VLESS-WS-706MS` (url=1479ms, status=HTTP 204)
12. `AKUN-030-CLOUDFLARE-VLESS-WS-531MS` (url=777ms, status=HTTP 204)
13. `AKUN-031-CLOUDFLARE-VLESS-WS-319MS` (url=989ms, status=HTTP 204)
14. `AKUN-033-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-306MS` (url=1143ms, status=HTTP 204)
15. `AKUN-035-CLOUDFLARE-VLESS-WS-867MS` (url=1388ms, status=HTTP 204)
16. `AKUN-037-UNKNOWN-VLESS-WS-1131MS` (url=1835ms, status=HTTP 204)
17. `AKUN-038-UNKNOWN-VLESS-WS-1137MS` (url=1579ms, status=HTTP 204)
18. `AKUN-042-DEV-VLESS-WS-831MS` (url=1400ms, status=HTTP 204)
19. `AKUN-044-CLOUDFLARE-VLESS-WS-913MS` (url=2314ms, status=HTTP 204)
20. `AKUN-047-CLOUDFLARE-VLESS-WS-1034MS` (url=1312ms, status=HTTP 204)
21. `AKUN-049-UNKNOWN-VLESS-WS-1147MS` (url=3812ms, status=HTTP 204)
22. `AKUN-050-UNKNOWN-VLESS-WS-446MS` (url=825ms, status=HTTP 204)
23. `AKUN-052-CLOUDFLARE-VLESS-WS-1095MS` (url=2235ms, status=HTTP 204)
24. `AKUN-053-CLOUDFLARE-VLESS-WS-518MS` (url=1702ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
