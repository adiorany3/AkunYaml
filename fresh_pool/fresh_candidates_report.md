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
- Kandidat strict NekoBox-tested: 10
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
1. `AKUN-001-UNKNOWN-VLESS-WS-491MS`
2. `AKUN-002-TIME-VLESS-WS-330MS` (url=785ms, status=HTTP 204)
3. `AKUN-003-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-423MS` (url=823ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-439MS` (url=769ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-232MS` (url=595ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-466MS` (url=655ms, status=HTTP 204)
7. `AKUN-007-DEV-VLESS-WS-363MS` (url=614ms, status=HTTP 204)
8. `AKUN-008-CHATGPT-VLESS-WS-737MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-832MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-1005MS`
11. `AKUN-023-UNKNOWN-VLESS-WS-1043MS` (url=1675ms, status=HTTP 204)
12. `AKUN-028-UNKNOWN-VLESS-WS-361MS` (url=1608ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
