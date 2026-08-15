# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 30
- Kandidat strict NekoBox-tested: 5
- Proxy di openclash_fresh_pool.yaml: 34

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
1. `AKUN-001-UNKNOWN-VLESS-WS-260MS`
2. `AKUN-003-UNKNOWN-VLESS-WS-244MS` (url=782ms, nekobox=5193ms, status=no)
3. `AKUN-004-UNKNOWN-VLESS-WS-305MS` (url=830ms, nekobox=5205ms, status=no)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-262MS` (url=3530ms, nekobox=5221ms, status=no)
5. `AKUN-006-SPEEDTEST-VLESS-WS-291MS` (url=661ms, nekobox=8184ms, status=no)
6. `AKUN-008-CLOUDFLARE-VLESS-WS-292MS` (url=721ms, nekobox=8205ms, status=no)
7. `AKUN-009-UNKNOWN-VLESS-WS-271MS` (url=938ms, nekobox=8172ms, status=no)
8. `AKUN-002-CLOUDFLARE-VLESS-WS-261MS`
9. `AKUN-013-SPEEDTEST-VLESS-WS-292MS` (url=572ms, nekobox=8192ms, status=no)
10. `AKUN-014-SPEEDTEST-VLESS-WS-355MS` (url=569ms, nekobox=334ms, status=no)
11. `AKUN-015-NOTION-WEB-VLESS-WS-231MS` (url=684ms, nekobox=5202ms, status=no)
12. `AKUN-003-LEVIKOGJGFDD-VLESS-WS-322MS`
13. `AKUN-019-UNKNOWN-VLESS-WS-256MS` (url=991ms, nekobox=5205ms, status=no)
14. `AKUN-022-CLOUDFLARE-VLESS-WS-288MS` (url=788ms, nekobox=429ms, status=no)
15. `AKUN-026-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-238MS` (url=639ms, nekobox=8170ms, status=no)
16. `AKUN-027-UNKNOWN-VLESS-WS-262MS` (url=564ms, nekobox=498ms, status=no)
17. `AKUN-028-LEVIKOGJGFDD-VLESS-WS-270MS` (url=589ms, nekobox=5272ms, status=no)
18. `AKUN-029-SPEEDTEST-VLESS-WS-247MS` (url=811ms, nekobox=5213ms, status=no)
19. `AKUN-030-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-291MS` (url=670ms, nekobox=5258ms, status=no)
20. `AKUN-031-NOTION-WEB-VLESS-WS-333MS` (url=548ms, nekobox=8177ms, status=no)
21. `AKUN-032-UNKNOWN-VLESS-WS-255MS` (url=1664ms, nekobox=5211ms, status=no)
22. `AKUN-034-UNKNOWN-VLESS-WS-303MS` (url=3148ms, nekobox=5239ms, status=no)
23. `AKUN-035-SPEEDTEST-VLESS-WS-283MS` (url=771ms, nekobox=5296ms, status=no)
24. `AKUN-037-BIGCOMMERCE-VLESS-WS-364MS` (url=663ms, nekobox=8183ms, status=no)
25. `AKUN-038-CLOUDFLARE-VLESS-WS-330MS` (url=2163ms, nekobox=5211ms, status=no)
26. `AKUN-004-UNKNOWN-VLESS-WS-392MS`
27. `AKUN-042-DIGITALOCEAN-VLESS-WS-419MS` (url=1824ms, nekobox=5213ms, status=no)
28. `AKUN-044-UNKNOWN-VLESS-WS-304MS` (url=820ms, nekobox=5202ms, status=no)
29. `AKUN-005-CLOUDFLARE-VLESS-WS-333MS`
30. `AKUN-052-UNKNOWN-VLESS-WS-657MS` (url=2135ms, nekobox=8186ms, status=no)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
