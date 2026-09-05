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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-105MS` (url=364ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=347ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS` (url=354ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-110MS` (url=360ms, status=HTTP 204)
5. `AKUN-005-AKARI-JP-TYO1-09-VLESS-WS-115MS` (url=379ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-115MS` (url=338ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-115MS` (url=351ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-120MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-127MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-118MS`
11. `AKUN-017-UNKNOWN-VLESS-WS-393MS` (url=2421ms, status=HTTP 204)
12. `AKUN-039-CLOUDFLARE-VLESS-WS-121MS` (url=373ms, status=HTTP 204)
13. `AKUN-040-CLOUDFLARE-VLESS-WS-126MS` (url=380ms, status=HTTP 204)
14. `AKUN-041-CLOUDFLARE-VLESS-WS-114MS` (url=348ms, status=HTTP 204)
15. `AKUN-042-CLOUDFLARE-VLESS-WS-115MS` (url=340ms, status=HTTP 204)
16. `AKUN-043-CLOUDFLARE-VLESS-WS-113MS` (url=370ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
