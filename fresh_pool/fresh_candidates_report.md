# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 14
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 18

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
1. `AKUN-001-RS-RAPIDSEEDBOX-20190717-VLESS-WS-87MS` (url=345ms, status=HTTP 204)
2. `AKUN-002-GO-DADDY-COM-LLC-VLESS-WS-88MS` (url=1309ms, status=HTTP 204)
3. `AKUN-003-VEESP-SIA-VLESS-WS-92MS` (url=337ms, status=HTTP 204)
4. `AKUN-004-ESA-VLESS-WS-97MS` (url=321ms, status=HTTP 204)
5. `AKUN-005-DA-INTERNATIONAL-VLESS-WS-97MS` (url=327ms, status=HTTP 204)
6. `AKUN-006-GO-DADDY-COM-LLC-VLESS-WS-90MS` (url=315ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-88MS` (url=321ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-103MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-279MS`
10. `AKUN-010-41-216-182-0-41-216-182-VLESS-WS-776MS`
11. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-776MS` (url=1477ms, status=HTTP 204)
12. `AKUN-029-ORG-VLESS-WS-90MS` (url=1333ms, status=HTTP 204)
13. `AKUN-032-IT7NET-104-224-180-0-22-VLESS-WS-97MS` (url=1148ms, status=HTTP 204)
14. `AKUN-034-CLOUDFLARE-VLESS-WS-705MS` (url=1494ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
