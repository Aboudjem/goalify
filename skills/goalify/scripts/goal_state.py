#!/usr/bin/env python3
"""
goal_state.py: read a goalify brief (and the files around it) into plain data.

Every v3 helper reads briefs through this one parser: the run preview, `/goalify verify`,
`/goalify status` and the brief lint. A change to the brief template then breaks one parser
and its tests, not four features.

Standard library only. It reads files and never writes, runs, or fetches anything, with one
exception: `--status --html` writes `.goal/index.html` through render_preview.py.

Usage:
    python3 goal_state.py <brief.md>              # JSON dump of the parsed brief
    python3 goal_state.py --status [dir] [--html] # one row per brief in a .goal/ folder

Exit 0 on success, 2 on a usage error or a missing file.
"""
import json
import os
import re
import sys
import time

# The sections the brief template in SKILL.md defines, in order. Matching is on the start of
# the "## " heading, so "## Context (verified, re-confirm live)" counts as "Context".
REQUIRED_SECTIONS = [
    "GOAL",
    "Context",
    "Decisions",
    "Phases",
    "Process directives",
    "Definition of done",
    "Progress checklist",
    "Final output",
    "Archive gate",
]

FILENAME_RE = re.compile(r"^(?P<slug>.+?)-(?P<stamp>\d{8}(?:-\d{4,6})?|\d{4}-\d{2}-\d{2})\.md$")
TITLE_RE = re.compile(r"^#\s+GOAL:\s*(?P<title>.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(?P<heading>.+?)\s*$", re.MULTILINE)
OWN_PATH_RE = re.compile(r"This file's own path:\s*`?(?P<path>[^`\s]+)`?")
AUTHORED_RE = re.compile(r"Authored\s+(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\s+by\s+goalify"
                         r"(?:\s+(?P<version>\d+\.\d+\.\d+))?")
ITEM_RE = re.compile(r"^(?P<indent>\s*)[-*]\s+\[(?P<mark>[ xX])\]\s+(?P<text>.*)$")
CODE_RE = re.compile(r"`([^`\n]+)`")
STAMP_RE = re.compile(r"^(?:#+\s*)?(?:\*\*)?completion stamp(?:\*\*)?:?\s*(?P<rest>.*)$",
                      re.IGNORECASE | re.MULTILINE)
PHASE_RE = re.compile(r"^(?P<num>\d+)\.\s+(?P<text>.+)$")
VERSION_LINE_RE = re.compile(r"goalify\s+(\d+\.\d+\.\d+)")

# A single-word span is a command only if it is one of these. Everything else that is one word
# (`MERGED`, `200`, `src/`) is an expected value or a path, not something to run.
SINGLE_WORD_COMMANDS = {
    "true", "false", "make", "pytest", "tox", "nox", "just", "ls", "pwd", "date", "ruff",
    "mypy", "tsc", "cargo", "go", "npm", "pnpm", "yarn", "bun", "deno", "jest", "vitest",
}
_FIRST_TOKEN_RE = re.compile(r"^(?:\.{0,2}/|~/)?[a-z0-9_][a-zA-Z0-9_.+/-]*$")
_ENV_ASSIGN_RE = re.compile(r"^[A-Z_][A-Z0-9_]*=\S*$")
PLACEHOLDER_RE = re.compile(r"<[^<>]+>")
# "verified by `grep ...` printing nothing": the check passes when the command prints nothing.
EXPECT_EMPTY_RE = re.compile(
    r"\b(?:print(?:s|ing)?|return(?:s|ing)?|output(?:s|ting)?|show(?:s|ing)?)\s+nothing\b"
    r"|\bno output\b|\bempty output\b|\bzero (?:matches|hits|results|lines)\b|\bno matches\b",
    re.IGNORECASE)
SEPARATE_AGENT_RE = re.compile(r"\bseparate\b.{0,40}\b(?:agent|verifier|reviewer)\b",
                               re.IGNORECASE | re.DOTALL)


