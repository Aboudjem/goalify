# Quickstart

Set up a big autonomous Claude Code run the right way: prepare a `/goal` file *before* you `/clear`,
then run it in a fresh, full-context session.

`goalify` only **authors** the file — it does not run your task. You run it. The file deletes itself
when the run finishes successfully.

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

This gives you `/goalify`, which authors the run file. You execute that file with Claude Code's built-in
`/goal <path>` command ([Claude Code 2.1.139+](https://code.claude.com/docs/en/goal)). Claude Code
auto-discovers the skill. (A brand-new top-level skills directory may need a restart the first time
before it is watched.) To update later, re-pull and re-copy; to remove, delete `~/.claude/skills/goalify`.

---

## 2. Use it in 3 steps

1. **Ask** in plain language: `goalify this: <your big task>` — e.g.
   *"goalify this: migrate our Express API from callbacks to async/await and keep the tests green."*
2. **Answer the short MCQ** (only if goalify finds a genuine fork in scope/structure/risk). Then it
   writes one self-contained `/goal` file to an absolute path and prints two commands.
3. **Run the two commands it printed:**
   ```text
   /clear
   /goal <absolute-path-it-gave-you>
   ```
   A fresh session reads the file at full context, fans out its own agents, verifies, tests, and
   **deletes the file** when every success criterion is met.

That's it. Nothing in your repo changes during step 1 — goalify only researches and writes the plan.
The work happens in the fresh `/goal` session, under the hard rules baked into the file
(no hallucination, separate-agent verification, tests, gated destructive actions).

---

## What you get

- **One self-contained file** with a declarative goal, verified context (absolute paths), your locked
  decisions, dependency-ordered phases with fan-out guardrails, machine-checkable success criteria, a
  progress checklist, and a gated self-destruct.
- **A fresh-context run** — the execute session starts at 100% context, not the dregs of a long chat.
- **Zero residue** — the file removes itself on success (and survives to resume if not).

See a real example: [`examples/sample-goal-file.md`](../examples/sample-goal-file.md).

---

## When NOT to use it

- A trivial change — just ask Claude to do it.
- Open-ended exploration with no definable end state — goalify will decline; explore interactively instead.
- Work you want done *right now* in this session — use `autopilot` / `ultrawork` / `ralph`.
