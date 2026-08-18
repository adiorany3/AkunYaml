# Changelog v4.7

## YouTube Gambling Sponsor Guard

- Added router-only `gambling-mini` category provider.
- Added `OPENWRT_GAMBLING_BLOCK=true`.
- Added `OPENWRT_LITE_GAMBLING_BLOCK=true`.
- Category rule runs after threat intelligence and before broad ads/trackers.
- Added feed-guard validation with a minimum expected entry count.
- No gambling keyword heuristic is used.
- YouTube media/playback hosts remain protected from REJECT rules.
- OpenClash Android remains byte-identical to v4.6.
- Added `youtube_gambling_sponsor_audit.py`.
