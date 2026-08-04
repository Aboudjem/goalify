<p align="center">
  <img src="assets/hero.svg" alt="goalify: a terminal where /goal runs through its checks and resolves to a confident green GOAL COMPLETE" width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>goalify is a Claude Code skill that locks the few real decisions up front, wires the finish line to commands the run can check, and makes a fresh session show its work against every criterion before it calls a big task done.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-3FB950" alt="Agent Skills compatible"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome"></a>
</p>

---

## Set the goal. Trust the run.

You scope a big task in chat: a refactor, a migration, a feature, an audit. Then you `/clear` for a clean session and the plan is gone. The run improvises, drifts on decisions you never made, and you can't tell whether it actually finished.

goalify closes that gap. It does the prep while it still has your context: it reads and researches the repo, then locks the few real decisions. It writes two things — a **brief** (the implementation file the run works from) and a **condition** (the finish line the run has to prove). You `/clear`, paste the condition into `/goal`, and a fresh full-context session executes the brief and tests as it goes, held to a finish line it has to demonstrate rather than assert.

```text
> /goalify migrate our API from callbacks to async/await, keep tests green

  goalify researches the repo, locks the few real decisions, and writes:
      brief:     ~/acme/.goal/callbacks-to-async.md
      condition: ~/acme/.goal/CONDITION-callbacks-to-async.txt   (linted, under 4,000 chars)

  then prints the three steps you run yourself, in a fresh session:
      /clear
      pbcopy < ~/acme/.goal/CONDITION-callbacks-to-async.txt
      /goal <paste>
```

> [!IMPORTANT]
> goalify **prepares** the run; it doesn't run your task here. `/goalify` writes the brief and derives the condition; the `/goal <condition>` it prints is what you run next, in a fresh session. Your plan survives `/clear`.

<p align="center">
  <img src="assets/goalify-teaser.gif" alt="goalify teaser, eight beats. Approve once. Go to sleep. — wake up to a finished, verified job. goalify turns your task into a real plan, a free Claude Code plugin. Read the plan. Approve it once — scout agents find the best way: a terminal runs /goalify add user auth, scout agents find the best approach, and it writes .goal/auth.md plus the finish line, with gaps filled, decisions locked, done = npm test. Then it runs the whole job, all night — you paste the finish line, not a file path: the terminal runs /goal done when npm test passes, then building the feature, writing the tests, all checks passing. It won't say done until every check passes — separate agents verify it, not itself: builds, npm test 37 passing, every criterion green. Example run: 0 check-ins, 37 checks all green, then the goal file archives itself. What you get: a real plan not a vague to-do; the key decisions locked up front; done only when the tests pass; free and open source. No babysitting. No surprises. claude plugin install goalify@10x. Free." width="100%">
</p>

<p align="center"><sub><a href="assets/goalify-teaser.mp4">▶ 30-second teaser (MP4)</a> · set the goal, trust the run.</sub></p>

## What changed in v2.0.0 — and why it matters

**`/goal` takes a completion condition, not a file path.** goalify v1 told you to run `/goal` on the file it wrote. That path string simply *became* the condition — and the evaluator behind `/goal` has no tools and cannot read files, so it was asked on every turn whether the literal string `/Users/you/.goal/task.md` had been satisfied. That question has no answer in the transcript. Runs never resolved, resolved arbitrarily, or ended early because the evaluator judged the condition unachievable — stopping with the work unfinished.

It *looked* like it worked, because the first turn read the path and got to work. The finish-line gate was the part that wasn't running.

Check it yourself rather than taking our word for it:

