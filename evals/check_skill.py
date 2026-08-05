#!/usr/bin/env python3
"""
goalify skill eval — machine-checkable static assertions.

This is the deterministic half of the eval suite (the behavioral scenarios live in
`scenarios.md` and are run against Haiku/Sonnet/Opus). It encodes the CONFIRMED
research edits as pass/fail checks so a regression is caught in CI.

It doubles as the RED→GREEN demonstration, reproducible from this repo's own history:
point it at `git show v1.1.0:skills/goalify/SKILL.md` and it FAILS (RED, 29/52); point it
at the current `goalify` SKILL.md and it PASSES (GREEN, 52/52).

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
        "handoff does NOT make pbcopy the required step":
            "never the required step" in low and "pbcopy < <paste>" not in low,
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
