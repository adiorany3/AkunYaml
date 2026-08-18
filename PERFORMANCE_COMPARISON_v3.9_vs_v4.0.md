# v3.9 vs v4.0 Performance Comparison

| Output | v3.9 probes/min | v4.0 probes/min | Reduction | Proxies | v4.0 YAML |
|---|---:|---:|---:|---:|---:|
| `openclash_auto.yaml` | 38.33 | 9.33 | 75.7% | 14 | 37.0 KiB |
| `openclash_lite.yaml` | 38.33 | 9.33 | 75.7% | 14 | 24.9 KiB |
| `openclash_android.yaml` | 38.33 | 9.33 | 75.7% | 14 | 28.4 KiB |
| `openclash_fresh_pool.yaml` | 45.00 | 9.33 | 79.3% | 34 | 38.3 KiB |

Metric counts direct node probes from non-lazy `url-test`, `fallback`, and `load-balance` groups. Lazy groups remain available and are checked when used.
