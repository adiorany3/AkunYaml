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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-146MS` (url=397ms, status=HTTP 204)
2. `AKUN-002-RESERVED-FOR-TW-VLESS-WS-138MS` (url=359ms, status=HTTP 204)
3. `AKUN-003-DEV-VLESS-WS-134MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-127MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-134MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-187MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-368MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-404MS`
9. `AKUN-009-NETCRAFTERS-VLESS-WS-467MS`
10. `AKUN-010-PAGM-NET-VLESS-WS-555MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-704MS` (url=1301ms, status=HTTP 204)
12. `AKUN-017-NET-151-242-2-0-24-VLESS-WS-743MS` (url=1319ms, status=HTTP 204)
13. `AKUN-023-CLOUDFLARE-VLESS-WS-837MS` (url=2424ms, status=HTTP 204)
14. `AKUN-025-DEV-VLESS-WS-143MS` (url=359ms, status=HTTP 204)
15. `AKUN-026-CLOUDFLARE-VLESS-WS-153MS` (url=350ms, status=HTTP 204)
16. `AKUN-028-UNKNOWN-VLESS-WS-1135MS` (url=1904ms, status=HTTP 204)
17. `AKUN-029-JIKECLOUD-VLESS-WS-708MS` (url=2418ms, status=HTTP 204)
18. `AKUN-030-PAGM-NET-VLESS-WS-519MS` (url=1231ms, status=HTTP 204)
19. `AKUN-039-UNKNOWN-VLESS-WS-841MS` (url=1169ms, status=HTTP 204)
20. `AKUN-041-UNKNOWN-VLESS-WS-855MS` (url=1724ms, status=HTTP 204)
21. `AKUN-042-UNKNOWN-VLESS-WS-837MS` (url=1477ms, status=HTTP 204)
22. `AKUN-043-CLOUDFLARE-VLESS-WS-1204MS` (url=4592ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
