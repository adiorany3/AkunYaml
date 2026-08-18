# Android Cold Fallback v4.2

v4.2 memperbaiki topology multi-host khusus `openclash_android.yaml` setelah audit konektivitas Android.

## Tujuan

- `BUG_SERVERS[0]` menjadi satu-satunya host untuk jalur normal Android.
- Host kedua dan seterusnya tidak masuk ke `WARM-UP`, `AUTO-FAST`, AI pool, streaming pool, atau fallback normal.
- Tidak ada lagi fallback per akun (`*-FB`).
- Backup dikelompokkan berdasarkan host (`ANDROID-BACKUP-H2`, `ANDROID-BACKUP-H3`, dst.) dan ditempatkan di belakang `ANDROID-COLD-BACKUP`.
- `GLOBAL` dibuat shallow dan lazy untuk mengurangi health-check bertingkat.
- Android selalu memakai `mode: rule`, termasuk ketika adblock dimatikan.

## Topology

```text
Normal:
H1 account nodes
  -> WARM-UP (hot, small pool)
  -> AUTO-FAST (lazy)
  -> GLOBAL

Backup:
H2 nodes -> ANDROID-BACKUP-H2 (lazy)
H3 nodes -> ANDROID-BACKUP-H3 (lazy)
          -> ANDROID-COLD-BACKUP (lazy)
          -> GLOBAL setelah primary pools
```

## Setting

```json
{
  "ANDROID_MULTI_HOST_MODE": "primary-cold-fallback",
  "ANDROID_FALLBACK_HOST_LIMIT": "3",
  "ANDROID_FALLBACK_TOTAL_CAP": "24",
  "ANDROID_FALLBACK_INTERVAL": "300",
  "ANDROID_FALLBACK_LAZY": "true",
  "ANDROID_GLOBAL_FALLBACK_INTERVAL": "180",
  "ANDROID_GLOBAL_FALLBACK_LAZY": "true",
  "ANDROID_AUTO_FAST_LAZY": "true"
}
```

Mode lama `primary-fallback` tetap diterima sebagai alias dan otomatis diarahkan ke `primary-cold-fallback`.

## Hasil audit paket default

- Android `mode: rule`.
- Android provider tetap YAML-only.
- `MATCH,GLOBAL` tetap menjadi rule akhir.
- `WARM-UP` menjadi satu-satunya hot primary pool.
- `AUTO-FAST` lazy.
- Active direct probes pada output Android default turun menjadi sekitar 4 probe/menit dari sekitar 9,33 probe/menit pada v4.1/v4.0.
- Threat-safe, YouTube guard, app ads, streaming ads, popup/game ads, dan security hardening tetap lolos regression test.

Gunakan multi-host hanya untuk host/server yang memang Anda miliki atau berhak gunakan.
