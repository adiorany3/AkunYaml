# YouTube Gambling Sponsor Guard v4.7

Version 4.7 adds an OpenWrt-only category guard for gambling destinations that may be reached from sponsored content or advertising flows.

## Scope

- OpenWrt/OpenClash Auto: enabled
- OpenWrt/OpenClash Lite: enabled
- OpenWrt/OpenClash Fresh Pool: enabled
- OpenClash Android: unchanged

## Design

The guard uses a dedicated domain-category provider instead of broad `DOMAIN-KEYWORD` rules. This reduces false positives from normal domains that happen to contain words associated with gambling.

The rule is inserted after threat-intelligence protection and before broad advertising/tracker providers:

1. high-confidence threat rules
2. threat intelligence
3. gambling destination guard
4. enhanced ad/popup providers
5. Indonesia ads
6. global ads and trackers

YouTube playback compatibility remains higher priority where required. The guard does not reject the primary media/CDN domains used by YouTube playback.

## Configuration

`local_config.json`:

```json
{
  "OPENWRT_GAMBLING_BLOCK": "true",
  "OPENWRT_LITE_GAMBLING_BLOCK": "true"
}
```

For a very low-memory Lite router, `OPENWRT_LITE_GAMBLING_BLOCK` can be set to `false` independently.

## Limits

OpenClash cannot inspect the semantic content of an encrypted YouTube ad and determine whether a sponsor is gambling before the destination domain is contacted. This guard therefore focuses on blocking known gambling destinations and keeping generic sponsored-ad filtering active without breaking video playback.
