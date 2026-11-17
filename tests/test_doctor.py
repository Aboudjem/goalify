#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/doctor.py (duplicate-install check) and the version stamp.

Pins: a 2.5.0 hand copy plus a 2.6.1 plugin gives exactly one warning naming both; a single
copy gives none; a leftover cache folder that is not installed is ignored; $CLAUDE_CONFIG_DIR is scanned too; and the version
line in the SKILL.md body equals plugin.json.

Standard library only. Run: python3 tests/test_doctor.py
Exit 0 = all pass, 1 = at least one failed.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCTOR = os.path.join(ROOT, "skills", "goalify", "scripts", "doctor.py")

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def skill(dirpath, version):
    os.makedirs(dirpath, exist_ok=True)
    open(os.path.join(dirpath, "SKILL.md"), "w").write(
        f"---\nname: goalify\ndescription: x\nmetadata:\n  version: {version}\n---\n\n# goalify\n")


def plugin(home, version, installed=True, config=None):
    config = config or os.path.join(home, ".claude")
    d = os.path.join(config, "plugins", "cache", "10x", "goalify", version)
    skill(os.path.join(d, "skills", "goalify"), version)
    if installed:
        p = os.path.join(config, "plugins", "installed_plugins.json")
        data = {"version": 2, "plugins": {"goalify@10x": [{"scope": "user", "installPath": d,
                                                            "version": version}]}}
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(data, open(p, "w"))


def doctor(home, config_dir=None):
    proj = os.path.join(home, "proj")
    os.makedirs(proj, exist_ok=True)
    # Never let the tester's own $CLAUDE_CONFIG_DIR leak into a test.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    if config_dir:
        env["CLAUDE_CONFIG_DIR"] = config_dir
    return subprocess.run([sys.executable, DOCTOR, "--home", home, "--project", proj],
                          capture_output=True, text=True, env=env)


