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
- Proxy di openclash_fresh_pool.yaml: 30

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-152MS` (url=1601ms, nekobox=386ms, status=yes)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-140MS` (url=338ms, nekobox=424ms, status=yes)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-145MS` (url=317ms, nekobox=379ms, status=yes)
4. `AKUN-004-CLOUD-NETWORK-HK-VLESS-WS-174MS` (url=322ms, nekobox=401ms, status=yes)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-146MS` (url=348ms, nekobox=411ms, status=yes)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-146MS` (url=347ms, nekobox=374ms, status=yes)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-141MS` (url=363ms, nekobox=399ms, status=yes)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-134MS` (url=352ms, nekobox=399ms, status=yes)
9. `AKUN-009-NOTION-WEB-VLESS-WS-150MS` (url=350ms, nekobox=1400ms, status=yes)
10. `AKUN-010-CLOUDFLARE-VLESS-WS-132MS` (url=336ms, nekobox=429ms, status=yes)
11. `AKUN-011-CLOUDFLARE-VLESS-WS-154MS` (url=360ms, nekobox=399ms, status=yes)
12. `AKUN-012-CLOUDFLARE-VLESS-WS-218MS` (url=347ms, nekobox=425ms, status=yes)
13. `AKUN-013-CLOUDFLARE-VLESS-WS-183MS` (url=341ms, nekobox=402ms, status=yes)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-145MS` (url=360ms, nekobox=409ms, status=yes)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-187MS` (url=368ms, nekobox=384ms, status=yes)
16. `AKUN-016-CLOUDFLARE-VLESS-WS-155MS` (url=364ms, nekobox=405ms, status=yes)
17. `AKUN-017-CLOUDFLARE-VLESS-WS-171MS` (url=376ms, nekobox=353ms, status=yes)
18. `AKUN-018-ZVC-VLESS-WS-125MS` (url=370ms, nekobox=393ms, status=yes)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-109MS` (url=356ms, nekobox=385ms, status=yes)
20. `AKUN-020-BIGCOMMERCE-VLESS-WS-174MS` (url=361ms, nekobox=386ms, status=yes)
21. `AKUN-021-CLOUDFLARE-VLESS-WS-196MS` (url=354ms, status=HTTP 204)
22. `AKUN-022-CLOUDFLARE-VLESS-WS-183MS` (url=375ms, status=HTTP 204)
23. `AKUN-023-CLOUDFLARE-VLESS-WS-162MS` (url=331ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-145MS` (url=362ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-175MS` (url=335ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-219MS` (url=366ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-182MS` (url=602ms, status=HTTP 204)
28. `AKUN-028-CLOUDFLARE-VLESS-WS-231MS` (url=362ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-157MS` (url=340ms, status=HTTP 204)
30. `AKUN-031-CLOUDFLARE-VLESS-WS-226MS` (url=390ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
