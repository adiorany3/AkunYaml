# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 16
- Kandidat strict NekoBox-tested: 7
- Proxy di openclash_fresh_pool.yaml: 20

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
1. `AKUN-004-CLOUDFLARE-VLESS-WS-93MS`
2. `AKUN-002-CLOUDFLARE-VLESS-WS-112MS` (url=352ms, nekobox=6183ms, status=no)
3. `AKUN-002-CLOUDFLARE-VLESS-WS-97MS`
4. `AKUN-001-CLOUDFLARE-VLESS-WS-98MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-106MS` (url=357ms, nekobox=6177ms, status=no)
6. `AKUN-006-CLOUDFLARE-VLESS-WS-117MS` (url=362ms, nekobox=6173ms, status=no)
7. `AKUN-005-CLOUDFLARE-VLESS-WS-123MS`
8. `AKUN-003-CLOUDFLARE-VLESS-WS-105MS`
9. `AKUN-006-CLOUDFLARE-VLESS-WS-130MS`
10. `AKUN-007-CLOUDFLARE-VLESS-WS-126MS`
11. `AKUN-012-CLOUDFLARE-VLESS-WS-356MS` (url=3050ms, status=HTTP 204)
12. `AKUN-013-FREIFUNKFRANKEN-VLESS-WS-621MS` (url=1998ms, status=HTTP 204)
13. `AKUN-014-CLOUDFLARE-VLESS-WS-98MS` (url=789ms, status=HTTP 204)
14. `AKUN-015-UNKNOWN-VLESS-WS-412MS` (url=2841ms, status=HTTP 204)
15. `AKUN-021-CLOUDFLARE-VLESS-WS-847MS` (url=1471ms, status=HTTP 204)
16. `AKUN-054-CLOUDFLARE-VLESS-WS-115MS` (url=1319ms, status=HTTP 204)

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
