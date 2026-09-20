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
- Kandidat strict NekoBox-tested: 7
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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-128MS` (url=451ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-130MS` (url=403ms, nekobox=308ms, status=no)
3. `AKUN-003-UNKNOWN-VLESS-WS-164MS` (url=448ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-159MS` (url=426ms, status=HTTP 204)
5. `AKUN-005-PMBET-NET-VLESS-WS-210MS` (url=417ms, status=HTTP 204)
6. `AKUN-006-CY-ANNETEN-19971112-VLESS-WS-172MS` (url=442ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-157MS` (url=438ms, status=HTTP 204)
8. `AKUN-008-ALOIPTELTD-SG-VLESS-WS-150MS` (url=421ms, status=HTTP 204)
9. `AKUN-003-OLOIN-1-VLESS-WS-223MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-132MS` (url=420ms, status=HTTP 204)
11. `AKUN-011-TENCENT-VLESS-WS-143MS` (url=433ms, status=HTTP 204)
12. `AKUN-001-CLOUDFLARE-VLESS-WS-141MS`
13. `AKUN-013-CLOUDFLARE-VLESS-WS-161MS` (url=411ms, nekobox=305ms, status=no)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-145MS` (url=442ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-127MS` (url=418ms, status=HTTP 204)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-144MS` (url=419ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-120MS` (url=445ms, status=HTTP 204)
18. `AKUN-018-UNKNOWN-VLESS-WS-151MS` (url=443ms, status=HTTP 204)
19. `AKUN-006-PMBET-NET-VLESS-WS-206MS`
20. `AKUN-020-TENCENT-VLESS-WS-158MS` (url=658ms, status=HTTP 204)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-125MS` (url=461ms, status=HTTP 204)
22. `AKUN-022-UNKNOWN-VLESS-WS-201MS` (url=503ms, status=HTTP 204)
23. `AKUN-023-NASEEJ-VLESS-WS-210MS` (url=458ms, status=HTTP 204)
24. `AKUN-024-NASEEJ-VLESS-WS-227MS` (url=488ms, status=HTTP 204)
25. `AKUN-002-CLOUDFLARE-VLESS-WS-173MS`
26. `AKUN-026-CLOUDFLARE-VLESS-WS-186MS` (url=424ms, status=HTTP 204)
27. `AKUN-005-CLOUDFLARE-VLESS-WS-162MS`
28. `AKUN-004-CLOUDFLARE-VLESS-WS-183MS`
29. `AKUN-007-UNKNOWN-VLESS-WS-178MS`
30. `AKUN-030-UNKNOWN-VLESS-WS-143MS` (url=406ms, nekobox=6186ms, status=no)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