tmp = tempfile.mkdtemp(prefix="goalify-doctor-")
try:
    h1 = os.path.join(tmp, "h1")
    skill(os.path.join(h1, ".claude", "skills", "goalify"), "2.5.0")
    plugin(h1, "2.6.1")
    p = doctor(h1)
    warns = [l for l in p.stdout.splitlines() if l.startswith("WARN:")]
    check("hand copy 2.5.0 + plugin 2.6.1: exit 1", p.returncode == 1, p.stdout)
    check("hand copy 2.5.0 + plugin 2.6.1: names both versions",
          "2.5.0" in p.stdout and "2.6.1" in p.stdout, p.stdout)
    check("hand copy 2.5.0 + plugin 2.6.1: the version-mismatch warning names both",
          any("2.5.0" in w and "2.6.1" in w for w in warns), f"{warns}")
    check("hand copy 2.5.0 + plugin 2.6.1: prints the update commands",
          "claude plugin update goalify@10x" in p.stdout)

    h2 = os.path.join(tmp, "h2")
    plugin(h2, "3.0.0")
    p = doctor(h2)
    check("single plugin copy: exit 0, no warning",
          p.returncode == 0 and "WARN" not in p.stdout and "exactly one goalify copy, version 3.0.0"
          in p.stdout, p.stdout)
    check("doctor says it makes no network call", "no network call" in p.stdout)

    h3 = os.path.join(tmp, "h3")
    plugin(h3, "2.5.0", installed=False)
    plugin(h3, "3.0.0")
    p = doctor(h3)
    check("a leftover cache folder that is not installed is ignored", p.returncode == 0
          and "ignored" in p.stdout, p.stdout)

    h4 = os.path.join(tmp, "h4")
    plugin(h4, "3.0.0")
    skill(os.path.join(h4, ".agents", "skills", "goalify"), "1.0.0")
    p = doctor(h4)
    check("an ~/.agents copy is found and counted", p.returncode == 1 and "1.0.0" in p.stdout,
          p.stdout)

    # `npx skills add` keeps one copy in <project>/.agents/skills and links it into
    # <project>/.claude/skills. That is one copy, and it is not a hand copy.
    h6 = os.path.join(tmp, "h6")
    proj6 = os.path.join(h6, "proj")
    skill(os.path.join(proj6, ".agents", "skills", "goalify"), "3.1.0")
    os.makedirs(os.path.join(proj6, ".claude", "skills"))
    os.symlink(os.path.join(proj6, ".agents", "skills", "goalify"),
               os.path.join(proj6, ".claude", "skills", "goalify"))
    p = doctor(h6)
    check("skills CLI install: the linked copy counts once, exit 0",
          p.returncode == 0 and "1 installed copy found" in p.stdout, p.stdout)
    check("skills CLI install: named as a skills CLI copy, not a hand copy",
          "skills CLI copy (npx skills add)" in p.stdout and "hand copy" not in p.stdout, p.stdout)
    plugin(h6, "3.1.0")
    p = doctor(h6)
    check("skills CLI copy + plugin: warns and prints the remove command",
          p.returncode == 1 and "npx skills remove goalify" in p.stdout, p.stdout)

    check("skills CLI linked install: the label says linked into",
          "linked into " + os.path.join(proj6, ".claude", "skills") in p.stdout, p.stdout)

    # `npx skills add --copy` copies the .agents folder into .claude/skills instead of
    # linking it. That is still one install, named as copied, not linked and not a hand copy.
    h8 = os.path.join(tmp, "h8")
    proj8 = os.path.join(h8, "proj")
    skill(os.path.join(proj8, ".agents", "skills", "goalify"), "3.1.2")
    skill(os.path.join(proj8, ".claude", "skills", "goalify"), "3.1.2")
    p = doctor(h8)
    check("skills CLI --copy install: the two folders count once, exit 0",
          p.returncode == 0 and "1 installed copy found" in p.stdout, p.stdout)
    check("skills CLI --copy install: the label says copied into, not linked into",
          "copied into " + os.path.join(proj8, ".claude", "skills") in p.stdout
          and "linked into" not in p.stdout and "hand copy" not in p.stdout, p.stdout)
    skill(os.path.join(proj8, ".claude", "skills", "goalify"), "3.0.0")
    p = doctor(h8)
    check("a .claude copy that differs from .agents stays a hand copy and is warned",
          p.returncode == 1 and "hand copy" in p.stdout and "2 installed copies found" in p.stdout,
          p.stdout)

    # Claude Code reads $CLAUDE_CONFIG_DIR instead of ~/.claude when it is set.
    h7 = os.path.join(tmp, "h7")
    cfg7 = os.path.join(tmp, "custom-config")
    plugin(h7, "3.1.1", config=cfg7)
    p = doctor(h7)
    check("CLAUDE_CONFIG_DIR unset: a plugin only in a custom config folder is not seen",
          "No goalify copy found" in p.stdout, p.stdout)
    p = doctor(h7, cfg7)
    check("CLAUDE_CONFIG_DIR set: its installed plugin is found, exit 0",
          p.returncode == 0 and "exactly one goalify copy, version 3.1.1" in p.stdout
          and "Claude Code plugin in $CLAUDE_CONFIG_DIR" in p.stdout, p.stdout)
    skill(os.path.join(cfg7, "skills", "goalify"), "2.0.0")
    plugin(h7, "1.9.0", installed=False, config=cfg7)
    skill(os.path.join(h7, ".claude", "skills", "goalify"), "3.1.1")
    p = doctor(h7, cfg7)
    check("CLAUDE_CONFIG_DIR set: its hand copy and ~/.claude are both scanned, mismatch warned",
          p.returncode == 1 and "2.0.0" in p.stdout and "3 installed copies found" in p.stdout,
          p.stdout)
    check("CLAUDE_CONFIG_DIR set: a leftover in its plugin cache is ignored",
          "1.9.0" in p.stdout and "ignored" in p.stdout, p.stdout)
    p = doctor(h7, os.path.join(h7, ".claude"))
    check("CLAUDE_CONFIG_DIR pointing at ~/.claude: each copy listed once",
          "1 installed copy found" in p.stdout, p.stdout)

    h5 = os.path.join(tmp, "h5")
    os.makedirs(h5)
    p = doctor(h5)
    check("no copy: says how to install, exit 0", p.returncode == 0 and "Install" in p.stdout)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# --- The version stamp in the SKILL.md body matches plugin.json ---
skill_text = open(os.path.join(ROOT, "skills", "goalify", "SKILL.md"), encoding="utf-8").read()
plugin_v = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))["version"]
m = re.search(r"This is goalify (\d+\.\d+\.\d+)", skill_text)
check("SKILL.md body says 'This is goalify X.Y.Z'", bool(m))
check("the body version equals plugin.json", bool(m) and m.group(1) == plugin_v,
      f"body={m.group(1) if m else None} plugin={plugin_v}")
check("the brief template header names the goalify version",
      "by goalify <version>" in skill_text)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
