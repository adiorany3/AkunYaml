# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 19
- Kandidat strict NekoBox-tested: 10
- Proxy di openclash_fresh_pool.yaml: 23

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
1. `AKUN-001-RESERVED-FOR-TW-VLESS-WS-127MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-143MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-131MS`
4. `AKUN-004-NETCRAFTERS-VLESS-WS-465MS`
5. `AKUN-005-PAGM-NET-VLESS-WS-529MS`
6. `AKUN-006-PAGM-NET-VLESS-WS-524MS`
7. `AKUN-007-JIKECLOUD-VLESS-WS-550MS`
8. `AKUN-008-H2NEXUS-VLESS-WS-714MS`
9. `AKUN-009-IQIRAQ-VLESS-WS-809MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-820MS`
11. `AKUN-030-CLOUDFLARE-VLESS-WS-870MS` (url=1594ms, status=HTTP 204)
12. `AKUN-032-CLOUDFLARE-VLESS-WS-134MS` (url=1352ms, status=HTTP 204)
13. `AKUN-034-DEV-VLESS-WS-144MS` (url=370ms, status=HTTP 204)
14. `AKUN-035-UNKNOWN-VLESS-WS-871MS` (url=1450ms, status=HTTP 204)
15. `AKUN-036-CLOUDFLARE-VLESS-WS-228MS` (url=2227ms, status=HTTP 204)
16. `AKUN-037-JIKECLOUD-VLESS-WS-1154MS` (url=3281ms, status=HTTP 204)
17. `AKUN-043-NET-151-242-2-0-24-VLESS-WS-783MS` (url=2948ms, status=HTTP 204)
18. `AKUN-045-UNKNOWN-VLESS-WS-822MS` (url=2442ms, status=HTTP 204)
19. `AKUN-046-UNKNOWN-VLESS-WS-1195MS` (url=2040ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
