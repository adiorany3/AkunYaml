# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 10
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 13

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-106MS` (url=356ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-110MS` (url=319ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-115MS` (url=1370ms, status=HTTP 204)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-104MS` (url=340ms, status=HTTP 204)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-116MS` (url=331ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-375MS` (url=758ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-504MS`
8. `AKUN-008-NETCRAFTERS-VLESS-WS-455MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-855MS`
10. `AKUN-010-ALIBABA-VLESS-WS-106MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
