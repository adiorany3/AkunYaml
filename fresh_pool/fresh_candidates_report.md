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
- Kandidat strict NekoBox-tested: 10
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
1. `AKUN-001-RESERVED-FOR-TW-VLESS-WS-136MS` (url=370ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-119MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-236MS`
4. `AKUN-004-PAGM-NET-VLESS-WS-533MS`
5. `AKUN-005-NETCRAFTERS-VLESS-WS-488MS`
6. `AKUN-006-PAGM-NET-VLESS-WS-357MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-775MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-874MS`
9. `AKUN-009-JIKECLOUD-VLESS-WS-647MS`
10. `AKUN-010-CLOUDFLARE-VLESS-WS-127MS`
11. `AKUN-030-CLOUDFLARE-VLESS-WS-115MS` (url=320ms, status=HTTP 204)
12. `AKUN-033-UNKNOWN-VLESS-WS-493MS` (url=2182ms, status=HTTP 204)
13. `AKUN-034-UNKNOWN-VLESS-WS-1141MS` (url=1879ms, status=HTTP 204)
14. `AKUN-037-JIKECLOUD-VLESS-WS-1128MS` (url=2323ms, status=HTTP 204)
15. `AKUN-041-H2NEXUS-VLESS-WS-753MS` (url=1333ms, status=HTTP 204)
16. `AKUN-042-IQIRAQ-VLESS-WS-805MS` (url=3042ms, status=HTTP 204)
17. `AKUN-045-UNKNOWN-VLESS-WS-798MS` (url=1209ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
