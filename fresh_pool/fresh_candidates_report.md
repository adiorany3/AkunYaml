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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-277MS` (url=4346ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-258MS` (url=946ms, status=HTTP 204)
3. `AKUN-003-VEESP-VLESS-WS-327MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-286MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-300MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-363MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-340MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-349MS`
9. `AKUN-009-PUBLICDOMAINREGISTRY-NET-VLESS-WS-479MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-493MS`
11. `AKUN-020-AMAZON-VLESS-WS-430MS` (url=7534ms, status=HTTP 204)
12. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-410MS` (url=664ms, status=HTTP 204)
13. `AKUN-023-CLOUDFLARE-VLESS-WS-343MS` (url=1269ms, status=HTTP 204)
14. `AKUN-029-CLOUDFLARE-VLESS-WS-397MS` (url=4416ms, status=HTTP 204)
15. `AKUN-030-UNKNOWN-VLESS-WS-321MS` (url=654ms, status=HTTP 204)
16. `AKUN-032-UNKNOWN-VLESS-WS-429MS` (url=660ms, status=HTTP 204)
17. `AKUN-033-CLOUDFLARE-VLESS-WS-688MS` (url=1054ms, status=HTTP 204)
18. `AKUN-034-UNKNOWN-VLESS-WS-627MS` (url=828ms, status=HTTP 204)
19. `AKUN-035-CLOUDFLARE-VLESS-WS-778MS` (url=1201ms, status=HTTP 204)
20. `AKUN-036-UNKNOWN-VLESS-WS-1126MS` (url=2984ms, status=HTTP 204)
21. `AKUN-045-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-1108MS` (url=1739ms, status=HTTP 204)
22. `AKUN-046-CLOUDFLARE-VLESS-WS-297MS` (url=819ms, status=HTTP 204)
23. `AKUN-047-CLOUDFLARE-VLESS-WS-347MS` (url=687ms, status=HTTP 204)
24. `AKUN-049-NPMJS-VLESS-WS-1040MS` (url=1947ms, status=HTTP 204)
25. `AKUN-052-CLOUDFLARE-VLESS-WS-427MS` (url=1364ms, status=HTTP 204)
26. `AKUN-054-CLOUDFLARE-VLESS-WS-319MS` (url=1359ms, status=HTTP 204)
27. `AKUN-055-CLOUDFLARE-VLESS-WS-853MS` (url=3108ms, status=HTTP 204)
28. `AKUN-057-CLOUDFLARE-VLESS-WS-374MS` (url=2737ms, status=HTTP 204)
29. `AKUN-058-CLOUDFLARE-VLESS-WS-384MS` (url=2127ms, status=HTTP 204)
30. `AKUN-059-VEESP-VLESS-WS-442MS` (url=861ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
