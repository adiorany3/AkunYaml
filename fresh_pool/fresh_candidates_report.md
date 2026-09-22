# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 16
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 20

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
1. `AKUN-008-UNKNOWN-VLESS-WS-122MS`
2. `AKUN-003-CY-ANNETEN-19971112-VLESS-WS-140MS` (url=683ms, status=HTTP 204)
3. `AKUN-005-UNKNOWN-VLESS-WS-165MS` (url=415ms, nekobox=445ms, status=yes)
4. `AKUN-001-ZUOAI-VLESS-WS-111MS`
5. `AKUN-002-CLOUDFLARE-VLESS-WS-123MS`
6. `AKUN-003-CLOUDFLARE-VLESS-WS-147MS`
7. `AKUN-006-CLOUDFLARE-VLESS-WS-155MS`
8. `AKUN-007-UNKNOWN-VLESS-WS-111MS`
9. `AKUN-016-CLOUDFLARE-VLESS-WS-215MS` (url=503ms, status=HTTP 204)
10. `AKUN-017-UNKNOWN-VLESS-WS-639MS` (url=1499ms, status=HTTP 204)
11. `AKUN-018-CLOUDFLARE-VLESS-WS-280MS` (url=438ms, status=HTTP 204)
12. `AKUN-004-CLOUDFLARE-VLESS-WS-245MS`
13. `AKUN-010-ZUOAI-VLESS-WS-381MS`
14. `AKUN-009-IPOWERWEB-NET-VLESS-WS-355MS`
15. `AKUN-023-UNKNOWN-VLESS-WS-139MS` (url=1042ms, status=HTTP 204)
16. `AKUN-031-UNKNOWN-VLESS-WS-446MS` (url=1905ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
