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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-106MS` (url=364ms, status=HTTP 204)
2. `AKUN-002-ALIBABA-VLESS-WS-118MS` (url=376ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-120MS` (url=369ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-115MS` (url=384ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-120MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-127MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-118MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-107MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-106MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-105MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-117MS` (url=1388ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-115MS` (url=362ms, status=HTTP 204)
13. `AKUN-019-CLOUDFLARE-VLESS-WS-371MS` (url=1414ms, status=HTTP 204)
14. `AKUN-020-UNKNOWN-VLESS-WS-839MS` (url=1610ms, status=HTTP 204)
15. `AKUN-040-CLOUDFLARE-VLESS-WS-127MS` (url=1380ms, status=HTTP 204)
16. `AKUN-041-CLOUDFLARE-VLESS-WS-112MS` (url=340ms, status=HTTP 204)
17. `AKUN-042-CLOUDFLARE-VLESS-WS-136MS` (url=390ms, status=HTTP 204)
18. `AKUN-043-CLOUDFLARE-VLESS-WS-123MS` (url=319ms, status=HTTP 204)
19. `AKUN-055-NETCRAFTERS-VLESS-WS-463MS` (url=1211ms, status=HTTP 204)
20. `AKUN-056-CLOUDFLARE-VLESS-WS-535MS` (url=1079ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
