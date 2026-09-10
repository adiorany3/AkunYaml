# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 27
- Kandidat strict NekoBox-tested: 5
- Proxy di openclash_fresh_pool.yaml: 31

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-119MS` (url=722ms, status=HTTP 204)
2. `AKUN-002-NET-83-147-12-0-22-VLESS-WS-127MS` (url=401ms, nekobox=6175ms, status=no)
3. `AKUN-002-CLOUDFLARE-VLESS-WS-122MS`
4. `AKUN-004-DEV-VLESS-WS-132MS` (url=422ms, nekobox=6189ms, status=no)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-127MS` (url=660ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-141MS` (url=390ms, nekobox=6178ms, status=no)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-142MS` (url=1609ms, status=HTTP 204)
8. `AKUN-009-CLOUDFLARE-VLESS-WS-119MS` (url=379ms, nekobox=6179ms, status=no)
9. `AKUN-010-CLOUDFLARE-VLESS-WS-134MS` (url=692ms, status=HTTP 204)
10. `AKUN-011-CLOUDFLARE-VLESS-WS-138MS` (url=670ms, status=HTTP 204)
11. `AKUN-003-CLOUDFLARE-VLESS-WS-143MS`
12. `AKUN-004-CLOUDFLARE-VLESS-WS-123MS`
13. `AKUN-015-UNKNOWN-VLESS-WS-148MS` (url=721ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-129MS` (url=628ms, status=HTTP 204)
15. `AKUN-019-UNKNOWN-VLESS-WS-142MS` (url=683ms, status=HTTP 204)
16. `AKUN-020-CLOUDFLARE-VLESS-WS-162MS` (url=708ms, status=HTTP 204)
17. `AKUN-021-TENCENT-VLESS-WS-131MS` (url=662ms, status=HTTP 204)
18. `AKUN-024-CLOUDFLARE-VLESS-WS-691MS` (url=1104ms, status=HTTP 204)
19. `AKUN-027-CLOUDFLARE-VLESS-WS-131MS` (url=1011ms, status=HTTP 204)
20. `AKUN-044-CLOUDFLARE-VLESS-WS-143MS` (url=439ms, status=HTTP 204)
21. `AKUN-047-CLOUDFLARE-VLESS-WS-137MS` (url=390ms, nekobox=6179ms, status=no)
22. `AKUN-001-CLOUDFLARE-VLESS-WS-168MS`
23. `AKUN-005-CLOUDFLARE-VLESS-WS-156MS`
24. `AKUN-050-CLOUDFLARE-VLESS-WS-148MS` (url=778ms, status=HTTP 204)
25. `AKUN-052-CLOUDFLARE-VLESS-WS-139MS` (url=492ms, status=HTTP 204)
26. `AKUN-054-ORG-VLESS-WS-142MS` (url=1672ms, status=HTTP 204)
27. `AKUN-057-UNKNOWN-VLESS-WS-256MS` (url=2971ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
