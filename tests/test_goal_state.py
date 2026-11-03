#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/goal_state.py, the parser every v3 helper reads briefs through.

Pins: section parsing, Definition-of-done items and the commands pulled out of them, checklist
ticks, the completion stamp, and JSON mode. The `--status` table has its own suite,
tests/test_status.py.

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
