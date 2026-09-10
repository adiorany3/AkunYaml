# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 20
- Kandidat strict NekoBox-tested: 5
- Proxy di openclash_fresh_pool.yaml: 24

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
1. `AKUN-001-UNKNOWN-VLESS-WS-105MS` (url=690ms, status=HTTP 204)
2. `AKUN-002-NET-83-147-12-0-22-VLESS-WS-112MS` (url=332ms, nekobox=6173ms, status=no)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-110MS` (url=367ms, nekobox=6170ms, status=no)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-116MS` (url=362ms, nekobox=6168ms, status=no)
5. `AKUN-005-UNKNOWN-VLESS-WS-112MS` (url=678ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-127MS` (url=351ms, nekobox=6171ms, status=no)
7. `AKUN-008-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-128MS` (url=350ms, nekobox=274ms, status=no)
8. `AKUN-009-NOTION-WEB-VLESS-WS-130MS` (url=1350ms, status=HTTP 204)
9. `AKUN-011-CLOUDFLARE-VLESS-WS-147MS` (url=1381ms, status=HTTP 204)
10. `AKUN-001-CLOUDFLARE-VLESS-WS-110MS`
11. `AKUN-002-CLOUDFLARE-VLESS-WS-121MS`
12. `AKUN-004-DEV-VLESS-WS-138MS`
13. `AKUN-005-UNKNOWN-VLESS-WS-123MS`
14. `AKUN-003-CLOUDFLARE-VLESS-WS-164MS`
15. `AKUN-017-CLOUDFLARE-VLESS-WS-129MS` (url=374ms, status=HTTP 204)
16. `AKUN-018-UNKNOWN-VLESS-WS-305MS` (url=478ms, status=HTTP 204)
17. `AKUN-022-UNKNOWN-VLESS-WS-398MS` (url=1814ms, status=HTTP 204)
18. `AKUN-031-CLOUDFLARE-VLESS-WS-175MS` (url=1700ms, status=HTTP 204)
19. `AKUN-032-CLOUDFLARE-VLESS-WS-128MS` (url=399ms, status=HTTP 204)
20. `AKUN-035-PAI50288-VLESS-WS-1185MS` (url=2053ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
