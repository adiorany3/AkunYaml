# Android No-QUIC Sniffer Compatibility Fix

## Problem
Some Clash Meta for Android builds use an older embedded Meta/Mihomo core that rejects the `QUIC` entry under `sniffer.sniff` and stops loading the profile with an error similar to:

`no find the sniffer QUIC`

## Fix
- Android output keeps domain sniffing for `HTTP` and `TLS` only.
- `QUIC` is not injected into `openclash_android.yaml` during network hardening.
- Existing Android output is repaired by removing a stale `QUIC` sniffer entry.
- Router/OpenClash output can continue using QUIC sniffing where the target core supports it.
- Android rule providers remain YAML-only. No `.mrs` dependency is reintroduced.
- Android audit now rejects a profile if QUIC sniffer is reintroduced.

## Result
The Android profile remains in `mode: rule`, keeps ad/tracker/malware blocking, preserves the YouTube playback guard, and ends with `MATCH,GLOBAL`.
