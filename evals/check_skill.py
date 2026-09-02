#!/usr/bin/env python3
"""
goalify skill eval — machine-checkable static assertions.

This is the deterministic half of the eval suite (the behavioral scenarios live in
`scenarios.md` and are run against Haiku/Sonnet/Opus). It encodes the CONFIRMED
research edits as pass/fail checks so a regression is caught in CI.

It doubles as the RED→GREEN demonstration, reproducible from this repo's own history:
point it at `git show v1.1.0:skills/goalify/SKILL.md` and it FAILS (RED, 30/82); point it
at the current `goalify` SKILL.md and it PASSES (GREEN, 82/82).

Usage:
    python3 evals/check_skill.py [path-to-SKILL.md]   # default: skills/goalify/SKILL.md
Exit code 0 = all checks pass, 1 = at least one failed.
No third-party deps; standard library only.
"""
import os
import re
import sys


def parse_frontmatter(block):
    """Minimal YAML parse for top-level scalars + folded/literal block scalars."""
    data = {}
    lines = block.split("\n")
    i = 0
    key_re = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line[:1] in (" ", "\t"):
            i += 1
            continue
        km = key_re.match(line)
        if not km:
            i += 1
            continue
        key, rest = km.group(1), km.group(2).strip()
        if rest.startswith(("|", ">")):
            collected = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    collected.append("")
                    i += 1
                    continue
                if nxt[:1] in (" ", "\t"):
                    collected.append(nxt.strip())
                    i += 1
                else:
                    break
            data[key] = " ".join(c for c in collected if c != "").strip()
            continue
        val = rest
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        data[key] = val
        i += 1
    return data


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "skills/goalify/SKILL.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} not found")
        return 1

    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not m:
        print(f"FAIL: no YAML frontmatter in {path}")
        return 1
    block = m.group(1)
    fm = parse_frontmatter(block)
    body = text[m.end():]
    # Normalized prose view: strip blockquote markers, collapse whitespace (so
    # line-wraps don't break phrase matches), and drop backticks and emphasis (so
    # `/clear` matches "/clear" and **bold** matches plain). Substring checks below
    # run against this; the raw `body` is kept only for the line-count check.
    unquoted = re.sub(r"(?m)^\s{0,3}>\s?", "", body)
    low = re.sub(r"\s+", " ", unquoted).replace("`", "").replace("*", "").lower()

    checks = []  # (name, ok, detail)

    # --- Frontmatter hard limits (agentskills.io / Anthropic spec) ---
    name = fm.get("name", "")
    checks.append(("name matches ^[a-z0-9-]+$ and <=64",
                   bool(re.fullmatch(r"[a-z0-9-]+", name)) and len(name) <= 64,
                   f"name={name!r}"))
    parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
    checks.append(("name matches parent directory",
                   name == parent, f"name={name!r} dir={parent!r}"))
    desc = fm.get("description", "")
    checks.append(("description non-empty and <=1024 chars",
                   bool(desc.strip()) and len(desc) <= 1024, f"len={len(desc)}"))

    # --- metadata.version present (version belongs INSIDE metadata, not bare) ---
    checks.append(("metadata.version present",
                   bool(re.search(r"^\s+version:\s*[\"']?\d+\.\d+\.\d+", block, re.MULTILINE)),
                   "looks for an indented version under metadata"))
    checks.append(("no bare top-level `version:` field",
                   not re.search(r"^version:", block, re.MULTILINE), "spec has no top-level version"))

    # --- Slash-command ergonomics: argument-hint + documented $ARGUMENTS ---
    checks.append(("frontmatter declares argument-hint (self-explanatory /goalify command)",
                   bool(fm.get("argument-hint", "").strip()),
                   "argument-hint tells the /goalify command what to type"))
    checks.append(("body documents the /goalify command and $ARGUMENTS",
                   ("/goalify" in low) and ("$arguments" in low),
                   "the slash command and its $ARGUMENTS must be documented in the body"))

    # --- Description: WHEN-only, disambiguated, branded (research 00 claim 2) ---
    dlow = desc.lower()
    checks.append(("description carries the 'goalify' trigger", "goalify" in dlow, ""))
    checks.append(("description disambiguates vs autopilot/ultrawork/ralph",
                   all(w in dlow for w in ("autopilot", "ultrawork", "ralph")), ""))
    checks.append(("description says AUTHOR-not-execute",
                   ("author" in dlow) and ("not" in dlow) and ("execute" in dlow or "executing" in dlow), ""))
    # WHEN-only: must NOT enumerate its own process (the documented shortcut misfire).
    summarizes_workflow = ("research" in dlow and "mcq" in dlow and ("fan-out" in dlow or "fan out" in dlow))
    checks.append(("description does NOT summarize the research+MCQ+fan-out workflow",
                   not summarizes_workflow, "WHEN-only; no process summary in the description"))

    # --- Tool references: capability + fallback, not a bare vague noun (claim 6) ---
    checks.append(("tool fan-out has a capability+fallback (no reliance on a vague tool noun)",
                   ("if none is available" in low) and ("sequential" in low),
                   "expects 'if none is available, run the searches sequentially'"))

    # --- Generated-MD template hardening (research 02) ---
    template_clauses = {
        "output-redirection rule": ("2>&1" in body) and ("tail" in low),
        "anti-placeholder / full-implementations": "full implementation" in low or "placeholder" in low,
        "search-before-assuming-missing": "search before assuming" in low or "assuming missing" in low or "false negative" in low,
        "machine-checkable success criteria (named command/test)": "verified by" in low and ("exit 0" in low or "named test" in low or "named command" in low),
        "copyable progress checklist": "progress checklist" in low,
        "just-in-time identifiers (not dumps)": "just-in-time" in low or "lightweight identifier" in low,
        "fan-out guardrail: serialize builds/tests/same-file writes": "serialize builds" in low,
        "separate-agent verification / never self-approve": "separate agent" in low and "self-approve" in low,
        "commit before risky steps": "commit before risky" in low,
        "re-read this file each loop": "re-read this file" in low or "re-read the" in low,
        "maximum-effort directive": "maximum effort" in low,
        "names a portable max-effort mode (ultracode/ultrawork)": "ultracode" in low or "ultrawork" in low,
    }
    for clause, ok in template_clauses.items():
        checks.append((f"template: {clause}", ok, ""))

    # --- v2 CONTRACT: the handoff is a derived condition STRING, not a file path ---
    # These encode the v2.0.0 correction. `/goal` takes a condition (docs + binary);
    # v1 told users to pass a path, which the tool-less evaluator can never verify.
    path_handoff_re = re.compile(r"/goal\s+(?:<\s*(?:abs|absolute|path)|~/|/users/)")
    v2_clauses = {
        "handoff is a condition string, never a file path":
            "condition string, never a file path" in low,
        "no text instructs passing a file path to /goal":
            not path_handoff_re.search(low),
        "condition is DERIVED from the brief's definition of done":
            "derive it from the brief" in low,
        "condition has a 4,000-character limit that is linted, not estimated":
            ("4,000 characters" in low or "4,000-char" in low) and "lint" in low,
        "condition carries a sentinel token":
            "sentinel" in low,
        "closeout-turn rule (defeats evaluator transcript truncation)":
            "closeout turn" in low and "truncat" in low,
        "freshly-quoted-output evidence rule":
            "freshly quoted" in low,
        "condition carries an explicit turn bound":
            "turn bound" in low,
        "condition lint forbids a bare $ (hook-substitution hazard)":
            "bare $" in low,
        "evaluator is documented as tool-less / transcript-only":
            "no tools" in low and "transcript" in low,
        "subagent barrier (never end a turn with a live subagent)":
            "subagent barrier" in low and "still live" in low,
        "model routing (fast for breadth, deep for architecture)":
            "fast model" in low and "deep model" in low,
        "dry run + caps (phases, subagents, turn cap)":
            "dry run" in low and "turn cap" in low,
        "no predicted token/dollar cost is invented":
            "never predict a dollar or token" in low,
        "3-strike escalation ladder":
            "3-strike" in low,
        "archive-not-delete gate (audit trail preserved)":
            "archive gate" in low and "mv " in body,
        # D6: the handoff must hand the user a COMMAND, not a file. A `pbcopy` step puts a
        # path in their hand at the exact moment they type `/goal` — the most reliable way
        # to produce the wrong input. Assert the inline form is mandated AND that the copy
        # step is explicitly demoted, so a future edit cannot quietly restore it.
        "handoff prints the complete /goal line inline, ready to copy in one piece":
            "inline" in low and "verbatim" in low and "entire condition text" in low,
        # TIGHTENED in v2.3.0: the old form only checked that pbcopy was *demoted*. The
        # v2.3.0 handoff removes the copy STEP outright (the condition is short enough to
        # read on screen), so the ban is now asserted directly as well as the demotion of
        # the saved-condition file, which still exists as a durable record.
        "handoff does NOT make pbcopy the required step":
            "never the required step" in low and "no pbcopy step" in low
            and "pbcopy < <paste>" not in low,
        "handoff shows no <paste> placeholder in place of the condition":
            "/goal <paste>" not in low,
        "handoff sets --permission-mode auto for unattended runs":
            "--permission-mode auto" in low,
        "handoff prints the headless form":
            "claude -p" in low,
        "documents that /goal success is NOT proof of completion":
            "not proof of completion" in low,
        "offers a verify-only re-check":
            "verify-only" in low,
        "cross-harness: Codex /goal also takes an inline objective":
            "codex" in low and "inline objective" in low,
        "documents that process directives do not bind Codex (untrusted demotion)":
            "untrusted" in low and "definition of done carries" in low,
        "brief separates definition of done from process directives":
            "definition of done" in low and "process directives" in low,
    }
    for clause, ok in v2_clauses.items():
        checks.append((f"v2: {clause}", ok, ""))

    # --- v2.3 CONTRACT: plain words, a SHORT condition, a one-line handoff, visible work ---
    # v2.2 was correct and unreadable: it taught a 4,000-character acceptance protocol as the
    # default shape, printed a handoff with a copy step, and let a run go dark for an hour and
    # then report in prose. These assertions pin the three fixes.

    # Two strings are locked byte-identical across the whole repo. They are compared against the
    # RAW text (not `low`), because the point of locking them is that the wording does not drift.
    STORY = ("Hand Claude a huge task. Come back to proof it's done — "
             "not a promise that it is.")
    CANON = ("Do everything in ~/acme/.goal/api-migration.md and prove it — done when the "
             "last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.")

    # The brief TEMPLATE is checked in its own scope. A substring check over the whole body
    # cannot tell "the skill mentions X somewhere" from "the template the skill authors REQUIRES
    # X", and every clause below is a requirement placed on the generated brief.
    tm = re.search(r"^```markdown\s*\n(.*?)\n```\s*$", body, re.DOTALL | re.MULTILINE)
    tmpl = tm.group(1) if tm else ""
    tmpl_low = re.sub(r"\s+", " ", tmpl).replace("`", "").replace("*", "").lower()

    v23_clauses = {
        # -- the plain-words story, verbatim, in both places a newcomer meets the skill --
        "the plain-words story appears VERBATIM in the frontmatter description":
            STORY in desc,
        "the plain-words story appears VERBATIM in the body's overview":
            STORY.lower() in low,

        # -- a SHORT, plain condition is the default shape --
        "condition default is ONE short, plain sentence of ~120-150 characters":
            "one short, plain sentence" in low and "120–150 characters" in low,
        "the 4,000-char limit is framed as a ceiling, not a target":
            "ceiling, not a target" in low,
        "ships the canonical short worked-example condition, byte-identical":
            CANON in body,
        "the four teeth (brief path, quoted evidence, sentinel, turn bound) are MANDATORY":
            "four teeth, all mandatory" in low,
        "lint enforces the short read AND all four teeth":
            "reads in one breath" in low and "all four teeth present" in low,
        "heavy process directives belong in the brief, not in the condition":
            "belongs in the brief" in low,

        # -- the handoff is /clear + ONE short inline /goal line, nothing else --
        "handoff is /clear then ONE short /goal line with the condition inline":
            "/clear, then one short /goal <condition> line" in low,
        "handoff forbids a file launcher and a wrapper script":
            "no file launcher" in low and "no wrapper script" in low,
        "handoff never leaves the user holding only a path":
            "never be left holding only a path" in low,

        # -- the brief the skill AUTHORS must demand an ADHD-friendly report --
        "template: final report is short bullets under Done / Proof / Next":
            "done / proof / next" in tmpl_low and "short bullets" in tmpl_low,
        "template: final report bans long paragraphs":
            "no long paragraphs" in tmpl_low,
        "template: final report states a stopped run is NOT proof of completion":
            "not proof of completion" in tmpl_low,

        # -- the brief the skill AUTHORS must demand live, visible progress --
        "template: mandates live visible progress via the task tracker (TaskCreate)":
            "live visible progress" in tmpl_low and "taskcreate" in tmpl_low
            and "one task per phase" in tmpl_low,
        "template: tasks flip in_progress -> completed, not batched at the end":
            "in_progress → completed" in tmpl_low and "batch at the end" in tmpl_low,
        "template: the brief's own progress checklist is the resume state":
            "progress checklist" in tmpl_low and "resume state" in tmpl_low,
        "template: closeout turn reruns every check together and quotes fresh output":
            "closeout turn" in tmpl_low and "rerun every" in tmpl_low
            and "freshly quoted" in tmpl_low,

        # -- PREPARE itself obeys the same two rules --
        "PREPARE creates visible tasks for its own steps":
            "create one task per step" in low,
        "PREPARE NEVER prints the handoff while a subagent or background task is live":
            "never print the handoff while anything is still running" in low,
        "PREPARE reads every subagent's file deliverable from disk before handing off":
            "read its file deliverable from disk" in low,

        # -- vocabulary lock: a brief is a file, a condition is a string, nothing else --
        "vocabulary lock: the brief is a FILE and the condition is a STRING":
            "the brief — a file" in low and "the condition — a string" in low,
        # The banned bigram is not spelled out in this label on purpose: the repo-wide
        # vocabulary scan in tests/test_manifests.py greps every tracked file for it, and a
        # test that names it would flag itself.
        "vocabulary lock: the blurred file-plus-goal phrasing never appears in the skill":
            not re.search(r"goal[-\s]+file", low),
    }
    for clause, ok in v23_clauses.items():
        checks.append((f"v2.3: {clause}", ok, ""))

    # --- v2.6 CONTRACT: a capped run wraps up instead of dying mid-edit ---
    # A turn cap used to be a cliff: the brief gave a bound and said nothing about approaching it,
    # so a run could stop with half an edit on disk and a report that never mentioned the cap.
    #
    # The turn-bound assertion is scoped to the four-teeth block on purpose. `low` already carries
    # "stopping rule, not a completion rule" under Honest limits, a hundred lines away, so a
    # body-wide check for that phrase is GREEN before this change and proves nothing.
    teeth_m = re.search(r"four teeth, all mandatory(.*?)###", low, re.DOTALL)
    teeth = teeth_m.group(1) if teeth_m else ""
    v26_clauses = {
        "template: the brief tells the run to wrap up as it nears the turn cap":
            "near the turn cap" in tmpl_low and "stop starting new work" in tmpl_low,
        "template: the wrap-up commits what is green and says the run stopped early":
            "commit everything that is green" in tmpl_low and "stopped early at the cap" in tmpl_low,
        "template: wrapping up at the cap still does NOT archive the brief":
            "still refuses to archive" in tmpl_low,
        "the turn-bound tooth itself says a cap is a stopping rule, not a completion rule":
            "stopping rule, not a completion rule" in teeth,
    }
    for clause, ok in v26_clauses.items():
        checks.append((f"v2.6: {clause}", ok, ""))

    # --- Gated, low-freedom end-of-run gate: archive since v2.0.0 (claim 4) ---
    checks.append(("end-of-run gate is a LOW-FREEDOM gated block",
                   "low freedom" in low and "pre-condition" in low and "do not modify" in low, ""))
    checks.append(("end-of-run gate has rationalization counters",
                   "rationalization" in low and "basically done" in low, ""))
    checks.append(("end-of-run gate keeps the file if criteria fail (resume)",
                   "resume" in low and ("do not delete" in low or "leave the file" in low), ""))

    # --- Loophole-close: never run /clear or /goal itself (research 01 §4.8) ---
    checks.append(("hard rule: never run /clear or /goal itself",
                   "never run `/clear` or `/goal` yourself" in body or
                   ("never run /clear or /goal" in low), ""))

    # --- Progressive disclosure (body < 500 lines) ---
    checks.append(("SKILL.md body < 500 lines", body.count("\n") < 500, f"{body.count(chr(10))} lines"))

    # --- Report ---
    failed = [c for c in checks if not c[1]]
    for nm, ok, detail in checks:
        tag = "PASS" if ok else "FAIL"
        extra = f"  ({detail})" if detail and not ok else ""
        print(f"{tag}: {nm}{extra}")
    print("-" * 60)
    print(f"{len(checks) - len(failed)}/{len(checks)} checks passed for {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
