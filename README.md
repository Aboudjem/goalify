<p align="center">
  <img src="assets/hero.svg" alt="goalify writes a brief file and a condition string; you paste the whole condition into /goal — never the path alone." width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>Prep a big coding task while Claude still has your context. Run it unattended in a fresh session. Get evidence you can check yourself.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
</p>

You scope a big task in chat — a refactor, a migration, an audit. Then you `/clear` so the run can
start clean, and the plan dies with the old chat. The fresh run improvises, drifts on decisions you
never made, and when it stops you can't tell whether it finished or just stopped talking.

goalify is a Claude Code skill that closes that gap: it does the prep while it still has your
context, and wires the finish line to commands the run has to quote. The whole handoff:

```text
claude plugin marketplace add Aboudjem/10x        # once
claude plugin install goalify@10x

/goalify migrate our API to async/await
    brief      ~/acme/.goal/api-migration.md      a file — the run works from it
    condition  157 chars                          a string — you paste it below

/clear
/goal Read and fully execute the brief at ~/acme/.goal/api-migration.md, done when the last turn quotes npm test passing and says ASYNC-OK. Or stop after 40 turns.
```

That last line is one line. It scrolls; you paste all of it. (The printout above is abridged; the
strings in it are exact.)

## What changes

| | Without goalify | With goalify |
|---|---|---|
| **Your plan after `/clear`** | gone with the old chat | saved as a brief the run is told to re-read as it works |
| **Decisions mid-run** | improvised on the spot | locked with you before the run starts |
| **"Done" means** | the run stopped talking | the last turn quotes `npm test` passing and says `ASYNC-OK` |
| **When it stops** | scroll back and hope | on success, every check rerun at the end; either way you can re-check |

## Two artifacts, two readers

<p align="center">
  <img src="assets/two-artifacts.svg" alt="The brief file goes to the worker; the condition string goes to /goal's tool-less evaluator. Never the path alone." width="100%">
</p>

goalify writes a **brief** and a **condition**, and they go to different readers. The brief is a
file: the worker — the fresh session doing the job — opens it and works from it. The condition is a
string: it goes to the worker as its objective, and to the evaluator behind `/goal`, which decides
every turn whether the work is proven. The evaluator has no tools and cannot open files. That is
why `/goal`'s argument is the condition text itself, and why the condition names the brief's path
*inside* it: the worker follows the path; the evaluator only reads the words.

|  | **The brief** | **The condition** |
|---|---|---|
| **Is it `/goal`'s argument?** | **No** — the condition names its path | **Yes** — this is the argument |
| What it is | a Markdown file | a plain string |
| Who reads it | the **worker** only | **both** — the worker as its objective, the evaluator as the finish line |
| Why that shape | full context, absolute paths, cited research; it can be long | the evaluator gets no tools and a truncated transcript, so ≤ 4,000 characters and quotable |

Deriving the condition from the brief's definition of done keeps the two in step — a mitigation,
not a guarantee. goalify also saves the condition to `.goal/CONDITION-<slug>.txt` so you can copy it
without scrolling back; that file is just where the string lives, never what you hand to `/goal`. The mechanics
(sentinels, the closeout turn, transcript truncation, what happens to the brief afterwards) are in
the [FAQ](docs/faq.md).

## Install

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Restart Claude Code if it's already open. Needs Claude Code 2.1.139+ for the built-in
[`/goal`](https://code.claude.com/docs/en/goal).

<details>
<summary>Manual install, skill only</summary>

```bash
git clone https://github.com/Aboudjem/goalify
mkdir -p ~/.claude/skills
cp -r goalify/skills/goalify ~/.claude/skills/goalify
```

</details>

## Use it

1. **`/goalify <your task>`.** goalify inspects the repo, researches what it doesn't know, and asks
   at most one short batch of questions — only where there is a genuine fork.
2. **Read what it wrote** — the brief, and the condition it derived from the brief's definition of
   done.
3. **`/clear`, then paste the condition** — the whole string, not the path it names. Handing `/goal`
   the path on its own fails quietly: nothing errors, and the first turn reads the path and starts
   working, so the run looks healthy. But the check is now asking whether the text
   `~/acme/.goal/api-migration.md` is satisfied — a question no transcript can answer, so the run
   can never prove it finished.

```text v1-antipattern
# paste the condition text itself — the same string, byte for byte, that goalify printed
/goal Read and fully execute the brief at ~/acme/.goal/api-migration.md, done when the last turn quotes npm test passing and says ASYNC-OK. Or stop after 40 turns.

# not the path on its own — nothing errors; the check just becomes unprovable
/goal ~/acme/.goal/api-migration.md
```

Use it for a substantial, well-specified job. Skip it for a one-line fix — just ask Claude. Skip it
for work you want done *right now* in this session. And skip it for open-ended exploration with no
definable end state: goalify will decline rather than write a vague brief.

Unattended runs and the headless `claude -p` form are in the
[quickstart](docs/quickstart.md#2-use-it).

## What you get

- **A brief that survives `/clear`** — self-contained, absolute paths, your decisions locked, and
  phases in dependency order, so the run never has to guess what you meant.
- **A condition wired to real commands** — a made-up word the run has to print (`ASYNC-OK` above), the
  exact commands whose output must be quoted, and a turn bound, all under 4,000 characters.
- **A fresh-context run** — the work starts at 100% context instead of the dregs of a long chat.
- **A closeout turn** — every check reruns together at the end, so the evidence lands where the
  evaluator can still see it.
- **A paper trail** — on success the brief is archived to `.goal/done/` with a completion stamp; on
  failure it stays put, checklist intact, so you can resume.

## Honest limits

> [!IMPORTANT]
> A `/goal` run that stops is not proof it finished. The evaluator applies independent judgment and
> can end a run by deciding the condition is unachievable — no wording prevents that. Reread the
> closeout evidence, or rerun the brief's definition-of-done commands yourself, before you believe a
> green result.

The brief and the condition are two specs that can drift; deriving one from the other and linting it
is a mitigation, not a proof. A turn cap is a stopping rule, not a completion rule. The full list,
including what does **not** carry over to other harnesses, is in [honest limits](docs/limits.md).

<p align="center"><sub><a href="assets/goalify-teaser.mp4">▶ Watch the 30-second teaser</a> · <a href="assets/goalify-teaser.gif">GIF</a></sub></p>

## Docs

- [Quickstart](docs/quickstart.md) — your first run, step by step
- [A worked example](examples/sample-brief.md) — a real brief and the condition derived from it
- [Running it under Codex](docs/codex.md) — the same condition, and what does not carry over
- [Honest limits](docs/limits.md) — everything goalify does not promise
- [FAQ](docs/faq.md) · [Changelog](CHANGELOG.md) · [Security](SECURITY.md) ·
  [the skill itself](skills/goalify/SKILL.md) · [evals](evals)

## Contributing & license

Issues and PRs welcome; goalify is built test-first
([contributing](CONTRIBUTING.md) · [code of conduct](CODE_OF_CONDUCT.md)). [MIT](LICENSE).

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. The `/goal` behavior
documented here was re-derived from the shipped Claude Code 2.1.221 and codex-cli 0.146.0 binaries,
2026. <a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
