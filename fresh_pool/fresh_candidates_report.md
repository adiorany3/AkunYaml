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
- Kandidat strict NekoBox-tested: 9
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
1. `AKUN-002-CLOUDFLARE-VLESS-WS-113MS`
2. `AKUN-001-TENCENT-VLESS-WS-113MS`
3. `AKUN-004-CLOUDFLARE-VLESS-WS-106MS` (url=375ms, nekobox=6190ms, status=no)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-122MS` (url=398ms, nekobox=445ms, status=yes)
5. `AKUN-008-CLOUDFLARE-VLESS-WS-102MS`
6. `AKUN-004-UNKNOWN-VLESS-WS-106MS`
7. `AKUN-003-CLOUDFLARE-VLESS-WS-114MS`
8. `AKUN-006-CLOUDFLARE-VLESS-WS-136MS`
9. `AKUN-009-DE-VLESS-WS-626MS`
10. `AKUN-013-UNKNOWN-VLESS-WS-398MS` (url=2129ms, status=HTTP 204)
11. `AKUN-034-CLOUDFLARE-VLESS-WS-913MS` (url=1812ms, status=HTTP 204)
12. `AKUN-045-PAI50288-VLESS-WS-1147MS` (url=2983ms, status=HTTP 204)
13. `AKUN-007-CLOUDFLARE-VLESS-WS-677MS`
14. `AKUN-053-CLOUDFLARE-VLESS-WS-1137MS` (url=3764ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
