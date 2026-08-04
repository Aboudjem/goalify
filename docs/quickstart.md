# Quickstart

Set up a big autonomous Claude Code run the right way: prepare a `/goal` file *before* you `/clear`,
then run it in a fresh, full-context session.

`goalify` only **authors** the run — it does not do your task. You start it. goalify writes two things:
a **brief** (the implementation file the run works from) and a **condition** (the finish line the run
has to prove). The brief is archived to `.goal/done/` when the run finishes successfully.

---

## 0. Prerequisites

- **Claude Code**, installed and working. (goalify is a Claude Code / Agent Skills skill.)
- A task worth a full session — a refactor, a migration, a feature, an audit. For a one-line fix,
  just ask Claude to do it; you don't need a `/goal` file.

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

## 2. Use it in 3 steps

1. **Ask** in plain language: `goalify this: <your big task>` — e.g.
   *"goalify this: migrate our Express API from callbacks to async/await and keep the tests green."*
2. **Answer the short MCQ** (only if goalify finds a genuine fork in scope/structure/risk). Then it
   writes the brief to an absolute path, derives the completion condition from it, and prints three
   commands.
3. **Run the three commands it printed:**
   ```text
   /clear
   pbcopy < <the-condition-file-it-gave-you>
   /goal <paste>
   ```
   `/goal` does not change your permission mode. Auto mode is the default in current Claude Code, so
   an unattended run usually needs nothing extra; if you have changed it, turn auto mode back on
   (Shift+Tab, `--permission-mode auto`, or `/permissions`). A fresh session then reads the brief at
   full context, fans out its own agents, verifies, tests, and **proves every criterion in a closeout
   turn** before it stops.

   > **`/goal` takes the condition, not the path.** Handing it the brief's path makes that path string
   > the condition, and the evaluator behind `/goal` has no tools and cannot read files — so it could
   > never verify it. This is the bug v2.0.0 fixed; if you have an older habit, this is the step that
   > changed.

That's it. Nothing in your repo changes during step 1 — goalify only researches and writes the plan.
The work happens in the fresh `/goal` session, under the hard rules baked into the file
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
re-run the brief's definition-of-done commands yourself, before you believe a green result.

See a real example: [`examples/sample-goal-file.md`](../examples/sample-goal-file.md).

---

## When NOT to use it

- A trivial change — just ask Claude to do it.
- Open-ended exploration with no definable end state — goalify will decline; explore interactively instead.
- Work you want done *right now* in this session — use `autopilot` / `ultrawork` / `ralph`.
