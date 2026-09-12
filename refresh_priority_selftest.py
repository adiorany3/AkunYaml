"""Offline checks for fresh-source priority and immutable manual input."""

import tempfile
from pathlib import Path
from types import SimpleNamespace

import generate_yaml as generator


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    pool = root / "fresh_pool"
    pool.mkdir()
    saved = "vless://saved@example.com:443#saved"
    current = "https://source.example/subscription"
    (pool / "fresh_candidates_seed.txt").write_text(saved + "\n", encoding="utf-8")
    assert generator._merge_saved_candidate_seed(current, pool).splitlines() == [current, saved]

source = Path(generator.__file__).read_text(encoding="utf-8")
assert 'Path(manual_file).write_text' not in source

def node(name: str, server: str):
    return SimpleNamespace(name=name, clash={"name": name, "type": "vless", "server": server, "port": 443})

manual = node("SAME", "manual.example")
same_content = node("SAME", "manual.example")
different = node("SAME", "automatic.example")
resolved = generator._resolve_proxy_name_collisions([same_content, different], reserved=[manual])
assert len(resolved) == 1
assert resolved[0].name.startswith("SAME-") and len(resolved[0].name) <= 64
assert resolved[0].clash["name"] == resolved[0].name
first_name = resolved[0].name
assert generator._resolve_proxy_name_collisions(resolved, reserved=[manual])[0].name == first_name

print("PASS: current subscriptions first; manual input immutable; identical proxy deduped; different proxy renamed")
