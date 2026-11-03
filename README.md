<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
    <img src="assets/hero-dark.svg" alt="goalify: hand Claude a huge task, come back to proof." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="latest release"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=ff3d9a" alt="GitHub stars"></a>
</p>

<p align="center">
  <b>English</b> · <a href="READMEs/zh-CN.md">简体中文</a> · <a href="READMEs/ja.md">日本語</a> · <a href="READMEs/es.md">Español</a> · <a href="READMEs/fr.md">Français</a>
</p>

<p align="center">
  <strong>Hand Claude a huge task. Come back to proof it's done, not a promise that it is.</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">Website</a> · <a href="#install">Install</a> · <a href="#how-it-works">How it works</a> · <a href="#new-in-30">New in 3.0</a> · <a href="#how-it-compares">How it compares</a> · <a href="#good-to-know">Good to know</a>
</p>

goalify turns any request into a **goal**: a clear finish line your AI keeps working toward
until it's proven, or until it hits the turn limit you set. It does all the thinking first: it checks the job can work, reads the docs,
finds your real test commands and asks you every question it has, once. Then your AI works in a
clean session, non-stop, for hours or even days, with zero interruptions. It's done when the
proof is on screen, not when it says so.

Works best in **Claude Code** and **Codex**, which both have a built-in `/goal` that keeps the run
going. In Claude Code, a separate evaluator checks the proof after every turn; Codex audits its own
progress against the same finish line. It installs in 70+ other AI agents too, where you get the same
preparation and finish line, and start the run yourself.

## Install

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Any other agent that reads skills, in one line:

```bash
npx skills add Aboudjem/goalify
```

Then type `/goalify` and describe the job. You need Claude Code 2.1.139 or newer, the release that
added `/goal`.

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="assets/goalify-demo.gif" alt="goalify in a loop: the brief and the condition, the run preview, then a green VERIFIED receipt." width="88%"></a>
  <br><sub><a href="assets/goalify-promo.mp4">Watch the full video</a> · <a href="assets/goalify-promo-vertical.mp4">vertical cut</a> · <a href="assets/goalify-promo-15s.mp4">15-second cut</a></sub>
</p>

## Without goalify, with goalify

| Without goalify                                 | With goalify                                                 |
| :---------------------------------------------- | :----------------------------------------------------------- |
| It stops at 3am to ask which database you meant | Every question is asked once, before the run                 |
| The plan lives in a chat that `/clear` wipes    | The plan is a file the fresh session re-reads every loop     |
| It invents an `npm test` your repo doesn't have | Checks come from your repo and your CI                       |
| "Done!" means it said so                        | Done means the last turn quoted the passing output           |
| You find the gaps the next morning              | `/goalify verify` re-runs the checks and hands you a receipt |

## How it works

goalify only prepares. Claude Code's own `/goal` does the running. goalify's job is to leave the
run nothing to ask about.

1. **Homework.** Can this work? goalify reads your project, the docs and your CI, and finds the
   commands that really prove the job is done.
2. **Questions, once.** It asks the few real choices in one batch. That's the last time it asks.
3. **Two things come out.** The **brief** is a file with everything the run needs: your
   decisions, exact paths, the order of work. The **condition** is one line for `/goal` that says
   what proof looks like. A **preview page** opens so you can see the whole plan first.
4. **`/clear`, paste, walk away.** The run starts fresh, with all its context free for your job.
   In Claude Code, a separate evaluator reads the transcript after every turn and lets it stop only when the
   proof is there, or at the turn cap you set.
5. **Check it later.** `/goalify verify` re-runs the brief's checks and writes a receipt.

The line you paste looks like this. It wraps on screen, so grab all of it:

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

The brief's path rides inside that sentence, because the evaluator behind `/goal` has no tools and
can't open files. It reads the line you paste and the run's transcript, never the brief. Handing
`/goal` a bare path errors nothing and proves nothing, which is why it's the easiest mistake to make:

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="assets/hero.svg" alt="Four steps: describe the job, get a brief and a condition, paste the condition, come back to proof." width="72%">
</p>

### Why it can run for days

A long run usually dies in one of two ways: it stops to ask you something, or it says "done" while
something is still broken. goalify handles the first by asking everything up front and writing the
answers into the brief. It handles the second with the condition: the last turn has to re-run
every check, quote the output, and print a made-up word like `ASYNC-OK`, so a run that skipped the
work would have to lie outright. Near its turn cap, the run wraps up cleanly and says what's left.
If it stops early, the brief keeps its checklist, and pasting the same line resumes it.

## New in 3.0

<p align="center">
  <img src="assets/preview-and-receipt.svg" alt="The 3.0 loop: a run preview before, a non-stop run, then a proof receipt that says VERIFIED." width="88%">
</p>

