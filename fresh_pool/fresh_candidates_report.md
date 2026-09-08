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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-006-TENCENT-VLESS-WS-113MS`
2. `AKUN-005-CLOUDFLARE-VLESS-WS-116MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-108MS` (url=371ms, nekobox=6179ms, status=no)
4. `AKUN-003-UNKNOWN-VLESS-WS-110MS`
5. `AKUN-001-UNKNOWN-VLESS-WS-120MS`
6. `AKUN-008-CLOUDFLARE-VLESS-WS-361MS` (url=789ms, nekobox=1177ms, status=yes)
7. `AKUN-009-DE-VLESS-WS-690MS`
8. `AKUN-002-CLOUDFLARE-VLESS-WS-110MS`
9. `AKUN-007-CLOUDFLARE-VLESS-WS-137MS`
10. `AKUN-004-466688-VLESS-WS-154MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
