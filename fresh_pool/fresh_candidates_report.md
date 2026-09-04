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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-105MS` (url=379ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-112MS` (url=380ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=338ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS` (url=311ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-114MS` (url=310ms, status=HTTP 204)
6. `AKUN-006-AKARI-JP-TYO1-09-VLESS-WS-106MS` (url=374ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-123MS` (url=367ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-116MS` (url=378ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-115MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-118MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-108MS` (url=349ms, status=HTTP 204)
12. `AKUN-014-CLOUDINARY-VLESS-WS-119MS` (url=371ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-124MS` (url=1385ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-118MS` (url=334ms, status=HTTP 204)
15. `AKUN-017-UNKNOWN-VLESS-WS-386MS` (url=729ms, status=HTTP 204)
16. `AKUN-031-CLOUDFLARE-VLESS-WS-115MS` (url=310ms, status=HTTP 204)
17. `AKUN-032-CLOUDFLARE-VLESS-WS-116MS` (url=340ms, status=HTTP 204)
18. `AKUN-047-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=371ms, status=HTTP 204)
19. `AKUN-057-CLOUDFLARE-VLESS-WS-843MS` (url=5696ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
