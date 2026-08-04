---
name: goalify
description: >-
  Set up a big coding task to run on its own after `/clear`: goalify scopes the
  work here, locks the few real decisions, writes a self-contained
  implementation brief, and derives the `/goal` completion condition that makes
  a fresh session prove it finished — because `/goal` takes a condition string,
  never a file path. Use when the user says "goalify", "goalify this", "goalify
  <task>", "/goalify <task>", "prep a goal", "prepare a goal file", "make an md
  for /goal", "set up an autonomous run to launch later", or wants a Codex
  `/goal` objective. This skill AUTHORS the handoff now; it does NOT execute the
  work in this session. For a task to be done immediately here, use autopilot,
  ultrawork, or ralph instead, not goalify.
argument-hint: "[task to prepare a /goal run for]"
license: MIT
metadata:
  version: 2.0.0
---

# goalify

## Overview

Prepare the best possible autonomous run in THIS session, then hand off so the user can `/clear` and
launch it in a fresh session that has full context to work in.

**goalify produces TWO artifacts, not one:**

1. **The brief** — a self-contained implementation Markdown file at an absolute path under `.goal/`.
   It is the source of truth for the **worker** (the fresh session doing the job).
2. **The condition** — a plain-text completion condition, ≤ 4,000 characters, *derived from* the
   brief's success criteria. It is the source of truth for the **evaluator** (the Stop hook that
   decides "is this done?"). This is what the user actually passes to `/goal`.

> **The v2 correction — v1 of this skill got this wrong.** `/goal` takes a **condition string, never a
> file path**. Hand it a path and that literal path string *becomes* the condition. The evaluator has
> no file access, so every turn it is asked whether "`/Users/me/.goal/task.md`" is satisfied — and it
> never resolves, resolves arbitrarily, or gives up and reports success. The gate looks like it works
> because the *first* turn reads the path and starts working. Never put a path where a condition goes.

**Core principle — two phases, never mix them:**

- **PREPARE (here, now):** understand the project, scope the work, verify the facts, lock the genuine
  decisions with one interactive question batch, then author the brief **and** derive the condition.
  Keep your own chat output short.
- **EXECUTE (later, after `/clear`):** the user pastes the condition into `/goal`; that fresh session
  reads the brief, does the heavy work, and must prove completion in its own transcript.

You are doing the PREPARE phase. Do **not** start the heavy implementation here.

## Invocation

Triggered by natural language ("goalify this: &lt;task&gt;") or as the slash command `/goalify <task>`.
When invoked as a command, **`$ARGUMENTS`** is the task to prepare a run for — treat it as the objective
and begin PREPARE. If no task is given, infer it from the recent conversation, or ask once (one line).

## When to use / not

- **Use when:** a substantial, well-specified task should run autonomously in a clean session.
- **Don't use for:** a tiny task you can just do now; answering a question; or work the user wants done
  immediately in THIS session (use autopilot / ultrawork / ralph).
- **Declarative-vs-exploration gate.** A `/goal` run needs a definable end state and a way to test it.
  If the request is open-ended exploration ("poke around and see what's interesting"), do NOT produce a
  run — say so and offer to explore interactively instead. A vague spec produces a meh autonomous run.

## How `/goal` actually works (verify before you contradict this)

Sourced from https://code.claude.com/docs/en/goal and from the shipped Claude Code binary. These
constraints are why the condition is shaped the way it is — do not "simplify" them away.

1. **Condition, not path.** Docs: *"Run `/goal` followed by the condition you want satisfied."* Binary:
   `No goal set. Usage: /goal <condition>`. There is no file-path branch.
2. **≤ 4,000 characters.** Docs: *"The condition can be up to 4,000 characters."* Binary:
   `Goal condition is limited to <N> characters`. Assert this before printing the handoff.
3. **The evaluator has no tools and cannot read files.** Docs: *"It doesn't run commands or read files
   independently, so write the condition as something Claude's own output can demonstrate."* It judges
   the transcript only. A ticked checkbox in a Markdown file is invisible to it.
4. **It must quote its evidence** and is instructed to answer "insufficient evidence in transcript"
   when it cannot. Unquotable evidence blocks the run forever.
5. **The transcript it sees is TRUNCATED once the session is long.** Above ~50% of the evaluator
   model's context budget (25% on a prompt-too-long retry) older messages are dropped and replaced by a
   notice telling it to refuse when the evidence may sit in the omitted prefix. Below that budget it
   sees everything. On a long autonomous run — goalify's whole use case — assume **evidence proven on
   turn 3 is invisible on turn 90.** Undocumented; binary-only. This is why the closeout turn exists.
