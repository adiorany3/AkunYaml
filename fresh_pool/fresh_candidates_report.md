# Fresh Candidate Pool

File ini dibuat otomatis oleh GitHub Actions setelah node diuji.
Tujuannya: OpenWrt punya cadangan config/node fresh sebelum semua node utama mati.

## Output Fresh Pool
- `openclash_fresh_pool.yaml`: config darurat berisi kandidat fresh yang sudah lolos test GitHub.
- `fresh_pool/fresh_candidates.txt`: link akun kandidat fresh hasil URL test Mihomo.
- `fresh_pool/fresh_candidates_strict.txt`: link akun yang lolos sampai test NekoBox/sing-box.
- `fresh_pool/fresh_candidates.json`: metadata ringkas fresh pool.

## Ringkasan
- Kandidat fresh URL-tested: 8
- Kandidat strict NekoBox-tested: 8
- Proxy di openclash_fresh_pool.yaml: 12

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
1. `AKUN-001-RS-RAPIDSEEDBOX-20190717-VLESS-WS-271MS` (url=534ms, status=HTTP 204)
2. `AKUN-002-VEESP-SIA-VLESS-WS-275MS`
3. `AKUN-003-GO-DADDY-COM-LLC-VLESS-WS-267MS`
4. `AKUN-004-SPECIAL-IPV4-BENCHMARK-T-VLESS-WS-271MS`
5. `AKUN-005-CLOUDFLARE-VLESS-WS-268MS`
6. `AKUN-006-CLOUDFLARE-VLESS-WS-623MS`
7. `AKUN-007-NL-TELEMAGIC-20111109-VLESS-WS-911MS`
8. `AKUN-008-CLOUDFLARE-VLESS-WS-853MS`

## Catatan
Fresh pool bukan pengganti AutoPilot. AutoPilot tetap memilih jalur sehat di router.
Fresh pool adalah cadangan siap-download ketika semua group utama mulai gagal berulang.
