# Android Banking Safe Mode v4.4

## Tujuan

Mode ini mengurangi konflik antara OpenClash for Android dan aplikasi perbankan yang sensitif terhadap proxy DNS, Fake-IP, sniffer, atau rule ad/tracker.

Default saat ini hanya mencakup:

- `seabank.co.id`

## Perilaku SeaBank

Untuk domain banking yang terdaftar, profil Android menerapkan empat lapis kompatibilitas:

1. `DIRECT` routing.
2. Fake-IP bypass melalui `dns.fake-ip-filter`.
3. Public DoH khusus melalui `dns.nameserver-policy`.
4. Sniffer skip melalui `sniffer.skip-domain`.

Urutan rule tetap konservatif:

```text
LAN / AI / allowlist / YouTube guard
→ malware
→ phishing
→ cryptominer
→ BANKING SAFE DIRECT
→ marketplace live guard
→ privacy / scam / ads / tracker
→ MATCH,GLOBAL
```

Jadi domain bank tidak dibebaskan dari tiga threat feed ber-confidence tinggi yang berada di atas Banking Safe Mode.

## Setting

`local_config.json`:

```json
{
  "ANDROID_BANKING_SAFE_MODE": "true",
  "ANDROID_BANKING_DOMAINS": [
    "seabank.co.id"
  ],
  "ANDROID_BANKING_EXACT_DOMAINS": []
}
```

`ANDROID_BANKING_DOMAINS` menggunakan suffix-domain. Contoh `seabank.co.id` juga mencakup subdomain di bawahnya.

`ANDROID_BANKING_EXACT_DOMAINS` digunakan jika hanya satu hostname tertentu yang harus diizinkan DIRECT.

## Batasan

Banking Safe Mode hanya memperbaiki jalur jaringan di dalam konfigurasi Mihomo/OpenClash. Mode ini tidak menyembunyikan VPN, tidak mengubah status perangkat, dan tidak mencoba melewati pemeriksaan keamanan aplikasi bank.

Jika SeaBank tetap menolak login ketika interface VPN aktif, gunakan fitur per-app VPN exclusion/split tunneling dari client Android jika tersedia, atau nonaktifkan VPN saat memakai aplikasi bank.
