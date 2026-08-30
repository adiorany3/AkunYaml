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
1. `AKUN-001-UNKNOWN-VLESS-WS-363MS`
2. `AKUN-002-UNKNOWN-VLESS-WS-327MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-325MS`
4. `AKUN-004-UNKNOWN-VLESS-WS-267MS`
5. `AKUN-005-UNKNOWN-VLESS-WS-300MS`
6. `AKUN-006-NETCRAFTERS-VLESS-WS-719MS`
7. `AKUN-007-PAGM-NET-VLESS-WS-755MS`
8. `AKUN-008-UNKNOWN-VLESS-WS-552MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-1055MS`
10. `AKUN-010-PAGM-NET-VLESS-WS-785MS`
11. `AKUN-018-UNKNOWN-VLESS-WS-1290MS` (url=2291ms, status=HTTP 204)
12. `AKUN-020-CLOUDFLARE-VLESS-WS-427MS` (url=682ms, status=HTTP 204)
13. `AKUN-021-JIKECLOUD-VLESS-WS-1242MS` (url=2630ms, status=HTTP 204)
14. `AKUN-022-UNKNOWN-VLESS-WS-1003MS` (url=1999ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
