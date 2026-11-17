#!/usr/bin/env python3
"""
End-to-end test on the shipped demo (examples/demo): a real small project, its brief and its
condition go through the same scripts a user runs, and the receipt has to tell the truth.

Pins: the condition passes condition_lint; the brief and the condition pass the brief lint and
a preview page is written; verify says VERIFIED (exit 0) when the code is right and NOT VERIFIED
(exit 1) when the same brief still has every box ticked but one test fails; the report opens
with the verdict; and the demo writes nothing inside this repo.

Standard library only. Run: python3 tests/test_demo.py
Exit 0 = all pass, 1 = at least one failed.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(ROOT, "examples", "demo")
RUN = os.path.join(DEMO, "run.py")
LINT = os.path.join(ROOT, "skills", "goalify", "scripts", "condition_lint.py")

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def tracked_state():
    p = subprocess.run(["git", "status", "--porcelain", "--", "examples"], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def demo(target, *flags):
    return subprocess.run([sys.executable, RUN, "--dir", target] + list(flags),
                          capture_output=True, text=True)


tmp = tempfile.mkdtemp(prefix="goalify-demo-test-")
try:
    before = tracked_state()
    target = os.path.join(tmp, "proj")

    # --- the job was done: VERIFIED ---
    p = demo(target)
    lines = p.stdout.splitlines()
    check("demo: exit 0 when the code is right", p.returncode == 0, p.stdout + p.stderr)
    check("demo: the report opens with VERDICT: VERIFIED and the count",
          lines[:1] == ["VERDICT: VERIFIED (2/2 checks passed)"], p.stdout)
    check("demo: both commands really ran and passed",
          "  1. PASS (exit 0) python3 -m unittest -q test_slugify" in lines
          and '  2. PASS (exit 1, expects no output) grep -n "TODO" slugify.py' in lines, p.stdout)
    goal = os.path.join(os.path.realpath(target), ".goal")
    check("demo: the brief lint passed and wrote the preview page",
          os.path.getsize(os.path.join(goal, "preview.html")) > 2000
          if os.path.exists(os.path.join(goal, "preview.html")) else False)
    receipts = glob.glob(os.path.join(goal, "RECEIPT-slugify-*.html"))
    page = open(receipts[0], encoding="utf-8").read() if receipts else ""
    check("demo: one receipt, and it says VERIFIED", len(receipts) == 1 and ">VERIFIED<" in page)
    log = os.path.join(goal, "verify-slugify", "1.log")
    logged = open(log, encoding="utf-8").read() if os.path.exists(log) else ""
    check("demo: the log holds the real test output (3 tests ran)",
          "Ran 3 tests" in logged and "OK" in logged, logged)
    cond = open(os.path.join(goal, "CONDITION-slugify.txt"), encoding="utf-8").read().strip()
    q = subprocess.run([sys.executable, LINT, cond], capture_output=True, text=True)
    check("demo: the condition passes condition_lint", q.returncode == 0, q.stdout)
    check("demo: the condition names the brief's real path, not the placeholder",
          os.path.join(goal, "slugify-20261117.md") in cond and "__DEMO_DIR__" not in cond)
    brief_text = open(os.path.join(goal, "slugify-20261117.md"), encoding="utf-8").read()
    check("demo: no placeholder is left in the built brief", "__DEMO_DIR__" not in brief_text)

    # --- the run said done, one test fails: NOT VERIFIED ---
    p = demo(target, "--broken")
    lines = p.stdout.splitlines()
    check("broken demo: exit 1", p.returncode == 1, p.stdout + p.stderr)
    check("broken demo: the report opens with VERDICT: NOT VERIFIED",
          lines[:1] == ["VERDICT: NOT VERIFIED (1/2 checks passed)"], p.stdout)
    check("broken demo: every box in the brief is still ticked (the claim) while the check fails",
          "- [ ]" not in open(os.path.join(goal, "slugify-20261117.md"), encoding="utf-8").read()
          and "  1. FAIL (exit 1) python3 -m unittest -q test_slugify" in lines, p.stdout)
    check("broken demo: the first next step is the failing log",
          len(lines) > 2 and lines[2].startswith("  1. Read the log of the first failing check: ")
          and lines[2].endswith(os.path.join("verify-slugify", "1.log")), p.stdout)
    logged = open(log, encoding="utf-8").read() if os.path.exists(log) else ""
    check("broken demo: the log shows the failing assertion",
          "FAILED" in logged and "release-3-1-notes" in logged, logged[-400:])

    # --- usage ---
    p = demo(target, "--nope")
    check("demo: an unknown option exits 2 and says what to do", p.returncode == 2
          and "--help" in p.stdout, p.stdout)
    check("demo: nothing was written inside the repo's examples/", tracked_state() == before)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
