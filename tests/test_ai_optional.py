"""AI is opt-in; stale AI cache must not leak into disabled builds."""
import ast
import json
import os
import re
from pathlib import Path

import pytest

from local_runner import DEFAULT_ENV, load_ai_adblock_domains

ROOT = Path(__file__).resolve().parents[1]


def test_project_defaults_disable_ai_without_disabling_feeds():
    config = json.loads((ROOT / "local_config.json").read_text())
    assert config["AI_ADBLOCK_ENABLED"] == DEFAULT_ENV["AI_ADBLOCK_ENABLED"] == "false"
    assert config["SECURITY_FEED_GUARD"] == "true"


@pytest.mark.parametrize("flag", [None, "false", "0", "off", "", "invalid", "true", "1", "yes", "on"])
def test_runner_and_generator_cache_require_explicit_opt_in(tmp_path, monkeypatch, flag):
    if flag is None:
        monkeypatch.delenv("AI_ADBLOCK_ENABLED", raising=False)
    else:
        monkeypatch.setenv("AI_ADBLOCK_ENABLED", flag)
    cache = tmp_path / ".runtime_cache/ai_adblock_blocklist.txt"
    cache.parent.mkdir()
    cache.write_text("ads.example\n")
    enabled = flag in {"true", "1", "yes", "on"}
    assert load_ai_adblock_domains(tmp_path, set()) == (["ads.example"] if enabled else [])
    assert load_ai_adblock_domains(tmp_path, {"ads.example"}) == []

    # Exercise the actual generator cache expression without starting network/node tests.
    tree = ast.parse((ROOT / "generate_yaml.py").read_text())
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "ai_blocked_domains" for t in node.targets))
    reads = []

    def read(path):
        reads.append(path)
        return "ads.example\n"

    context = {"os": os, "re": re, "_read_text_file": read}
    exec(compile(ast.Module(body=[assignment], type_ignores=[]), "generate_yaml.py", "exec"), context)  # noqa: S102 - execute only the local cache expression
    assert context["ai_blocked_domains"] == (["ads.example"] if enabled else [])
    assert bool(reads) == enabled
