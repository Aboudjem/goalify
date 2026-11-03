#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/verify.py (`/goalify verify` and the proof receipt).

Pins: true/false checks give 1/2 and exit 1; a destructive command is refused without an
explicit --allow; no runnable command gives UNVERIFIABLE; an archived brief with a failing
check is NOT VERIFIED (the receipt can contradict the stamp); nothing runs without --yes when
stdin is not a terminal; nothing is written outside .goal/; and the receipt is escaped and
makes no external request.

Standard library only. Run: python3 tests/test_verify.py
Exit 0 = all pass, 1 = at least one failed.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(ROOT, "skills", "goalify", "scripts", "verify.py")
EXTERNAL_RE = re.compile(r'(?:src|href)\s*=\s*["\']?(https?:)?//[^"\'\s>]+', re.IGNORECASE)

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def brief(title, dod_lines, stamp=None):
    dod = "\n".join(f"- [x] {line}" for line in dod_lines)
    text = f"""# GOAL: {title}

> Self-contained implementation brief. Authored 2026-11-03 by goalify 3.0.0.
> This file's own path: /tmp/example/.goal/x-20261103.md

## GOAL (the autonomous directive)

{title}.

## Context

- Fixture.

## Decisions

- None.

## Phases

1. **Do it.** Then prove it.

## Process directives

- **Closeout turn.** Rerun every check.

## Definition of done

{dod}

## Progress checklist

- [x] Did it
- [ ] All criteria hold

## Final output

- Done / Proof / Next

## Archive gate (LOW FREEDOM)

Pre-condition: every box ticked.
"""
    if stamp:
        text += f"\n---\nCOMPLETION STAMP: {stamp}\n"
    return text


def setup(tmp, name, text, archived=False):
    proj = os.path.join(tmp, name)
    gdir = os.path.join(proj, ".goal")
    target = os.path.join(gdir, "done") if archived else gdir
    os.makedirs(target)
    p = os.path.join(target, "x-20261103.md")
    open(p, "w", encoding="utf-8").write(text)
    return proj, p


def run(args, cwd=None, stdin=""):
    return subprocess.run([sys.executable, VERIFY] + args, capture_output=True, text=True,
                          cwd=cwd, input=stdin)


def snapshot(proj):
    out = {}
    for d, _, ns in os.walk(proj):
        for n in ns:
            p = os.path.join(d, n)
            out[os.path.relpath(p, proj)] = os.stat(p).st_mtime_ns
    return out


