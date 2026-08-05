# Quickstart

Set up a big autonomous Claude Code run the right way: prepare the brief and its condition *before*
you `/clear`, then run it in a fresh, full-context session.

`goalify` only **authors** the run — it does not do your task. You start it. goalify writes two
things: a **brief** (the implementation file the run works from) and a **condition** (the string the
run has to prove it satisfied). The brief is archived to `.goal/done/` when the run finishes successfully.

---

## 0. Prerequisites

- **Claude Code**, installed and working. (goalify is a Claude Code / Agent Skills skill.)
- A task worth a full session — a refactor, a migration, a feature, an audit. For a one-line fix,
  just ask Claude to do it; you don't need an autonomous run.

---

## 1. Install

Easiest is the plugin:

```shell
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Or drop in the skill manually:

```shell
git clone https://github.com/Aboudjem/goalify.git
mkdir -p ~/.claude/skills
cp -R goalify/skills/goalify ~/.claude/skills/goalify
```

This gives you `/goalify`, which authors the run. You start it with Claude Code's built-in
`/goal <condition>` command ([Claude Code 2.1.139+](https://code.claude.com/docs/en/goal)). Claude Code
auto-discovers the skill. (A brand-new top-level skills directory may need a restart the first time
before it is watched.) To update later, re-pull and re-copy; to remove, delete `~/.claude/skills/goalify`.

---

<p align="center">
  <img src="../assets/how-it-works.svg" alt="Three steps: goalify researches and decides, writes the brief and derives the condition, then you run it fresh." width="100%">
</p>

goalify inspects the repo and locks the few real decisions; writes the brief and derives the condition
from it; then you `/clear` and paste the condition into `/goal`, and the run proves every criterion in
a closeout turn before archiving the brief.

## 2. Use it

1. **Ask** in plain language: `goalify this: <your big task>` — e.g.
   *"goalify this: migrate our Express API from callbacks to async/await and keep the tests green."*

2. **Answer the short question batch** (only if goalify finds a genuine fork in scope, structure or
   risk). Then it writes the brief to an absolute path, derives the completion condition from it, and
   prints the two commands you run yourself.

3. **Run them.** `/clear` first, then the `/goal` line goalify printed. That line is long: it is the
   condition text itself, and it opens by naming the brief's absolute path so the fresh session knows
   where to start. Paste it whole.

   What `/goal` receives is the *text*, not a file. The evaluator behind `/goal` has no tools and
   cannot open anything, so if you hand it the brief's path that path just becomes the condition, and
   every turn it is asked whether the string `~/acme/.goal/api-migration.md` is satisfied — a question
   the transcript can never answer. Nothing errors when that happens, which is what makes it worth
   knowing: the check keeps running, it just runs against something unprovable, while the first turn
   reads the path and starts working — so the run looks fine right up until it doesn't end.

   ```text v1-antipattern
   # this is the shape of what you paste — the condition text
   /goal Read and fully execute the brief at ~/acme/.goal/api-migration.md — implement every phase.
   Done when npm test passes: the most recent turn must quote its output showing 0 failures and
   contain ASYNC-OK. Or stop after 40 turns.

   # not the brief's path
   /goal ~/acme/.goal/api-migration.md
   ```

   `/goal` does not change your permission mode. Auto mode is the default in current Claude Code, so
   an unattended run usually needs nothing extra; if you have changed it, turn auto mode back on
   (Shift+Tab, `--permission-mode auto`, or `/permissions`). A fresh session then reads the brief at
   full context, fans out its own agents, verifies, tests, and **proves every criterion in a closeout
   turn** before it stops.

If the condition is long and you would rather not scroll back for it, goalify also saved it to
`.goal/CONDITION-<slug>.txt`, so `pbcopy < .goal/CONDITION-<slug>.txt` gets you the same text. That is
a convenience, not the step.

That's it. Nothing in your repo changes during step 1 — goalify only researches and writes the two
artifacts. The work happens in the fresh `/goal` session, under the hard rules baked into the brief
(no hallucination, separate-agent verification, tests, gated destructive actions).

---

## What you get

- **One self-contained brief** with a declarative goal, verified context (absolute paths), your locked
  decisions, dependency-ordered phases with fan-out guardrails, a definition of done wired to real
  commands, a progress checklist, and a gated archive step.
- **A linted condition string** — under 4,000 characters, with a sentinel, the exact commands whose
  output must be quoted, a closeout-turn requirement, and an explicit turn bound.
- **A fresh-context run** — the execute session starts at 100% context, not the dregs of a long chat.
- **A deliberate paper trail, not clutter** — on success the brief moves to `.goal/done/` with a
  completion stamp (and stays put to resume if not), so you can compare what was promised against what
  happened. The condition file stays in `.goal/` too; delete both whenever you like.

One caveat worth knowing up front: **a `/goal` run that stops is not proof the work is done.** The
evaluator can end a run by judging the condition unachievable. Read the closeout evidence packet, or
re-run the brief's definition-of-done commands yourself, before you believe a green result. More in
[honest limits](limits.md).

See a real example: [`examples/sample-brief.md`](../examples/sample-brief.md).

---

## When NOT to use it

- A trivial change — just ask Claude to do it.
- Open-ended exploration with no definable end state — goalify will decline; explore interactively instead.
- Work you want done *right now* in this session — use `autopilot` / `ultrawork` / `ralph`.