def looks_like_command(span):
    """True when a backticked span reads as a shell command rather than a value or a path."""
    span = span.strip()
    if not span or span[0] in "([{'\"$<":
        return False
    tokens = span.split()
    while tokens and _ENV_ASSIGN_RE.match(tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return False
    first = tokens[0]
    if not _FIRST_TOKEN_RE.match(first) or first.endswith("/"):
        return False
    if len(tokens) == 1:
        return first in SINGLE_WORD_COMMANDS or first.startswith("./")
    # "src/server.js and" style prose fragments: a file name followed by words is not a command
    # unless the first token is something executable-looking (no extension other than a script).
    if re.search(r"\.(?:md|json|txt|html|css|svg|png|yml|yaml|toml|lock)$", first):
        return False
    return True


def commands_in(text):
    """Backticked commands in a Definition-of-done item.

    When the item says "verified by", only the spans after it count, so a span that names the
    thing being checked (`cb(`, `src/`) is never mistaken for the check itself.
    """
    lowered = text.lower()
    cut = lowered.find("verified by")
    scope = text[cut:] if cut >= 0 else text
    return [s.strip() for s in CODE_RE.findall(scope) if looks_like_command(s)]


def _split_sections(text):
    """Ordered list of (heading, body) for every '## ' heading outside a code fence."""
    lines = text.split("\n")
    out, heading, buf, fence = [], None, [], None
    for line in lines:
        stripped = line.lstrip()
        fm = re.match(r"(`{3,}|~{3,})", stripped)
        if fm:
            mark = fm.group(1)[0]
            if fence is None:
                fence = mark
            elif fence == mark:
                fence = None
        if fence is None and line.startswith("## "):
            if heading is not None:
                out.append((heading, "\n".join(buf).strip("\n")))
            heading, buf = line[3:].strip(), []
            continue
        if heading is not None:
            buf.append(line)
    if heading is not None:
        out.append((heading, "\n".join(buf).strip("\n")))
    return out


def find_section(sections, name):
    """Body of the first section whose heading starts with `name` (case-insensitive)."""
    key = name.lower()
    for heading, body in sections:
        h = heading.lower()
        if h == key or h.startswith(key + " ") or h.startswith(key + "(") or h.startswith(key + ":"):
            return body
    return None


def parse_items(body):
    """Checkbox items, with indented continuation lines folded into one item."""
    items = []
    if not body:
        return items
    current = None
    for line in body.split("\n"):
        m = ITEM_RE.match(line)
        if m:
            current = {"checked": m.group("mark") in "xX", "text": m.group("text").strip()}
            items.append(current)
            continue
        if current is not None and line.strip() and line[:1] in (" ", "\t"):
            current["text"] += " " + line.strip()
            continue
        if line.strip():
            # Any other non-indented line (prose, a plain bullet, a heading) ends the item.
            current = None
    return items


def parse_bullets(body):
    """Plain '- ' bullets (not checkboxes), continuation lines folded in."""
    bullets = []
    if not body:
        return bullets
    current = None
    for line in body.split("\n"):
        if re.match(r"^[-*]\s+(?!\[[ xX]\])", line):
            current = line[2:].strip()
            bullets.append(current)
            continue
        if bullets and line.strip() and line.startswith("  "):
            bullets[-1] += " " + line.strip()
            continue
        if not line.strip():
            continue
    return bullets


def parse_phases(body):
    """Numbered top-level phases: '1. **Title.** text' or '1. text'."""
    phases = []
    if not body:
        return phases
    for line in body.split("\n"):
        m = PHASE_RE.match(line)
        if m:
            text = m.group("text").strip()
            title_m = re.match(r"\*\*(.+?)\*\*\s*(.*)$", text)
            if title_m:
                title, rest = title_m.group(1).strip().rstrip("."), title_m.group(2).strip()
            else:
                first = re.split(r"(?<=[.:])\s", text, maxsplit=1)
                title = first[0].rstrip(".:")
                rest = first[1] if len(first) > 1 else ""
            phases.append({"num": int(m.group("num")), "title": title, "text": rest})
        elif phases and line.startswith("   ") and line.strip():
            phases[-1]["text"] = (phases[-1]["text"] + " " + line.strip()).strip()
    return phases


def completion_stamp(text):
    """The text of the last completion stamp in the brief, or None."""
    matches = list(STAMP_RE.finditer(text))
    if not matches:
        return None
    m = matches[-1]
    rest = m.group("rest").strip()
    if rest:
        return rest
    tail = text[m.end():].strip().split("\n")
    return tail[0].strip() if tail and tail[0].strip() else ""


def slug_and_stamp(path):
    name = os.path.basename(path)
    m = FILENAME_RE.match(name)
    if m:
        return m.group("slug"), m.group("stamp")
    return os.path.splitext(name)[0], ""


def goal_dir_of(path):
    """The .goal/ folder a brief belongs to (its parent, or the grandparent for done/)."""
    parent = os.path.dirname(os.path.abspath(path))
    if os.path.basename(parent) == "done":
        return os.path.dirname(parent)
    return parent


def condition_file_for(path, slug=None):
    slug = slug or slug_and_stamp(path)[0]
    cand = os.path.join(goal_dir_of(path), f"CONDITION-{slug}.txt")
    return cand if os.path.exists(cand) else None


def read_condition(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def blockers_for(path, slug, stamp, mtime=None):
    """BLOCKERS-* files in the brief's .goal/ whose name carries the brief's slug or stamp.

    The template names them `.goal/BLOCKERS-<stamp>.md`, so the stamp ties a blockers file to
    its brief. Matching by name rather than by "newer than the brief" keeps one brief's
    blockers from marking every older open brief as blocked.
    """
    gdir = goal_dir_of(path)
    found = []
    try:
        names = sorted(os.listdir(gdir))
    except OSError:
        return found
    for name in names:
        if not name.startswith("BLOCKERS-"):
            continue
        full = os.path.join(gdir, name)
        named = (slug and slug in name) or (stamp and stamp.replace("-", "") in name.replace("-", ""))
        if named:
            found.append(full)
    return found


def parse_brief(path):
    """Parse one brief into a dict. Raises OSError if the file cannot be read."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    sections = _split_sections(text)
    slug, stamp = slug_and_stamp(path)
    title_m = TITLE_RE.search(text)
    own_m = OWN_PATH_RE.search(text)
    auth_m = AUTHORED_RE.search(text)

    dod = []
    for item in parse_items(find_section(sections, "Definition of done")):
        cmds = commands_in(item["text"])
        kind = "command" if cmds else ("agent" if SEPARATE_AGENT_RE.search(item["text"]) else "none")
        dod.append({
            "text": item["text"],
            "checked": item["checked"],
            "commands": cmds,
            "placeholders": [c for c in cmds if PLACEHOLDER_RE.search(c)],
            "expect_empty": bool(EXPECT_EMPTY_RE.search(item["text"])),
            "kind": kind,
        })
    checklist = parse_items(find_section(sections, "Progress checklist"))
    mtime = os.path.getmtime(path)
    cond_file = condition_file_for(path, slug)
    archived = os.path.basename(os.path.dirname(os.path.abspath(path))) == "done"

    # The objective sentence: the first paragraph of the GOAL section.
    goal_body = find_section(sections, "GOAL") or ""
    objective = ""
    for para in re.split(r"\n\s*\n", goal_body.strip()):
        para = " ".join(para.split())
        if para:
            objective = para
            break

    return {
        "path": os.path.abspath(path),
        "slug": slug,
        "stamp": stamp,
        "title": title_m.group("title") if title_m else "",
        "objective": objective,
        "own_path": own_m.group("path") if own_m else "",
        "authored": auth_m.group("date") if auth_m else "",
        "goalify_version": (auth_m.group("version") or "") if auth_m else "",
        "sections": [h for h, _ in sections],
        "section_bodies": {h: b for h, b in sections},
        "missing_sections": [s for s in REQUIRED_SECTIONS if find_section(sections, s) is None],
        "phases": parse_phases(find_section(sections, "Phases")),
        "decisions": parse_bullets(find_section(sections, "Decisions")),
        "dod": dod,
        "checklist": checklist,
        "ticks": [sum(1 for i in checklist if i["checked"]), len(checklist)],
        "archived": archived,
        "completion_stamp": completion_stamp(text),
        "condition_file": cond_file,
        "condition": read_condition(cond_file) if cond_file else None,
        "blockers": blockers_for(path, slug, stamp),
        "mtime": mtime,
    }


def is_brief(path):
    """A brief is a .md file whose first heading is '# GOAL:'."""
    if not path.endswith(".md") or not os.path.isfile(path):
        return False
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(4096)
    except OSError:
        return False
    return bool(TITLE_RE.search(head))


def _age(seconds):
    seconds = max(0, int(seconds))
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def collect_status(goal_dir, now=None):
    """One row per brief in goal_dir and goal_dir/done, plus orphan CONDITION files."""
    now = time.time() if now is None else now
    rows, slugs = [], set()
    paths = []
    for sub in ("", "done"):
        d = os.path.join(goal_dir, sub) if sub else goal_dir
        if os.path.isdir(d):
            paths += [os.path.join(d, n) for n in sorted(os.listdir(d))]
    for p in paths:
        if not is_brief(p):
            continue
        b = parse_brief(p)
        slugs.add(b["slug"])
        if b["archived"]:
            state = "DONE"
        elif b["blockers"]:
            state = "BLOCKED"
        else:
            state = "OPEN"
        rows.append({
            "slug": b["slug"], "state": state, "ticks": b["ticks"],
            "age": _age(now - b["mtime"]), "mtime": b["mtime"], "path": b["path"],
            "condition": b["condition"], "condition_file": b["condition_file"],
            "title": b["title"], "stamp": b["completion_stamp"], "blockers": b["blockers"],
        })
    if os.path.isdir(goal_dir):
        for name in sorted(os.listdir(goal_dir)):
            m = re.match(r"^CONDITION-(.+)\.txt$", name)
            if m and m.group(1) not in slugs:
                full = os.path.join(goal_dir, name)
                rows.append({
                    "slug": m.group(1), "state": "ORPHAN-CONDITION", "ticks": [0, 0],
                    "age": _age(now - os.path.getmtime(full)), "mtime": os.path.getmtime(full),
                    "path": None, "condition": read_condition(full), "condition_file": full,
                    "title": "", "stamp": None, "blockers": [],
                })
    order = {"OPEN": 0, "BLOCKED": 1, "DONE": 2, "ORPHAN-CONDITION": 3}
    rows.sort(key=lambda r: (order[r["state"]], -r["mtime"], r["slug"]))
    return rows


def format_status(rows):
    if not rows:
        return "No briefs found. Prepare one with /goalify <task>."
    w = max(len(r["slug"]) for r in rows)
    lines = [f"{'brief'.ljust(w)}  {'state'.ljust(16)}  ticks  age"]
    for r in rows:
        ticks = f"{r['ticks'][0]}/{r['ticks'][1]}" if r["path"] else "-"
        lines.append(f"{r['slug'].ljust(w)}  {r['state'].ljust(16)}  {ticks.ljust(5)}  {r['age']}")
    resumable = [r for r in rows if r["state"] in ("OPEN", "BLOCKED")]
    for r in resumable:
        lines.append("")
        lines.append(f"{r['slug']} ({r['state'].lower()}), resume with:")
        if r["condition"]:
            lines.append(f"  /clear")
            lines.append(f"  /goal {r['condition']}")
        else:
            lines.append("  (no CONDITION file next to this brief, so there is no line to reprint;"
                         " re-derive the condition from its Definition of done)")
        for bl in r["blockers"]:
            lines.append(f"  blockers: {os.path.basename(bl)}")
    lines.append("")
    lines.append("Read-only: status never runs /goal and never edits a file.")
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 2
    if args[0] == "--status":
        rest = [a for a in args[1:] if not a.startswith("--")]
        now = None
        if "--now" in args:
            i = args.index("--now")
            now = float(args[i + 1])
            rest = [a for a in rest if a != args[i + 1]]
        goal_dir = rest[0] if rest else os.path.join(os.getcwd(), ".goal")
        if not os.path.isdir(goal_dir):
            print(f"No .goal/ folder at {goal_dir}. Prepare a run with /goalify <task>.")
            return 0
        rows = collect_status(goal_dir, now)
        print(format_status(rows))
        if "--html" in args:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import render_preview  # noqa: E402  (sibling script, standard library only)
            out = render_preview.write_status_index(goal_dir, rows)
            print("")
            print("Index page (optional): file://" + out)
        return 0
    path = args[0]
    if not os.path.isfile(path):
        print(f"no such brief: {path}")
        return 2
    data = parse_brief(path)
    data.pop("section_bodies", None)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
