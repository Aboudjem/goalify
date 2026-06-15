#!/usr/bin/env python3
"""
Smoke tests for goalify manifests and evals.

Tests:
  1. plugin.json parses as valid JSON and has required fields.
  2. marketplace.json parses as valid JSON and has required fields.
  3. evals/check_skill.py exits 0 against the real SKILL.md (regression guard).

No third-party deps; standard library only.
Run: python3 tests/test_manifests.py
Exit 0 = all pass, 1 = at least one failed.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    tag = "PASS" if ok else "FAIL"
    msg = f"{tag}: {name}"
    if detail and not ok:
        msg += f"  ({detail})"
    print(msg)
    if not ok:
        failures.append(name)


# --- plugin.json ---
plugin_path = os.path.join(ROOT, ".claude-plugin", "plugin.json")
try:
    with open(plugin_path) as f:
        plugin = json.load(f)
    check("plugin.json parses as valid JSON", True)
    check("plugin.json has 'name'", bool(plugin.get("name")), f"got {plugin.get('name')!r}")
    check("plugin.json name == 'goalify'", plugin.get("name") == "goalify", f"got {plugin.get('name')!r}")
    check("plugin.json has 'version'", bool(plugin.get("version")), f"got {plugin.get('version')!r}")
    check("plugin.json has 'description' >=10 chars", len(plugin.get("description", "")) >= 10)
    check("plugin.json 'author' is a dict with 'name'", isinstance(plugin.get("author"), dict) and bool(plugin["author"].get("name")))
    check("plugin.json 'keywords' is a list", isinstance(plugin.get("keywords"), list), "must be array, not string")
    check("plugin.json 'license' == 'MIT'", plugin.get("license") == "MIT")
    check("plugin.json keywords include 'claude-code'", "claude-code" in plugin.get("keywords", []))
    check("plugin.json keywords include 'goalify'", "goalify" in plugin.get("keywords", []))
except (json.JSONDecodeError, FileNotFoundError) as e:
    check("plugin.json parses as valid JSON", False, str(e))

# --- marketplace.json ---
mkt_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
try:
    with open(mkt_path) as f:
        mkt = json.load(f)
    check("marketplace.json parses as valid JSON", True)
    check("marketplace.json has 'plugins' list", isinstance(mkt.get("plugins"), list) and len(mkt["plugins"]) > 0)
    p0 = mkt["plugins"][0] if mkt.get("plugins") else {}
    check("marketplace.json plugin[0] has 'name'", bool(p0.get("name")))
    check("marketplace.json plugin[0] has 'source'", bool(p0.get("source")))
    check("marketplace.json plugin[0] has 'description' >=10 chars", len(p0.get("description", "")) >= 10)
    check("marketplace.json plugin[0] has 'version'", bool(p0.get("version")))
except (json.JSONDecodeError, FileNotFoundError) as e:
    check("marketplace.json parses as valid JSON", False, str(e))

# --- evals/check_skill.py regression guard ---
skill_path = os.path.join(ROOT, "skills", "goalify", "SKILL.md")
eval_script = os.path.join(ROOT, "evals", "check_skill.py")
result = subprocess.run(
    [sys.executable, eval_script, skill_path],
    capture_output=True, text=True
)
check(
    "evals/check_skill.py exits 0 on skills/goalify/SKILL.md",
    result.returncode == 0,
    f"exit={result.returncode}\n{result.stdout[-400:] if result.stdout else ''}"
)

# --- Report ---
print("-" * 60)
passed = _total - len(failures)
print(f"{passed}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
