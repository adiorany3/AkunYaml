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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-104MS` (url=371ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-110MS` (url=350ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=331ms, status=HTTP 204)
4. `AKUN-004-AKARI-JP-TYO1-09-VLESS-WS-114MS` (url=379ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-113MS` (url=311ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-116MS` (url=347ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-117MS` (url=365ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-115MS` (url=365ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-111MS`
10. `AKUN-010-CLOUDINARY-VLESS-WS-115MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-114MS` (url=389ms, status=HTTP 204)
12. `AKUN-013-UNKNOWN-VLESS-WS-361MS` (url=994ms, status=HTTP 204)
13. `AKUN-015-CLOUDFLARE-VLESS-WS-107MS` (url=323ms, status=HTTP 204)
14. `AKUN-017-CLOUDFLARE-VLESS-WS-118MS` (url=370ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-862MS` (url=2390ms, status=HTTP 204)
16. `AKUN-030-CLOUDFLARE-VLESS-WS-114MS` (url=339ms, status=HTTP 204)
17. `AKUN-031-CLOUDFLARE-VLESS-WS-121MS` (url=339ms, status=HTTP 204)
18. `AKUN-032-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-115MS` (url=361ms, status=HTTP 204)
19. `AKUN-033-CLOUDFLARE-VLESS-WS-121MS` (url=348ms, status=HTTP 204)
20. `AKUN-034-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-151MS` (url=319ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
