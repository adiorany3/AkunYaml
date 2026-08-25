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
1. `AKUN-001-RUSSIA-VLESS-WS-111MS` (url=682ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-104MS` (url=681ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-121MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-106MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-109MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-113MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-113MS`
9. `AKUN-009-AIMALL-VLESS-WS-113MS`
10. `AKUN-010-CHATGPT-VLESS-WS-147MS`
11. `AKUN-013-DE5-VLESS-WS-107MS` (url=400ms, status=HTTP 204)
12. `AKUN-014-DE5-VLESS-WS-118MS` (url=340ms, status=HTTP 204)
13. `AKUN-015-UNKNOWN-VLESS-WS-361MS` (url=1358ms, status=HTTP 204)
14. `AKUN-016-DEV-VLESS-WS-363MS` (url=699ms, status=HTTP 204)
15. `AKUN-017-MYBB-VLESS-WS-373MS` (url=656ms, status=HTTP 204)
16. `AKUN-019-DEV-VLESS-WS-349MS` (url=656ms, status=HTTP 204)
17. `AKUN-020-UNKNOWN-VLESS-WS-494MS` (url=820ms, status=HTTP 204)
18. `AKUN-021-DE5-VLESS-WS-497MS` (url=377ms, status=HTTP 204)
19. `AKUN-023-UNKNOWN-VLESS-WS-365MS` (url=706ms, status=HTTP 204)
20. `AKUN-024-CLOUDFLARE-VLESS-WS-367MS` (url=332ms, status=HTTP 204)
21. `AKUN-027-UNKNOWN-VLESS-WS-356MS` (url=1472ms, status=HTTP 204)
22. `AKUN-028-UNKNOWN-VLESS-WS-106MS` (url=1217ms, status=HTTP 204)
23. `AKUN-033-UNKNOWN-VLESS-WS-499MS` (url=333ms, status=HTTP 204)
24. `AKUN-034-TIME-VLESS-WS-123MS` (url=328ms, status=HTTP 204)
25. `AKUN-036-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-127MS` (url=699ms, status=HTTP 204)
26. `AKUN-037-NOTION-WEB-VLESS-WS-115MS` (url=364ms, status=HTTP 204)
27. `AKUN-038-UNKNOWN-VLESS-WS-492MS` (url=652ms, status=HTTP 204)
28. `AKUN-040-UNKNOWN-VLESS-WS-113MS` (url=681ms, status=HTTP 204)
29. `AKUN-041-UNKNOWN-VLESS-WS-493MS` (url=669ms, status=HTTP 204)
30. `AKUN-042-CLOUDFLARE-VLESS-WS-111MS` (url=666ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
