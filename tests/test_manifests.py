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
import xml.etree.ElementTree as ET

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
PATH_TOKEN = (
    r"(?:"
    r"<\s*(?:abs|absolute|path|file)"      # <path>, <ABSOLUTE PATH>, <file...>
    r"|~/|\./"                             # ~/x, ./x
    # /Users/x — a further separator or an extension is required, so that the bare word
    # `/goal` (or any other slash-command) is not mistaken for the start of a path.
    r"|/[A-Za-z._~-][\w.\-]*(?:/|\.[A-Za-z])"
    r"|\$\{?HOME"                          # $HOME/x
    r"|[A-Za-z]:\\"                        # C:\Users\me\plan.md
    r"|[\w.\-/]*\.(?:md|markdown|txt)\b"   # .goal/auth.md, docs/plan.md
    r")"
)
# `\W{0,4}` absorbs quoting and emphasis that would otherwise sit between the command and
# the path. Belt and braces with _scannable() below, which strips those characters anyway.
PATH_HANDOFF_RE = re.compile(r"/goal\s+\W{0,4}" + PATH_TOKEN, re.I)

# A line is normalised before it is scanned, because the banned instruction is written by
# humans in prose, not by a fuzzer. Without this, every one of these slipped through while
# reading as an unambiguous instruction to do the banned thing:
#     /goal "~/acme/.goal/plan.md"   <- v1-antipattern specimen (also backtick/emphasis)
#     /goal C:\Users\me\plan.md      <- v1-antipattern specimen (Windows drive form)
# Markdown links collapse to their target first, then quoting/emphasis characters are
# dropped. Known remaining gap, stated rather than papered over: a path introduced by
# intervening *words* ("/goal followed by ~/x.md") is not caught by a regex, and the
# counted exemption list plus review is the backstop for that.
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
STRIP_RE = re.compile(r"[`*_\"'\u2018\u2019\u201c\u201d()\[\]]")


def _scannable(line):
    return STRIP_RE.sub("", MD_LINK_RE.sub(r"\2", line))
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mp3", ".woff", ".woff2",
              ".ico", ".pdf", ".zip", ".ttf", ".otf"}
tracked = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, cwd=ROOT,
).stdout.splitlines()
EXEMPT_MARKER = "v1-antipattern"
# Teaching "don't type this" means printing the thing you must not type, so a line may opt
# out. Two carriers, both invisible to a reader:
#   - the marker on the line itself (prose and comments);
#   - the marker in a fenced block's INFO STRING (```text v1-antipattern). CommonMark trims
#     the info string and GitHub renders only the first word as the language, so the marker
#     never appears on the page — which matters, because a wrong-example block has to stay
#     clean enough to read next to the right one.
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
path_handoffs = []
exempt = []
scanned = 0
for rel in tracked:
    if os.path.splitext(rel)[1].lower() in BINARY_EXT:
        continue
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
            scanned += 1
            fence = None          # the opening fence string, while inside a block
            fence_exempt = False
            prev = ""             # so a command wrapped onto the next line is still seen
            prev_exempt = False
            prev_hit = False
            for ln, line in enumerate(f, 1):
                m = FENCE_RE.match(line)
                if m:
                    if fence is None:
                        fence, fence_exempt = m.group(1)[0], EXEMPT_MARKER in m.group(2)
                        prev = ""
                        continue
                    if m.group(1)[0] == fence and not m.group(2).strip():
                        fence, fence_exempt = None, False
                        prev = ""
                        continue
                cur = _scannable(line)
                cur_hit = bool(PATH_HANDOFF_RE.search(cur))
                # Only consult the two-line window when neither line matched on its own,
                # so a wrapped command is caught once rather than reported twice.
                win_hit = (
                    not cur_hit and not prev_hit and bool(prev)
                    and bool(PATH_HANDOFF_RE.search(prev.rstrip("\n") + " " + cur))
                )
                if cur_hit or win_hit:
                    if EXEMPT_MARKER in line or fence_exempt or (win_hit and prev_exempt):
                        exempt.append(f"{rel}:{ln}")
                    else:
                        path_handoffs.append(f"{rel}:{ln}")
                prev, prev_exempt, prev_hit = cur, (EXEMPT_MARKER in line), cur_hit or win_hit
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
EXPECTED_EXEMPTIONS = 10
check(
    f"v1-antipattern exemptions stay pinned at {EXPECTED_EXEMPTIONS} "
    f"({len(exempt)} in use: {', '.join(exempt) or 'none'})",
    len(exempt) == EXPECTED_EXEMPTIONS,
    "adding one is a deliberate act: confirm the line DESCRIBES the old handoff rather "
    "than instructing it, then bump EXPECTED_EXEMPTIONS in the same commit",
)

