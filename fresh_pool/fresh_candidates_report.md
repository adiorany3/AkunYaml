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
1. `AKUN-001-UNKNOWN-VLESS-WS-110MS` (url=373ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-109MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-116MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-111MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-123MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-112MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-111MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-114MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-114MS` (url=356ms, status=HTTP 204)
12. `AKUN-013-CLOUDFLARE-VLESS-WS-126MS` (url=1362ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-112MS` (url=321ms, status=HTTP 204)
14. `AKUN-015-CLOUDFLARE-VLESS-WS-126MS` (url=347ms, status=HTTP 204)
15. `AKUN-016-NETCRAFTERS-VLESS-WS-454MS` (url=1013ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-500MS` (url=1111ms, status=HTTP 204)
17. `AKUN-022-CLOUDFLARE-VLESS-WS-828MS` (url=1595ms, status=HTTP 204)
18. `AKUN-042-UNKNOWN-VLESS-WS-371MS` (url=1875ms, status=HTTP 204)
19. `AKUN-044-ALIBABA-VLESS-WS-130MS` (url=371ms, status=HTTP 204)
20. `AKUN-046-CLOUDFLARE-VLESS-WS-117MS` (url=354ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
