# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 12
- Kandidat strict NekoBox-tested: 6
- Proxy di openclash_fresh_pool.yaml: 16

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-108MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-98MS`
3. `AKUN-004-CLOUDFLARE-VLESS-WS-112MS` (url=360ms, nekobox=1418ms, status=yes)
4. `AKUN-005-NET-83-147-12-0-22-VLESS-WS-112MS` (url=353ms, nekobox=6177ms, status=no)
5. `AKUN-003-CLOUDFLARE-VLESS-WS-122MS`
6. `AKUN-007-CLOUDFLARE-VLESS-WS-114MS` (url=380ms, nekobox=6179ms, status=no)
7. `AKUN-008-CLOUDFLARE-VLESS-WS-115MS` (url=361ms, nekobox=6173ms, status=no)
8. `AKUN-011-CLOUDFLARE-VLESS-WS-122MS` (url=2271ms, status=HTTP 204)
9. `AKUN-012-OVH-VLESS-WS-605MS` (url=2149ms, status=HTTP 204)
10. `AKUN-005-CLOUDFLARE-VLESS-WS-839MS`
11. `AKUN-055-UNKNOWN-VLESS-WS-370MS` (url=763ms, nekobox=1352ms, status=no)
12. `AKUN-006-CLOUDFLARE-VLESS-WS-1174MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
