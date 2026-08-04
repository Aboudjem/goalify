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
import re
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

# --- Version consistency across all four sources of truth ---
# Enforced by a test, not by discipline: a release where these drift is a broken release.
def _skill_version():
    with open(os.path.join(ROOT, "skills", "goalify", "SKILL.md"), encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^\s+version:\s*[\"']?(\d+\.\d+\.\d+)", text, re.MULTILINE)
    return m.group(1) if m else None


def _changelog_version():
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^##\s*\[(\d+\.\d+\.\d+)\]", line)
            if m:
                return m.group(1)
    return None


versions = {
    "SKILL.md metadata.version": _skill_version(),
    "plugin.json version": plugin.get("version"),
    "marketplace.json plugins[0].version": (mkt.get("plugins") or [{}])[0].get("version"),
    "CHANGELOG.md latest release": _changelog_version(),
}
distinct = set(versions.values())
check(
    "version is identical across SKILL.md, plugin.json, marketplace.json, CHANGELOG.md",
    len(distinct) == 1 and None not in distinct,
    ", ".join(f"{k}={v!r}" for k, v in versions.items()),
)

# --- v2 CONTRACT: no tracked doc may tell a user to pass a file path to /goal ---
# `/goal` takes a condition string (code.claude.com/docs/en/goal + the shipped binary).
# v1.1.0 shipped `/goal <path>` everywhere (v1-antipattern); it can never be verified by the
# tool-less evaluator. This test makes the regression impossible to reintroduce.
# Catches absolute paths (/Users/..., ~/..., $HOME), explicit <path> placeholders, AND
# relative paths (./x, .goal/auth.md, docs/plan.md). The relative form is the one that
# matters: the v1.1.0 teaser rendered `/goal .goal/auth.md` on screen (v1-antipattern), and an
# absolute-path-only regex over *.md alone let it through.
PATH_HANDOFF_RE = re.compile(
    r"/goal\s+(?:"
    r"<\s*(?:abs|absolute|path|file)"      # <path>, <ABSOLUTE PATH>, <file...>
    r"|~/|\./|/[A-Za-z._~-]"               # ~/x, ./x, /Users/x
    r"|\$\{?HOME"                          # $HOME/x
    r"|[\w.\-/]*\.(?:md|markdown|txt)\b"   # .goal/auth.md, docs/plan.md
    r")",
    re.I,
)
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mp3", ".woff", ".woff2",
              ".ico", ".pdf", ".zip", ".ttf", ".otf"}
tracked = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, cwd=ROOT,
).stdout.splitlines()
EXEMPT_MARKER = "v1-antipattern"
path_handoffs = []
exempt = []
scanned = 0
for rel in tracked:
    if os.path.splitext(rel)[1].lower() in BINARY_EXT:
        continue
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
            scanned += 1
            for ln, line in enumerate(f, 1):
                if PATH_HANDOFF_RE.search(line):
                    if EXEMPT_MARKER in line:
                        exempt.append(f"{rel}:{ln}")
                    else:
                        path_handoffs.append(f"{rel}:{ln}")
    except (IsADirectoryError, FileNotFoundError, OSError):
        continue
check(
    f"no tracked text file passes a file path to /goal (v2 contract; {scanned} files scanned)",
    not path_handoffs,
    "found at " + ", ".join(path_handoffs[:8]),
)
# Documenting the banned pattern requires writing it, so a line may opt out with the
# marker below. The cap is pinned to exactly the number in use, so ADDING an exemption
# fails the build and forces a deliberate review rather than sliding through a spare
# slot. Note what this enforces: a COUNT. It cannot tell prose about the old handoff
# from an instruction to use it — that judgement is the reviewer's, and the cap exists
# to make sure a reviewer is actually summoned.
EXPECTED_EXEMPTIONS = 3
check(
    f"v1-antipattern exemptions stay pinned at {EXPECTED_EXEMPTIONS} "
    f"({len(exempt)} in use: {', '.join(exempt) or 'none'})",
    len(exempt) == EXPECTED_EXEMPTIONS,
    "adding one is a deliberate act: confirm the line DESCRIBES the old handoff rather "
    "than instructing it, then bump EXPECTED_EXEMPTIONS in the same commit",
)

