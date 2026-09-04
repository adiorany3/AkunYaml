#!/usr/bin/env python3
from pathlib import Path
import sys, yaml

ROUTER_FILES = [
    Path('openclash_auto.yaml'),
    Path('openclash_lite.yaml'),
    Path('openclash_fresh_pool.yaml'),
]
EXTRA = [
    'adservice.google.com',
    'pagead2.googleadservices.com',
    'afs.googlesyndication.com',
    'stats.g.doubleclick.net',
    'm.doubleclick.net',
    'mediavisor.doubleclick.net',
    'adtrafficquality.google',
    'googleadapis.com',
    'mobileads.google.com',
    'pagead.l.google.com',
]
PROTECTED_SUFFIX = [
    'googlevideo.com',
    'ytimg.com',
    'youtubei.googleapis.com',
    'youtube.googleapis.com',
    'ggpht.com',
]
PROTECTED_EXACT = ['static.doubleclick.net', 'jnn-pa.googleapis.com']


def reject_cover_index(rules, domain):
    domain = domain.lower().rstrip('.')
    best = None
    for idx, rule in enumerate(rules):
        parts = [p.strip() for p in rule.split(',')]
        if len(parts) != 3 or parts[2].upper() != 'REJECT':
            continue
        kind, value = parts[0].upper(), parts[1].lower().rstrip('.')
        covered = kind == 'DOMAIN' and value == domain
        covered = covered or (kind == 'DOMAIN-SUFFIX' and (domain == value or domain.endswith('.' + value)))
        if covered and (best is None or idx < best):
            best = idx
    return best

def fail(msg):
    print('[ERROR]', msg)
    return 1

def main():
    errors = 0
    for path in ROUTER_FILES:
        data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        rules = [str(x) for x in data.get('rules', []) or []]
        extra_indexes = []
        for domain in EXTRA:
            idx = reject_cover_index(rules, domain)
            if idx is None:
                errors += fail(f'{path.name}: missing REJECT coverage for {domain}')
            else:
                extra_indexes.append(idx)
        for domain in PROTECTED_EXACT:
            if any(r == f'DOMAIN,{domain},REJECT' or r == f'DOMAIN-SUFFIX,{domain},REJECT' for r in rules):
                errors += fail(f'{path.name}: protected compatibility host rejected: {domain}')
        if 'DOMAIN,static.doubleclick.net,YOUTUBE' not in rules:
            errors += fail(f'{path.name}: static.doubleclick.net compatibility guard missing')
        for domain in PROTECTED_SUFFIX:
            if any(r.startswith(f'DOMAIN-SUFFIX,{domain},') and r.endswith(',REJECT') for r in rules):
                errors += fail(f'{path.name}: playback suffix rejected: {domain}')
        first_extra = min(extra_indexes) if extra_indexes else len(rules)
        gv = rules.index('DOMAIN-SUFFIX,googlevideo.com,YOUTUBE')
        if first_extra >= gv:
            errors += fail(f'{path.name}: extra ad rules are not ahead of playback guard')
        print(f'[OK] YouTube playback-safe router audit: {path.name}')

    android = Path('openclash_android.yaml')
    if android.exists():
        rules = [str(x) for x in (yaml.safe_load(android.read_text(encoding='utf-8')) or {}).get('rules', []) or []]
        # v4.6 router extras must not be injected as a dedicated pre-playback layer on Android.
        # Existing app-ad rules may contain some exact domains later in the file, which is allowed.
        yt_idx = rules.index('DOMAIN-SUFFIX,googlevideo.com,YOUTUBE') if 'DOMAIN-SUFFIX,googlevideo.com,YOUTUBE' in rules else -1
        if yt_idx >= 0:
            for d in EXTRA:
                try:
                    idx = rules.index(f'DOMAIN,{d},REJECT')
                except ValueError:
                    continue
                if idx < yt_idx:
                    errors += fail(f'openclash_android.yaml: router-only YouTube extra leaked before playback guard: {d}')
        print('[OK] Android remains outside router-only YouTube extra layer')

    filters = Path('youtube_browser_filters.txt').read_text(encoding='utf-8')
    for d in EXTRA:
        if f'||{d}^$domain=youtube.com' not in filters:
            errors += fail(f'browser filter missing: {d}')
    for bad in ('||googlevideo.com', '||static.doubleclick.net'):
        if bad in filters:
            errors += fail(f'browser filter blocks protected host: {bad}')
    if errors:
        print(f'[FAIL] {errors} issue(s)')
        return 1
    print('[OK] YouTube playback-safe v4.6 audit')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
