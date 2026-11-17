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

Claude Code keeps its config in ~/.claude, or in $CLAUDE_CONFIG_DIR when that is set. doctor
scans both, so a custom config folder is not missed.

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


def config_dirs(home, env=None):
    """Claude Code config folders to scan: ~/.claude, plus $CLAUDE_CONFIG_DIR when set."""
    env = os.environ if env is None else env
    dirs = [os.path.join(home, ".claude")]
    custom = env.get("CLAUDE_CONFIG_DIR", "").strip()
    if custom:
        custom = os.path.expanduser(custom)
        if os.path.realpath(custom) != os.path.realpath(dirs[0]):
            dirs.append(custom)
    return dirs


def active_plugin_paths(config_dir):
    """installPath of every goalify plugin Claude Code has installed (installed_plugins.json)."""
    path = os.path.join(config_dir, "plugins", "installed_plugins.json")
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


def skills_cli_twin(skill_dir):
    """The .agents copy that `npx skills add --copy` made next to this .claude copy, or None.

    `<root>/.claude/skills/goalify` is one install with `<root>/.agents/skills/goalify` when
    it is a real folder and both SKILL.md files hold the same bytes."""
    skills = os.path.dirname(skill_dir)
    claude = os.path.dirname(skills)
    if os.path.basename(skills) != "skills" or os.path.basename(claude) != ".claude":
        return None
    twin = os.path.join(os.path.dirname(claude), ".agents", "skills", os.path.basename(skill_dir))
    try:
        with open(os.path.join(skill_dir, "SKILL.md"), "rb") as a, \
                open(os.path.join(twin, "SKILL.md"), "rb") as b:
            same = a.read() == b.read()
    except OSError:
        return None
    return os.path.realpath(twin) if same else None


def find_copies(home, project):
    copies = []

    def add(kind, skill_dir, note=""):
        md = os.path.join(skill_dir, "SKILL.md")
        if os.path.isfile(md):
            # `npx skills add` keeps one real copy in .agents/skills and links it into each
            # agent's folder. With --copy it copies it there instead. Name it for what it
            # is, and list it once.
            real = os.path.realpath(skill_dir)
            if os.path.islink(skill_dir) and os.sep + ".agents" + os.sep in real:
                kind = "skills CLI copy (npx skills add), linked into " + os.path.dirname(skill_dir)
            else:
                twin = skills_cli_twin(skill_dir)
                if twin:
                    kind = "skills CLI copy (npx skills add --copy), copied into " + os.path.dirname(skill_dir)
                    real = twin
            if any(c["path"] == real for c in copies):
                return
            copies.append({"kind": kind, "path": real,
                           "version": skill_version(md), "note": note})

    for cdir in config_dirs(home):
        where = "" if cdir == os.path.join(home, ".claude") else " in $CLAUDE_CONFIG_DIR"
        add("Claude Code hand copy (user" + where + ")", os.path.join(cdir, "skills", "goalify"))
        active = active_plugin_paths(cdir)
        for d in sorted(glob.glob(os.path.join(cdir, "plugins", "cache", "*", "goalify", "*"))):
            skill_dir = os.path.join(d, "skills", "goalify")
            if os.path.realpath(d) in active:
                add("Claude Code plugin" + where, skill_dir, "installed")
            elif os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
                real = os.path.realpath(skill_dir)
                if any(c["path"] == real for c in copies):
                    continue
                copies.append({"kind": "plugin cache leftover" + where, "path": real,
                               "version": skill_version(os.path.join(skill_dir, "SKILL.md")),
                               "note": "not installed, not loaded", "inactive": True})
    if project:
        add("Claude Code hand copy (project)", os.path.join(project, ".claude", "skills", "goalify"))
    add("skills CLI copy (npx skills add, ~/.agents)", os.path.join(home, ".agents", "skills", "goalify"))
    if project:
        add("skills CLI copy (npx skills add, project)", os.path.join(project, ".agents", "skills", "goalify"))
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
              "claude plugin update goalify@10x. Remove a skills CLI copy with: npx skills remove goalify. "
              "Move any hand copy out of ~/.claude/skills/.")
        print("Note: no network call is made, so this cannot tell you the latest release.")
        return 1
    print(f"OK: exactly one goalify copy, version {loaded[0]['version']}.")
    print("Note: no network call is made, so this cannot tell you the latest release.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
