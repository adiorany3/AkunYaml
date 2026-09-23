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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-001-INTERNETWORKS-45-131-6-0-VLESS-WS-113MS` (url=395ms, status=HTTP 204)
2. `AKUN-004-AEZA-NETWORK-VLESS-WS-121MS`
3. `AKUN-007-UNKNOWN-VLESS-WS-110MS`
4. `AKUN-004-IPOWERWEB-NET-VLESS-WS-108MS` (url=395ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-116MS` (url=386ms, status=HTTP 204)
6. `AKUN-003-CLOUDFLARE-VLESS-WS-123MS`
7. `AKUN-001-CY-ANNETEN-19971112-VLESS-WS-114MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-119MS` (url=900ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-120MS` (url=424ms, status=HTTP 204)
10. `AKUN-005-CLOUDFLARE-VLESS-WS-126MS`
11. `AKUN-011-CLOUDFLARE-VLESS-WS-122MS` (url=398ms, status=HTTP 204)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-127MS` (url=400ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-125MS` (url=1396ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-132MS` (url=1402ms, status=HTTP 204)
15. `AKUN-015-UNKNOWN-VLESS-WS-130MS` (url=1380ms, status=HTTP 204)
16. `AKUN-016-SPEEDTEST-VLESS-WS-141MS` (url=390ms, status=HTTP 204)
17. `AKUN-017-UNKNOWN-VLESS-WS-132MS` (url=1384ms, status=HTTP 204)
18. `AKUN-018-CLOUDFLARE-VLESS-WS-150MS` (url=413ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-129MS` (url=408ms, status=HTTP 204)
20. `AKUN-021-CLOUDFLARE-VLESS-WS-144MS` (url=403ms, status=HTTP 204)
21. `AKUN-008-MEDIUM-VLESS-WS-137MS`
22. `AKUN-023-AIMALL-VLESS-WS-134MS` (url=385ms, status=HTTP 204)
23. `AKUN-006-RS-RAPIDSEEDBOX-20190717-VLESS-WS-138MS`
24. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-133MS`
25. `AKUN-026-UNKNOWN-VLESS-WS-136MS` (url=388ms, status=HTTP 204)
26. `AKUN-027-UNKNOWN-VLESS-WS-138MS` (url=372ms, nekobox=6181ms, status=no)
27. `AKUN-028-CLOUDFLARE-VLESS-WS-131MS` (url=407ms, status=HTTP 204)
28. `AKUN-029-UNKNOWN-VLESS-WS-135MS` (url=400ms, status=HTTP 204)
29. `AKUN-009-UNKNOWN-VLESS-WS-131MS`
30. `AKUN-031-CLOUDFLARE-VLESS-WS-126MS` (url=1410ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
