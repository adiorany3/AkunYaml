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
1. `AKUN-007-CLOUDFLARE-VLESS-WS-99MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-108MS` (url=634ms, status=HTTP 204)
3. `AKUN-003-CLOUDFLARE-VLESS-WS-108MS` (url=630ms, status=HTTP 204)
4. `AKUN-004-UNKNOWN-VLESS-WS-104MS` (url=346ms, nekobox=6169ms, status=no)
5. `AKUN-005-CLOUDFLARE-VLESS-WS-105MS` (url=368ms, nekobox=1259ms, status=no)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-101MS` (url=611ms, status=HTTP 204)
7. `AKUN-007-DEV-VLESS-WS-107MS` (url=388ms, nekobox=6174ms, status=no)
8. `AKUN-008-CLOUDFLARE-VLESS-WS-101MS` (url=1656ms, status=HTTP 204)
9. `AKUN-009-CLOUDFLARE-VLESS-WS-103MS` (url=613ms, status=HTTP 204)
10. `AKUN-011-CLOUDFLARE-VLESS-WS-106MS` (url=633ms, status=HTTP 204)
11. `AKUN-002-CLOUDFLARE-VLESS-WS-113MS`
12. `AKUN-004-CLOUDFLARE-VLESS-WS-105MS`
13. `AKUN-014-CLOUDFLARE-VLESS-WS-119MS` (url=627ms, status=HTTP 204)
14. `AKUN-016-CLOUDFLARE-VLESS-WS-114MS` (url=1651ms, status=HTTP 204)
15. `AKUN-017-CLOUDFLARE-VLESS-WS-120MS` (url=628ms, status=HTTP 204)
16. `AKUN-006-CLOUDFLARE-VLESS-WS-106MS`
17. `AKUN-019-UNKNOWN-VLESS-WS-122MS` (url=626ms, status=HTTP 204)
18. `AKUN-020-CLOUDFLARE-VLESS-WS-137MS` (url=630ms, status=HTTP 204)
19. `AKUN-021-TENCENT-VLESS-WS-111MS` (url=547ms, status=HTTP 204)
20. `AKUN-022-CLOUDFLARE-VLESS-WS-107MS` (url=657ms, status=HTTP 204)
21. `AKUN-001-CLOUDFLARE-VLESS-WS-106MS`
22. `AKUN-003-CLOUDFLARE-VLESS-WS-115MS`
23. `AKUN-025-CLOUDFLARE-VLESS-WS-137MS` (url=688ms, status=HTTP 204)
24. `AKUN-027-CLOUDFLARE-VLESS-WS-115MS` (url=655ms, status=HTTP 204)
25. `AKUN-028-UNKNOWN-VLESS-WS-121MS` (url=639ms, status=HTTP 204)
26. `AKUN-031-FREIFUNKFRANKEN-VLESS-WS-617MS` (url=3841ms, status=HTTP 204)
27. `AKUN-034-UNKNOWN-VLESS-WS-653MS` (url=897ms, status=HTTP 204)
28. `AKUN-035-CLOUDFLARE-VLESS-WS-663MS` (url=931ms, status=HTTP 204)
29. `AKUN-040-CLOUDFLARE-VLESS-WS-122MS` (url=1634ms, status=HTTP 204)
30. `AKUN-005-CLOUDFLARE-VLESS-WS-117MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
