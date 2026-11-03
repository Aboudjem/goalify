#!/usr/bin/env python3
"""
verify.py: `/goalify verify`. Re-run a brief's Definition-of-done checks and write a receipt.

goalify never does the task. This only runs the brief's own checks, and only when you ask:
it lists the commands first and runs nothing without a yes. It edits nothing outside `.goal/`,
never archives or un-archives a brief, and refuses destructive commands unless each one is
allowed by name.

Standard library only.

Usage:
    python3 verify.py [brief.md] --list             # show the commands, run nothing
    python3 verify.py [brief.md] --yes              # run them (after the user said yes)
    python3 verify.py [brief.md]                    # on a terminal: show, then ask once
    options: --allow "<exact destructive command>"  (repeatable)  --timeout <seconds>

With no brief, the newest brief in ./.goal/ or ./.goal/done/ is used.

Writes .goal/RECEIPT-<slug>-<stamp>.html and logs to .goal/verify-<slug>/<n>.log.
Exit 0 = VERIFIED, 1 = NOT VERIFIED, 3 = UNVERIFIABLE, 2 = usage error or the user said no.
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import goal_state  # noqa: E402
import render_preview as rp  # noqa: E402

DESTRUCTIVE = [
    (re.compile(r"\brm\s+(?:-[a-zA-Z]*[rf][a-zA-Z]*\s+)+"), "rm -r / rm -f"),
    (re.compile(r"\bgit\s+push\b"), "git push"),
    (re.compile(r"\bgit\s+reset\b"), "git reset"),
    (re.compile(r"\bgit\s+clean\b"), "git clean"),
    (re.compile(r"\bgit\s+checkout\s+--\s"), "git checkout --"),
    (re.compile(r"\b(?:npm|pnpm|yarn)\s+publish\b"), "npm publish"),
    (re.compile(r"\bterraform\s+(?:apply|destroy)\b"), "terraform apply/destroy"),
    (re.compile(r"\bDROP\s+(?:TABLE|DATABASE|SCHEMA)\b", re.IGNORECASE), "DROP"),
    (re.compile(r"\b(?:curl|wget)\b[^|]*\|\s*(?:ba|z)?sh\b"), "curl ... | sh"),
    (re.compile(r"\bsudo\b"), "sudo"),
    (re.compile(r"\bmkfs\b|\bdd\s+if="), "mkfs / dd"),
    (re.compile(r"\bkubectl\s+delete\b"), "kubectl delete"),
    (re.compile(r"\bgh\s+release\s+delete\b|\bgh\s+repo\s+delete\b"), "gh delete"),
]
TAIL_LINES = 20


def destructive_reason(cmd):
    for rx, label in DESTRUCTIVE:
        if rx.search(cmd):
            return label
    return None


def newest_brief(goal_dir):
    cands = []
    for sub in ("", "done"):
        d = os.path.join(goal_dir, sub) if sub else goal_dir
        if os.path.isdir(d):
            for n in os.listdir(d):
                p = os.path.join(d, n)
                if goal_state.is_brief(p):
                    cands.append((os.path.getmtime(p), p))
    return max(cands)[1] if cands else None


def plan(brief, allowed):
    """One entry per DoD command with what verify will do with it."""
    steps = []
    for i, item in enumerate(brief["dod"]):
        for cmd in item["commands"]:
            if goal_state.PLACEHOLDER_RE.search(cmd):
                action, why = "skip", "has a <placeholder>, so it cannot run as written"
            elif destructive_reason(cmd) and cmd not in allowed:
                action, why = "refuse", (f"matches the destructive pattern {destructive_reason(cmd)}; "
                                         'allow it by name with --allow "<command>"')
            else:
                action, why = "run", ""
            steps.append({"item": i, "cmd": cmd, "action": action, "why": why})
    return steps


def print_plan(brief, steps):
    print(f"Brief: {brief['path']}")
    print(f"Definition of done: {len(brief['dod'])} item(s), {len(steps)} command(s)")
    for n, s in enumerate(steps, 1):
        tag = {"run": "will run", "skip": "skip", "refuse": "REFUSED"}[s["action"]]
        print(f"  {n}. [{tag}] {s['cmd']}" + (f"   ({s['why']})" if s["why"] else ""))
    agents = [i for i in brief["dod"] if i["kind"] == "agent"]
    if agents:
        print(f"  + {len(agents)} item(s) checked by a separate agent: shown on the receipt as "
              "claimed, not re-run")


def run_steps(steps, cwd, log_dir, timeout):
    os.makedirs(log_dir, exist_ok=True)
    for n, s in enumerate(steps, 1):
        if s["action"] != "run":
            s.update(code=None, tail="", log=None)
            continue
        log = os.path.join(log_dir, f"{n}.log")
        t0 = time.time()
        try:
            p = subprocess.run(s["cmd"], shell=True, executable="/bin/bash", cwd=cwd,
                               capture_output=True, text=True, timeout=timeout)
            code, out = p.returncode, (p.stdout or "") + (p.stderr or "")
        except subprocess.TimeoutExpired as e:
            code = 124
            out = ((e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes)
                   else (e.stdout or "")) + f"\n[timed out after {timeout}s]"
        with open(log, "w", encoding="utf-8") as f:
            f.write(f"$ {s['cmd']}\n{out}\n[exit {code}]\n")
        s.update(code=code, tail="\n".join(out.rstrip().split("\n")[-TAIL_LINES:]),
                 log=log, secs=round(time.time() - t0, 1))
    return steps


def verdict_of(steps):
    runnable = [s for s in steps if s["action"] == "run"]
    if not runnable:
        return "UNVERIFIABLE"
    if all(s.get("code") == 0 for s in runnable) and len(runnable) == len(steps):
        return "VERIFIED"
    return "NOT VERIFIED"


def closeout_quotes(brief):
    path = os.path.join(goal_state.goal_dir_of(brief["path"]), f"closeout-{brief['slug']}.md")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return path, f.read()
    return None, None


def receipt_html(brief, steps, verdict, when):
    esc, inline, clip = rp.esc, rp.inline, rp.clip
    passed = sum(1 for s in steps if s["action"] == "run" and s.get("code") == 0)
    cls = {"VERIFIED": "ok", "NOT VERIFIED": "no", "UNVERIFIABLE": "un"}[verdict]
    word = {"VERIFIED": "Proven, not promised.", "NOT VERIFIED": "Not proven yet.",
            "UNVERIFIABLE": "Nothing here can be checked by a command."}[verdict]
    hero = (
        '<header class="hero" style="min-height:min(70vh,640px)">\n'
        '<span class="badge glass rv"><i></i>Proof receipt · ' + esc(when) + "</span>\n"
        f'<h1 class="rv long">{inline(brief["title"])}</h1>\n'
        f'<div class="rv" style="margin-top:22px"><span class="verdict {cls}">{esc(verdict)}</span></div>\n'
        f'<p class="rv"><span class="grad">{esc(word)}</span> {passed} of {len(steps)} check '
        f"command(s) passed when re-run just now, in this repo. Fresh output, not the run's word "
        "for it.</p>\n</header>\n")

    rows = []
    for i, item in enumerate(brief["dod"]):
        mine = [s for s in steps if s["item"] == i]
        if not mine:
            badge = ('<span class="st skip">CLAIMED</span>' if item["kind"] == "agent"
                     else '<span class="st skip">NO COMMAND</span>')
            sub = ("Checked by a separate agent during the run. verify cannot re-run an agent, "
                   "so this stays a claim." if item["kind"] == "agent"
                   else "This item names no command, so verify cannot check it.")
            mark = ('<span class="ok" aria-hidden="true" style="border-color:var(--yellow);'
                    'color:var(--yellow)">?</span>')
            rows.append(f'<div class="check glass">{mark}<div>'
                        f'<div class="txt">{inline(clip(item["text"], 320))}</div>'
                        f'<div class="cmds">{badge}</div><p class="note">{esc(sub)}</p></div></div>')
            continue
        parts = []
        for s in mine:
            if s["action"] == "run":
                st = "pass" if s.get("code") == 0 else "fail"
                lab = "PASS" if st == "pass" else f"FAIL · exit {s.get('code')}"
                parts.append(f'<div class="cmds"><span class="st {st}">{esc(lab)}</span>'
                             f'<span class="cmd">{esc(s["cmd"])}</span></div>'
                             f'<pre class="out">{esc(s.get("tail") or "(no output)")}</pre>')
            else:
                lab = "SKIPPED" if s["action"] == "skip" else "REFUSED"
                parts.append(f'<div class="cmds"><span class="st skip">{lab}</span>'
                             f'<span class="cmd">{esc(s["cmd"])}</span></div>'
                             f'<p class="note">{esc(s["why"])}</p>')
        ok_all = all(s["action"] == "run" and s.get("code") == 0 for s in mine)
        mark = ('<span class="ok" aria-hidden="true">✓</span>' if ok_all else
                '<span class="ok" aria-hidden="true" style="border-color:var(--red);color:var(--red)">✕</span>')
        rows.append(f'<div class="check glass">{mark}<div>'
                    f'<div class="txt">{inline(clip(rp.display_text(item["text"], item["commands"]), 320))}'
                    f'</div>{"".join(parts)}</div></div>')
    proof = ('<section class="rv">\n<div class="eyebrow">Promised vs proven</div>\n'
             "<h2>Every check, re-run</h2>\n"
             '<p class="lede">Each criterion from the brief, next to the exit code and the last '
             f"lines of output from a fresh run. Full logs are in <code>.goal/verify-{esc(brief['slug'])}/</code>.</p>\n"
             f'<div class="checks">{"".join(rows)}</div>\n</section>\n')

    claimed = [f'<div class="card glass" style="--c:var(--cyan)"><h3>Checklist (claimed)</h3>'
               f'<div class="big">{brief["ticks"][0]}/{brief["ticks"][1]}</div>'
               "<p>boxes the run ticked in the brief. That is what it said, not what was re-run.</p></div>"]
    if brief["completion_stamp"] is not None:
        claimed.append('<div class="card glass" style="--c:var(--yellow)"><h3>Completion stamp (claimed)</h3>'
                       f'<p>{inline(clip(brief["completion_stamp"], 400))}</p></div>')
    else:
        claimed.append('<div class="card glass" style="--c:var(--yellow)"><h3>Completion stamp</h3>'
                       "<p>None. The brief has not been archived as done.</p></div>")
    cpath, ctext = closeout_quotes(brief)
    if ctext:
        claimed.append('<div class="card glass" style="--c:var(--pink)"><h3>Closeout (reported by the run)</h3>'
                       f'<pre class="out">{esc(clip(ctext, 1500))}</pre></div>')
    if brief["archived"] and verdict != "VERIFIED":
        claimed.append('<div class="card glass" style="--c:var(--red)"><h3>Stamp vs checks</h3>'
                       "<p>The brief is archived as done, but its checks do not all pass now. "
                       "The fresh run wins.</p></div>")
    side = ('<section class="rv">\n<div class="eyebrow">What the run said</div>\n'
            "<h2>Claims, kept apart from proof</h2>\n"
            f'<div class="grid">{"".join(claimed)}</div>\n</section>\n')
    note = ('<section class="rv"><p class="note">goalify never does the task. verify only re-ran '
            "the brief's own checks, because you asked, and wrote nothing outside "
            "<code>.goal/</code>.</p></section>\n")
    return rp.page(f"{verdict} · {rp.plain(brief['title'])[:60]} · goalify receipt",
                   hero + proof + side + note, "A goalify proof receipt: the brief's checks, re-run.")


def main(argv):
    args = argv[1:]
    allowed, timeout, positional = [], 600, []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--allow" and i + 1 < len(args):
            allowed.append(args[i + 1]); i += 2; continue
        if a == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1]); i += 2; continue
        if a in ("-h", "--help"):
            print(__doc__.strip()); return 0
        positional.append(a); i += 1
    flags = {a for a in positional if a.startswith("--")}
    paths = [a for a in positional if not a.startswith("--")]
    unknown = flags - {"--list", "--yes"}
    if unknown:
        print(f"unknown option(s): {', '.join(sorted(unknown))}"); return 2

    brief_path = paths[0] if paths else newest_brief(os.path.join(os.getcwd(), ".goal"))
    if not brief_path or not os.path.isfile(brief_path):
        print("No brief found. Pass one: verify.py <brief.md>")
        return 2
    brief = goal_state.parse_brief(brief_path)
    steps = plan(brief, allowed)
    print_plan(brief, steps)
    if "--list" in flags:
        print("Nothing was run (--list).")
        return 0
    if not any(s["action"] == "run" for s in steps):
        verdict = "UNVERIFIABLE"
    else:
        if "--yes" not in flags:
            if not sys.stdin.isatty():
                print("Not run: pass --yes once the user has agreed to run these commands.")
                return 2
            ans = input("Run these commands now? [y/N] ").strip().lower()
            if ans not in ("y", "yes"):
                print("Not run.")
                return 2
        gdir = goal_state.goal_dir_of(brief["path"])
        run_steps(steps, os.path.dirname(gdir), os.path.join(gdir, f"verify-{brief['slug']}"), timeout)
        verdict = verdict_of(steps)
    when = time.strftime("%Y-%m-%d %H:%M")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    gdir = goal_state.goal_dir_of(brief["path"])
    out = rp.write_page(os.path.join(gdir, f"RECEIPT-{brief['slug']}-{stamp}.html"),
                        receipt_html(brief, steps, verdict, when))
    passed = sum(1 for s in steps if s["action"] == "run" and s.get("code") == 0)
    print(f"{passed}/{len(steps)} checks passed")
    for n, s in enumerate(steps, 1):
        if s["action"] == "run":
            print(f"  {n}. {'PASS' if s.get('code') == 0 else 'FAIL'} (exit {s.get('code')}) {s['cmd']}")
    print(f"VERDICT: {verdict}")
    print("Receipt: file://" + out)
    return {"VERIFIED": 0, "NOT VERIFIED": 1, "UNVERIFIABLE": 3}[verdict]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
