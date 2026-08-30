# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 20
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 24

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-121MS` (url=384ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-124MS`
3. `AKUN-003-RESERVED-FOR-TW-VLESS-WS-117MS`
4. `AKUN-004-NETCRAFTERS-VLESS-WS-519MS`
5. `AKUN-005-H2NEXUS-VLESS-WS-732MS`
6. `AKUN-006-NET-151-242-2-0-24-VLESS-WS-778MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-851MS`
8. `AKUN-008-IQIRAQ-VLESS-WS-929MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-124MS`
10. `AKUN-010-JIKECLOUD-VLESS-WS-616MS`
11. `AKUN-032-JIKECLOUD-VLESS-WS-1105MS` (url=1929ms, status=HTTP 204)
12. `AKUN-033-UNKNOWN-VLESS-WS-1165MS` (url=1858ms, status=HTTP 204)
13. `AKUN-034-CLOUDFLARE-VLESS-WS-877MS` (url=1643ms, status=HTTP 204)
14. `AKUN-035-PAGM-NET-VLESS-WS-525MS` (url=1429ms, status=HTTP 204)
15. `AKUN-036-PAGM-NET-VLESS-WS-524MS` (url=1399ms, status=HTTP 204)
16. `AKUN-037-CLOUDFLARE-VLESS-WS-1383MS` (url=3522ms, status=HTTP 204)
17. `AKUN-043-UNKNOWN-VLESS-WS-815MS` (url=2243ms, status=HTTP 204)
18. `AKUN-044-CLOUDFLARE-VLESS-WS-250MS` (url=379ms, status=HTTP 204)
19. `AKUN-045-UNKNOWN-VLESS-WS-425MS` (url=1100ms, status=HTTP 204)
20. `AKUN-046-UNKNOWN-VLESS-WS-848MS` (url=1840ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
