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
1. `AKUN-001-UNKNOWN-VLESS-WS-208MS` (url=761ms, status=HTTP 204)
2. `AKUN-002-UNKNOWN-VLESS-WS-227MS` (url=583ms, status=HTTP 204)
3. `AKUN-003-UNKNOWN-VLESS-WS-217MS` (url=419ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-243MS` (url=3636ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-214MS` (url=814ms, status=HTTP 204)
6. `AKUN-006-LEVIKOGJGFDD-VLESS-WS-209MS` (url=489ms, status=HTTP 204)
7. `AKUN-007-UNKNOWN-VLESS-WS-192MS` (url=481ms, status=HTTP 204)
8. `AKUN-008-UNKNOWN-VLESS-WS-226MS`
9. `AKUN-009-UNKNOWN-VLESS-WS-227MS`
10. `AKUN-010-UNKNOWN-VLESS-WS-231MS`
11. `AKUN-012-LEVIKOGJGFDD-VLESS-WS-225MS` (url=642ms, status=HTTP 204)
12. `AKUN-014-CLOUDFLARE-VLESS-WS-244MS` (url=635ms, status=HTTP 204)
13. `AKUN-016-CLOUDFLARE-VLESS-WS-269MS` (url=475ms, status=HTTP 204)
14. `AKUN-017-CLOUDFLARE-VLESS-WS-242MS` (url=700ms, status=HTTP 204)
15. `AKUN-018-CLOUDFLARE-VLESS-WS-233MS` (url=655ms, status=HTTP 204)
16. `AKUN-019-CLOUDFLARE-VLESS-WS-224MS` (url=401ms, status=HTTP 204)
17. `AKUN-021-CLOUDFLARE-VLESS-WS-257MS` (url=446ms, status=HTTP 204)
18. `AKUN-022-CLOUDFLARE-VLESS-WS-239MS` (url=520ms, status=HTTP 204)
19. `AKUN-024-UNKNOWN-VLESS-WS-242MS` (url=686ms, status=HTTP 204)
20. `AKUN-025-UNKNOWN-VLESS-WS-228MS` (url=949ms, status=HTTP 204)
21. `AKUN-026-UNKNOWN-VLESS-WS-225MS` (url=587ms, status=HTTP 204)
22. `AKUN-027-UNKNOWN-VLESS-WS-224MS` (url=506ms, status=HTTP 204)
23. `AKUN-028-UNKNOWN-VLESS-WS-225MS` (url=485ms, status=HTTP 204)
24. `AKUN-029-EU-VLESS-WS-226MS` (url=643ms, status=HTTP 204)
25. `AKUN-030-UNKNOWN-VLESS-WS-214MS` (url=532ms, status=HTTP 204)
26. `AKUN-031-UNKNOWN-VLESS-WS-203MS` (url=452ms, status=HTTP 204)
27. `AKUN-032-UNKNOWN-VLESS-WS-230MS` (url=565ms, status=HTTP 204)
28. `AKUN-033-UNKNOWN-VLESS-WS-240MS` (url=501ms, status=HTTP 204)
29. `AKUN-034-UNKNOWN-VLESS-WS-245MS` (url=552ms, status=HTTP 204)
30. `AKUN-037-UNKNOWN-VLESS-WS-244MS` (url=4118ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
