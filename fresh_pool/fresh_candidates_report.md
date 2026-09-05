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
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 22

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS` (url=372ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-112MS` (url=337ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-109MS` (url=340ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-110MS` (url=374ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-106MS` (url=361ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-110MS` (url=349ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-98MS` (url=379ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-114MS` (url=350ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-106MS` (url=379ms, status=HTTP 204)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-120MS` (url=359ms, status=HTTP 204)
11. `AKUN-012-CLOUDFLARE-VLESS-WS-114MS` (url=354ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-118MS` (url=359ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-113MS` (url=370ms, status=HTTP 204)
14. `AKUN-021-CLOUDFLARE-VLESS-WS-839MS` (url=1582ms, status=HTTP 204)
15. `AKUN-044-ALIBABA-VLESS-WS-107MS` (url=1382ms, status=HTTP 204)
16. `AKUN-045-CLOUDFLARE-VLESS-WS-124MS` (url=1340ms, status=HTTP 204)
17. `AKUN-052-CLOUDFLARE-VLESS-WS-392MS` (url=1233ms, status=HTTP 204)
18. `AKUN-059-NETCRAFTERS-VLESS-WS-476MS` (url=1064ms, status=HTTP 204)
19. `AKUN-060-RTXCONFIGZ-VLESS-WS-1091MS` (url=3109ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
