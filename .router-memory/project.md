# Project context

AkunYaml, main, HEAD 69e31c30c2821029b5250e0b3ca8df4425ee20cb. Many pre-existing output/cache changes: preserve. Prior notes stale, not relied on.

Removed only remote schema declaration from output/sing-box/singbox_direct_adblock.json. JSON parsing, before/after semantic equality excluding schema, byte comparison, scoped git diff --check passed. Target SHA256 0c92d4fa672840903d0893add67fa0df339a07bfc765b082c2d5cb806336b672. No sing-box executable available. No trust settings changed.

Generator generate_yaml.py:1023 still emits schema; regeneration may restore it. Generator unchanged for scoped request. No project AGENTS.md found. rg unavailable. Revalidate source before future work.
