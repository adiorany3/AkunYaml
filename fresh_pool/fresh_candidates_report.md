# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 11
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 14

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-115MS` (url=381ms, status=HTTP 204)
2. `AKUN-002-ALIBABA-VLESS-WS-112MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-498MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-653MS`
7. `AKUN-007-NETCRAFTERS-VLESS-WS-469MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-841MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-121MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-107MS`
11. `AKUN-050-RTXCONFIGZ-VLESS-WS-1076MS` (url=3112ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
