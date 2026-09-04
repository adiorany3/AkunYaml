# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 18
- Kandidat strict NekoBox-tested: 10
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-102MS` (url=361ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-117MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-117MS` (url=321ms, status=HTTP 204)
4. `AKUN-004-DEV-VLESS-WS-113MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-117MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-121MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-102MS`
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-116MS`
9. `AKUN-009-AKARI-JP-TYO1-09-VLESS-WS-111MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-101MS`
11. `AKUN-013-CLOUDFLARE-VLESS-WS-122MS` (url=358ms, status=HTTP 204)
12. `AKUN-016-UNKNOWN-VLESS-WS-390MS` (url=1750ms, status=HTTP 204)
13. `AKUN-028-CLOUDFLARE-VLESS-WS-112MS` (url=343ms, status=HTTP 204)
14. `AKUN-029-CLOUDINARY-VLESS-WS-129MS` (url=400ms, status=HTTP 204)
15. `AKUN-030-CLOUDFLARE-VLESS-WS-113MS` (url=358ms, status=HTTP 204)
16. `AKUN-031-CLOUDFLARE-VLESS-WS-119MS` (url=350ms, status=HTTP 204)
17. `AKUN-033-CLOUDFLARE-VLESS-WS-124MS` (url=385ms, status=HTTP 204)
18. `AKUN-058-CLOUDFLARE-VLESS-WS-116MS` (url=1381ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
