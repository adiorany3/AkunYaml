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
- Kandidat strict NekoBox-tested: 7
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
1. `AKUN-001-BIGCOMMERCE-VLESS-WS-104MS` (url=385ms, status=HTTP 204)
2. `AKUN-001-CLOUDFLARE-VLESS-WS-111MS`
3. `AKUN-003-CLOUDFLARE-VLESS-WS-97MS` (url=369ms, status=HTTP 204)
4. `AKUN-007-CLOUDFLARE-VLESS-WS-107MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-108MS` (url=379ms, status=HTTP 204)
6. `AKUN-006-MEDIUM-VLESS-WS-104MS` (url=363ms, status=HTTP 204)
7. `AKUN-007-CLOUDFLARE-VLESS-WS-105MS` (url=357ms, nekobox=6179ms, status=no)
8. `AKUN-009-CLOUDFLARE-VLESS-WS-105MS` (url=374ms, status=HTTP 204)
9. `AKUN-010-CLOUDFLARE-VLESS-WS-109MS` (url=389ms, status=HTTP 204)
10. `AKUN-011-NOTION-WEB-VLESS-WS-113MS` (url=358ms, nekobox=6192ms, status=no)
11. `AKUN-004-CLOUDFLARE-VLESS-WS-102MS`
12. `AKUN-005-CLOUDFLARE-VLESS-WS-114MS`
13. `AKUN-015-CLOUDFLARE-VLESS-WS-117MS` (url=573ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-109MS` (url=377ms, status=HTTP 204)
15. `AKUN-017-UNKNOWN-VLESS-WS-125MS` (url=1362ms, status=HTTP 204)
16. `AKUN-018-CLOUDFLARE-VLESS-WS-124MS` (url=368ms, status=HTTP 204)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-111MS` (url=1380ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-111MS` (url=368ms, status=HTTP 204)
19. `AKUN-002-CLOUDFLARE-VLESS-WS-104MS`
20. `AKUN-022-CLOUDFLARE-VLESS-WS-113MS` (url=1369ms, status=HTTP 204)
21. `AKUN-006-CLOUDFLARE-VLESS-WS-118MS`
22. `AKUN-025-CLOUDFLARE-VLESS-WS-114MS` (url=371ms, status=HTTP 204)
23. `AKUN-026-CLOUDFLARE-VLESS-WS-117MS` (url=381ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-108MS` (url=1358ms, status=HTTP 204)
25. `AKUN-028-CLOUDFLARE-VLESS-WS-108MS` (url=360ms, status=HTTP 204)
26. `AKUN-029-CLOUDFLARE-VLESS-WS-114MS` (url=347ms, nekobox=261ms, status=no)
27. `AKUN-003-CLOUDFLARE-VLESS-WS-115MS`
28. `AKUN-031-UNKNOWN-VLESS-WS-173MS` (url=380ms, status=HTTP 204)
29. `AKUN-034-CLOUDFLARE-VLESS-WS-152MS` (url=1999ms, status=HTTP 204)
30. `AKUN-035-OVH-VLESS-WS-615MS` (url=2782ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
