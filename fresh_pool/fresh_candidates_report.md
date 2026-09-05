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
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 21

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
1. `AKUN-001-UNKNOWN-VLESS-WS-109MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-107MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-106MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-108MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-112MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-106MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-121MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-121MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-108MS`
11. `AKUN-014-CLOUDFLARE-VLESS-WS-115MS` (url=361ms, status=HTTP 204)
12. `AKUN-016-CLOUDFLARE-VLESS-WS-108MS` (url=301ms, status=HTTP 204)
13. `AKUN-017-AKARI-JP-TYO1-09-VLESS-WS-115MS` (url=390ms, status=HTTP 204)
14. `AKUN-018-CLOUDFLARE-VLESS-WS-124MS` (url=364ms, status=HTTP 204)
15. `AKUN-019-CLOUDFLARE-VLESS-WS-124MS` (url=332ms, status=HTTP 204)
16. `AKUN-020-NETCRAFTERS-VLESS-WS-478MS` (url=999ms, status=HTTP 204)
17. `AKUN-044-UNKNOWN-VLESS-WS-704MS` (url=2394ms, status=HTTP 204)
18. `AKUN-047-CLOUDFLARE-VLESS-WS-114MS` (url=343ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
