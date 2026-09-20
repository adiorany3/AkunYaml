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
1. `AKUN-001-CY-ANNETEN-19971112-VLESS-WS-105MS` (url=385ms, status=HTTP 204)
2. `AKUN-002-NET-147-90-26-0-24-VLESS-WS-110MS` (url=384ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-121MS` (url=405ms, status=HTTP 204)
4. `AKUN-004-CY-ANNETEN-19971112-VLESS-WS-122MS` (url=395ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-118MS` (url=1376ms, status=HTTP 204)
6. `AKUN-006-PMBET-NET-VLESS-WS-111MS` (url=381ms, status=HTTP 204)
7. `AKUN-007-OLOIN-1-VLESS-WS-115MS` (url=377ms, nekobox=409ms, status=yes)
8. `AKUN-005-DIGITALOCEAN-VLESS-WS-122MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-118MS` (url=413ms, status=HTTP 204)
10. `AKUN-002-CLOUDFLARE-VLESS-WS-131MS`
11. `AKUN-008-CLOUDFLARE-VLESS-WS-123MS`
12. `AKUN-012-SDCL-TW-NET-VLESS-WS-123MS` (url=403ms, status=HTTP 204)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-119MS` (url=439ms, status=HTTP 204)
14. `AKUN-014-TYCHRON-02-VLESS-WS-134MS` (url=386ms, status=HTTP 204)
15. `AKUN-015-NASEEJ-VLESS-WS-135MS` (url=419ms, status=HTTP 204)
16. `AKUN-010-CLOUDFLARE-VLESS-WS-128MS`
17. `AKUN-017-ALIBABA-VLESS-WS-118MS` (url=392ms, status=HTTP 204)
18. `AKUN-001-ACE-SG-VLESS-WS-126MS`
19. `AKUN-019-CLOUDFLARE-VLESS-WS-123MS` (url=1410ms, status=HTTP 204)
20. `AKUN-020-TYCHRON-02-VLESS-WS-134MS` (url=400ms, status=HTTP 204)
21. `AKUN-004-CLOUDFLARE-VLESS-WS-148MS`
22. `AKUN-003-CLOUDFLARE-VLESS-WS-122MS`
23. `AKUN-024-CLOUDFLARE-VLESS-WS-128MS` (url=394ms, status=HTTP 204)
24. `AKUN-025-CLOUDFLARE-VLESS-WS-175MS` (url=417ms, status=HTTP 204)
25. `AKUN-026-UNKNOWN-VLESS-WS-119MS` (url=1371ms, status=HTTP 204)
26. `AKUN-027-LUCIDACLOUD-VLESS-WS-138MS` (url=418ms, status=HTTP 204)
27. `AKUN-006-TYCHRON-02-VLESS-WS-136MS`
28. `AKUN-029-UNKNOWN-VLESS-WS-302MS` (url=3620ms, status=HTTP 204)
29. `AKUN-030-UNKNOWN-VLESS-WS-235MS` (url=778ms, status=HTTP 204)
30. `AKUN-009-NET-147-90-26-0-24-VLESS-WS-125MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
