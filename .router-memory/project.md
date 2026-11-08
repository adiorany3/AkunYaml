# Project context

AkunYaml at /Users/macbookpro/Documents/GitHub/AkunYaml; main; HEAD 0141b846f0c8586731238b1eb7db6f74856bc104. Numerous pre-existing feed/cache/generated and gameblock changes: preserve. Current source inspected; old note stale.

SSL EOF fix: build_support.fetch now retries transport/read errors and transient HTTP statuses up to three attempts, with 1/2-second backoff. Permanent HTTP and certificate verification failures fail immediately. TLS verification, URL allowlist, size bound, and fail-closed staged publishing preserved. Final errors identify source URL. No silent cache fallback.

Added tests/test_provider_download.py. Focused pytest: 39 passed. Live HTTPS category-games.mrs fetch succeeded (10167 bytes). Scoped diff --check passed. Global check flagged pre-existing subscription cache whitespace; untouched. Full unified refresh not run.

SHA256 build_support.py: 17f42a5ab07530684bba59a6262275ab030c18016ff2bd4b241885c30794056e. tests/test_provider_download.py: df1dff97f694cdf6fb50cc01cb4b5bfa42b24edb56a313954a28a8de88b0e7ef.

Previous gameblock edits remain: game providers prioritized before DIRECT. Revalidate before further edits. No project AGENTS.md. rg unavailable; use git grep and git --no-pager. Next: retry original update command; remaining failures identify URL.
