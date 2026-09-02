#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/condition_lint.py.

The linter is the mechanical half of the condition-lint checklist in SKILL.md, so this
file pins two things: that each rule fires on its own specimen, and that the linter does
not claim more than it can see. Several anti-patterns in examples/conditions.md pass every
rule and are still bad conditions; that is asserted here rather than hidden, because a
linter people over-trust is worse than one they read the limits of.

No third-party deps; standard library only.
Run: python3 tests/test_condition_lint.py
Exit 0 = all pass, 1 = at least one failed.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINT = os.path.join(ROOT, "skills", "goalify", "scripts", "condition_lint.py")

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def run(condition, stdin=False):
    """Return (exit code, set of failed rule ids)."""
    if stdin:
        p = subprocess.run([sys.executable, LINT], input=condition,
                           capture_output=True, text=True)
    else:
        p = subprocess.run([sys.executable, LINT, condition],
                           capture_output=True, text=True)
    failed = set(re.findall(r"^FAIL: ([a-z-]+)", p.stdout, re.MULTILINE))
    return p.returncode, failed, p.stdout


check("the linter exists at skills/goalify/scripts/condition_lint.py", os.path.exists(LINT))

# --- Conditions that must pass every rule ---
CANONICAL = ("Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last "
             "turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.")
GOOD = [
    ("the canonical shape from SKILL.md", CANONICAL),
    ("an absolute brief path named mid-sentence (the shape SKILL.md mandates)",
     "Do everything in /Users/example/widget-api/.goal/cb-to-async.md and prove it, done when "
     "the last turn quotes npm test passing and says WIDGET-OK. Stop after 40 turns."),
    ("a trailing 'or stop after N turns' bound",
     "Work through ~/api/.goal/x.md, done when the last turn quotes make test passing and says "
     "MAKE-OK, or stop after 20 turns."),
]
for name, cond in GOOD:
    rc, failed, _ = run(cond)
    check(f"good: {name}", rc == 0 and not failed, f"exit={rc} failed={sorted(failed)}")

# --- One specimen per rule. Each names the rules that MUST fire, and no others. ---
LONG = "Do everything in ~/a/.goal/b.md, done when the last turn quotes npm test passing " \
       + ("and the docs are rebuilt " * 200) + "and says LONG-OK. Stop after 10 turns."
BAD = [
    ("a bare path as the whole condition", "~/acme/.goal/api-migration.md",
     {"done-when", "path-as-condition", "stop-rule"}),
    ("a quoted bare path", '"/Users/me/.goal/plan.md"',
     {"done-when", "path-as-condition", "stop-rule"}),
    # Leading with the path is the v1 antipattern's silhouette even when the rest is toothed.
    # Pinned as a deliberate choice, not an accident of the regex.
    ("a toothed condition that still leads with the path",
     "/Users/me/.goal/plan.md, done when the last turn quotes npm test passing and says "
     "LEAD-OK. Stop after 30 turns.",
     {"path-as-condition"}),
    ("no finish line",
     "Do everything in ~/a/.goal/b.md and prove it. Stop after 30 turns.",
     {"done-when"}),
    ("no turn bound",
     "Do everything in ~/a/.goal/b.md, done when the last turn quotes npm test passing and "
     "says B-OK.",
     {"stop-rule"}),
    ("a stop-after clause with no number",
     "Do everything in ~/a/.goal/b.md, done when the last turn quotes npm test passing and "
     "says B-OK. Stop after the tests pass.",
     {"stop-after-number"}),
    ("a bare $ the hook prompt could rewrite",
     "Do everything in ~/a/.goal/b.md, done when the last turn quotes echo $ARGUMENTS and "
     "says B-OK. Stop after 30 turns.",
     {"bare-dollar"}),
    ("longer than the 4,000-character limit", LONG, {"length"}),
]
for name, cond, expected in BAD:
    rc, failed, _ = run(cond)
    check(f"bad: {name}", rc == 1 and failed == expected,
          f"exit={rc} failed={sorted(failed)} expected={sorted(expected)}")

# --- Input handling ---
rc, failed, _ = run(CANONICAL, stdin=True)
check("a condition can be piped in on stdin", rc == 0 and not failed, f"exit={rc}")
rc, _, out = run("   ", stdin=True)
check("an empty condition exits 2 rather than passing", rc == 2, f"exit={rc}")

# --- The advisory length note never changes the exit code ---
rc, failed, out = run(
    "Do everything in /Users/example/widget-api/.goal/cb-to-async.md and prove it, done when "
    "the last turn quotes npm test passing and says WIDGET-OK. Stop after 40 turns.")
check("the over-a-glance NOTE is advisory and does not fail the lint",
      rc == 0 and "NOTE:" in out, f"exit={rc}")

# --- Every worked condition in the gallery must lint clean ---
GALLERY = os.path.join(ROOT, "examples", "conditions.md")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")


def fenced_blocks(text):
    out, fence, info, buf = [], None, "", []
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if m:
            if fence is None:
                fence, info, buf = m.group(1)[0], m.group(2).strip(), []
                continue
            if m.group(1)[0] == fence and not m.group(2).strip():
                out.append((info, "\n".join(buf)))
                fence, info, buf = None, "", []
                continue
        if fence is not None:
            buf.append(line)
    return out


if os.path.exists(GALLERY):
    blocks = fenced_blocks(open(GALLERY, encoding="utf-8").read())
    worked = [b for info, b in blocks if info == "text"]
    labelled = [b for info, b in blocks if info != "text" and info.split(" ", 1)[0] == "text"]
    dirty = []
    for cond in worked:
        rc, failed, _ = run(cond)
        if rc != 0:
            dirty.append((cond[:40], sorted(failed)))
    check("gallery: every worked condition lints clean", not dirty, f"{dirty}")

    caught = [c[:40] for c in labelled if run(c)[0] != 0]
    # Five of the eight anti-patterns pass every rule and are still bad conditions: an
    # unnamed command, a self-satisfying claim, a lawyerly restatement of the brief, a
    # ticked checkbox the evaluator cannot see, and a sentinel that is just the word "done".
    # The linter cannot see any of those, and this count says so out loud. If it moves, a
    # rule changed and the honest-limits paragraph in the linter's docstring needs re-reading.
    check("gallery: the linter catches exactly the three mechanical anti-patterns",
          len(caught) == 3, f"caught {len(caught)}: {caught}")
    check("gallery: the bare-path anti-pattern is one of them",
          any(c.startswith("~/acme/.goal/") for c in caught), f"{caught}")

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
