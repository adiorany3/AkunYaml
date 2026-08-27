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
1. `AKUN-001-EDIS-BE-NET-VLESS-WS-66MS` (url=314ms, status=HTTP 204)
2. `AKUN-002-EDIS-CZ-NET-VLESS-WS-71MS` (url=310ms, status=HTTP 204)
3. `AKUN-003-BAXET-GROUP-INC-VLESS-WS-66MS` (url=304ms, status=HTTP 204)
4. `AKUN-004-ESA-VLESS-WS-66MS` (url=309ms, status=HTTP 204)
5. `AKUN-005-CH-INTERWAY-VLESS-WS-66MS` (url=285ms, status=HTTP 204)
6. `AKUN-006-ALPHAVPS-VLESS-WS-70MS` (url=297ms, status=HTTP 204)
7. `AKUN-007-IPXO-VLESS-WS-74MS`
8. `AKUN-008-IPXO-VLESS-WS-70MS`
9. `AKUN-009-ESA-VLESS-WS-67MS`
10. `AKUN-010-NFORCE-VLESS-WS-73MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-70MS` (url=355ms, status=HTTP 204)
12. `AKUN-013-AKAMAI-VLESS-WS-73MS` (url=287ms, status=HTTP 204)
13. `AKUN-014-BG-NETWORK-VLESS-WS-74MS` (url=283ms, status=HTTP 204)
14. `AKUN-015-IRON-HOSTING-CENTRE-LTD-VLESS-WS-74MS` (url=285ms, status=HTTP 204)
15. `AKUN-016-NETCRAFTERS-VLESS-WS-77MS` (url=314ms, status=HTTP 204)
16. `AKUN-017-NETCRAFTERS-VLESS-WS-68MS` (url=282ms, status=HTTP 204)
17. `AKUN-018-SS-SYSTEC-VLESS-WS-74MS` (url=470ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-67MS` (url=301ms, status=HTTP 204)
19. `AKUN-020-CLOUDFLARE-VLESS-WS-78MS` (url=287ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-76MS` (url=285ms, status=HTTP 204)
21. `AKUN-023-UNKNOWN-VLESS-WS-66MS` (url=286ms, status=HTTP 204)
22. `AKUN-024-UNKNOWN-VLESS-WS-70MS` (url=289ms, status=HTTP 204)
23. `AKUN-025-UNKNOWN-VLESS-WS-76MS` (url=291ms, status=HTTP 204)
24. `AKUN-030-CLOUDFLARE-VLESS-WS-289MS` (url=646ms, status=HTTP 204)
25. `AKUN-031-UNKNOWN-VLESS-WS-346MS` (url=646ms, status=HTTP 204)
26. `AKUN-039-LAOWU-VLESS-WS-678MS` (url=1376ms, status=HTTP 204)
27. `AKUN-042-CLOUDFLARE-VLESS-WS-731MS` (url=1435ms, status=HTTP 204)
28. `AKUN-048-41-216-182-0-41-216-182-VLESS-WS-809MS` (url=1389ms, status=HTTP 204)
29. `AKUN-050-UNKNOWN-VLESS-WS-791MS` (url=1372ms, status=HTTP 204)
30. `AKUN-054-090227-VLESS-WS-825MS` (url=1636ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
