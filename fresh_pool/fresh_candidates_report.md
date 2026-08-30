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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-112MS` (url=342ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-120MS` (url=1339ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-105MS` (url=380ms, status=HTTP 204)
4. `AKUN-004-DEV-VLESS-WS-134MS`
5. `AKUN-005-RESERVED-FOR-TW-VLESS-WS-134MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-164MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-346MS`
8. `AKUN-008-PAGM-NET-VLESS-WS-499MS`
9. `AKUN-009-NETCRAFTERS-VLESS-WS-465MS`
10. `AKUN-010-JIKECLOUD-VLESS-WS-431MS`
11. `AKUN-017-UNKNOWN-VLESS-WS-386MS` (url=3759ms, status=HTTP 204)
12. `AKUN-024-UNKNOWN-VLESS-WS-777MS` (url=1292ms, status=HTTP 204)
13. `AKUN-028-UNKNOWN-VLESS-WS-798MS` (url=2461ms, status=HTTP 204)
14. `AKUN-030-UNKNOWN-VLESS-WS-807MS` (url=1506ms, status=HTTP 204)
15. `AKUN-035-CLOUDFLARE-VLESS-WS-851MS` (url=2711ms, status=HTTP 204)
16. `AKUN-036-CLOUDFLARE-VLESS-WS-877MS` (url=2520ms, status=HTTP 204)
17. `AKUN-039-NET-151-242-2-0-24-VLESS-WS-805MS` (url=1556ms, status=HTTP 204)
18. `AKUN-040-UNKNOWN-VLESS-WS-1136MS` (url=1838ms, status=HTTP 204)
19. `AKUN-041-JIKECLOUD-VLESS-WS-1106MS` (url=2351ms, status=HTTP 204)
20. `AKUN-042-PAGM-NET-VLESS-WS-519MS` (url=2220ms, status=HTTP 204)
21. `AKUN-045-H2NEXUS-VLESS-WS-740MS` (url=2571ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
