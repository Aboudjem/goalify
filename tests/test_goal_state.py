#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/goal_state.py, the parser every v3 helper reads briefs through.

Pins: section parsing, Definition-of-done items and the commands pulled out of them, checklist
ticks, the completion stamp, the sibling CONDITION file, BLOCKERS files, and the `--status`
table (golden output, byte-identical resume lines, read-only).

Standard library only. Run: python3 tests/test_goal_state.py
Exit 0 = all pass, 1 = at least one failed.
"""
import os
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


# --- The shipped sample brief parses into the template's shape ---
sample = goal_state.parse_brief(os.path.join(ROOT, "examples", "sample-brief.md"))
check("sample: no required section is missing", sample["missing_sections"] == [],
      f"{sample['missing_sections']}")
check("sample: title is read from '# GOAL:'", sample["title"].startswith("Migrate the widget-api"))
check("sample: the brief's own absolute path is read",
      sample["own_path"] == "/Users/example/widget-api/.goal/cb-to-async-2026-05-29.md",
      sample["own_path"])
check("sample: five phases, numbered 1..5",
      [p["num"] for p in sample["phases"]] == [1, 2, 3, 4, 5], f"{sample['phases']}")
check("sample: phase titles come from the bold lead",
      sample["phases"][0]["title"] == "Discover/verify (parallel reads)", sample["phases"][0]["title"])
check("sample: four Definition-of-done items", len(sample["dod"]) == 4, f"{len(sample['dod'])}")
check("sample: 'verified by' scopes the commands (cb( is not a command, the grep is)",
      sample["dod"][0]["commands"] == ['grep -rn "cb(" /Users/example/widget-api/src'],
      f"{sample['dod'][0]['commands']}")
check("sample: npm test is found inside a cd && chain",
      sample["dod"][2]["commands"] == ["cd /Users/example/widget-api && npm test"],
      f"{sample['dod'][2]['commands']}")
check("sample: a separate-agent item has kind 'agent', not 'none'",
      sample["dod"][3]["kind"] == "agent", sample["dod"][3]["kind"])
check("sample: progress checklist is 0/8", sample["ticks"] == [0, 8], f"{sample['ticks']}")
check("sample: three locked decisions", len(sample["decisions"]) == 3, f"{sample['decisions']}")
check("sample: not archived, no stamp",
      sample["archived"] is False and sample["completion_stamp"] is None)

# --- Command detection on its own ---
cases = {
    "make test": True, "true": True, "false": True, "pytest": True, "./run.sh": True,
    "MERGED": False, "200": False, "src/": False, "(…, cb) =>": False, "cb(": False,
    "['3.0.0']": False, ".goal/contract.md": False, "CI=1 npm test": True,
    "python3 tests/run_all.py": True, "<landing URL>": False,
}
wrong = [k for k, v in cases.items() if goal_state.looks_like_command(k) != v]
check("looks_like_command separates commands from values and paths", not wrong, f"{wrong}")
check("placeholders in a command are flagged",
      goal_state.PLACEHOLDER_RE.search("curl -s <landing URL>") is not None)

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

    empty = os.path.join(tmp, "empty")
    os.makedirs(empty)
    e = subprocess.run([sys.executable, os.path.join(SCRIPTS, "goal_state.py"), "--status", empty],
                       capture_output=True, text=True)
    check("status: an empty folder says so and exits 0",
          e.returncode == 0 and "No briefs found" in e.stdout, e.stdout)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# --- JSON dump mode ---
j = subprocess.run([sys.executable, os.path.join(SCRIPTS, "goal_state.py"),
                    os.path.join(ROOT, "examples", "sample-brief.md")], capture_output=True, text=True)
check("json mode: exits 0 and prints the slug", j.returncode == 0 and '"slug"' in j.stdout)
m = subprocess.run([sys.executable, os.path.join(SCRIPTS, "goal_state.py"), "/nonexistent.md"],
                   capture_output=True, text=True)
check("json mode: a missing brief exits 2", m.returncode == 2, f"exit={m.returncode}")

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
