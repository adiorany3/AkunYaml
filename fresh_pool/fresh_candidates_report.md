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
1. `AKUN-001-RESERVED-FOR-TW-VLESS-WS-145MS`
2. `AKUN-002-DEV-VLESS-WS-199MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-193MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-220MS`
5. `AKUN-005-NETCRAFTERS-VLESS-WS-495MS`
6. `AKUN-006-PAGM-NET-VLESS-WS-563MS`
7. `AKUN-007-PAGM-NET-VLESS-WS-560MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-442MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-701MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-924MS`
11. `AKUN-027-INTERLIR-CUSTOMER-VLESS-WS-943MS` (url=1703ms, status=HTTP 204)
12. `AKUN-028-CLOUDFLARE-VLESS-WS-182MS` (url=431ms, status=HTTP 204)
13. `AKUN-031-DEV-VLESS-WS-211MS` (url=494ms, status=HTTP 204)
14. `AKUN-032-CLOUDFLARE-VLESS-WS-212MS` (url=375ms, status=HTTP 204)
15. `AKUN-033-CLOUDFLARE-VLESS-WS-212MS` (url=859ms, status=HTTP 204)
16. `AKUN-034-IQIRAQ-VLESS-WS-936MS` (url=2692ms, status=HTTP 204)
17. `AKUN-035-UNKNOWN-VLESS-WS-970MS` (url=2566ms, status=HTTP 204)
18. `AKUN-036-UNKNOWN-VLESS-WS-1176MS` (url=4089ms, status=HTTP 204)
19. `AKUN-038-JIKECLOUD-VLESS-WS-1124MS` (url=3092ms, status=HTTP 204)
20. `AKUN-043-NET-151-242-2-0-24-VLESS-WS-793MS` (url=2966ms, status=HTTP 204)
21. `AKUN-044-CLOUDFLARE-VLESS-WS-1797MS` (url=4569ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
