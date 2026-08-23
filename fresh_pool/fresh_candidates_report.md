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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-255MS` (url=4858ms, status=HTTP 204)
2. `AKUN-002-CLOUDFLARE-VLESS-WS-260MS` (url=879ms, status=HTTP 204)
3. `AKUN-003-DEV-VLESS-WS-239MS` (url=979ms, status=HTTP 204)
4. `AKUN-004-EU-VLESS-WS-277MS` (url=710ms, status=HTTP 204)
5. `AKUN-005-UNKNOWN-VLESS-WS-287MS` (url=5263ms, status=HTTP 204)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-293MS` (url=464ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-265MS` (url=1096ms, status=HTTP 204)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-312MS` (url=1508ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-272MS` (url=554ms, status=HTTP 204)
10. `AKUN-010-DEV-VLESS-WS-274MS` (url=1447ms, status=HTTP 204)
11. `AKUN-011-NOTION-WEB-VLESS-WS-295MS` (url=516ms, status=HTTP 204)
12. `AKUN-012-DEV-VLESS-WS-312MS` (url=559ms, status=HTTP 204)
13. `AKUN-013-TIME-VLESS-WS-212MS` (url=542ms, status=HTTP 204)
14. `AKUN-014-CLOUDFLARE-VLESS-WS-260MS` (url=1461ms, status=HTTP 204)
15. `AKUN-015-CLOUDFLARE-VLESS-WS-501MS` (url=521ms, status=HTTP 204)
16. `AKUN-016-UNKNOWN-VLESS-WS-513MS` (url=636ms, status=HTTP 204)
17. `AKUN-017-UNKNOWN-VLESS-WS-477MS` (url=517ms, status=HTTP 204)
18. `AKUN-018-CHATGPT-VLESS-WS-249MS` (url=683ms, status=HTTP 204)
19. `AKUN-019-CLOUDFLARE-VLESS-WS-296MS` (url=557ms, status=HTTP 204)
20. `AKUN-020-OPENAI-VLESS-WS-301MS` (url=548ms, status=HTTP 204)
21. `AKUN-021-EU-VLESS-WS-282MS` (url=2721ms, status=HTTP 204)
22. `AKUN-022-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-241MS` (url=828ms, status=HTTP 204)
23. `AKUN-023-SPEEDTEST-VLESS-WS-366MS` (url=488ms, status=HTTP 204)
24. `AKUN-024-CLOUDFLARE-VLESS-WS-272MS` (url=572ms, status=HTTP 204)
25. `AKUN-025-CLOUDFLARE-VLESS-WS-295MS` (url=588ms, status=HTTP 204)
26. `AKUN-026-CLOUDFLARE-VLESS-WS-296MS` (url=451ms, status=HTTP 204)
27. `AKUN-027-CLOUDFLARE-VLESS-WS-536MS` (url=649ms, status=HTTP 204)
28. `AKUN-028-DE5-VLESS-WS-310MS` (url=1887ms, status=HTTP 204)
29. `AKUN-029-CLOUDFLARE-VLESS-WS-536MS` (url=961ms, status=HTTP 204)
30. `AKUN-030-CLOUDFLARE-VLESS-WS-567MS` (url=5518ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
