# Changelog v4.2 Android Cold Fallback

- Menghapus fallback per akun `*-FB` pada Android.
- Menjadikan H1 sebagai satu-satunya endpoint di normal routing pools.
- Mengelompokkan H2/H3 sebagai host-level cold backup.
- Menambahkan `ANDROID-COLD-BACKUP` sebagai fallback host-level.
- `GLOBAL` Android menjadi shallow fallback: `WARM-UP -> AUTO-FAST -> ANDROID-COLD-BACKUP` jika backup tersedia.
- `GLOBAL` Android sekarang lazy dengan interval default 180 detik.
- `AUTO-FAST` Android sekarang lazy secara default.
- Interval cold backup dinaikkan menjadi 300 detik.
- Android dipaksa tetap `mode: rule`, juga saat profil adblock `off`.
- Family/category DNS untuk `child-safe` dan `threat-safe` sekarang diterapkan langsung oleh core builder, tidak bergantung pada post-processing runner.
- `openclash_android.yaml` diregenerasi memakai topology v4.2 dan seluruh layer adblock/security dipulihkan melalui pipeline normal.
- Regression audit baru memastikan tidak ada nested fallback per akun dan secondary host tidak bocor ke hot pools.
- Active direct probes output Android default turun dari sekitar 9,33 menjadi 4 probe/menit.
