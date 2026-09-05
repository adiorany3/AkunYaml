# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 8
- Kandidat strict NekoBox-tested: 0
- Proxy di openclash_fresh_pool.yaml: 11

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-113MS` (url=385ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-116MS` (url=319ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-116MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-111MS`
5. `AKUN-005-AKARI-JP-TYO1-09-VLESS-WS-116MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-365MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-124MS`
8. `AKUN-008-NETCRAFTERS-VLESS-WS-475MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
