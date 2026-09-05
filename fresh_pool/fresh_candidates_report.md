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
- Kandidat strict NekoBox-tested: 0
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-113MS` (url=323ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-107MS` (url=357ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=380ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-105MS` (url=345ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-108MS` (url=339ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-116MS` (url=368ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-134MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-128MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-114MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-128MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-113MS` (url=360ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-130MS` (url=370ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-114MS` (url=1350ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-116MS` (url=359ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-366MS` (url=1460ms, status=HTTP 204)
16. `AKUN-018-NETCRAFTERS-VLESS-WS-462MS` (url=1222ms, status=HTTP 204)
17. `AKUN-022-CLOUDFLARE-VLESS-WS-815MS` (url=1514ms, status=HTTP 204)
18. `AKUN-050-AKARI-JP-TYO1-09-VLESS-WS-116MS` (url=379ms, status=HTTP 204)
19. `AKUN-051-CLOUDFLARE-VLESS-WS-108MS` (url=331ms, status=HTTP 204)
20. `AKUN-053-RTXCONFIGZ-VLESS-WS-1044MS` (url=4262ms, status=HTTP 204)
21. `AKUN-058-CLOUDFLARE-VLESS-WS-506MS` (url=2114ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
