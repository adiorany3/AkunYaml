# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 21
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 25

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
1. `AKUN-001-DEV-VLESS-WS-117MS` (url=356ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-117MS` (url=348ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-126MS` (url=321ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-130MS` (url=1364ms, status=HTTP 204)
5. `AKUN-005-RESERVED-FOR-TW-VLESS-WS-134MS` (url=346ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-324MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-408MS`
8. `AKUN-008-NETCRAFTERS-VLESS-WS-469MS`
9. `AKUN-009-PAGM-NET-VLESS-WS-452MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-867MS`
11. `AKUN-026-CLOUDFLARE-VLESS-WS-882MS` (url=2594ms, status=HTTP 204)
12. `AKUN-031-JIKECLOUD-VLESS-WS-525MS` (url=1880ms, status=HTTP 204)
13. `AKUN-032-CLOUDFLARE-VLESS-WS-170MS` (url=1109ms, status=HTTP 204)
14. `AKUN-033-UNKNOWN-VLESS-WS-1150MS` (url=2864ms, status=HTTP 204)
15. `AKUN-034-PAGM-NET-VLESS-WS-369MS` (url=1333ms, status=HTTP 204)
16. `AKUN-035-JIKECLOUD-VLESS-WS-1185MS` (url=2281ms, status=HTTP 204)
17. `AKUN-036-CLOUDFLARE-VLESS-WS-1167MS` (url=1614ms, status=HTTP 204)
18. `AKUN-040-H2NEXUS-VLESS-WS-791MS` (url=1359ms, status=HTTP 204)
19. `AKUN-041-UNKNOWN-VLESS-WS-824MS` (url=1610ms, status=HTTP 204)
20. `AKUN-042-CLOUDFLARE-VLESS-WS-905MS` (url=1464ms, status=HTTP 204)
21. `AKUN-043-UNKNOWN-VLESS-WS-1799MS` (url=1171ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
