# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 21
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 25

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-124MS`
2. `AKUN-002-DEV-VLESS-WS-133MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-135MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-132MS`
5. `AKUN-005-RESERVED-FOR-TW-VLESS-WS-160MS`
6. `AKUN-006-UNKNOWN-VLESS-WS-202MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-296MS`
8. `AKUN-008-NETCRAFTERS-VLESS-WS-507MS`
9. `AKUN-009-PAGM-NET-VLESS-WS-554MS`
10. `AKUN-010-PAGM-NET-VLESS-WS-517MS`
11. `AKUN-018-CLOUDFLARE-VLESS-WS-224MS` (url=1408ms, status=HTTP 204)
12. `AKUN-022-CLOUDFLARE-VLESS-WS-706MS` (url=1353ms, status=HTTP 204)
13. `AKUN-027-UNKNOWN-VLESS-WS-796MS` (url=1230ms, status=HTTP 204)
14. `AKUN-029-UNKNOWN-VLESS-WS-814MS` (url=1718ms, status=HTTP 204)
15. `AKUN-030-CLOUDFLARE-VLESS-WS-848MS` (url=1633ms, status=HTTP 204)
16. `AKUN-031-UNKNOWN-VLESS-WS-836MS` (url=1450ms, status=HTTP 204)
17. `AKUN-034-H2NEXUS-VLESS-WS-773MS` (url=1605ms, status=HTTP 204)
18. `AKUN-037-NET-151-242-2-0-24-VLESS-WS-748MS` (url=1790ms, status=HTTP 204)
19. `AKUN-038-JIKECLOUD-VLESS-WS-1494MS` (url=1839ms, status=HTTP 204)
20. `AKUN-039-UNKNOWN-VLESS-WS-1272MS` (url=1951ms, status=HTTP 204)
21. `AKUN-040-CLOUDFLARE-VLESS-WS-2206MS` (url=2019ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
