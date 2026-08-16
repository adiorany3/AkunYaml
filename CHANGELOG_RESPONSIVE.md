# Responsive Network Tuning

## 2026-08-16

- Added ARC DNS cache.
- Added fallback-lazy-query when DNS fallback exists.
- Added proxy-server-nameserver for independent proxy hostname resolution.
- Kept tcp-concurrent and unified-delay enabled.
- Changed TCP keep-alive idle from 600 seconds to 30 seconds.
- Added no-resolve to private IPv4 rules.
- Reduced WARM-UP active pool to 5 nodes, checked every 20 seconds.
- Reduced WARM-UP-CF active pool to 4 nodes, checked every 30 seconds.
- AUTO-FAST now checks up to 8 nodes every 45 seconds.
- PING-CHECK now scans all nodes every 180 seconds.
- Secondary application groups and fallback pools use lazy health-checks.
- GLOBAL now checks only core automatic groups instead of duplicating checks across all raw nodes and application groups.
- No forced DNS HTTP/3 and no MTU override were added because those depend strongly on ISP/router path characteristics.
