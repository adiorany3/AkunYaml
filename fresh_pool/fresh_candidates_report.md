# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 25
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-001-GTHOST-VLESS-WS-154MS` (url=977ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-163MS` (url=524ms, status=HTTP 204)
3. `AKUN-009-CY-ANNETEN-19971112-VLESS-WS-217MS`
4. `AKUN-008-DMIT-CUSTOMER-US-CA-9001-VLESS-WS-165MS`
5. `AKUN-006-CLOUDFLARE-VLESS-WS-173MS` (url=449ms, status=HTTP 204)
6. `AKUN-003-CLOUDFLARE-VLESS-WS-167MS`
7. `AKUN-005-PMBET-NET-VLESS-WS-178MS`
8. `AKUN-002-CLOUDFLARE-VLESS-WS-189MS`
9. `AKUN-010-CY-ANNETEN-19971112-VLESS-WS-191MS` (url=474ms, status=HTTP 204)
10. `AKUN-004-ZUOAI-VLESS-WS-146MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-344MS` (url=1024ms, status=HTTP 204)
12. `AKUN-006-CLOUDFLARE-VLESS-WS-150MS`
13. `AKUN-007-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-183MS`
14. `AKUN-019-CLOUDFLARE-VLESS-WS-188MS` (url=482ms, status=HTTP 204)
15. `AKUN-020-CLOUDFLARE-VLESS-WS-151MS` (url=461ms, status=HTTP 204)
16. `AKUN-022-CLOUDFLARE-VLESS-WS-237MS` (url=457ms, status=HTTP 204)
17. `AKUN-023-CLOUDFLARE-VLESS-WS-284MS` (url=462ms, status=HTTP 204)
18. `AKUN-024-IPOWERWEB-NET-VLESS-WS-172MS` (url=467ms, status=HTTP 204)
19. `AKUN-001-CLOUDFLARE-VLESS-WS-243MS`
20. `AKUN-026-UNKNOWN-VLESS-WS-257MS` (url=430ms, nekobox=6173ms, status=no)
21. `AKUN-028-CLOUDFLARE-VLESS-WS-467MS` (url=1892ms, status=HTTP 204)
22. `AKUN-030-UNKNOWN-VLESS-WS-596MS` (url=3372ms, status=HTTP 204)
23. `AKUN-032-UNKNOWN-VLESS-WS-677MS` (url=1527ms, status=HTTP 204)
24. `AKUN-035-UNKNOWN-VLESS-WS-201MS` (url=1074ms, status=HTTP 204)
25. `AKUN-059-FREIFUNKFRANKEN-VLESS-WS-986MS` (url=4720ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
