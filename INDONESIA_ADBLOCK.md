# Indonesia Adblock Layer v3.7

Lapisan ini menambahkan pemblokiran iklan regional Indonesia/Malaysia ke output OpenClash router.

## Sumber

- ABPindo DNS/domain list sebagai provider regional.
- Provider global yang sudah ada tetap dipertahankan untuk cakupan internasional.

## Implementasi

Provider router:

- Nama: `ads_indonesia`
- Behavior: `domain`
- Format: `text`
- Path cache: `./rule_providers/ads_indonesia.txt`
- Refresh mengikuti `ADBLOCK_PROVIDER_INTERVAL`.

Rule dievaluasi setelah threat protection dan sebelum `ads_domain` global.
Allowlist tetap memiliki prioritas lebih tinggi.

## Profil

Aktif pada:

- `openclash_auto.yaml`
- `openclash_lite.yaml`
- `openclash_fresh_pool.yaml`

Profil `openclash_android.yaml` tetap menggunakan provider YAML-only agar kompatibel dengan core Android lama. Provider ABPindo DNS berbentuk plain text tidak dipaksakan ke profil tersebut.

## Toggle

Default:

```text
INDONESIA_ADBLOCK=true
```

Set `INDONESIA_ADBLOCK=false` jika ingin menonaktifkan provider regional tanpa menghapus kode.

## Browser

Filter browser penuh ABPindo tidak dicampur ke YAML OpenClash karena berisi aturan URL dan cosmetic filtering yang tidak cocok untuk rule-provider DNS/domain. Referensi subscription disimpan pada `browser_filter_subscriptions_v3.7.txt`.
