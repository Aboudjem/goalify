#!/usr/bin/env python3
"""
doctor.py: which goalify copies are installed on this machine, and do they agree?

Two copies of the same skill load side by side, and a stale one can win. (Observed
2026-08-06: a stale copy printed a handoff while agents were still running.) This lists every
copy it can find locally, with its version, and warns when there is more than one or when
versions differ.

It makes no network call, so it cannot know the latest release. It only compares the copies
on this machine, which is where the real failure lives.

Standard library only. Reads files, never writes, runs or fetches anything.

Usage:
    python3 doctor.py [--home <dir>] [--project <dir>] [--json]

Exit 0 = exactly one copy (or none), 1 = more than one copy or a version mismatch.
"""
import glob
import json
import os
import re
import sys

VERSION_RE = re.compile(r"^\s+version:\s*[\"']?(\d+\.\d+\.\d+)", re.MULTILINE)
BODY_VERSION_RE = re.compile(r"This is goalify (\d+\.\d+\.\d+)")


def skill_version(skill_md):
    try:
        text = open(skill_md, encoding="utf-8").read()
    except OSError:
        return None
    m = VERSION_RE.search(text) or BODY_VERSION_RE.search(text)
    return m.group(1) if m else "unknown"


def active_plugin_paths(home):
    """installPath of every goalify plugin Claude Code has installed (installed_plugins.json)."""
    path = os.path.join(home, ".claude", "plugins", "installed_plugins.json")
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    plugins = data.get("plugins", data) if isinstance(data, dict) else {}
    out = set()
    for key, entries in plugins.items():
        if not key.split("@", 1)[0] == "goalify":
            continue
        for e in entries if isinstance(entries, list) else [entries]:
            if isinstance(e, dict) and e.get("installPath"):
                out.add(os.path.realpath(e["installPath"]))
    return out


def find_copies(home, project):
    copies = []

    def add(kind, skill_dir, note=""):
        md = os.path.join(skill_dir, "SKILL.md")
        if os.path.isfile(md):
            copies.append({"kind": kind, "path": os.path.realpath(skill_dir),
                           "version": skill_version(md), "note": note})

    add("Claude Code hand copy (user)", os.path.join(home, ".claude", "skills", "goalify"))
    if project:
        add("Claude Code hand copy (project)", os.path.join(project, ".claude", "skills", "goalify"))
    active = active_plugin_paths(home)
    for d in sorted(glob.glob(os.path.join(home, ".claude", "plugins", "cache", "*", "goalify", "*"))):
        skill_dir = os.path.join(d, "skills", "goalify")
        if os.path.realpath(d) in active:
            add("Claude Code plugin", skill_dir, "installed")
        elif os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
            copies.append({"kind": "plugin cache leftover", "path": os.path.realpath(skill_dir),
                           "version": skill_version(os.path.join(skill_dir, "SKILL.md")),
                           "note": "not installed, not loaded", "inactive": True})
    add("Agent Skills copy (npx skills, ~/.agents)", os.path.join(home, ".agents", "skills", "goalify"))
    add("Codex copy", os.path.join(home, ".codex", "skills", "goalify"))
    return copies


def main(argv):
    args = argv[1:]
    home = os.path.expanduser("~")
    project = os.getcwd()
    if "--home" in args:
        home = args[args.index("--home") + 1]
    if "--project" in args:
        project = args[args.index("--project") + 1]
    copies = find_copies(home, project)
    loaded = [c for c in copies if not c.get("inactive")]
    versions = sorted({c["version"] for c in loaded})
    problems = []
    if len(loaded) > 1:
        problems.append(f"{len(loaded)} goalify copies are installed. More than one can load side by "
                        "side, and a stale one can win.")
    if len(versions) > 1:
        problems.append("the copies disagree on the version: " + ", ".join(versions))

    if "--json" in args:
        print(json.dumps({"copies": copies, "problems": problems}, indent=2))
        return 1 if problems else 0

    print(f"goalify doctor: {len(loaded)} installed cop{'y' if len(loaded) == 1 else 'ies'} found")
    for c in copies:
        flag = "  (ignored: " + c["note"] + ")" if c.get("inactive") else ""
        print(f"  {c['version']:<8} {c['kind']}: {c['path']}{flag}")
    if not loaded:
        print("No goalify copy found. Install: claude plugin marketplace add Aboudjem/10x, then "
              "claude plugin install goalify@10x")
        return 0
    if problems:
        for p in problems:
            print("WARN: " + p)
        print("Fix: keep one copy. For the plugin: claude plugin marketplace update 10x, then "
              "claude plugin update goalify@10x. Move any hand copy out of ~/.claude/skills/.")
        print("Note: no network call is made, so this cannot tell you the latest release.")
        return 1
    print(f"OK: exactly one goalify copy, version {loaded[0]['version']}.")
    print("Note: no network call is made, so this cannot tell you the latest release.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
