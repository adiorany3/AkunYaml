# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 22
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 26

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-123MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-138MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-132MS`
4. `AKUN-004-DEV-VLESS-WS-133MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-336MS`
6. `AKUN-006-PAGM-NET-VLESS-WS-589MS`
7. `AKUN-007-PAGM-NET-VLESS-WS-599MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-691MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-405MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-774MS`
11. `AKUN-026-UNKNOWN-VLESS-WS-797MS` (url=1234ms, status=HTTP 204)
12. `AKUN-030-CLOUDFLARE-VLESS-WS-135MS` (url=393ms, status=HTTP 204)
13. `AKUN-032-CLOUDFLARE-VLESS-WS-136MS` (url=388ms, status=HTTP 204)
14. `AKUN-033-UNKNOWN-VLESS-WS-183MS` (url=413ms, status=HTTP 204)
15. `AKUN-034-DEV-VLESS-WS-190MS` (url=1337ms, status=HTTP 204)
16. `AKUN-036-IQIRAQ-VLESS-WS-1026MS` (url=1866ms, status=HTTP 204)
17. `AKUN-037-UNKNOWN-VLESS-WS-172MS` (url=699ms, status=HTTP 204)
18. `AKUN-039-UNKNOWN-VLESS-WS-1197MS` (url=1851ms, status=HTTP 204)
19. `AKUN-040-NETCRAFTERS-VLESS-WS-594MS` (url=1179ms, status=HTTP 204)
20. `AKUN-041-JIKECLOUD-VLESS-WS-1136MS` (url=2229ms, status=HTTP 204)
21. `AKUN-047-CLOUDFLARE-VLESS-WS-885MS` (url=1562ms, status=HTTP 204)
22. `AKUN-048-UNKNOWN-VLESS-WS-1093MS` (url=2014ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
