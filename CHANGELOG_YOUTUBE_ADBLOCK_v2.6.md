# v2.6 YouTube Adblock Enhancement

- Activated `apply_security()` and `apply_youtube_guard()` in the actual output pipeline.
- Default profile changed to `balanced` with YouTube mode `enhanced`.
- Uses MetaCubeX `category-ads-all.mrs` and `tracker.mrs` providers.
- Adds conservative YouTube/Google ad endpoint blocking for DoubleClick, Google Syndication, Google Ad Services, 2mdn, and IMA SDK.
- Keeps YouTube playback domains, especially `googlevideo.com`, outside explicit REJECT rules.
- Keeps DNS-level ad blocking disabled by default to reduce playback breakage.
- Expands browser cosmetic filters without brittle scriptlet rules.
- Adds `youtube_adblock_audit.py` and runs it automatically during Mac refresh before final target validation.
- All four bundled YAML outputs pass static OpenClash target validation and the YouTube adblock audit.
