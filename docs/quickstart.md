# Quickstart

Set up a big autonomous Claude Code run the right way. You do the prep **before** you `/clear`, then
start the run in a fresh session that still has its full context.

goalify only **authors** the run. It does not do your task, and you are the one who starts it. It
writes two things: a **brief**, the Markdown file the run works from, and a **condition**, the plain
string the run has to prove it satisfied.

---

## 0. Prerequisites

- **Claude Code**, installed and working. goalify is a Claude Code skill (Agent Skills).
- **A task worth a full session** — a refactor, a migration, a feature, an audit. For a one-line fix,
  just ask Claude to do it; you do not need an autonomous run for that.

---

## 1. Install

**The plugin is the shortest route:**

```shell
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

**Or copy the skill in by hand:**

```shell
git clone https://github.com/Aboudjem/goalify.git
mkdir -p ~/.claude/skills
cp -R goalify/skills/goalify ~/.claude/skills/goalify
```

Either way, you get `/goalify`, which authors the run. You start the run yourself with Claude Code's
built-in `/goal <condition>` command, which needs
[Claude Code 2.1.139+](https://code.claude.com/docs/en/goal).

**Claude Code finds the skill on its own.** One exception: a brand-new top-level skills directory may
need one restart before Claude Code watches it. To update later, pull again and re-copy. To remove
it, delete `~/.claude/skills/goalify`.

---

<p align="center">
  <img src="../assets/how-it-works.svg" alt="Three steps: goalify researches and decides, writes the brief and derives the condition, then you run it fresh." width="100%">
</p>

goalify inspects the repo and locks the few real decisions, then writes the brief and derives the
condition from it. You `/clear` and paste the condition into `/goal`. The run proves every criterion
in a closeout turn before the brief is archived.

## 2. Use it

1. **Ask in plain language.** Type `goalify this: <your big task>` — for example,
   *"goalify this: migrate our Express API from callbacks to async/await and keep the tests green."*

2. **Answer the short batch of questions.** You only get one if goalify finds a genuine fork in
   scope, structure or risk. Then it writes the brief to an absolute path, derives the completion
   condition from it, and prints the two commands you run yourself.

3. **Run those two commands.** `/clear` first, then the `/goal` line goalify printed. That line is
   long because it is the condition text itself, and it opens by naming the brief's absolute path so
   the fresh session knows where to start reading. Paste the whole thing.

   **What `/goal` receives is text, not a file.** The evaluator behind `/goal` has no tools and
   cannot open anything. Hand it the brief's path and that path just becomes the condition, so every
   turn the evaluator is asked whether the string `~/acme/.goal/api-migration.md` is satisfied — a
   question the transcript can never answer.

   **Nothing errors when that happens,** which is what makes it worth knowing. The check keeps
   running, it just runs against something unprovable, while the first turn reads the path and starts
   working. The run looks fine right up until it does not end.

   ```text v1-antipattern
   # the shape of what you paste — the condition text itself (ONE line; wrapped here to fit)
   /goal Read and fully execute the brief at ~/acme/.goal/api-migration.md, done when the
   last turn quotes npm test passing and says ASYNC-OK. Or stop after 40 turns.

   # not the brief's path
   /goal ~/acme/.goal/api-migration.md
   ```

   **`/goal` does not change your permission mode.** Auto mode is the default in current Claude Code,
   so an unattended run usually needs nothing extra. If you have changed it, turn auto mode back on
   (Shift+Tab, `--permission-mode auto`, or `/permissions`).

   A fresh session then reads the brief at full context, fans out its own agents, verifies, tests,
   and **proves every criterion in a closeout turn** before it stops.

If the condition is long and you would rather not scroll back for it, goalify also saved it to
`.goal/CONDITION-<slug>.txt`, so `pbcopy < .goal/CONDITION-<slug>.txt` gets you the same text. That
is a convenience, not the step.

**Running it with no terminal UI at all:** the headless form is
`claude -p "/goal <condition>" --permission-mode auto`. Same condition string, passed on the
command line instead of pasted.

That is it. **Step 1 touches nothing in your repo except `.goal/`** — goalify researches, then
writes the two artifacts there, and changes no code. The work happens in the fresh `/goal` session,
under the hard rules baked into the brief: no hallucination, separate-agent verification, tests, and
gated destructive actions.

---

## What you get

- **One self-contained brief** — a declarative goal, verified context with absolute paths, your
  locked decisions, phases in dependency order with fan-out guardrails, a definition of done wired to
  real commands, a progress checklist, and a gated archive step.
- **A linted condition string** — under 4,000 characters, with a sentinel, the exact commands whose
  output must be quoted, a closeout-turn requirement, and an explicit turn bound.
- **A fresh-context run** — the execute session starts at 100% context, not the dregs of a long chat.
- **A deliberate paper trail, not clutter** — on success the brief moves to `.goal/done/` with a
  completion stamp; if the run did not finish, it stays put so you can resume. Either way you can
  compare what was promised against what happened. The condition file stays in `.goal/` too, and you
  can delete both whenever you like.

One caveat worth knowing up front: **a `/goal` run that stops is not proof the work is done.** The
evaluator can end a run by judging the condition unachievable. Read the closeout evidence packet, or
re-run the brief's definition-of-done commands yourself, before you believe a green result. More in
[honest limits](limits.md).

See a real example: [`examples/sample-brief.md`](../examples/sample-brief.md).

---

## When NOT to use it

- **A trivial change** — just ask Claude to do it.
- **Open-ended exploration with no definable end state** — goalify declines rather than write a vague
  brief, so explore interactively instead.
- **Work you want done right now, in this session** — use `autopilot`, `ultrawork` or `ralph`.
