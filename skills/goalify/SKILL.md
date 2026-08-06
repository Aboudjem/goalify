---
name: goalify
description: >-
  You describe a big coding job. goalify writes the instructions the AI works
  from, and the finish line it has to prove it reached. The instructions are a
  brief (a file); the finish line is a condition (a short string you paste into
  `/goal`), because `/goal` takes a condition string, never a file path. Use when
  the user says "goalify", "goalify this", "goalify <task>", "/goalify <task>",
  "prep a goal", "prepare a brief for /goal", "make an md for /goal", "set up an
  autonomous run to launch later", or wants a Codex `/goal` objective. This skill
  AUTHORS those two artifacts now; it does NOT execute the work in this session.
  For a task to be done immediately here, use autopilot, ultrawork, or ralph
  instead, not goalify.
argument-hint: "[task to prepare a /goal run for]"
license: MIT
metadata:
  version: 2.3.0
---

# goalify

## Overview

In one line, for anyone: **You describe a big coding job. goalify writes the instructions the AI works
from, and the finish line it has to prove it reached.**

Prepare the best possible autonomous run in THIS session, then hand off so the user can `/clear` and
launch it in a fresh session that has full context to work in.

**goalify produces TWO artifacts, not one — and they have fixed names. Use these words everywhere:**

1. **The brief** — a *file*: a self-contained implementation Markdown file at an absolute path under
   `.goal/`. It is the source of truth for the **worker** (the fresh session doing the job).
2. **The condition** — a *string*: one short, plain sentence (≤ 4,000 characters, and normally nowhere
   near that), *derived from* the brief's success criteria. It is the source of truth for the
   **evaluator** (the Stop hook that decides "is this done?"), and it is what the user pastes
   into `/goal`.

There is no third artifact and no combined one. `/goal` takes the condition string, never a path.

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