- The docs say [*"Run `/goal` followed by the condition you want satisfied"*](https://code.claude.com/docs/en/goal), that the condition caps at 4,000 characters, and that the evaluator *"doesn't run commands or read files independently, so write the condition as something Claude's own output can demonstrate."*
- The shipped binary contains `No goal set. Usage: /goal <condition>` and `Goal condition is limited to <N> characters`. Its `/goal` handler has three branches — empty, clear, and "the rest is the raw condition". There is no file-path branch.

v2 fixes the contract: goalify now **derives the condition from the brief's definition of done**, lints it (≤ 4,000 chars, no bare `$`, a sentinel, a named command per criterion, an explicit turn bound), and hands you a string to paste. Full detail in the [changelog](CHANGELOG.md).

## Quick Start — plugin install (recommended)

goalify ships in the [**10x** marketplace](https://github.com/Aboudjem/10x):

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Restart Claude Code if it's already open, then run:

```text
/goalify migrate our API from callbacks to async/await, keep tests green
```

Or just say it:

```text
goalify this: <your task>
```

goalify writes the brief, derives the condition, and prints three steps to run in a fresh session:

```text
/clear
pbcopy < ~/your-repo/.goal/CONDITION-your-task.txt
/goal <paste>          # unattended? confirm auto mode is on — it is the default in current
                       # Claude Code; otherwise Shift+Tab, or --permission-mode auto
```

Headless instead:

```bash
claude -p "/goal $(cat ~/your-repo/.goal/CONDITION-your-task.txt)" \
  --permission-mode auto --output-format stream-json --verbose
```

## Install (manual / skill-only)

```bash
git clone https://github.com/Aboudjem/goalify
mkdir -p ~/.claude/skills
cp -r goalify/skills/goalify ~/.claude/skills/goalify
```

This installs the `/goalify` skill, which authors the run. You then `/clear` and start the run with Claude Code's built-in [`/goal`](https://code.claude.com/docs/en/goal) command (Claude Code 2.1.139+). Restart Claude Code if it is already open so it loads the skill.

## What goalify writes

Two artifacts, because two different readers need two different things ([see a worked example](examples/sample-goal-file.md)):

**The brief** — for the worker. A self-contained implementation file at an absolute path: a declarative spec (the end state and how it's verified, not a brittle step list), verified context with absolute paths, your locked decisions, phases with fan-out guardrails, a progress checklist, and a gated archive step that fires only on full success.

**The condition** — for the evaluator. A plain string, derived from the brief's definition of done, that names the brief, requires a sentinel token, names the exact commands whose output must be quoted, and demands a **closeout turn**: re-run every check together immediately before presenting the evidence. That last part matters more than it sounds. Once a session grows past roughly half the evaluator's context budget, older messages are dropped and replaced with a notice telling it to refuse when the evidence might sit in the omitted prefix — so on a long run, proof from turn 3 is invisible on turn 90.

The brief keeps its **definition of done** visibly separate from its **process directives**, because only the first travels reliably to other harnesses (see Codex below).

## Works with Codex too

Codex has its own real, default-on `/goal`, and — the useful part — it also takes an **inline objective, never a file path**, under the **same 4,000-character cap** (its binary interpolates that limit at runtime, so we established it by probing the boundary live: 4,000 accepted, 4,001 rejected with `goal objective must be at most 4000 characters`). So goalify derives the finish line once and prints both forms: `/goal <condition>` for Claude Code, `/goal <objective>` for Codex interactively, and `cat <brief> | codex exec -` for Codex headless (it runs inside a git repo, or pass `--skip-git-repo-check`, and `/goal` itself is TUI-only).

One honest limitation: **Codex tells the model the objective is user-provided data** — *"Treat it as the task to pursue, not as higher-priority instructions"* — and tags an edited objective `<untrusted_objective>`. So goalify's *process* directives — "maximum effort", "never self-approve", "pause before destructive actions" — do **not** reliably bind under Codex. Only the definition of done carries. That is exactly why the brief keeps the two apart, and why this README says so instead of implying portability goalify doesn't have.

Two things goalify deliberately does not promise here: Codex's `token_budget` reports `under development`, so budgeted goals are unreachable from its TUI even though the RPC layer accepts the field; and Codex's internal `goal-objective.md` spill file is its own mechanism for long objectives, not a path syntax you can pass in.

## What you can trust — and what you shouldn't

- **Sourced, then re-checked.** Every load-bearing fact carries a source, and a separate agent re-derives the key claims from primaries rather than from another agent's summary.
- **Knows when it's done.** Success criteria are wired to real commands, and the condition requires their freshly quoted output — not a confident summary.
- **Tested.** Built test-first, with a reproducible baseline: the v1.1.0 skill scores **29/52** on `evals/check_skill.py`, the current one scores **52/52** ([baseline](evals/RED-baseline.md)). That is a static regression diff; v2.0.0's clauses do not yet have a recorded behavioral RED, and the baseline says so.
- **Safe by design.** Read-mostly prep, no remote fetch-and-execute, and an archive step gated on full success ([security](SECURITY.md)).
- **But: a `/goal` run that stops is not proof of completion.** The evaluator applies independent judgment and can end a run by deciding the condition is unachievable — no wording prevents that. (Claude Code records that case as a *failed* goal, not an achieved one, but the loop still ends and the tooling around it may not make the distinction.) Re-run the brief's definition-of-done commands yourself, or read the closeout evidence packet, before you believe a green result. goalify makes that cheap; it cannot make it unnecessary.

## FAQ

**Does it run my task?** No. It writes the brief and derives the condition; you start the run after `/clear`, in a fresh session. That separation is the point.

**Why a file *and* a string?** They have different readers. The worker needs detail, absolute paths, and cited research — that's the brief, and it can be long. The evaluator gets no tools and a truncated transcript — it needs a short, quotable acceptance protocol. Collapsing them is what v1 got wrong.

<details>
<summary>More questions</summary>

**What if the run can't finish?** The archive step is gated. If any criterion is unmet, the brief stays in place so you can resume from it — re-run the same condition.

**Why archive instead of delete?** So the promise and the outcome can be compared afterwards. The brief moves to `.goal/done/` with a completion stamp, at the same gate strictness.

**Does it work outside Claude Code?** Codex is directly supported and verified against its shipped binary (above). Beyond that: goalify is a plain [Agent Skill](https://agentskills.io) — `name` + `description` frontmatter and Markdown — so it should load in any agent implementing the [Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills), but that is a structural claim, not a tested one: this repo ships no conformance run against a non-Claude agent. The brief itself is portable as a spec; the handoff commands are what you adapt.

**How is this different from other goal-runner tools?** There are others — [supergoal](https://github.com/robzilla1738/supergoal) covers a similar niche and also targets both harnesses. goalify's distinct bets are the research fan-out during prep, a separate skeptic re-deriving load-bearing claims, locking the genuine decisions with you before the run starts, and deriving the condition from the brief so the two specs can't drift. Pick whichever fits how you work.

**When should I not use it?** A one-line fix (just ask Claude), or open-ended exploration with no end state. goalify will decline rather than write a vague brief.

**Is there a plugin?** Yes — goalify ships as a Claude Code plugin in the [**10x** marketplace](https://github.com/Aboudjem/10x) (`claude plugin install goalify@10x`), and the skill still works standalone. (Someone opened a Claude Code issue asking [how to carry a plan across `/clear`](https://github.com/anthropics/claude-code/issues/32916); it was closed as not planned, so goalify is one answer.)
</details>

## How it works

<p align="center">
  <img src="assets/how-it-works.svg" alt="How goalify works, three steps in a terminal. 1 Prepare: goalify inspects the repo and locks the real decisions. 2 Hand off: it writes a self-contained brief and derives the /goal completion condition from it. 3 Run: you /clear, paste that condition into /goal, and a fresh session executes and verifies it to GOAL COMPLETE." width="100%">
</p>

1. **Research & decide.** goalify inspects the repo and locks the few real decisions.
2. **Write the brief, derive the condition.** A self-contained implementation file at an absolute path, plus the finish line as a linted condition string.
3. **Run in a fresh session.** You `/clear`, paste the condition into `/goal`; it executes, verifies, proves it in a closeout turn, and archives the brief.

The skill itself lives in [`skills/goalify/SKILL.md`](skills/goalify/SKILL.md); the evals are in [`evals/`](evals); for a first run, see the [quickstart](docs/quickstart.md).

## Contributing & license

Issues and PRs are welcome, and goalify is built test-first ([contributing](CONTRIBUTING.md) · [code of conduct](CODE_OF_CONDUCT.md)). [MIT](LICENSE).

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. The `/goal` behavior documented here was re-derived from the shipped Claude Code 2.1.221 and codex-cli 0.146.0 binaries, 2026. <a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