# --- The shipped example must satisfy every clause the SKILL.md template mandates ---
example_path = os.path.join(ROOT, "examples", "sample-goal-file.md")
try:
    with open(example_path, encoding="utf-8") as f:
        ex_raw = f.read()
    ex = re.sub(r"\s+", " ", re.sub(r"(?m)^\s{0,3}>\s?", "", ex_raw))
    for ch in ("`", "*", "'", "’"):
        ex = ex.replace(ch, "")
    ex = ex.lower()
    example_clauses = {
        "declares its own absolute path": "this files own path" in ex,
        "re-read-each-loop rail": "re-read this file" in ex,
        "states it is the brief, not the stop condition": "not the stop condition" in ex,
        "GOAL directive section": "goal (the autonomous directive)" in ex,
        "verified-context section": "re-confirm live" in ex,
        "locked decisions section": "locked by the user" in ex,
        "fan-out guardrail": "serialize" in ex,
        "subagent barrier": "subagent barrier" in ex,
        "no-hallucination rule": "no hallucination" in ex,
        "separate-agent verification": "separate agent" in ex and "self-approve" in ex,
        "full-implementations rule": "full implementation" in ex,
        "search-before-assuming rule": "search before assuming" in ex,
        "output redirection": "2>&1" in ex_raw,
        "commit-before-risky rule": "commit before risky" in ex,
        "3-strike escalation": "3-strike" in ex,
        "definition of done wired to commands": "definition of done" in ex and "verified by" in ex,
        "progress checklist": "progress checklist" in ex,
        "final output section": "final output" in ex,
        "archive gate is LOW FREEDOM": "low freedom" in ex and "do not modify" in ex,
        "archive gate has rationalization counters": "basically done" in ex,
        "archive gate keeps the file on failure": "leave the file" in ex,
        "archive gate has a path rail": "path rail" in ex,
    }
    for clause, ok in example_clauses.items():
        check(f"example: {clause}", ok)

    # The condition is what the user actually pastes into /goal. Claude Code rejects
    # anything over 4,000 chars, and the hook prompt substitutes bare `$ARGUMENTS`/`$N`
    # sequences — so both are asserted here rather than eyeballed.
    cond_m = re.search(r"```text\n(.*?)\n```", ex_raw, re.DOTALL)
    check("example ships a derived /goal condition string", bool(cond_m))
    if cond_m:
        condition = cond_m.group(1)
        check(
            "example condition is <= 4,000 characters (Claude Code hard limit)",
            len(condition) <= 4000,
            f"{len(condition)} chars",
        )
        check(
            "example condition states its own character count correctly",
            f"{len(condition):,} characters" in ex_raw,
            f"actual={len(condition):,}",
        )
        check(
            "example condition contains no bare $ (hook-substitution hazard)",
            not re.search(r"(?<!\\)\$", condition),
            "escape or reword any $ sequence",
        )
        flat_cond = " ".join(condition.split())
        for clause, needle in [
            ("names the brief by absolute path", "/Users/example/widget-api/.goal/"),
            ("carries a sentinel token", "_EVIDENCE"),
            ("requires the most recent turn", "most recent assistant turn"),
            ("requires a dedicated closeout turn", "closeout turn"),
            ("rejects unquoted claims", "freshly quoted"),
            ("blocks the impossible escape hatch", "do not declare this goal impossible"),
            ("carries an explicit turn bound", "stop after"),
        ]:
            check(f"example condition: {clause}", needle in flat_cond)
except (FileNotFoundError, OSError) as e:
    check("examples/sample-goal-file.md is readable", False, str(e))

# --- Report ---
print("-" * 60)
passed = _total - len(failures)
print(f"{passed}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
