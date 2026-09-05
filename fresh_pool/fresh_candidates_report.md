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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-113MS` (url=371ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-103MS` (url=1377ms, status=HTTP 204)
3. `AKUN-003-AKARI-JP-TYO1-09-VLESS-WS-106MS` (url=361ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS` (url=300ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-123MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-121MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-117MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-111MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-122MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-120MS` (url=360ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-121MS` (url=317ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-115MS` (url=361ms, status=HTTP 204)
14. `AKUN-022-CLOUDFLARE-VLESS-WS-110MS` (url=332ms, status=HTTP 204)
15. `AKUN-034-CLOUDFLARE-VLESS-WS-366MS` (url=1640ms, status=HTTP 204)
16. `AKUN-056-CLOUDFLARE-VLESS-WS-776MS` (url=3612ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