# --- Same contract, but read through the RENDERED text of XML/SVG artifacts ---
# The line-oriented scan above has a blind spot: SVG splits a rendered string across
# <tspan> children, so `/goal` is followed by `<` in the source and never by the path a
# reader actually sees. assets/hero.svg rendered exactly that banned command through two
# releases and no line-oriented regex could see it. Flattening itertext() per <text>
# element — and again across all of them in document order, to catch a command split
# across sibling elements — closes the hole.
#
# A counter-example that is drawn struck-through is not an instruction, so a <text> (or
# any ancestor) may opt out with data-antipattern="v1". The count is pinned, exactly as
# above: adding one has to be a deliberate, reviewed act.
SVG_ANTIPATTERN_ATTR = "data-antipattern"


def _localname(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _exempt_text_elements(tree):
    """Elements whose rendered text is a marked counter-example (self or ancestor)."""
    parent = {}
    for p in tree.iter():
        for c in p:
            parent[c] = p
    exempt = set()
    for el in tree.iter():
        node = el
        while node is not None:
            if node.get(SVG_ANTIPATTERN_ATTR) == "v1":
                exempt.add(el)
                break
            node = parent.get(node)
    return exempt


rendered_hits = []
rendered_exempt = []
xml_scanned = 0
for rel in tracked:
    if os.path.splitext(rel)[1].lower() not in (".svg", ".xml"):
        continue
    try:
        tree = ET.parse(os.path.join(ROOT, rel))
    except ET.ParseError as e:
        check(f"{rel} is well-formed XML", False, str(e))
        continue
    xml_scanned += 1
    exempt_els = _exempt_text_elements(tree)
    # Walk the WHOLE document, not just <text>. Scanning `<text>` alone left the same hole
    # one element deeper: `<foreignObject>` renders visible words with no <text> ancestor,
    # so an SVG could display the banned command and pass. `<style>` is skipped because it
    # is CSS, not rendered copy.
    def flat_of(node):
        parts = []

        def walk(n):
            if n in exempt_els or _localname(n.tag) in ("style", "script"):
                return
            if n.text:
                parts.append(n.text)
            for c in n:
                walk(c)
                if c.tail:
                    parts.append(c.tail)

        walk(node)
        return " ".join(" ".join(parts).split())

    for el in tree.iter():
        if _localname(el.tag) != "text":
            continue
        flat = _scannable(" ".join("".join(el.itertext()).split()))
        if flat and el in exempt_els and PATH_HANDOFF_RE.search(flat):
            rendered_exempt.append(f"{rel}:{flat[:60]}")

    joined = _scannable(flat_of(tree.getroot()))
    hit = PATH_HANDOFF_RE.search(joined)
    if hit:
        rendered_hits.append(f"{rel} (rendered text): {hit.group(0)!r}")

check(
    f"no XML/SVG artifact RENDERS a file path after /goal ({xml_scanned} parsed, "
    f"tspan-split text flattened)",
    not rendered_hits,
    "found " + "; ".join(rendered_hits[:4]),
)
EXPECTED_SVG_ANTIPATTERNS = 1
check(
    f"struck-through counter-examples in SVG stay pinned at {EXPECTED_SVG_ANTIPATTERNS} "
    f"({len(rendered_exempt)} in use)",
    len(rendered_exempt) == EXPECTED_SVG_ANTIPATTERNS,
    "each must be drawn struck-through and marked "
    f'{SVG_ANTIPATTERN_ATTR}="v1"; bump this constant in the same commit',
)

# --- Vocabulary: the two artifacts are a brief (a file) and a condition (a string) ---
# PATH_HANDOFF_RE only catches *paths*. It cannot catch the phrasing that blurs the two
# artifacts into one imaginary input, which is the confusion underneath the path bug.
# Backticks and emphasis are stripped first so the markdown form is caught too.
BLUR_RE = re.compile(r"goal[-\s ]+file|/goal\s+MD\b|/goal\s+run\s+file", re.I)
blur_hits = []
for rel in tracked:
    if os.path.splitext(rel)[1].lower() in BINARY_EXT:
        continue
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
            for ln, line in enumerate(f, 1):
                norm = re.sub(r"[`*_]", "", line)
                if BLUR_RE.search(norm):
                    blur_hits.append(f"{rel}:{ln}")
    except (IsADirectoryError, FileNotFoundError, OSError):
        continue
check(
    "no tracked file blurs the file and the string into one phantom artifact "
    "(a brief is a file; a condition is a string)",
    not blur_hits,
    "found at " + ", ".join(blur_hits[:8]),
)

# --- Every shipped SVG must be safe on GitHub AND actually animate ---
# GitHub serves assets/*.svg byte-for-byte under `default-src 'none'; sandbox`, so an
# external reference or a <script> is dead weight at best. "Animated" is asserted because
# a static replacement for an animated asset is a silent regression nothing else catches.
EXTERNAL_REF_RE = re.compile(
    r"""<script|@import|xlink:href\s*=\s*["']https?:|href\s*=\s*["']https?:"""
    r"""|url\(\s*['"]?https?:|src\s*=\s*["']https?:|<image\b""",
    re.I,
)
SMIL_RE = re.compile(r"<(?:animate|animateTransform|animateMotion|set)\b", re.I)
GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded", "math", "emoji",
}
shipped_svgs = sorted(r for r in tracked if r.startswith("assets/") and r.endswith(".svg"))
check("assets/ ships at least three SVGs", len(shipped_svgs) >= 3, f"found {shipped_svgs}")
for rel in shipped_svgs:
    raw = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    try:
        ET.fromstring(raw)
        wellformed, why = True, ""
    except ET.ParseError as e:
        wellformed, why = False, str(e)
    check(f"{rel}: well-formed XML", wellformed, why)
    ext = EXTERNAL_REF_RE.search(raw)
    check(f"{rel}: no <script> and no external reference", not ext,
          f"matched {ext.group(0)!r}" if ext else "")
    check(f"{rel}: is animated (@keyframes or SMIL)",
          "@keyframes" in raw or bool(SMIL_RE.search(raw)),
          "a static SVG here is a silent regression")
    stacks = (re.findall(r'font-family\s*=\s*"([^"]*)"', raw)
              + re.findall(r"font-family\s*=\s*'([^']*)'", raw)
              + re.findall(r"font-family\s*:\s*([^;{}]+)", raw))
    bad_stacks = [
        v.strip() for v in stacks
        if v.split(",")[-1].strip().strip("\"'").lower() not in GENERIC_FAMILIES
    ]
    check(f"{rel}: every font stack ends in a generic family (unmatched falls back to serif)",
          not bad_stacks, f"{bad_stacks[:2]}")

# --- The shipped example must satisfy every clause the SKILL.md template mandates ---
example_path = os.path.join(ROOT, "examples", "sample-brief.md")
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
    check("examples/sample-brief.md is readable", False, str(e))

# --- Report ---
print("-" * 60)
passed = _total - len(failures)
print(f"{passed}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
