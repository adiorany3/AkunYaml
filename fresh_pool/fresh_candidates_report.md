# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 17
- Kandidat strict NekoBox-tested: 7
- Proxy di openclash_fresh_pool.yaml: 21

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
1. `AKUN-007-CLOUDFLARE-VLESS-WS-84MS`
2. `AKUN-002-DEV-VLESS-WS-83MS` (url=349ms, nekobox=6333ms, status=no)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-84MS` (url=652ms, status=HTTP 204)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-89MS`
5. `AKUN-003-CLOUDFLARE-VLESS-WS-86MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-95MS` (url=676ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-88MS` (url=631ms, nekobox=6167ms, status=no)
8. `AKUN-004-TENCENT-VLESS-WS-90MS`
9. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-89MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-87MS` (url=687ms, status=HTTP 204)
11. `AKUN-002-CLOUDFLARE-VLESS-WS-93MS`
12. `AKUN-015-PAGES-VLESS-WS-90MS` (url=651ms, status=HTTP 204)
13. `AKUN-006-CLOUDFLARE-VLESS-WS-97MS`
14. `AKUN-018-UNKNOWN-VLESS-WS-87MS` (url=361ms, nekobox=6171ms, status=no)
15. `AKUN-019-UK-GB-DCL-01-20191003-VLESS-WS-154MS` (url=709ms, status=HTTP 204)
16. `AKUN-020-UNKNOWN-VLESS-WS-337MS` (url=2017ms, status=HTTP 204)
17. `AKUN-022-FREIFUNKFRANKEN-VLESS-WS-580MS` (url=1743ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
