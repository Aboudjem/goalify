<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
    <img src="assets/hero-dark.svg" alt="goalify: give your AI a big job, get proof back." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="latest release"></a>
</p>

<p align="center">
  <b>English</b> · <a href="READMEs/zh-CN.md">简体中文</a> · <a href="READMEs/ja.md">日本語</a> · <a href="READMEs/es.md">Español</a> · <a href="READMEs/fr.md">Français</a>
</p>

<p align="center">
  <strong>Give your AI a big job. Get proof back.</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">Website</a> · <a href="#install">Install</a> · <a href="#how-it-works">How it works</a> · <a href="#sample-report">Sample report</a> · <a href="#proof">Proof</a> · <a href="#faq">FAQ</a> · <a href="#limits">Limits</a>
</p>

goalify asks its questions first, writes the plan, and checks the result against your real tests.

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

The demo receipt, from `make demo` in a clone of this repo (a real run on 2026-11-17, trimmed):

```text
VERDICT: VERIFIED (2/2 checks passed)
Checks:
  1. PASS (exit 0) python3 -m unittest -q test_slugify
  2. PASS (printed nothing, as expected) grep -n "TODO" slugify.py
```

Your agent said the job was done. Was it? goalify sets the finish line before the work starts:
your own tests, passing. At the end, `/goalify verify` runs them again and writes a receipt.