6. **The evaluator can end the run early by judging the condition unachievable.** The hook outcome is
   literally named `success`, so nothing blocks and the loop stops — but the goal is recorded
   `met:false, failed:true`: failed, not achieved. Net effect, the run can stop with the work unfinished.
   No wording suppresses this, so goalify documents it rather than pretending otherwise (Honest limits).
7. **Bounding lives inside the condition.** The docs endorse phrasing like *"or stop after 20 turns"*.
8. **`/goal` does not change your permission mode** — whatever is in effect stays in effect. Auto mode
   is the default in current Claude Code, so an unattended run usually needs nothing extra; if you have
   changed it, pair `/goal` with auto mode (`--permission-mode auto`, settings `defaultMode`, or
   `/permissions`).
9. **`$` interpolation hazard.** The hook prompt passes through a substitution for `$ARGUMENTS` and
   `$<digit>`. A condition containing a bare `$` sequence can be rewritten under you. Lint it out.
10. **Requires Claude Code 2.1.139+**, a trusted workspace, and hooks enabled. An active goal survives
    `--resume` / `--continue`; `/clear` kills it.

## Procedure (the PREPARE phase)

Work autonomously; only stop for the question batch. Track phases with the task tracker if one is
available (`TaskCreate`/`TaskUpdate`, or your environment's equivalent); write artifacts to disk.

1. **Understand the project & objective.** Inspect the working dir with evidence (`git status`,
   `git log`, README, key files, any RESUME/INDEX/memory). State the real objective in one line. If
   something important is implied but unstated, cover it.
2. **Scope the remaining work.** List the concrete deliverables and crisp success criteria. Don't ask
   the user what you can determine yourself.
3. **Fan out research (parallel, where independent).** Use whatever parallel-subagent capability the
   environment provides — a workflow-orchestration tool, or an Agent/Task dispatch tool; **if none is
   available, run the searches sequentially.** Cover: official docs for the domain; community intel
   (Reddit, X, HN, forums) for the gotchas most projects miss; comparable tools; packaging if shipping.
   Give each subagent an objective, an output format, its sources, and clear boundaries. **Reuse
   existing on-disk research first** (`~/.claude/skills/`, prior `docs/research/`, project memory).
   Every subagent cites sources and labels uncertainty; a separate skeptic re-derives load-bearing
   claims from primaries, never from another subagent's summary.
4. **Route models deliberately.** Use a fast model for mechanical breadth — file sweeps, link checks,
   inventory, drift detection — and a deep model for architecture, the brief's design, the condition
   wording, and every skeptic pass. Say which model each subagent used when you report.
5. **Ask only genuine decisions (one interactive batch).** Use the interactive question tool (e.g.
   `AskUserQuestion`), ≤ 4 questions, each a real fork that changes the artifacts (scope, structure,
   risk/approval bar, release authority). Mark a recommended option. Skip entirely if there are none.
6. **Author the brief** from the template below, filled with verified research, the answers, the scoped
   phases, and explicit machine-checkable success criteria.
7. **Derive the condition** from the brief's success criteria (see The condition), and **lint it**.
8. **Save the brief to an absolute path** under `.goal/` in the project (create the dir; if the repo has
   a `.gitignore`, **idempotently append** `.goal/` to it — grep first, append only if absent), or
   `~/.claude/goalify/` if not in a project. Name it `<slug>-<stamp>.md`. Write the condition next to it
   as `.goal/CONDITION-<slug>.txt` so the user can `pbcopy` it instead of hand-copying 4,000 characters.
9. **Hand off (short).** Print the bullet summary, the caps, and the three steps (see Handoff format).

### Dry run and caps

Before writing anything, print the plan as numbers the user can veto: **phase count · subagent count ·
turn cap · budget cap**. If the user asked for a dry run (`/goalify --dry-run <task>`, or "just show me
the plan"), print the plan, the success criteria, and the derived condition — and write no files.

Never predict a dollar or token *cost*: there is no citable basis for it, and inventing one violates the
no-hallucination rule. Caps are the honest control. Put the turn cap in the condition itself.

## The brief template (fill every section; tight, self-contained, absolute paths)

The brief has two halves that must stay visibly separate, because they do not travel equally well
(see Cross-harness): the **definition of done**, which is portable, and the **process directives**,
which bind reliably only in Claude Code.

```markdown
# GOAL: <objective in one line>

> Self-contained implementation brief. Authored <date> by goalify. Runs in a fresh session.
> This file's own path: <ABSOLUTE PATH>   ← archived, not deleted, on success (see Archive gate).
> Re-read THIS file at the start of every work loop; it is the source of truth, not the conversation.
> **This file is the brief, not the stop condition.** The condition is a separate string (see Handoff).

## GOAL (the autonomous directive)
<Declarative: the desired END STATE and how it is verified, not a brittle recipe. Where (ABSOLUTE
paths). That it runs at MAXIMUM EFFORT — fan out parallel subagents for independent discovery and
verification but serialize builds, tests, same-file writes and every git operation; correctness and
completeness over speed or token cost; use the environment's max-effort mode (e.g. ultracode /
ultrawork) if there is one — verifies with a SEPARATE agent, checks official docs when in doubt, tests
what it can, and does not stop until every success criterion holds.>

## Context (verified — re-confirm live; don't trust this summary)
<What the project is, current state with evidence, why this work. Research summarized WITH sources.
Carry lightweight, just-in-time identifiers — ABSOLUTE paths, queries, URLs — NOT pasted dumps.>

## Decisions (locked by the user — do not re-litigate)
<The answers from the question batch, and any locked constraints.>

## Phases
1. Re-verify the current state live (do not trust this file's summary).
2. <domain phases…>
N. Final verification + report.
<Per phase: what to do; what fans out in parallel (independent discovery/verification) vs what must
serialize (builds, tests, same-file writes, git, anything destructive); each subagent's objective,
output format and boundaries; which artifacts get written to disk. Right-size each phase.>

## Process directives (Claude Code; see Cross-harness for what survives elsewhere)
- **Maximum effort.** Fan out parallel subagents for ALL independent discovery and verification.
  "Good enough" is not done.
- **Subagent barrier.** Never write a deliverable, tick a criterion, or end a turn while any spawned
  subagent or background task is still live. Wait for each to return, read its artifact from disk, and
  confirm the artifact exists. An "idle" or "available" ping is NOT a delivered result.
- **No hallucination.** Never state a fact, number, version, flag or API you have not verified against
  a primary source; cite it; label uncertainty (confirmed · likely · uncertain · blocked ·
  needs-approval). Trust `--help` and binaries over doc-site summaries.
- **Multi-agent verification.** Nothing ships without a separate agent re-deriving load-bearing claims
  from primaries, not from another agent's summary. Never self-approve.
- **Full implementations only.** No placeholder, stub, or "simplified" version to make something pass.
- **Search before assuming missing.** grep yields false negatives; search before concluding something
  doesn't exist, and don't duplicate what's already there.
- **Redirect noisy output.** `cmd > /tmp/<name>.log 2>&1`, then `tail` — never flood the context.
- **Test when possible.** Re-test after every fix. Nothing is done untested.
- **Commit before risky steps** (if in a repo); `git reset --hard` + re-run is valid recovery.
- **Safety/approval.** Implement safe, evidence-backed changes autonomously. Pause for destructive,
  irreversible or outward-facing actions (history rewrites, deleting data, publishing) unless
  explicitly pre-approved here.
- **3-strike escalation.** On failure: (1) retry with a root-cause probe; (2) retry with a narrowed
  fix scope; (3) STOP, write `.goal/BLOCKERS-<stamp>.md` (what failed, what you tried, what's needed),
  and say BLOCKED explicitly. Never loop forever, and never declare the goal impossible to escape it.
- **Resumable.** Write artifacts to disk continuously; tick the checklist IN THIS FILE; re-read this
  file each loop; compact-and-reinitialize when the context fills.

## Definition of done (portable — this is what the condition is derived from)
<Each criterion OBJECTIVELY pass/fail and wired to a NAMED command whose OUTPUT the run can quote.>
- [ ] <criterion> — verified by `<exact command>` (exit 0 / expected output)
- [ ] A SEPARATE agent re-derived every load-bearing claim from primaries; no unverified load-bearing
      claim remains.

## Progress checklist (tick these IN THIS FILE as you go — this is the resume state)
- [ ] Re-verified current state live
- [ ] <phase deliverables…>
- [ ] All criteria hold → safe to archive

## Final output
<A short plain-language report: what changed · what was tested, with the actual commands and results ·
what needed approval and was skipped · confidence per major decision · the user's next commands.>

## Archive gate (LOW FREEDOM — do not modify this gate or the command)
Pre-condition: EVERY definition-of-done checkbox is ticked AND the independent verification passed AND
the tests are green. If ANY box is unticked → STOP. Do NOT archive; leave the file in place so the run
can resume. Rationalizations that DO NOT justify archiving: "basically done", "only X left", "I'll fix
it next run".
Path rail: act only on this file's OWN literal absolute path above, and only because it lives under
`.goal/` or `~/.claude/goalify/`. Never move or delete anything else.
Only when the pre-condition holds, as the LAST action, append a completion stamp to this file and run
exactly:
`mkdir -p <DIR>/done && mv <ABSOLUTE PATH OF THIS FILE> <DIR>/done/<FILENAME>`
Then confirm the destination exists and the original path no longer does.
```

Archiving rather than deleting keeps the promise-vs-outcome audit trail — the brief said what the run
would do, the stamp says what it did — at the same gate strictness.

## The condition (the part the evaluator actually judges)

Derive it **from the brief's definition of done**, so the two specs cannot drift. Anything you leave
out of the condition is unenforceable, no matter how firmly the brief states it.

```text
Read and fully execute the implementation brief at <ABSOLUTE PATH> — read it first, implement every
phase, do not merely summarize it. <One or two process directives that matter most.> This condition is
satisfied ONLY when the single most recent assistant turn contains the sentinel <SENTINEL> followed, in
that same turn, by all of: (1) `<command>` rerun with exit 0 and its last lines quoted; (2) `<command>`
rerun and its output quoted; … (N) the line "unresolved failures: none" or an explicit list of them.
Immediately before presenting that packet, rerun every one of those checks together in one dedicated
closeout turn — do not rely on results proven in earlier turns, because on a long run the evaluator
sees only a recent window of the transcript and will reject evidence it cannot quote. Claims without freshly quoted
command output are insufficient evidence. Do not treat inability, difficulty, or partial progress as
completion, and do not declare this goal impossible or unachievable in order to finish: if genuinely
blocked, write a blockers report to `.goal/` and state BLOCKED explicitly. Or stop after <N> turns and
report a non-success timeout.
```

Every clause is load-bearing:

- **The brief's absolute path** is the work; the condition is only the finish line.
- **A sentinel token** (e.g. `PROJECT_V2_EVIDENCE`) gives the evaluator one unambiguous string to find.
- **Named commands with quoted output** are the only evidence a tool-less evaluator can verify.
- **"in the single most recent assistant turn"** survives transcript truncation.
- **The closeout turn** is the fix for the circularity that "re-state the evidence at the end" has: a
  run cannot know which turn is its last, but it *can* be told to re-run everything together right
  before presenting the packet, so raw output lands at the transcript tail.
- **"Claims without freshly quoted command output are insufficient"** blocks a confident summary from
  passing as proof.
- **The anti-impossible clause** is aimed at the worker, and is best-effort only (see Honest limits).
- **The turn bound** keeps the loop finite and yours.

### Condition lint (run every check before printing the handoff)

- [ ] ≤ 4,000 characters — count it, don't estimate.
- [ ] Contains no bare `$` sequence (hook-substitution hazard). Escape or reword.
- [ ] Names at least one runnable command whose output can be quoted.
- [ ] Contains the sentinel, the closeout-turn clause, and an explicit turn bound.
- [ ] Contains no phrase that the condition text itself would satisfy — never make "the assistant said
      it is done" the success test.
- [ ] Every command in it appears in the brief's definition of done, and vice versa.

## Handoff format (what you print — short, bullets, not verbose)

```
Prepared the run. Here's what it will do:
- <bullet> <bullet> <bullet>   (high level, plain language)
Decisions you set: <one line, if any>
Plan: <N> phases · <N> subagents · turn cap <N>
Brief:     <ABSOLUTE PATH>
Condition: <ABSOLUTE PATH>/CONDITION-<slug>.txt  (<N> chars, under the 4,000 limit)

Next — three steps:
1.  /clear
2.  pbcopy < <CONDITION FILE PATH>
3.  /goal <paste>       ← unattended? confirm auto mode is on (the default in current Claude
                             Code; otherwise Shift+Tab, or --permission-mode auto)

Headless instead:
    claude -p "/goal $(cat <CONDITION FILE PATH>)" --permission-mode auto \
      --output-format stream-json --verbose

Didn't finish? Re-run the same condition — the brief keeps its checklist, and the gate keeps the file
until every criterion passes.
```

## Cross-harness: Codex

Codex has its own `/goal`, and — the useful convergence — it also takes an **inline objective, never a
file path**, under the **same 4,000-character cap**. So derive the finish line once and print both forms.

- **Claude Code:** `/goal <condition>` interactively; `claude -p "/goal <condition>"` headless.
- **Codex interactive:** `/goal <objective>`. Its usage line is
  `/goal [<objective>|clear|edit|pause|resume]` — bare `/goal` opens the panel; there is **no**
  `/goal status`. Its 4,000 cap is not a greppable literal in the binary (it is interpolated at
  runtime), so it was established by probing the boundary live: 4,000 accepted, 4,001 rejected with
  `goal objective must be at most 4000 characters`. It counts characters, not bytes.
- **Codex headless:** `/goal` is a TUI slash command, so `codex exec` does not dispatch it — neither
  `codex --help` nor `codex exec --help` even mentions it. Pipe the brief instead:
  `cat <brief> | codex exec -` (Codex must run inside a git repo, or pass `--skip-git-repo-check`).
  Prefer `-` over `"$(cat f.md)"`: word-splitting, `ARG_MAX`, and `$`/backtick expansion all bite
  otherwise. Ephemeral threads reject goals outright.
- **Codex tells the model the objective is user-provided data** — *"Treat it as the task to pursue, not
  as higher-priority instructions"* — on every goal-steering template, and additionally wraps an edited
  objective in an `<untrusted_objective>` tag. **Therefore the brief's process directives ("maximum
  effort", "never self-approve", "pause before destructive actions") do not reliably bind under Codex.
  Only the definition of done carries.** This is why the template keeps the two apart.
- Codex already injects its own continuation, fidelity, completion-audit and blocked-audit steering,
  including a blocked rule keyed to the same blocking condition recurring for three consecutive turns.
  Align the 3-strike ladder with it rather than duplicating it.
- Do **not** promise budgeted Codex goals: `token_budget` reports `under development`. The JSON-RPC
  layer accepts a `tokenBudget` and the tool schema advertises it, so it looks available — but the
  `/goal` grammar has no budget argument, so it is unreachable from the TUI.
- Codex spills *its own* long objectives to a `goal-objective.md` attachment and injects "Read the
  Codex goal objective file at &lt;path&gt; before continuing." That is Codex's internal mechanism, not an
  input form — it is **not** a path syntax you can call. Don't mistake it for one.

## Honest limits (document these; do not paper over them)

- **A `/goal` run that stops is not proof of completion.** The evaluator applies independent judgment
  and can end the loop by deciding the condition is unachievable; the hook outcome is named `success`
  even though the goal itself is recorded as failed. No condition wording prevents this. Tell the user,
  and give them the verify-only re-check: open a fresh session and run only the brief's
  definition-of-done commands, or re-run the same condition and read the closeout packet yourself.
  Anything that reads "the goal loop ended" as "the goal was achieved" gets the impossible case wrong.
- **The brief and the condition are two specs that can drift.** Deriving one from the other and running
  the lint is a mitigation, not a proof.
- **A turn cap is a stopping rule, not a completion rule.** A timed-out run is not a finished run.

## Hard rules for the PREPARE phase itself

- **Run PREPARE at maximum effort too.** Fan out research broadly in parallel, re-derive load-bearing
  claims with a separate skeptic, and don't settle for a shallow scan — the quality of the run is
  capped by the quality of these two artifacts. Use a max-effort mode (ultracode / ultrawork) if there
  is one.
- **Subagent barrier applies here too.** Do not author the brief, print the handoff, or end your turn
  while a research subagent is still running. An availability ping is not a result.
- **No hallucination here either.** Verify the project state with evidence before scoping.
- **Don't over-ask.** One question batch, only genuine forks. If none, don't ask.
- **Keep YOUR output short.** The artifacts carry the detail; the user is about to `/clear`.
- **Absolute paths everywhere.** The fresh session is a stranger to this one.
- **Never run `/clear` or `/goal` yourself** — print them for the user. They are the user's manual
  steps; a "helpful" attempt to run them defeats the fresh-context handoff.

## Common mistakes

- **Handing `/goal` a file path.** The single defect v2 exists to fix. The path names the brief; the
  condition is what the user actually types.
- Restating the whole brief inside the 4,000 characters. Spend them on the acceptance protocol.
- Success criteria the evaluator cannot see — a ticked checkbox in a file, a passing test nobody quoted.
- Proving everything early and presenting nothing at the end: on a long run truncation hides it.
  That is what the closeout turn is for.
- Starting the heavy implementation during PREPARE.
- A vague brief with no checkable criteria → the run never knows when it is done.
- Weakening the archive gate, or archiving when criteria failed (it must survive to resume).
- Pasting big dumps into the brief instead of just-in-time identifiers loaded when needed.

## Reuse

Before researching from scratch, pull from `~/.claude/skills/`, prior `docs/research/` notes, project
memory, and finished reference repos. Fold what's reusable into the brief with its source; research only
the genuinely new parts.
