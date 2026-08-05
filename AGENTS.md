# AGENTS.md — goalify

Instructions for AI agents and coding assistants working in or invoking this repository. Plain
Markdown, no required fields (per the AGENTS.md convention: the agent parses the text below).
Human-facing docs live in `README.md`; this file holds the extra context an agent needs.

## What this repo is

This repo is `goalify`, a Claude Code / Agent Skills skill that **turns a big coding task into a
self-contained implementation brief plus the `/goal` completion condition derived from it**. In one session it researches the task, locks the few real decisions
(asking the user only the genuine forks, one interactive MCQ batch), and authors **two** artifacts: a
self-contained implementation **brief** at an absolute path, and the **condition string** derived from
that brief's definition of done. The user then runs `/clear` and pastes the condition into `/goal`, so a
**fresh** session executes the big task at full context, proves every criterion in a closeout turn, and
archives the brief on success.

The repo is the skill at `skills/goalify/SKILL.md`, the `/goalify` author. There is no script to run;
the skill's output is the brief plus the condition. **`/goal` takes a condition string, never a file
path** — the docs say *"Run `/goal` followed by the condition you want satisfied"* and the shipped
binary contains `No goal set. Usage: /goal <condition>` with no file-path branch. The evaluator behind
`/goal` has no tools and cannot read files, so a path handed to it can never be verified
(Claude Code 2.1.139+, https://code.claude.com/docs/en/goal).

## How an agent should invoke / honor the skill

- If running inside Claude Code with the skill installed: trigger it by describing the user's intent,
  e.g. "goalify this: <task>", "prep a goal", "make the brief for /goal", "set up an autonomous run to
  launch later". Claude Code matches these to the skill's `description` and loads `SKILL.md`.
- Install: the plugin (`claude plugin marketplace add Aboudjem/10x` then `claude plugin install goalify@10x`), or drop in manually: `git clone https://github.com/Aboudjem/goalify`, then copy `skills/goalify` into `~/.claude/skills/`. The runner is Claude Code's built-in `/goal`; goalify does not ship its own.
- **This skill AUTHORS a handoff file; it does not execute the task.** If the user wants the work done
  immediately in the current session, that is `autopilot` / `ultrawork` / `ralph`, not goalify.

## Rules an agent MUST honor (they mirror the skill)

These are non-negotiable. Do not look for loopholes; violating the letter violates the spirit.

1. **Two phases, never mixed.** In PREPARE you research, decide, and author the file — you do NOT start
   the implementation. Execution happens later in the fresh `/goal` session.
2. **No hallucination.** Verify project state with evidence before scoping. Research subagents cite
   sources and label uncertainty; a separate skeptic re-derives load-bearing claims from primaries, not
   from another agent's summary.
3. **Never run `/clear` or `/goal` yourself.** Print them for the user — they are the user's two manual
   steps. Running them defeats the fresh-context handoff.
4. **The generated file is self-contained and absolute-path'd.** The fresh session is a stranger to this
   one; relative paths and "see above" do not survive `/clear`.
5. **The archive gate is gated and low-freedom.** The brief moves to `.goal/done/` with a completion
   stamp only after every criterion is met and verification passed; otherwise it stays in place so the
   run can resume. Do not modify the `mv` command or weaken the gate.
5b. **Never emit a file path where a condition belongs.** The handoff is `/clear` → copy the condition
   printed inline as a complete `/goal` line. Anything omitted from the condition is unenforceable,
   brief's definition of done and lint it (≤ 4,000 chars, no bare `$`, a sentinel, a named command per
   criterion, a closeout-turn requirement, an explicit turn bound).
6. **Don't over-ask.** One MCQ batch, only genuine forks. Skip it entirely if there are none.
7. **Decline when an autonomous run is the wrong tool** — a trivial task (just do it) or open-ended
   exploration (no definable end state). A vague spec produces a meh autonomous run.

Additional hygiene for agents editing this repo: never commit secrets or tokens. Keep the SVGs in
`assets/` GitHub-safe (no `<script>`, no external references). Don't invent facts; cite a primary
source for any load-bearing claim, especially "works with X" / standard-compliance claims.

## Where things live

- `skills/goalify/SKILL.md` — the skill: two-phase model, procedure, the goal-MD template, the
  one-vs-several decision, the handoff format, hard rules, common mistakes.
- `evals/` — `check_skill.py` (deterministic, in CI), `scenarios.md` (behavioral), `RED-baseline.md`
  (recorded RED→GREEN on Haiku/Sonnet/Opus).
- `examples/` — an illustrative brief plus the `/goal` condition derived from it.
- `tests/` — `test_manifests.py`: manifest validity, version consistency across all four sources, the
  "no file path to `/goal`" contract, and the shipped example's template clauses. A release gate.
- `video/` — Remotion source for the README teaser; typechecked in CI, and every relative import must
  be tracked by git.
- `assets/` — the animated SVG hero and "how it works" diagram, plus the social-preview card.
- `docs/` — the quickstart. (A local build journal lives in `docs/audit/`, which `.gitignore` excludes.)
- `README.md` — human-facing overview; `LICENSE` — MIT.

## Validate before claiming done

- `python3 evals/check_skill.py skills/goalify/SKILL.md` exits 0 (all checks pass).
- `python3 tests/test_manifests.py` exits 0 (plugin + marketplace manifests valid).
- `SKILL.md` frontmatter parses (valid YAML: `name`, `description`, `license`, `metadata.version`).
- `assets/*.svg` contain no `<script>` and no external references, and are well-formed XML.
- All relative Markdown links resolve.

## Q&A

**How do I set up a big autonomous Claude Code run?**
Install goalify, then say "goalify this: <your big task>". It researches, asks you the few real
decisions, writes one self-contained brief to an absolute path, and derives the completion condition
from it. It then prints three steps — `/clear`, copy the condition, paste it into `/goal` — and a fresh
full-context session executes the task and proves every criterion before it stops.

**Does it run the task itself?**
No. goalify only prepares the handoff file. You run it (after `/clear`) in a fresh session.

**Why does the brief archive itself?**
To kill spec-drift and clutter: it is single-use. On full success it moves to `.goal/done/` with a
completion stamp, so the promise and the outcome can be compared afterwards; if criteria fail it stays
in place so the run can resume.

**Is a stopped `/goal` run proof the work is done?**
No. The evaluator applies independent judgment and can end a run by deciding the condition is
unachievable; the hook outcome is literally named `success` even though the goal is recorded as failed.
Re-run the brief's definition-of-done commands, or read the run's closeout evidence packet, before
believing a green result.

**Does it work outside Claude Code?**
It is a spec-correct Agent Skill (`name` + `description` frontmatter + Markdown). The Agent Skills open
standard is portable across agents that support it; the `/clear` + `/goal` handoff phrasing is
Claude-Code-specific, so adapt the two handoff commands to your agent.
