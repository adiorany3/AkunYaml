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
1. `AKUN-001-VULTR-VLESS-WS-117MS` (url=550ms, status=HTTP 204)
2. `AKUN-002-NET-147-90-26-0-24-VLESS-WS-125MS` (url=750ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-138MS` (url=470ms, nekobox=461ms, status=no)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-149MS` (url=712ms, status=HTTP 204)
5. `AKUN-005-NET-147-90-26-0-24-VLESS-WS-131MS` (url=716ms, status=HTTP 204)
6. `AKUN-001-CLOUDFLARE-VLESS-WS-129MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-131MS` (url=676ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-138MS` (url=530ms, status=HTTP 204)
9. `AKUN-009-PMBET-NET-VLESS-WS-172MS` (url=554ms, status=HTTP 204)
10. `AKUN-009-ZUOAI-VLESS-WS-179MS`
11. `AKUN-011-UNKNOWN-VLESS-WS-126MS` (url=559ms, status=HTTP 204)
12. `AKUN-006-CLOUDFLARE-VLESS-WS-133MS`
13. `AKUN-013-CLOUDFLARE-VLESS-WS-110MS` (url=591ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-160MS` (url=553ms, status=HTTP 204)
15. `AKUN-007-CLOUDFLARE-VLESS-WS-135MS`
16. `AKUN-016-DEV-VLESS-WS-117MS` (url=534ms, status=HTTP 204)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-115MS` (url=641ms, status=HTTP 204)
18. `AKUN-018-NASEEJ-VLESS-WS-205MS` (url=617ms, status=HTTP 204)
19. `AKUN-004-UNKNOWN-VLESS-WS-211MS`
20. `AKUN-002-CLOUDFLARE-VLESS-WS-133MS`
21. `AKUN-021-CLOUDFLARE-VLESS-WS-135MS` (url=718ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-140MS` (url=694ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-139MS` (url=532ms, status=HTTP 204)
24. `AKUN-005-CLOUDFLARE-VLESS-WS-181MS`
25. `AKUN-025-DEV-VLESS-WS-174MS` (url=539ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-164MS` (url=579ms, status=HTTP 204)
27. `AKUN-008-CLOUDFLARE-VLESS-WS-209MS`
28. `AKUN-003-MEDIUM-VLESS-WS-124MS`
29. `AKUN-029-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-137MS` (url=868ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-214MS` (url=730ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
