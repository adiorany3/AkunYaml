# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 16
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 19

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-107MS` (url=366ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-109MS` (url=367ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-109MS` (url=334ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-117MS` (url=320ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-101MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-107MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-127MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-100MS`
9. `AKUN-009-AKARI-JP-TYO1-09-VLESS-WS-116MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-104MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-105MS` (url=374ms, status=HTTP 204)
12. `AKUN-015-CLOUDFLARE-VLESS-WS-119MS` (url=368ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-115MS` (url=342ms, status=HTTP 204)
14. `AKUN-018-UNKNOWN-VLESS-WS-390MS` (url=1379ms, status=HTTP 204)
15. `AKUN-019-NETCRAFTERS-VLESS-WS-466MS` (url=3089ms, status=HTTP 204)
16. `AKUN-058-CLOUDFLARE-VLESS-WS-805MS` (url=3469ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
