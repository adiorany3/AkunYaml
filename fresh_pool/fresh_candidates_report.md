# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 19
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 23

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-133MS`
2. `AKUN-002-DEV-VLESS-WS-141MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-129MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-139MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-145MS`
6. `AKUN-006-RESERVED-FOR-TW-VLESS-WS-127MS`
7. `AKUN-007-PAGM-NET-VLESS-WS-556MS`
8. `AKUN-008-PAGM-NET-VLESS-WS-575MS`
9. `AKUN-009-NETCRAFTERS-VLESS-WS-574MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-447MS`
11. `AKUN-016-CLOUDFLARE-VLESS-WS-698MS` (url=1343ms, status=HTTP 204)
12. `AKUN-017-CLOUDFLARE-VLESS-WS-727MS` (url=2248ms, status=HTTP 204)
13. `AKUN-022-IQIRAQ-VLESS-WS-800MS` (url=2086ms, status=HTTP 204)
14. `AKUN-024-UNKNOWN-VLESS-WS-837MS` (url=2099ms, status=HTTP 204)
15. `AKUN-033-UNKNOWN-VLESS-WS-1250MS` (url=1940ms, status=HTTP 204)
16. `AKUN-035-JIKECLOUD-VLESS-WS-1190MS` (url=2931ms, status=HTTP 204)
17. `AKUN-038-UNKNOWN-VLESS-WS-887MS` (url=2225ms, status=HTTP 204)
18. `AKUN-039-CLOUDFLARE-VLESS-WS-879MS` (url=1684ms, status=HTTP 204)
19. `AKUN-041-UNKNOWN-VLESS-WS-185MS` (url=1862ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