Two limits to know up front. A run that stops is not always a finished run. And `/goal` keeps your
permission mode, so a run can still pause on a permission prompt ([Limits](#limits)).

## Why use it

- **Answer once, up front.** Every question comes first, so the run has nothing left to ask you.
  Proof: the answers sit in the brief under "Decisions", as in [this real brief](examples/sample-brief.md).
- **A finish line from your own tests.** The `/goal` line names the test command that must pass.
  Proof: [the sample condition](examples/sample-condition.txt) says "done when the last turn quotes npm test passing".
- **A receipt that can fail.** `make demo` prints `VERDICT: VERIFIED (2/2 checks passed)`.
  Proof: `python3 examples/demo/run.py --broken` prints `VERDICT: NOT VERIFIED (1/2 checks passed)`.

## Without goalify, with goalify

| Without goalify | With goalify |
|:--|:--|
| The AI stops at 3am to ask you a question | All questions come first, one time |
| The plan is lost when you clear the chat | The plan is saved in a file. The AI reads it again and again |
| The AI uses a test that your project does not have | The tests come from your real project |
| "Done!" only means the AI said so | "Done" means the last step shows the tests passing |
| You find the problems the next morning | `/goalify verify` runs the tests again and gives you a receipt |

## Install

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Any other AI tool that reads skills, in one line:

```bash
npx skills add Aboudjem/goalify
```

During that install, skills.sh shows a medium risk warning for goalify. It flags that `verify`
runs the brief's check commands in a shell. verify lists those commands first and runs nothing
without your yes.

You need Claude Code 2.1.139 or newer. That version added `/goal`.

**Your first command.** Type `/goalify` and the job in one sentence:

```text
/goalify migrate the API client to async and keep every test green
```

goalify asks its questions, then prints a brief path and one `/goal` line to paste.

**See a real receipt in one minute**, without a long run. You need `git`, `python3` and `make`.

```bash
git clone https://github.com/Aboudjem/goalify && cd goalify
```

```bash
make demo
```

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="assets/goalify-demo.gif" alt="goalify in a loop: your request becomes a goal, all questions come first, the AI works alone, and at the end you get proof." width="88%"></a>
  <br><sub>An animation of the flow, not a screen recording.</sub>
  <br><sub><a href="assets/goalify-promo.mp4">Watch the full video</a> · <a href="assets/goalify-promo-vertical.mp4">vertical video</a> · <a href="assets/goalify-promo-30s.mp4">30-second video</a> · <a href="assets/goalify-promo-15s.mp4">15-second video</a></sub>
</p>

## How it works

goalify turns your request into a **goal**. A goal is a clear finish line. The AI keeps working
until the goal is done and proven, or until it reaches the limit you set.

It works best in **Claude Code** and **Codex**. Both have a built-in `/goal` command that keeps
the work going. In Claude Code, a second checker reads the work after every step. Codex checks
its own work against the same finish line. Other AI tools that read skills get the same plan and
finish line, and you start the work yourself.

goalify only prepares the work. The `/goal` command does the work. goalify makes sure the AI has
nothing left to ask.

1. **Homework.** Can this work? goalify reads your project, the docs and your tests. It finds the
   commands that show the job is really done.
2. **Questions, one time.** It asks you the few real choices, all together. After that, it does
   not ask again.
3. **Two things come out.** The **brief** is a file with the full plan: your choices, the exact
   files, the order of the work. The **condition** is one line for `/goal`. It says what proof
   looks like. A **preview page** also opens, so you can see the whole plan first.
4. **`/clear`, paste, walk away.** The work starts in a clean chat, with all its memory free for
   your job. In Claude Code, a second checker reads the work after every step. It lets the work
   stop only when the proof is there, or when it reaches your step limit.
5. **Check it later.** `/goalify verify` runs the checks again and writes a receipt.

The line you paste looks like this. It is long, so copy all of it:

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

The path to the brief is inside that line. This matters: the checker behind `/goal` cannot open
files. It only reads the line you paste and the chat. So do not give `/goal` only a file path.
Nothing breaks, but nothing is checked either. It is the easiest mistake to make:

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="assets/hero.svg" alt="Four steps: describe the job, get a brief and a condition, paste the condition, come back to proof." width="72%">
</p>

### Why a long run stays on track

Long AI work usually fails in two ways. The AI stops to ask you something. Or it says "done" when
something is still broken. goalify fixes the first problem: it asks everything at the start and
writes the answers in the brief. The condition fixes the second problem. At the end, the AI must
run every check again, show the result, and write a special word like `ASYNC-OK`. If the
AI skipped the work, it would have to lie. Near its step limit, the AI finishes cleanly and says
what is left. If it stops early, the brief keeps its checklist. Paste the same line again to
continue.

### What each command gives you

<p align="center">
  <img src="assets/preview-and-receipt.svg" alt="The loop: a preview of the plan before, the AI working alone, then a receipt that says VERIFIED." width="88%">
</p>

- **Plan preview.** After every `/goalify`, a page opens in your browser. It shows the steps, each
  check and the command that proves it, the limits, your choices, and a copy button for the
  `/goal` line. It also checks the brief and refuses to show a broken one. The `/goal` line in
  the chat is still the main step. The page is extra.
- **Proof receipts.** `/goalify verify` shows you the checks, asks you one time, runs them, and
  writes a receipt: **VERIFIED**, **NOT VERIFIED** or **UNVERIFIABLE**. It can say "not verified"
  even when the AI said "done". It will not run dangerous commands unless you allow each one.
- **Real tests, found for you.** goalify reads `package.json`, `pyproject.toml`, `Cargo.toml`,
  `go.mod`, Makefiles and your CI files. It skips npm's empty "no test specified" test. So the
  finish line never uses a test that cannot pass. It can also run the tests once at the start.
- **Status.** `/goalify status` lists every brief in `.goal/`: open, blocked or done. For each open
  one, it shows the full `/goal` line to continue.
- **Quick mode.** `/goalify --quick <task>` is for medium jobs. It skips the web research and the
  questions, but keeps every safety check. If the job could mean two different things, it stops
  and asks you to use the full mode.
- **Doctor.** `/goalify doctor` lists every copy of goalify on your computer. It warns you when an
  old copy is loaded next to the new one.
- **Safer copy and paste.** The condition cannot contain backticks or double quotes anymore. So
  the `claude -p "/goal ..."` line cannot run a hidden command when you paste it. Thanks to
  [@Hug0x0](https://github.com/Hug0x0) for this fix.

## Sample report

`/goalify verify` re-runs the brief's checks and prints the verdict first. This is a real run of
`python3 examples/demo/run.py --broken --dir /tmp/goalify-demo-broken` on 2026-11-17. The "run"
ticked every box, but one test fails:

```text
VERDICT: NOT VERIFIED (1/2 checks passed)
Next:
  1. Read the log of the first failing check: /private/tmp/goalify-demo-broken/.goal/verify-slugify/1.log
  2. Fix it, or paste the brief's /goal line again so the run resumes from its checklist.
  3. Run verify again for a fresh receipt: /goalify verify "/private/tmp/goalify-demo-broken/.goal/slugify-20261117.md"
Checks:
  1. FAIL (exit 1) python3 -m unittest -q test_slugify
  2. PASS (printed nothing, as expected) grep -n "TODO" slugify.py
Brief: /private/tmp/goalify-demo-broken/.goal/slugify-20261117.md
Receipt: file:///private/tmp/goalify-demo-broken/.goal/RECEIPT-slugify-20261117-164816.html
```

Check 2 must print nothing: `grep` finds no TODO left, so it passes.

Without `--broken`, the same demo prints `VERDICT: VERIFIED (2/2 checks passed)`. The HTML receipt
also opens with the verdict. Each mode builds in its own temp folder, so both receipts stay.

## Proof

Every number here comes from a command you can run in a clone of this repo.

| Claim | Command | What it prints today |
|:--|:--|:--|
| Every test suite passes | `make test` | `10/10 suites passed`, then `452/452 checks passed` |
| The receipt tells the truth both ways | `make demo`, then `python3 examples/demo/run.py --broken` | `VERDICT: VERIFIED (2/2 checks passed)`, then `VERDICT: NOT VERIFIED (1/2 checks passed)` |
| The plugin loads in Claude Code | `claude plugin validate . --strict` | `Validation passed` |
| The skills CLI finds the skill | `npx -y skills@1.9.0 add . --list` | one skill, `goalify` |

CI runs all four on every push and pull request.

## Works with

Only what was installed and run on the date shown.

| Agent | Install path | Tested |
|:--|:--|:--|
| Claude Code 2.1.326 | `claude plugin install goalify@10x` | 2026-11-17 |
| Claude Code 2.1.326 | `npx skills add Aboudjem/goalify -a claude-code` | 2026-11-17 |
| Codex CLI | `npx skills add Aboudjem/goalify -a codex` | 2026-11-17 |

Documented, not tested: Cursor, GitHub Copilot, Gemini CLI, OpenCode and the other agents the
skills CLI supports. Their codes and folders are in [docs/editors.md](docs/editors.md).

`/clear` and `/goal` are Claude Code commands. In other tools, start a new chat instead of `/clear`,
and give the AI the condition as its main task. Codex has its own `/goal`. See
[goalify in Codex](docs/codex.md) for what works the same and what does not.

<details>
<summary>Install by hand</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

You only need that one folder. The [quickstart](docs/quickstart.md) explains the rest. If you
had an older copy, run `/goalify doctor` to make sure only one copy is loaded.
</details>

## How it compares

Simple differences, checked against each project's README in November 2026.

| Tool | What it is | How it is different from goalify |
|:--|:--|:--|
| [supergoal](https://github.com/robzilla1738/supergoal) | A Claude Code plugin. It explores, asks, plans in phases and gives `/goal` one command. It checks the result against the plan at the end | The closest tool. goalify writes one full brief and a checked condition, shows a preview page before the work, and writes a proof receipt after |
| Ralph loops ([snarktank/ralph](https://github.com/snarktank/ralph) and others) | A loop that gives the AI the same prompt again and again | It usually stops on a word the AI writes, or after a number of rounds. With Claude Code's `/goal`, a second checker reads the work every step |
| [Spec Kit](https://github.com/github/spec-kit) | GitHub's toolkit to write a spec, a plan and tasks | Great for writing the spec. goalify is for the long work with nobody watching, and for proving it is finished |

## FAQ

**Does goalify do the job itself?**
No. It writes the brief and the condition, then stops. You start the run with `/goal`, in a clean chat.

**Why can I not give `/goal` the brief's path alone?**
The checker behind `/goal` cannot open files. It reads only the line you paste and the chat. A bare
path gives it nothing to check, so the run never stops on proof.

**What if the run stops before the job is done?**
The brief keeps its checklist. Paste the same `/goal` line again and the run continues where it stopped.

**How do I know the work is really finished?**
Run `/goalify verify` on the brief. It re-runs each check and writes a receipt that says VERIFIED,
NOT VERIFIED or UNVERIFIABLE.

**I have two copies of goalify. Which one loads?**
Run `/goalify doctor`. It lists every copy, says which ones are loaded, and prints the command to
remove the extra one.

More answers in the [full FAQ](docs/faq.md).

## Limits

> [!IMPORTANT]
> When a run stops, it is not always finished. The checker decides by itself. It can also stop
> the run if it thinks the goal cannot be reached. Before you trust a green result, run
> `/goalify verify` on the brief, or run its checks yourself.

- **goalify never does the job itself.** It writes the brief and the condition. It runs your
  checks only when you ask.
- **A run can still pause on a permission prompt.** `/goal` keeps your permission mode: manual mode
  asks before unapproved tool calls, and auto mode asks again after repeated blocks.
- **Verify re-runs checks, it does not review code.** A check that tests the wrong thing still passes.
- **What leaves your machine: nothing.** No server, no extra packages, no network calls. The helper
  scripts use only standard Python, and the preview page loads nothing from the internet.
- **No price guesses.** goalify never guesses a cost in money or tokens. Your step limit is your
  control.
- **Everything it does not promise** is listed in [honest limits](docs/limits.md).

## Learn more

- [Website](https://goalify-kappa.vercel.app) · [Quickstart](docs/quickstart.md) · [FAQ](docs/faq.md)
- [Example conditions](examples/conditions.md): good ones and bad ones, and what each bad one loses.
- [A full example](examples/sample-brief.md): a real brief and its condition, plus
  [its preview page](examples/sample-brief.html) (download it and open it in a browser).
- [Install in your AI tool](docs/editors.md) · [goalify in Codex](docs/codex.md) · [Honest limits](docs/limits.md)
- [Changelog](CHANGELOG.md) · [The skill itself](skills/goalify/SKILL.md) · [LICENSE](LICENSE)

---

<sub>Made by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. MIT license. The `/goal` facts on this page were
checked against Claude Code 2.1.326, its changelog and its docs on 2026-11-17.
The finer limits in [docs/limits.md](docs/limits.md) name the version they were measured on.
<a href="https://github.com/Aboudjem/goalify/issues">See a problem?</a></sub>