- **Run preview.** After every `/goalify`, a one-page view of the run opens in your browser:
  phases as a flow, each check and the command that proves it, the caps, your decisions, and a
  copy button for the `/goal` line. It also lints the brief and refuses to render a broken one.
  The inline `/goal` line in the chat is still the real handoff. The page is extra.
- **Proof receipts.** `/goalify verify` shows you the brief's check commands, asks once, runs them,
  and writes a receipt: **VERIFIED**, **NOT VERIFIED** or **UNVERIFIABLE**. It can contradict a run
  that claimed it was done. It refuses destructive commands unless you allow each one by name.
- **Real checks, found for you.** goalify reads `package.json`, `pyproject.toml`, `Cargo.toml`,
  `go.mod`, Makefiles and your CI workflows, and skips npm's "no test specified" stub, so the finish
  line never names a command that can't pass. It can also run them once as a baseline.
- **Status.** `/goalify status` lists every brief in `.goal/` (open, blocked or done, with its
  ticks) and reprints the full `/goal` line to resume each open one.
- **Express mode.** `/goalify --quick <task>` skips the web research and the questions for medium
  jobs, keeps every safety floor, and stops instead of guessing when the scope forks.
- **Doctor.** `/goalify doctor` lists every goalify copy on your machine and warns when an old one
  loads next to the new one.
- **Safer headless line.** Conditions can't carry backticks or double quotes anymore, so the
  `claude -p "/goal ..."` line can't run a command in your shell when you paste it. Thanks to
  [@Hug0x0](https://github.com/Hug0x0) for the fix.

## How it compares

Plain differences, checked against each project's README in November 2026.

| Tool                                                                            | What it is                                                                                                              | How it differs from goalify                                                                                                                                     |
| :------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [supergoal](https://github.com/robzilla1738/supergoal)                          | A Claude Code plugin that scouts, asks, plans phases and hands `/goal` one command, with a final audit against the plan | The closest neighbor. goalify writes one self-contained brief plus a linted condition, shows a preview page before the run, and writes a proof receipt after it |
| Ralph loops ([snarktank/ralph](https://github.com/snarktank/ralph) and friends) | A loop that feeds the same prompt to the agent again and again                                                          | Usually stops on a word the worker prints or an iteration cap. With Claude Code's `/goal`, a separate evaluator reads the transcript every turn                               |
| [Spec Kit](https://github.com/github/spec-kit)                                  | GitHub's spec-driven toolkit: specify, plan, tasks, implement                                                           | Great for writing the spec. goalify is about the long unattended run and proving it finished                                                                    |

## Works in your editor

| Agent                                        | One-line install                                                |
| :------------------------------------------- | :-------------------------------------------------------------- |
| Claude Code                                  | `claude plugin install goalify@10x`                             |
| Any of 70+ agents                            | `npx skills add Aboudjem/goalify`                               |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>`                    |
| Everything else                              | the agent codes and paths in [docs/editors.md](docs/editors.md) |

`/clear` and `/goal` are Claude Code commands. Elsewhere, start a fresh session instead of `/clear`
and give it the condition as a standing objective. Codex has its own `/goal`, and
[running it under Codex](docs/codex.md) covers what carries over.

<details>
<summary>Copy it in by hand</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Nothing else in the repository is needed at run time. The [quickstart](docs/quickstart.md) covers
the rest. If you ever had an older copy, run `/goalify doctor` to make sure only one is loaded.
</details>

## Good to know

> [!IMPORTANT]
> A run that stops is not proof it finished. The evaluator judges for itself and can end a run by
> deciding the finish line can't be reached. Before you trust a green result, run
> `/goalify verify` on the brief, or re-run its checks yourself.

- **goalify never does the task.** It writes the brief and the condition, and it only runs your
  checks when you ask.
- **Nothing phones home.** No server, no runtime dependency, no network call. The helper scripts
  are plain Python standard library, and the preview page makes no outside requests.
- **No cost guesses.** goalify never predicts a dollar or token figure. The turn cap is your control.
- **Everything it doesn't promise** is written down under [honest limits](docs/limits.md).

## Learn more

- [Website](https://goalify-kappa.vercel.app) · [Quickstart](docs/quickstart.md) · [FAQ](docs/faq.md)
- [Worked conditions](examples/conditions.md), good and bad, each bad one with what it loses.
- [A worked example](examples/sample-brief.md), a real brief and its condition, plus
  [its preview page](examples/sample-brief.html) (download it and open it in a browser).
- [Install in your editor](docs/editors.md) · [Under Codex](docs/codex.md) · [Honest limits](docs/limits.md)
- [Changelog](CHANGELOG.md) · [The skill itself](skills/goalify/SKILL.md) · [LICENSE](LICENSE)

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. MIT licensed. `/goal` behavior
re-checked against Claude Code 2.1.317 and its docs, November 2026.
<a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
