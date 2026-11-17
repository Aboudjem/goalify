#!/usr/bin/env python3
"""
run.py: the goalify demo. A real, small project, a brief, a condition, and a real receipt.

It copies this folder to a temp folder, fills in the brief's own path, checks the brief and the
condition with the same lint `/goalify` uses, then runs `verify.py` on it. Every line it prints
comes from the shipped scripts. Nothing is written inside the goalify repo.

Usage:
    python3 examples/demo/run.py            # the job was done: VERIFIED, exit 0
    python3 examples/demo/run.py --broken   # the run said "done" but one test fails: NOT VERIFIED, exit 1
    options: --dir <folder>   where to build the demo (default: <temp>/goalify-demo,
                              or <temp>/goalify-demo-broken with --broken, so each mode keeps
                              its own receipt)

Standard library only. No network call.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "skills", "goalify", "scripts")
PLACEHOLDER = "__DEMO_DIR__"
SLUG = "slugify"
BRIEF = f"{SLUG}-20261117.md"


def build(target, broken):
    """Lay the demo project out the way a real goalify project looks. Returns the brief path."""
    if os.path.isdir(target):
        shutil.rmtree(target)
    goal = os.path.join(target, ".goal")
    os.makedirs(goal)
    for name in ("slugify.py", "test_slugify.py"):
        shutil.copy(os.path.join(HERE, name), os.path.join(target, name))
    for src, dst in (("brief.md", BRIEF), ("condition.txt", f"CONDITION-{SLUG}.txt")):
        with open(os.path.join(HERE, src), encoding="utf-8") as f:
            text = f.read().replace(PLACEHOLDER, target)
        with open(os.path.join(goal, dst), "w", encoding="utf-8") as f:
            f.write(text)
    if broken:
        # The classic miss: the run reports "done", but the code drops digits again.
        path = os.path.join(target, "slugify.py")
        with open(path, encoding="utf-8") as f:
            code = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.replace('r"[a-z0-9]+"', 'r"[a-z]+"'))
    return os.path.join(goal, BRIEF)


def main(argv):
    args = argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__.strip())
        return 0
    broken = "--broken" in args
    # Each mode gets its own folder: the --broken run must not wipe the VERIFIED receipt.
    target = os.path.join(tempfile.gettempdir(), "goalify-demo-broken" if broken else "goalify-demo")
    if "--dir" in args:
        i = args.index("--dir")
        if i + 1 >= len(args):
            print("--dir needs a folder. Example: run.py --dir /tmp/goalify-demo")
            return 2
        target = args[i + 1]
        del args[i:i + 2]
    unknown = [a for a in args if a != "--broken"]
    if unknown:
        print(f"unknown option(s): {', '.join(unknown)}. Run with --help to see the two modes.")
        return 2
    target = os.path.realpath(target)
    brief = build(target, broken)
    cond = os.path.join(os.path.dirname(brief), f"CONDITION-{SLUG}.txt")

    # 1. The brief lint and the run preview: the same gate /goalify runs before the handoff.
    page = os.path.join(os.path.dirname(brief), "preview.html")
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "render_preview.py"), brief, cond,
                        "--out", page], capture_output=True, text=True)
    if p.returncode != 0:
        print("The demo brief did not pass the brief lint:")
        print((p.stdout + p.stderr).strip())
        return 2

    # 2. The receipt. --yes because this demo's two commands are fixed and harmless.
    sys.stdout.flush()
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "verify.py"), brief, "--yes"]).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv))
