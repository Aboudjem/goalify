# goalify on Codex

Loaded just in time from SKILL.md's "Cross-harness: Codex" pointer. Everything below was
verified against codex-cli (see docs/codex.md for the user-facing guide).

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
