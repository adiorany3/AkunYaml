# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 28
- Kandidat strict NekoBox-tested: 7
- Proxy di openclash_fresh_pool.yaml: 32

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
1. `AKUN-001-CLOUDFLARE-VLESS-WS-102MS` (url=376ms, status=HTTP 204)
2. `AKUN-001-CLOUDFLARE-VLESS-WS-109MS`
3. `AKUN-003-UNKNOWN-VLESS-WS-106MS` (url=342ms, nekobox=398ms, status=yes)
4. `AKUN-005-CLOUDFLARE-VLESS-WS-109MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-104MS` (url=368ms, status=HTTP 204)
6. `AKUN-006-UNKNOWN-VLESS-WS-106MS` (url=358ms, status=HTTP 204)
7. `AKUN-008-CLOUDFLARE-VLESS-WS-110MS` (url=362ms, status=HTTP 204)
8. `AKUN-002-CLOUDFLARE-VLESS-WS-110MS`
9. `AKUN-006-CLOUDFLARE-VLESS-WS-116MS`
10. `AKUN-011-DEV-VLESS-WS-114MS` (url=350ms, nekobox=263ms, status=no)
11. `AKUN-004-CLOUDFLARE-VLESS-WS-110MS`
12. `AKUN-014-CLOUDFLARE-VLESS-WS-110MS` (url=430ms, status=HTTP 204)
13. `AKUN-015-COM-VLESS-WS-125MS` (url=359ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-105MS` (url=370ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-117MS` (url=379ms, status=HTTP 204)
16. `AKUN-018-NOTION-WEB-VLESS-WS-112MS` (url=349ms, nekobox=6180ms, status=no)
17. `AKUN-019-CLOUDFLARE-VLESS-WS-135MS` (url=341ms, nekobox=263ms, status=no)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-146MS` (url=358ms, status=HTTP 204)
19. `AKUN-022-CLOUDFLARE-VLESS-WS-120MS` (url=974ms, status=HTTP 204)
20. `AKUN-030-CLOUDFLARE-VLESS-WS-861MS` (url=1393ms, status=HTTP 204)
21. `AKUN-047-CLOUDFLARE-VLESS-WS-117MS` (url=400ms, status=HTTP 204)
22. `AKUN-007-CLOUDFLARE-VLESS-WS-111MS`
23. `AKUN-050-CLOUDFLARE-VLESS-WS-125MS` (url=970ms, status=HTTP 204)
24. `AKUN-051-UNKNOWN-VLESS-WS-380MS` (url=788ms, status=HTTP 204)
25. `AKUN-052-DEV-VLESS-WS-118MS` (url=1620ms, status=HTTP 204)
26. `AKUN-056-PAI50288-VLESS-WS-1181MS` (url=2174ms, status=HTTP 204)
27. `AKUN-059-SOFT10-VLESS-WS-1030MS` (url=1831ms, status=HTTP 204)
28. `AKUN-060-CLOUDFLARE-VLESS-WS-734MS` (url=3180ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