tmp = tempfile.mkdtemp(prefix="goalify-verify-")
try:
    # --- true + false: 1/2, NOT VERIFIED, exit 1, receipt written ---
    proj, bp = setup(tmp, "tf", brief("Two checks", [
        "The first passes, verified by `true`.",
        "The second fails, verified by `false`.",
    ]))
    before = snapshot(proj)
    p = run([bp, "--yes"])
    check("true/false: exit 1", p.returncode == 1, f"exit={p.returncode}\n{p.stdout}")
    check("true/false: reports 1/2", "1/2 checks passed" in p.stdout, p.stdout)
    check("true/false: verdict NOT VERIFIED", "VERDICT: NOT VERIFIED" in p.stdout)
    receipts = glob.glob(os.path.join(proj, ".goal", "RECEIPT-x-*.html"))
    check("true/false: one receipt in .goal/", len(receipts) == 1, f"{receipts}")
    page = open(receipts[0], encoding="utf-8").read() if receipts else ""
    check("receipt: shows the NOT VERIFIED verdict and one PASS, one FAIL",
          "NOT VERIFIED" in page and ">PASS<" in page and "FAIL · exit 1" in page)
    check("receipt: labels the ticked checklist as claimed", "Checklist (claimed)" in page)
    after = snapshot(proj)
    new = sorted(set(after) - set(before))
    check("only .goal/ gained files (receipt and logs)",
          all(n.startswith(".goal" + os.sep) for n in new) and new, f"{new}")
    check("the brief itself was not modified",
          before[os.path.relpath(bp, proj)] == after[os.path.relpath(bp, proj)])
    check("logs written to .goal/verify-x/1.log and 2.log",
          os.path.exists(os.path.join(proj, ".goal", "verify-x", "1.log"))
          and os.path.exists(os.path.join(proj, ".goal", "verify-x", "2.log")))
    ext = [x.group(0) for x in EXTERNAL_RE.finditer(page)
           if "github.com/Aboudjem/goalify" not in x.group(0)]
    check("receipt: no external src/href", not ext, f"{ext}")

    # --- all pass: VERIFIED, exit 0 ---
    proj, bp = setup(tmp, "ok", brief("All good", ["It passes, verified by `true`.",
                                                   "So does this, verified by `echo hello`."]))
    p = run([bp, "--yes"])
    check("all pass: VERIFIED, exit 0", p.returncode == 0 and "VERDICT: VERIFIED" in p.stdout,
          p.stdout)

    # --- destructive: refused without --allow, never runs ---
    victim = os.path.join(tmp, "victim")
    os.makedirs(victim)
    proj, bp = setup(tmp, "rm", brief("Dangerous", [f"Cleaned, verified by `rm -rf {victim}`.",
                                                    "Also, verified by `true`."]))
    p = run([bp, "--yes"])
    check("destructive: refused, the target still exists", os.path.isdir(victim), p.stdout)
    check("destructive: the plan says REFUSED and names the pattern",
          "REFUSED" in p.stdout and "rm -r" in p.stdout, p.stdout)
    check("destructive: a refused check means NOT VERIFIED", p.returncode == 1, f"exit={p.returncode}")
    p = run([bp, "--yes", "--allow", f"rm -rf {victim}"])
    check("destructive: --allow with the exact command lets it run",
          not os.path.exists(victim) and p.returncode == 0, p.stdout)

    # --- no runnable command: UNVERIFIABLE ---
    proj, bp = setup(tmp, "none", brief("Nothing to run", [
        "It looks right.", "A SEPARATE agent re-derived every claim."]))
    p = run([bp, "--yes"])
    check("no commands: UNVERIFIABLE, exit 3", p.returncode == 3 and "UNVERIFIABLE" in p.stdout,
          f"exit={p.returncode}")
    proj, bp = setup(tmp, "ph", brief("Placeholder", ["Live, verified by `curl -s <landing URL>`."]))
    p = run([bp, "--yes"])
    check("placeholder-only: skipped, UNVERIFIABLE", p.returncode == 3 and "skip" in p.stdout,
          p.stdout)

    # --- archived brief with a failing check: the receipt contradicts the stamp ---
    proj, bp = setup(tmp, "arch", brief("Claimed done", ["Done, verified by `false`."],
                                        stamp="2026-11-01, every box ticked"), archived=True)
    p = run([bp, "--yes"])
    check("archived + failing: NOT VERIFIED, exit 1", p.returncode == 1, p.stdout)
    rec = glob.glob(os.path.join(proj, ".goal", "RECEIPT-x-*.html"))
    rpage = open(rec[0], encoding="utf-8").read() if rec else ""
    check("archived + failing: receipt says the stamp and the checks disagree",
          "Stamp vs checks" in rpage and "Completion stamp (claimed)" in rpage)
    check("archived + failing: the brief stays in done/ (verify never un-archives)",
          os.path.exists(bp))

    # --- asks first: nothing runs without --yes when stdin is not a terminal ---
    marker = os.path.join(tmp, "ran.txt")
    proj, bp = setup(tmp, "ask", brief("Asks", [f"Touched, verified by `touch {marker}`."]))
    p = run([bp])
    check("no --yes, no terminal: exits 2 and runs nothing",
          p.returncode == 2 and not os.path.exists(marker), p.stdout)
    p = run([bp, "--list"])
    check("--list: prints the command, runs nothing, writes no receipt",
          p.returncode == 0 and f"touch {marker}" in p.stdout and not os.path.exists(marker)
          and not glob.glob(os.path.join(proj, ".goal", "RECEIPT-*")))

    # --- escaping on the receipt ---
    proj, bp = setup(tmp, "xss", brief("<script>alert(1)</script> evil",
                                       ["Shown, verified by `echo '<img src=x onerror=alert(2)>'`."]))
    p = run([bp, "--yes"])
    rec = glob.glob(os.path.join(proj, ".goal", "RECEIPT-x-*.html"))
    xpage = open(rec[0], encoding="utf-8").read() if rec else ""
    check("receipt escaping: title and command output are escaped",
          "<script>alert" not in xpage and "<img src=x" not in xpage
          and "&lt;img src=x onerror=alert(2)&gt;" in xpage)

    # --- "printing nothing" checks: grep for leftovers passes when it finds none ---
    proj, bp = setup(tmp, "empty-ok", brief("No leftovers", [
        'No v1 calls remain, verified by `grep -rn "api/v1" src` printing nothing.']))
    os.makedirs(os.path.join(proj, "src"))
    open(os.path.join(proj, "src", "a.js"), "w").write("call('api/v2')\n")
    p = run([bp, "--yes"])
    check("prints-nothing: grep with no match (exit 1, empty) is a PASS and VERIFIED",
          p.returncode == 0 and "VERDICT: VERIFIED" in p.stdout and "expects no output" in p.stdout,
          p.stdout)
    rec = glob.glob(os.path.join(proj, ".goal", "RECEIPT-x-*.html"))
    check("prints-nothing: the receipt says it printed nothing",
          bool(rec) and "PASS · printed nothing" in open(rec[0], encoding="utf-8").read())
    open(os.path.join(proj, "src", "b.js"), "w").write("call('api/v1')\n")
    p = run([bp, "--yes"])
    check("prints-nothing: a leftover match (output) is a FAIL, NOT VERIFIED",
          p.returncode == 1 and "NOT VERIFIED" in p.stdout, p.stdout)
    proj, bp = setup(tmp, "empty-err", brief("Broken grep", [
        'Clean, verified by `grep -rn "api/v1" missing-dir` printing nothing.']))
    p = run([bp, "--yes"])
    check("prints-nothing: a grep error (exit 2) is a FAIL, not a pass",
          p.returncode == 1 and "NOT VERIFIED" in p.stdout, p.stdout)
    proj, bp = setup(tmp, "plain-exit1", brief("Plain", ["It runs, verified by `false`."]))
    p = run([bp, "--yes"])
    check("a plain check with exit 1 and no 'printing nothing' wording still FAILs",
          p.returncode == 1, p.stdout)

    # --- more destructive shapes are refused ---
    proj, bp = setup(tmp, "find", brief("Find", ["Cleaned, verified by `find . -name x -delete`."]))
    p = run([bp, "--yes"])
    check("destructive: find -delete is refused (nothing left to run: UNVERIFIABLE)",
          "REFUSED" in p.stdout and p.returncode == 3,
          p.stdout)

    # --- default brief: the newest in ./.goal ---
    proj, bp = setup(tmp, "dflt", brief("Default", ["Ok, verified by `true`."]))
    p = run(["--yes"], cwd=proj)
    check("no brief argument: uses the newest brief in ./.goal", p.returncode == 0 and bp in p.stdout,
          p.stdout)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
