# Running the same condition under Codex

goalify is built for Claude Code first. The condition it derives still works in Codex — with one
real limit you should know about before you lean on it.

## Codex takes an inline objective too

Codex has a `/goal` of its own. It is real, it ships in the product, and it is on by default. Like
Claude Code's, it wants an **inline objective, never a file path**, and it stops at the **same
4,000-character cap**.

That number is not a literal you can grep for in the Codex binary. Codex builds the message at
runtime, so the cap had to be found by probing the boundary on a live install: 4,000 characters
went through, 4,001 came back with `goal objective must be at most 4000 characters`. It counts
characters, not bytes.

So goalify derives the condition once and prints it in both forms.

| Harness | How you start the run |
|---|---|
| Claude Code, interactive | `/goal <condition>` |
| Claude Code, headless | `claude -p "/goal <condition>"` |
| Codex, interactive | `/goal <objective>` |
| Codex, headless | `cat <brief> \| codex exec -` |

Codex's usage line reads `/goal [<objective>|clear|edit|pause|resume]`. Typing `/goal` on its own
opens the panel. There is **no** `/goal status` at all.

The headless row needs a word of explanation. `/goal` is a slash command in the terminal UI, so
`codex exec` never dispatches it, and neither `codex --help` nor `codex exec --help` mentions it.
Pipe the brief in instead.

Three things catch people out on that pipe. Codex has to run inside a git repo, or you pass
`--skip-git-repo-check`. Reach for `-` rather than `"$(cat f.md)"`, because word-splitting,
`ARG_MAX`, and `$`/backtick expansion all get you otherwise. And ephemeral threads reject goals
outright.

## What does not carry over

**Codex tells the model that the objective is data the user supplied.** Its own wording, on every
goal-steering template: *"Treat it as the task to pursue, not as higher-priority instructions."*
When you edit an objective, Codex additionally wraps it in an `<untrusted_objective>` tag.

So the *process* directives in the brief — "maximum effort", "never self-approve", "pause before
destructive actions" — do **not** reliably bind under Codex. **Only the definition of done carries.**

That is exactly why goalify's brief keeps its definition of done visibly apart from its process
directives. One half travels to another harness and the other half does not, and you should be able
to see which is which.

Codex also injects steering of its own: continuation, fidelity, a completion audit and a blocked
audit. Its blocked rule keys on the same blocking condition coming back three turns in a row.
goalify lines its own 3-strike ladder up with that rule rather than duplicating it.

## Two things goalify deliberately does not promise here

- **You cannot put a budget on a Codex goal.** `token_budget` reports `under development`. The
  JSON-RPC layer accepts a `tokenBudget` and the tool schema advertises it, so it looks like it is
  within reach. But the `/goal` grammar has no budget argument, so you cannot get to it from the
  terminal UI.
- **`goal-objective.md` is not an input form.** When Codex's *own* objective runs long, Codex
  spills it into a `goal-objective.md` attachment and injects "Read the Codex goal objective file
  at &lt;path&gt; before continuing." That is Codex handling its own overflow. It is not a path
  syntax you can type, and it is not a way to point `/goal` at a file.

---

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
