# AGENTS.md — goalify

Instructions for AI agents and coding assistants working in or invoking this repository. Plain
Markdown, no required fields (per the AGENTS.md convention: the agent parses the text below).
Human-facing docs live in `README.md`; this file holds the extra context an agent needs.

## What this repo is

This repo is a Claude Code / Agent Skills skill, `goalify`, that **prepares a self-contained,
self-deleting `/goal` execution file**. In one session it researches the task, asks the user only the
genuine decisions (one interactive MCQ batch), scopes the work, and authors a single Markdown file with
hard rules baked in. The user then runs `/clear` and `/goal <abs-path>` so a **fresh** session executes
the big task at full context and deletes the file when done.

The skill definition is `skills/goalify/SKILL.md`. There are no scripts to run; the skill's whole
output is the goal file it authors.

## How an agent should invoke / honor the skill

- If running inside Claude Code with the skill installed: trigger it by describing the user's intent —
  "goalify this: <task>", "prep a goal", "make the md for /goal", "set up an autonomous run to launch
  later". Claude Code matches these to the skill's `description` and loads `SKILL.md`.
- Install as a plugin: `/plugin marketplace add Aboudjem/goalify` then `/plugin install goalify@goalify`.
- Install as a drop-in skill: copy `skills/goalify/` into `~/.claude/skills/goalify/`.
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
5. **The self-destruct is gated and low-freedom.** The generated file deletes itself only after every
   success criterion is met and verification passed; otherwise it stays so the run can resume. Do not
   modify the `rm` command or weaken the gate.
6. **Don't over-ask.** One MCQ batch, only genuine forks. Skip it entirely if there are none.
7. **Decline when a `/goal` file is the wrong tool** — a trivial task (just do it) or open-ended
   exploration (no definable end state). A vague spec produces a meh autonomous run.

Additional hygiene for agents editing this repo: never commit secrets or tokens. Keep the SVGs in
`assets/` GitHub-safe (no `<script>`, no external references). Don't invent facts; cite a primary
source for any load-bearing claim, especially "works with X" / standard-compliance claims.

## Where things live

- `skills/goalify/SKILL.md` — the skill: two-phase model, procedure, the goal-MD template, the
  one-vs-several decision, the handoff format, hard rules, common mistakes.
- `evals/` — `check_skill.py` (deterministic, in CI), `scenarios.md` (behavioral), `RED-baseline.md`
  (recorded RED→GREEN on Haiku/Sonnet/Opus).
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — plugin + marketplace manifests
  (GitHub self-source).
- `examples/` — a worked, redacted example of a goal file goalify produced.
- `assets/` — the animated SVG hero and "how it works" diagram, plus the social-preview card.
- `docs/` — quickstart and the build audit trail.
- `README.md` — human-facing overview; `LICENSE` — MIT.

## Validate before claiming done

- `python3 evals/check_skill.py skills/goalify/SKILL.md` exits 0 (25/25).
- `SKILL.md` frontmatter parses (valid YAML: `name`, `description`, `license`, `metadata.version`).
- `.claude-plugin/plugin.json` and `marketplace.json` are valid JSON and name the repo `Aboudjem/goalify`.
- `assets/*.svg` contain no `<script>` and no external references, and are well-formed XML.
- All relative Markdown links resolve.

## Q&A

**How do I set up a big autonomous Claude Code run?**
Install goalify, then say "goalify this: <your big task>". It researches, asks you the few real
decisions, and writes one self-contained `/goal` file to an absolute path. It then prints `/clear` and
`/goal <path>` — you run those two, and a fresh full-context session executes the task and deletes the
file when every success criterion is met.

**Does it run the task itself?**
No. goalify only prepares the handoff file. You run it (after `/clear`) in a fresh session.

**Why does the file delete itself?**
To kill spec-drift and clutter: it is single-use. It deletes itself only on full success; if criteria
fail it stays in place so the run can resume.

**Does it work outside Claude Code?**
It is a spec-correct Agent Skill (`name` + `description` frontmatter + Markdown). The Agent Skills open
standard is portable across agents that support it; the `/clear` + `/goal` handoff phrasing is
Claude-Code-specific, so adapt the two handoff commands to your agent.
