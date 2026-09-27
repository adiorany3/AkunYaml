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
- Kandidat strict NekoBox-tested: 8
- Proxy di openclash_fresh_pool.yaml: 32

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
1. `AKUN-001-877774-VLESS-WS-100MS` (url=425ms, status=HTTP 204)
2. `AKUN-002-UNKNOWN-VLESS-WS-98MS` (url=368ms, nekobox=412ms, status=yes)
3. `AKUN-008-MD-ITFRUIT-185153198-202-VLESS-WS-104MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-105MS` (url=954ms, status=HTTP 204)
5. `AKUN-005-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-105MS` (url=399ms, status=HTTP 204)
6. `AKUN-006-DIGITALOCEAN-VLESS-WS-97MS` (url=383ms, nekobox=433ms, status=yes)
7. `AKUN-003-CLOUDFLARE-VLESS-WS-99MS`
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-104MS` (url=390ms, status=HTTP 204)
9. `AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-106MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-103MS` (url=409ms, status=HTTP 204)
11. `AKUN-011-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-95MS` (url=391ms, status=HTTP 204)
12. `AKUN-012-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-98MS` (url=344ms, nekobox=453ms, status=no)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-105MS` (url=405ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-103MS` (url=396ms, status=HTTP 204)
15. `AKUN-016-DEV-VLESS-WS-105MS` (url=753ms, status=HTTP 204)
16. `AKUN-007-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-114MS`
17. `AKUN-018-CLOUDFLARE-VLESS-WS-107MS` (url=394ms, status=HTTP 204)
18. `AKUN-019-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-96MS` (url=405ms, status=HTTP 204)
19. `AKUN-020-UNKNOWN-VLESS-WS-99MS` (url=394ms, status=HTTP 204)
20. `AKUN-021-UNKNOWN-VLESS-WS-120MS` (url=610ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-101MS` (url=407ms, status=HTTP 204)
22. `AKUN-005-UNKNOWN-VLESS-WS-103MS`
23. `AKUN-024-RUSSIA-VLESS-WS-95MS` (url=392ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-101MS` (url=401ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-102MS` (url=399ms, status=HTTP 204)
26. `AKUN-027-CLOUDFLARE-VLESS-WS-100MS` (url=369ms, nekobox=277ms, status=no)
27. `AKUN-001-CLOUDFLARE-VLESS-WS-124MS`
28. `AKUN-029-CLOUDFLARE-VLESS-WS-112MS` (url=604ms, status=HTTP 204)
29. `AKUN-030-UNKNOWN-VLESS-WS-198MS` (url=687ms, status=HTTP 204)
30. `AKUN-031-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-233MS` (url=608ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
