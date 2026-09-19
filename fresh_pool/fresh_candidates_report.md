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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-112MS` (url=414ms, status=HTTP 204)
2. `AKUN-002-NET-147-90-26-0-24-VLESS-WS-134MS` (url=432ms, status=HTTP 204)
3. `AKUN-003-VULTR-VLESS-WS-132MS` (url=473ms, status=HTTP 204)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-131MS` (url=448ms, status=HTTP 204)
5. `AKUN-008-DEV-VLESS-WS-154MS`
6. `AKUN-007-CLOUDFLARE-VLESS-WS-132MS` (url=374ms, nekobox=601ms, status=no)
7. `AKUN-008-CLOUDFLARE-VLESS-WS-167MS` (url=608ms, status=HTTP 204)
8. `AKUN-007-NET-147-90-26-0-24-VLESS-WS-164MS`
9. `AKUN-010-CLOUDFLARE-VLESS-WS-163MS` (url=441ms, status=HTTP 204)
10. `AKUN-011-CLOUDFLARE-VLESS-WS-126MS` (url=438ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-163MS` (url=545ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-120MS` (url=419ms, status=HTTP 204)
13. `AKUN-014-UNKNOWN-VLESS-WS-171MS` (url=477ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-306MS` (url=918ms, status=HTTP 204)
15. `AKUN-016-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-309MS` (url=558ms, status=HTTP 204)
16. `AKUN-017-TENCENT-VLESS-WS-164MS` (url=422ms, status=HTTP 204)
17. `AKUN-018-CLOUDFLARE-VLESS-WS-178MS` (url=554ms, status=HTTP 204)
18. `AKUN-019-CLOUDFLARE-VLESS-WS-181MS` (url=507ms, status=HTTP 204)
19. `AKUN-006-DEV-VLESS-WS-189MS`
20. `AKUN-003-CLOUDFLARE-VLESS-WS-194MS`
21. `AKUN-005-CLOUDFLARE-VLESS-WS-190MS`
22. `AKUN-001-CLOUDFLARE-VLESS-WS-191MS`
23. `AKUN-024-CLOUDFLARE-VLESS-WS-136MS` (url=405ms, status=HTTP 204)
24. `AKUN-002-CLOUDFLARE-VLESS-WS-290MS`
25. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-135MS` (url=417ms, status=HTTP 204)
26. `AKUN-027-TYCHRON-02-VLESS-WS-286MS` (url=447ms, status=HTTP 204)
27. `AKUN-004-UNKNOWN-VLESS-WS-163MS`
28. `AKUN-029-CLOUDFLARE-VLESS-WS-159MS` (url=416ms, status=HTTP 204)
29. `AKUN-009-UNKNOWN-VLESS-WS-282MS`
30. `AKUN-031-ZUOAI-VLESS-WS-304MS` (url=422ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