Work autonomously; only stop for the question batch. **Keep live visible progress:** before you start,
create one task per step below in the task tracker (`TaskCreate`, or your environment's equivalent),
and flip each one `in_progress` → `completed` as it lands — never in one batch at the end. A silent
PREPARE is indistinguishable from a stalled one. Write artifacts to disk as you produce them.

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
   as `.goal/CONDITION-<slug>.txt` as a durable copy — a fallback for a long condition, not the
   primary instruction.
9. **Wait for everything, then hand off (short).** Confirm no subagent or background task is still
   live and that every subagent's file deliverable has been read from disk. Only then print the bullet
   summary, the caps, and the two steps — `/clear`, then the one short `/goal` line, inline and
   verbatim (see Handoff format).

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
- **Live visible progress.** At the start, create ONE task per phase in the task tracker
  (`TaskCreate`, or the environment's equivalent). Flip each `in_progress` → `completed` as the work
  lands — never in one batch at the end — and tick this file's progress checklist as you go; that
  checklist IS the resume state. A silent run is indistinguishable from a stalled one.
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
- **Closeout turn.** Immediately before the final report, rerun EVERY Definition-of-done check
  together in one dedicated turn and quote each command's fresh output in that same turn. The
  evaluator sees a truncated transcript that drops the oldest messages, so evidence scattered
  across earlier turns is exactly what it loses. Claims without freshly quoted output are not
  evidence.
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

## Final output (ADHD-friendly: short bullets under Done / Proof / Next — no long paragraphs)
<Exactly three headers, a few short bullets under each, and nothing else. No walls of text.>
- **Done** — what changed. One bullet per thing.
- **Proof** — each check that was run and its actual quoted output; what needed approval and was
  skipped; confidence per major decision (confirmed · likely · uncertain · blocked · needs-approval).
- **Next** — the user's next commands, plus anything still open.
<Then state plainly, in the report itself: a `/goal` run that stopped is not proof of completion — the
evaluator can end the loop by judging the condition unachievable — and give the verify-only re-check
(open a fresh session and run only the definition-of-done commands above).>

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

**Default to ONE short, plain sentence — roughly 120–150 characters, in everyday words.** The 4,000
characters are a ceiling, not a target. A condition the user cannot read at a glance is a condition
they cannot check before pasting it, and every extra clause is one more thing the evaluator can score
as unmet. Write it the way you would say it out loud, shaped exactly like this worked example:

```text
Do everything in ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

**Four teeth, all mandatory.** A condition missing any one of them is not shippable:

1. **The brief's path, named inside the condition** (`~/acme/.goal/api-migration.md`). That is how the
   run finds the work. The condition is the finish line, not the work.
2. **A quoted-evidence clause** (`the last turn quotes npm test passing`). The final turn must quote
   the output of a NAMED command. A tool-less evaluator can verify nothing else.
3. **A made-up sentinel word** (`ASYNC-OK`) — one unambiguous string to find, which no ordinary
   summary produces by accident.
4. **A turn bound** (`Stop after 40 turns`) — it keeps the loop finite and yours.

Say each tooth once, in plain words. Go longer only when the finish line genuinely needs more than one
command proved — then add those checks and nothing else. Everything else that matters (maximum effort,
never self-approve, the 3-strike ladder, "do not declare this goal impossible to escape it") belongs in
the brief, which the worker reads in full; the condition only has to be checkable.

**Why "the last turn" carries the weight.** On a long run the evaluator sees only a recent window of
the transcript, so evidence proven on turn 3 is invisible on turn 90. The brief therefore tells the run
to re-run every check together in one dedicated closeout turn immediately before it reports, which is
what defeats that truncation; the condition's "the last turn quotes …" clause is what makes skipping it
fail. Claims without freshly quoted command output are insufficient evidence — a confident summary is
not proof.

### Condition lint (run every check before printing the handoff)

- [ ] ≤ 4,000 characters — count it, don't estimate.
- [ ] Reads in one breath. Over ~150 characters, cut until every remaining clause is one of the four
      teeth or a genuinely extra check.
- [ ] Contains no bare `$` sequence (hook-substitution hazard). Escape or reword.
- [ ] All four teeth present: the brief's path, a quoted-evidence clause naming a runnable command,
      the sentinel, and an explicit turn bound.
- [ ] Plain words only — no jargon the user would have to decode before pasting it.
- [ ] Contains no phrase that the condition text itself would satisfy — never make "the assistant said
      it is done" the success test.
- [ ] Every command in it appears in the brief's definition of done, and vice versa.

## Handoff format (what you print — short, bullets, not verbose)

**Two steps: `/clear`, then ONE short `/goal <condition>` line with the entire condition text inline
and verbatim.** No file launcher, no wrapper script, no `pbcopy` step, no `<paste>` placeholder — the
user must never be left holding only a path. The reason is the whole v2 correction: a copy step puts a
**file path in the user's hand at the exact moment they are about to type `/goal`**, which is the most
reliable way to produce the wrong input. Make the wrong input hard to even form. The brief's absolute
path lives *inside* the condition text, so printing the line inline is also how the run gets pointed at
the brief without `/goal` ever receiving a bare path — and at ~150 characters, that line fits on screen.

```
Prepared the run. Here's what it will do:
- <bullet> <bullet> <bullet>   (high level, plain language)
Decisions you set: <one line, if any>
Plan: <N> phases · <N> subagents · turn cap <N>
Brief:     <ABSOLUTE PATH>
Condition: <N> chars, under the 4,000 limit

Next — two steps:
1.  /clear
2.  /goal <THE ENTIRE CONDITION TEXT, INLINE AND VERBATIM — every character of it, on one
    pasteable line. The brief's absolute path appears inside this text; that is how the run
    is pointed at the brief without handing /goal a bare path.>

    Unattended? Confirm auto mode is on — the default in current Claude Code; otherwise
    Shift+Tab, or --permission-mode auto.

A copy of the condition is saved at <ABSOLUTE PATH>/CONDITION-<slug>.txt as a durable record —
never the required step; step 2 above is.

Headless instead:  claude -p "/goal <THE SAME CONDITION TEXT>" --permission-mode auto

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
- **Subagent barrier — NEVER print the handoff while anything is still running.** Do not author the
  brief, print the handoff, or end your turn while any subagent or background task is still live. Wait
  for each one, read its file deliverable from disk, and confirm that file exists before you use it.
  An "idle", "available" or "complete" ping is NOT a delivered result. (Observed failure, 2026-08-06: a
  stale copy of this skill printed a handoff while agents were still listed as running.)
- **Live visible progress here too.** Create one task per PREPARE step up front and flip each to
  completed as it lands — not in one batch at the end.
- **No hallucination here either.** Verify the project state with evidence before scoping.
- **Don't over-ask.** One question batch, only genuine forks. If none, don't ask.
- **Keep YOUR output short.** The artifacts carry the detail; the user is about to `/clear`.
- **Absolute paths everywhere.** The fresh session is a stranger to this one.
- **Never run `/clear` or `/goal` yourself** — print them for the user. They are the user's manual
  steps; a "helpful" attempt to run them defeats the fresh-context handoff.

## Common mistakes

- **Handing `/goal` a file path.** The single defect v2 exists to fix. The path names the brief; the
  condition is what the user actually types.
- **A long, lawyerly condition where a plain 150-character one would do.** 4,000 is a ceiling, not a
  target; anything past the four teeth is surface area for the evaluator to score as unmet.
- **Printing the handoff while a subagent is still running**, or ending on a report the user has to
  read three paragraphs of to find out whether it worked.
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
