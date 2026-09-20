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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-124MS` (url=763ms, status=HTTP 204)
2. `AKUN-002-TENCENT-VLESS-WS-154MS` (url=750ms, status=HTTP 204)
3. `AKUN-003-CZ-LOTUNA-19970206-VLESS-WS-172MS` (url=744ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-146MS` (url=734ms, status=HTTP 204)
5. `AKUN-005-ALIBABA-VLESS-WS-116MS` (url=750ms, status=HTTP 204)
6. `AKUN-010-UNKNOWN-VLESS-WS-135MS`
7. `AKUN-002-CLOUDFLARE-VLESS-WS-124MS`
8. `AKUN-007-CY-ANNETEN-19971112-VLESS-WS-163MS`
9. `AKUN-009-CY-ANNETEN-19971112-VLESS-WS-198MS` (url=752ms, status=HTTP 204)
10. `AKUN-010-NET-83-147-12-0-22-VLESS-WS-122MS` (url=782ms, status=HTTP 204)
11. `AKUN-011-TYCHRON-02-VLESS-WS-180MS` (url=724ms, status=HTTP 204)
12. `AKUN-006-NASEEJ-VLESS-WS-201MS`
13. `AKUN-005-CLOUDFLARE-VLESS-WS-114MS`
14. `AKUN-014-NET-147-90-26-0-24-VLESS-WS-113MS` (url=740ms, status=HTTP 204)
15. `AKUN-015-NUXTCLOUD-VLESS-WS-128MS` (url=726ms, status=HTTP 204)
16. `AKUN-016-LUCIDACLOUD-VLESS-WS-110MS` (url=735ms, status=HTTP 204)
17. `AKUN-004-CLOUDFLARE-VLESS-WS-133MS`
18. `AKUN-003-ACE-SG-VLESS-WS-138MS`
19. `AKUN-019-NET-147-90-26-0-24-VLESS-WS-136MS` (url=758ms, status=HTTP 204)
20. `AKUN-001-UNKNOWN-VLESS-WS-229MS`
21. `AKUN-021-UNKNOWN-VLESS-WS-138MS` (url=738ms, status=HTTP 204)
22. `AKUN-022-SDCL-TW-NET-VLESS-WS-135MS` (url=728ms, status=HTTP 204)
23. `AKUN-023-PMBET-NET-VLESS-WS-302MS` (url=743ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-171MS` (url=739ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-168MS` (url=763ms, status=HTTP 204)
26. `AKUN-009-CLOUDFLARE-VLESS-WS-168MS`
27. `AKUN-027-ALOIPTELTD-SG-VLESS-WS-176MS` (url=745ms, status=HTTP 204)
28. `AKUN-008-CLOUDFLARE-VLESS-WS-176MS`
29. `AKUN-029-TENCENT-VLESS-WS-139MS` (url=722ms, status=HTTP 204)
30. `AKUN-033-UNKNOWN-VLESS-WS-649MS` (url=1466ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
