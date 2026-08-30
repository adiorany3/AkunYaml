# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 22
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 26

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
1. `AKUN-001-DEV-VLESS-WS-124MS` (url=358ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-124MS` (url=398ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-116MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-135MS`
5. `AKUN-005-UNKNOWN-VLESS-WS-148MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-149MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-191MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-332MS`
9. `AKUN-009-PAGM-NET-VLESS-WS-567MS`
10. `AKUN-010-PAGM-NET-VLESS-WS-544MS`
11. `AKUN-017-NETCRAFTERS-VLESS-WS-482MS` (url=1089ms, status=HTTP 204)
12. `AKUN-018-UNKNOWN-VLESS-WS-686MS` (url=2320ms, status=HTTP 204)
13. `AKUN-020-NET-151-242-2-0-24-VLESS-WS-728MS` (url=1562ms, status=HTTP 204)
14. `AKUN-024-UNKNOWN-VLESS-WS-828MS` (url=1151ms, status=HTTP 204)
15. `AKUN-030-IQIRAQ-VLESS-WS-832MS` (url=1570ms, status=HTTP 204)
16. `AKUN-032-INTERLIR-CUSTOMER-VLESS-WS-892MS` (url=3233ms, status=HTTP 204)
17. `AKUN-034-UNKNOWN-VLESS-WS-864MS` (url=1701ms, status=HTTP 204)
18. `AKUN-035-DEV-VLESS-WS-132MS` (url=1360ms, status=HTTP 204)
19. `AKUN-038-UNKNOWN-VLESS-WS-142MS` (url=424ms, status=HTTP 204)
20. `AKUN-039-UNKNOWN-VLESS-WS-1164MS` (url=2929ms, status=HTTP 204)
21. `AKUN-041-UNKNOWN-VLESS-WS-411MS` (url=941ms, status=HTTP 204)
22. `AKUN-046-UNKNOWN-VLESS-WS-138MS` (url=402ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
