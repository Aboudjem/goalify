#!/usr/bin/env python3
"""
run_all.py: every goalify test suite plus the skill eval, one line each.

Prints `PASS <name> n/n` (or `FAIL <name> n/m`) per suite, then a total, and exits non-zero
if any suite failed. A failing suite's last lines are printed under it so CI logs explain
themselves. Standard library only.

Run: python3 tests/run_all.py
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUITES = [
    ("check_skill", ["evals/check_skill.py", "skills/goalify/SKILL.md"]),
    ("test_manifests", ["tests/test_manifests.py"]),
    ("test_condition_lint", ["tests/test_condition_lint.py"]),
    ("goal_state", ["tests/test_goal_state.py"]),
    ("render_preview", ["tests/test_render_preview.py"]),
    ("verify", ["tests/test_verify.py"]),
    ("detect_checks", ["tests/test_detect_checks.py"]),
    ("status", ["tests/test_status.py"]),
    ("doctor", ["tests/test_doctor.py"]),
]
COUNT_RE = re.compile(r"(\d+)/(\d+) checks passed")


def main():
    failed = []
    for name, cmd in SUITES:
        path = os.path.join(ROOT, cmd[0])
        if not os.path.exists(path):
            print(f"FAIL {name} missing ({cmd[0]} not found)")
            failed.append(name)
            continue
        p = subprocess.run([sys.executable] + [os.path.join(ROOT, c) if c.endswith(".py") else c
                                               for c in cmd],
                           cwd=ROOT, capture_output=True, text=True)
        counts = COUNT_RE.findall(p.stdout)
        got, total = (counts[-1] if counts else ("?", "?"))
        ok = p.returncode == 0 and counts and got == total
        print(f"{'PASS' if ok else 'FAIL'} {name} {got}/{total}")
        if not ok:
            failed.append(name)
            tail = (p.stdout + p.stderr).strip().splitlines()[-12:]
            for line in tail:
                print(f"    {line}")
    print("-" * 60)
    print(f"{len(SUITES) - len(failed)}/{len(SUITES)} suites passed")
    print(("failed: " + ", ".join(failed)) if failed else "All suites passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
