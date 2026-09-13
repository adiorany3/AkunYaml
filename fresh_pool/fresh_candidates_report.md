# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 15
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-005-UNKNOWN-VLESS-WS-81MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-81MS` (url=637ms, nekobox=704ms, status=yes)
3. `AKUN-004-UNKNOWN-VLESS-WS-83MS`
4. `AKUN-001-CLOUDFLARE-VLESS-WS-85MS`
5. `AKUN-003-CLOUDFLARE-VLESS-WS-83MS`
6. `AKUN-006-TENCENT-VLESS-WS-89MS` (url=696ms, nekobox=661ms, status=yes)
7. `AKUN-007-DEV-VLESS-WS-94MS` (url=542ms, nekobox=266ms, status=no)
8. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-90MS` (url=714ms, nekobox=823ms, status=yes)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-89MS` (url=731ms, nekobox=917ms, status=yes)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-92MS` (url=787ms, status=HTTP 204)
11. `AKUN-007-PAGES-VLESS-WS-122MS`
12. `AKUN-014-CLOUDFLARE-VLESS-WS-104MS` (url=824ms, status=HTTP 204)
13. `AKUN-016-UK-GB-DCL-01-20191003-VLESS-WS-146MS` (url=739ms, status=HTTP 204)
14. `AKUN-018-UNKNOWN-VLESS-WS-188MS` (url=1257ms, status=HTTP 204)
15. `AKUN-060-CLOUDFLARE-VLESS-WS-702MS` (url=4211ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
