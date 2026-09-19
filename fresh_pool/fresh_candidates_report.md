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
1. `AKUN-001-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-114MS` (url=450ms, status=HTTP 204)
2. `AKUN-002-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-117MS` (url=434ms, status=HTTP 204)
3. `AKUN-002-NET-147-90-26-0-24-VLESS-WS-134MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-140MS` (url=506ms, status=HTTP 204)
5. `AKUN-009-TENCENT-VLESS-WS-132MS`
6. `AKUN-010-ZUOAI-VLESS-WS-122MS`
7. `AKUN-007-CLOUDFLARE-VLESS-WS-189MS` (url=441ms, status=HTTP 204)
8. `AKUN-001-CLOUDFLARE-VLESS-WS-195MS`
9. `AKUN-009-CLOUDFLARE-VLESS-WS-302MS` (url=454ms, status=HTTP 204)
10. `AKUN-010-UNKNOWN-VLESS-WS-205MS` (url=447ms, status=HTTP 204)
11. `AKUN-006-CLOUDFLARE-VLESS-WS-209MS`
12. `AKUN-003-ZUOAI-VLESS-WS-150MS`
13. `AKUN-008-NET-147-90-26-0-24-VLESS-WS-130MS`
14. `AKUN-014-ALOIPTELTD-SG-VLESS-WS-171MS` (url=937ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-158MS` (url=1047ms, status=HTTP 204)
16. `AKUN-005-CLOUDFLARE-VLESS-WS-143MS`
17. `AKUN-017-NASEEJ-VLESS-WS-275MS` (url=460ms, status=HTTP 204)
18. `AKUN-007-CLOUDFLARE-VLESS-WS-154MS`
19. `AKUN-004-TENCENT-VLESS-WS-142MS`
20. `AKUN-025-UNKNOWN-VLESS-WS-239MS` (url=2042ms, status=HTTP 204)
21. `AKUN-037-UNKNOWN-VLESS-WS-763MS` (url=1652ms, status=HTTP 204)
22. `AKUN-046-UNKNOWN-VLESS-WS-767MS` (url=1436ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
