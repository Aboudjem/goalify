#!/usr/bin/env python3
"""
Tests for `/goalify status` (skills/goalify/scripts/goal_state.py --status).

Pins: OPEN / BLOCKED / DONE / ORPHAN-CONDITION states on a fixture .goal/, a golden table,
resume lines byte-identical to their CONDITION files and lint-clean, read-only (running it
twice changes no file), and the --html index page.

Standard library only. Run: python3 tests/test_status.py
Exit 0 = all pass, 1 = at least one failed.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "goalify", "scripts")
sys.path.insert(0, SCRIPTS)
import goal_state  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures")
LINT = os.path.join(SCRIPTS, "condition_lint.py")
NOW = 2_000_000_000

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


# --- Status: golden table on a fixture .goal/ ---
tmp = tempfile.mkdtemp(prefix="goalify-status-")
try:
    gdir = os.path.join(tmp, ".goal")
    shutil.copytree(os.path.join(FIX, "status", ".goal"), gdir)
    for dirpath, _, names in os.walk(gdir):
        for n in names:
            os.utime(os.path.join(dirpath, n), (NOW - 3 * 86400, NOW - 3 * 86400))
    os.utime(os.path.join(gdir, "alpha-20261101.md"), (NOW - 5 * 3600, NOW - 5 * 3600))

    rows = goal_state.collect_status(gdir, NOW)
    states = {r["slug"]: r["state"] for r in rows}
    check("status: alpha is OPEN, beta BLOCKED, gamma DONE, ghost ORPHAN-CONDITION",
          states == {"alpha": "OPEN", "beta": "BLOCKED", "gamma": "DONE",
                     "ghost": "ORPHAN-CONDITION"}, f"{states}")
    alpha = next(r for r in rows if r["slug"] == "alpha")
    check("status: alpha ticks are 3/7", alpha["ticks"] == [3, 7], f"{alpha['ticks']}")
    gamma = next(r for r in rows if r["slug"] == "gamma")
    check("status: the archived brief's completion stamp is read",
          (gamma["stamp"] or "").startswith("2026-10-02"), f"{gamma['stamp']}")

    before = {os.path.join(d, n): os.stat(os.path.join(d, n)).st_mtime_ns
              for d, _, ns in os.walk(gdir) for n in ns}
    cmd = [sys.executable, os.path.join(SCRIPTS, "goal_state.py"), "--status", gdir,
           "--now", str(NOW)]
    out1 = subprocess.run(cmd, capture_output=True, text=True)
    out2 = subprocess.run(cmd, capture_output=True, text=True)
    after = {os.path.join(d, n): os.stat(os.path.join(d, n)).st_mtime_ns
             for d, _, ns in os.walk(gdir) for n in ns}
    check("status: exits 0", out1.returncode == 0, out1.stderr[-200:])
    check("status: running it twice changes no file (same set, same mtimes)", before == after)
    check("status: output is stable across runs", out1.stdout == out2.stdout)
    golden = open(os.path.join(FIX, "status", "expected.txt"), encoding="utf-8").read()
    check("status: output matches tests/fixtures/status/expected.txt", out1.stdout == golden,
          "\n" + out1.stdout)

    for slug in ("alpha", "beta"):
        cond = open(os.path.join(gdir, f"CONDITION-{slug}.txt"), encoding="utf-8").read().strip()
        line = f"  /goal {cond}"
        check(f"status: {slug}'s resume line equals its CONDITION file byte for byte",
              line in out1.stdout.split("\n"))
        lint = subprocess.run([sys.executable, LINT, cond], capture_output=True, text=True)
        check(f"status: {slug}'s reprinted condition passes condition_lint.py",
              lint.returncode == 0, lint.stdout[-200:])
    check("status: never prints a bare path as a resume step",
          "resume ~/" not in out1.stdout and "/goal /" not in out1.stdout)
    check("status: DONE and ORPHAN rows get no resume line",
          "gamma (done)" not in out1.stdout and "ghost (" not in out1.stdout)

    # --- --html writes .goal/index.html and nothing else ---
    h = subprocess.run(cmd + ["--html"], capture_output=True, text=True)
    idx = os.path.join(gdir, "index.html")
    page = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
    check("status --html: writes .goal/index.html and prints its file:// link",
          h.returncode == 0 and os.path.exists(idx) and "file://" + idx in h.stdout, h.stdout[-300:])
    check("status --html: the page carries alpha's full /goal line in a copy target",
          "/goal Do everything in /Users/example/app/.goal/alpha-20261101.md" in page
          and 'data-copy="c-alpha"' in page)
    check("status --html: no external src/href except the GitHub repo",
          not [x for x in re.findall(r'(?:src|href)="(https?://[^"]+)"', page)
               if "github.com/Aboudjem/goalify" not in x])
    new_files = {os.path.relpath(os.path.join(d, n), gdir) for d, _, ns in os.walk(gdir) for n in ns} \
        - {os.path.relpath(k, gdir) for k in before}
    check("status --html: index.html is the only new file", new_files == {"index.html"},
          f"{new_files}")

    empty = os.path.join(tmp, "empty")
    os.makedirs(empty)
    e = subprocess.run([sys.executable, os.path.join(SCRIPTS, "goal_state.py"), "--status", empty],
                       capture_output=True, text=True)
    check("status: an empty folder says so and exits 0",
          e.returncode == 0 and "No briefs found" in e.stdout, e.stdout)

finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
