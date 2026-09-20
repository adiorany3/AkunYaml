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
1. `AKUN-001-LUCIDACLOUD-VLESS-WS-104MS` (url=395ms, status=HTTP 204)
2. `AKUN-002-UNKNOWN-VLESS-WS-106MS` (url=402ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=350ms, nekobox=417ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-119MS` (url=418ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-122MS` (url=1390ms, status=HTTP 204)
6. `AKUN-006-CY-ANNETEN-19971112-VLESS-WS-124MS` (url=379ms, status=HTTP 204)
7. `AKUN-007-TYCHRON-02-VLESS-WS-120MS` (url=420ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-118MS` (url=389ms, status=HTTP 204)
9. `AKUN-009-CY-ANNETEN-19971112-VLESS-WS-126MS` (url=380ms, status=HTTP 204)
10. `AKUN-010-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=429ms, status=HTTP 204)
11. `AKUN-006-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-127MS`
12. `AKUN-012-ALOIPTELTD-SG-VLESS-WS-132MS` (url=389ms, status=HTTP 204)
13. `AKUN-007-CLOUDFLARE-VLESS-WS-128MS`
14. `AKUN-008-CLOUDFLARE-VLESS-WS-125MS`
15. `AKUN-002-UNKNOWN-VLESS-WS-131MS`
16. `AKUN-017-ALIBABA-VLESS-WS-132MS` (url=411ms, status=HTTP 204)
17. `AKUN-018-NUXTCLOUD-VLESS-WS-113MS` (url=389ms, status=HTTP 204)
18. `AKUN-010-PMBET-NET-VLESS-WS-125MS`
19. `AKUN-020-NET-147-90-26-0-24-VLESS-WS-126MS` (url=402ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-116MS` (url=391ms, status=HTTP 204)
21. `AKUN-022-CLOUDFLARE-VLESS-WS-133MS` (url=387ms, status=HTTP 204)
22. `AKUN-023-UNKNOWN-VLESS-WS-128MS` (url=1390ms, status=HTTP 204)
23. `AKUN-001-DIGITALOCEAN-VLESS-WS-125MS`
24. `AKUN-005-ACE-SG-VLESS-WS-119MS`
25. `AKUN-004-CLOUDFLARE-VLESS-WS-121MS`
26. `AKUN-027-SDCL-TW-NET-VLESS-WS-121MS` (url=388ms, status=HTTP 204)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-186MS` (url=559ms, status=HTTP 204)
28. `AKUN-029-AMAZON-VLESS-WS-385MS` (url=1301ms, status=HTTP 204)
29. `AKUN-035-CLOUDFLARE-VLESS-WS-723MS` (url=1092ms, status=HTTP 204)
30. `AKUN-009-NET-147-90-26-0-24-VLESS-WS-131MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
