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
- Kandidat strict NekoBox-tested: 8
- Proxy di openclash_fresh_pool.yaml: 15

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
1. `AKUN-005-CLOUDFLARE-VLESS-WS-125MS`
2. `AKUN-004-CLOUDFLARE-VLESS-WS-279MS` (url=341ms, nekobox=420ms, status=no)
3. `AKUN-006-CLOUDFLARE-VLESS-WS-437MS` (url=522ms, nekobox=408ms, status=yes)
4. `AKUN-007-CLOUDFLARE-VLESS-WS-298MS` (url=767ms, nekobox=1265ms, status=no)
5. `AKUN-008-MEDIUM-VLESS-WS-298MS` (url=584ms, nekobox=407ms, status=yes)
6. `AKUN-004-BIGCOMMERCE-VLESS-WS-305MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-703MS`
8. `AKUN-002-RS-RAPIDSEEDBOX-20190717-VLESS-WS-1164MS`
9. `AKUN-014-CLOUDFLARE-VLESS-WS-913MS` (url=5263ms, status=HTTP 204)
10. `AKUN-003-CLOUDFLARE-VLESS-WS-277MS`
11. `AKUN-001-CLOUDFLARE-VLESS-WS-249MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
