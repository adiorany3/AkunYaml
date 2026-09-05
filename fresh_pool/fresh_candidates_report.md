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
- Kandidat strict NekoBox-tested: 0
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS` (url=380ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-103MS` (url=352ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-104MS` (url=368ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-119MS` (url=363ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-110MS` (url=396ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-100MS` (url=372ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-117MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-127MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-104MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-105MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-111MS` (url=338ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-127MS` (url=385ms, status=HTTP 204)
13. `AKUN-014-ALIBABA-VLESS-WS-117MS` (url=1363ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-114MS` (url=359ms, status=HTTP 204)
15. `AKUN-016-UNKNOWN-VLESS-WS-371MS` (url=1130ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-503MS` (url=1053ms, status=HTTP 204)
17. `AKUN-033-CLOUDFLARE-VLESS-WS-826MS` (url=1552ms, status=HTTP 204)
18. `AKUN-044-CLOUDFLARE-VLESS-WS-116MS` (url=392ms, status=HTTP 204)
19. `AKUN-045-CLOUDFLARE-VLESS-WS-118MS` (url=321ms, status=HTTP 204)
20. `AKUN-058-NETCRAFTERS-VLESS-WS-462MS` (url=1022ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
