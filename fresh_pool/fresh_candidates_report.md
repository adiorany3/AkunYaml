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
- Kandidat strict NekoBox-tested: 10
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
1. `AKUN-001-SPEEDTEST-VLESS-WS-188MS` (url=1516ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-211MS` (url=1716ms, status=HTTP 204)
3. `AKUN-003-COGENT-VLESS-WS-880MS`
4. `AKUN-004-CLOUDFLARE-VLESS-WS-895MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-909MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-902MS`
7. `AKUN-007-UNKNOWN-VLESS-WS-926MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-898MS`
9. `AKUN-009-DEV-VLESS-WS-890MS`
10. `AKUN-010-AIMALL-VLESS-WS-919MS`
11. `AKUN-015-CLOUDFLARE-VLESS-WS-928MS` (url=1330ms, status=HTTP 204)
12. `AKUN-016-ESA-VLESS-WS-937MS` (url=1479ms, status=HTTP 204)
13. `AKUN-017-CLOUDFLARE-VLESS-WS-882MS` (url=1736ms, status=HTTP 204)
14. `AKUN-020-NOTION-WEB-VLESS-WS-940MS` (url=1722ms, status=HTTP 204)
15. `AKUN-023-UNKNOWN-VLESS-WS-927MS` (url=1832ms, status=HTTP 204)
16. `AKUN-024-UNKNOWN-VLESS-WS-926MS` (url=1461ms, status=HTTP 204)
17. `AKUN-025-RS-RAPIDSEEDBOX-20190717-VLESS-WS-935MS` (url=1309ms, status=HTTP 204)
18. `AKUN-026-CLOUDFLARE-VLESS-WS-898MS` (url=1497ms, status=HTTP 204)
19. `AKUN-027-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-978MS` (url=1551ms, status=HTTP 204)
20. `AKUN-028-UK-GB-DCL-01-20191003-VLESS-WS-873MS` (url=1861ms, status=HTTP 204)
21. `AKUN-029-UNKNOWN-VLESS-WS-924MS` (url=2048ms, status=HTTP 204)
22. `AKUN-030-CLOUDFLARE-VLESS-WS-910MS` (url=1706ms, status=HTTP 204)
23. `AKUN-031-CLOUDFLARE-VLESS-WS-895MS` (url=1623ms, status=HTTP 204)
24. `AKUN-032-UNKNOWN-VLESS-WS-221MS` (url=1495ms, status=HTTP 204)
25. `AKUN-034-CLOUDFLARE-VLESS-WS-920MS` (url=1842ms, status=HTTP 204)
26. `AKUN-035-CLOUDFLARE-VLESS-WS-887MS` (url=1108ms, status=HTTP 204)
27. `AKUN-036-SPEEDTEST-VLESS-WS-890MS` (url=1707ms, status=HTTP 204)
28. `AKUN-037-TIME-VLESS-WS-907MS` (url=1553ms, status=HTTP 204)
29. `AKUN-038-CLOUDFLARE-VLESS-WS-883MS` (url=1619ms, status=HTTP 204)
30. `AKUN-039-CLOUDFLARE-VLESS-WS-914MS` (url=1834ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
