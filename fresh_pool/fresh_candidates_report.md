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
- Kandidat strict NekoBox-tested: 20
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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-114MS` (url=355ms, nekobox=386ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-130MS` (url=383ms, nekobox=402ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-125MS` (url=310ms, nekobox=412ms, status=yes)
4. `AKUN-004-CLOUDFLARE-VLESS-WS-160MS` (url=337ms, nekobox=392ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-155MS` (url=353ms, nekobox=388ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-128MS` (url=364ms, nekobox=391ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-168MS` (url=368ms, nekobox=410ms, status=yes)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-184MS` (url=366ms, nekobox=8179ms, status=no)
9. `AKUN-008-CLOUDFLARE-VLESS-WS-154MS`
10. `AKUN-009-CLOUDFLARE-VLESS-WS-151MS`
11. `AKUN-010-CLOUDFLARE-VLESS-WS-174MS`
12. `AKUN-011-NOTION-WEB-VLESS-WS-116MS`
13. `AKUN-012-CLOUDFLARE-VLESS-WS-181MS`
14. `AKUN-013-CLOUDFLARE-VLESS-WS-191MS`
15. `AKUN-016-CLOUDFLARE-VLESS-WS-162MS` (url=326ms, nekobox=270ms, status=no)
16. `AKUN-014-UNKNOWN-VLESS-WS-204MS`
17. `AKUN-015-DEV-VLESS-WS-136MS`
18. `AKUN-016-UNKNOWN-VLESS-WS-177MS`
19. `AKUN-020-UNKNOWN-VLESS-WS-107MS` (url=369ms, nekobox=270ms, status=no)
20. `AKUN-017-CLOUDFLARE-VLESS-WS-176MS`
21. `AKUN-018-CLOUDFLARE-VLESS-WS-158MS`
22. `AKUN-019-CLOUDFLARE-VLESS-WS-178MS`
23. `AKUN-024-UNKNOWN-VLESS-WS-197MS` (url=354ms, nekobox=271ms, status=no)
24. `AKUN-025-UNKNOWN-VLESS-WS-152MS` (url=349ms, nekobox=272ms, status=no)
25. `AKUN-026-UNKNOWN-VLESS-WS-189MS` (url=413ms, nekobox=8167ms, status=no)
26. `AKUN-020-CCWU-VLESS-WS-200MS`
27. `AKUN-028-EU-VLESS-WS-170MS` (url=347ms, status=HTTP 204)
28. `AKUN-029-DEV-VLESS-WS-186MS` (url=342ms, status=HTTP 204)
29. `AKUN-030-UNKNOWN-VLESS-WS-202MS` (url=361ms, status=HTTP 204)
30. `AKUN-031-GOV-VLESS-WS-193MS` (url=350ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
