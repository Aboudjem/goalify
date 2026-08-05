<p align="center">
  <img src="assets/hero.svg" alt="goalify writes a brief file and a condition string; you paste the whole condition into /goal — never the path alone." width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>goalify preps a big coding task so it can run unattended in a fresh Claude Code session — and prove it actually finished.</strong>
</p>

<p align="center">
  Run <code>/goalify &lt;your task&gt;</code>. You get back a <strong>brief</strong> — a file the worker opens — and a<br>
  <strong>condition</strong> — the string you paste into <code>/goal</code>, which names the brief's path inside it.
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
</p>

---

```text
claude plugin marketplace add Aboudjem/10x        # once
claude plugin install goalify@10x

/goalify migrate our API to async/await
    brief      ~/acme/.goal/api-migration.md      a file — the run works from it
    condition  1,284 chars                        a string — you paste it below

/clear
/goal Read and fully execute the brief at ~/acme/.goal/api-migration.md, done when the last turn quotes npm test passing and says ASYNC-OK. Or stop after 40 turns.
```

That last line is one line. It scrolls; you paste all of it.

## Why

You scope a big task in chat — a refactor, a migration, an audit. Then you `/clear` for a clean
session, and the plan is gone. The run improvises, drifts on decisions you never made, and when it
stops you can't tell whether it finished or just ran out of things to say.

goalify does the prep while it still has your context, and wires the condition to commands the run
has to quote.

## Two artifacts, two readers

<p align="center">
  <img src="assets/two-artifacts.svg" alt="The brief file goes to the worker; the condition string goes to /goal's tool-less evaluator. Never the path alone." width="100%">
</p>

The condition goes to **both** readers. The worker gets it as its objective and can follow the path
inside it; the evaluator only ever judges it against what it can see in the transcript. `/goal`'s
argument is a string because that is what the command accepts — the evaluator's tool-lessness is why
a *path* cannot work as one.

|  | **The brief** | **The condition** |
|---|---|---|
| **Is it `/goal`'s argument?** | **No** — the condition names its path | **Yes** — this is the argument |
| What it is | a Markdown file | a plain string |
| Who reads it | the **worker** only | **both** — the worker as its objective, the evaluator as the finish line |
| Why it's shaped that way | full context, absolute paths, cited research; it can be long | the evaluator gets no tools and a truncated transcript, so ≤ 4,000 characters and quotable |

Deriving the condition from the brief's definition of done is what keeps the two in step — a
mitigation, not a guarantee. How it does that (sentinels, the closeout turn, transcript truncation,
what happens to the brief afterwards) is in the [FAQ](docs/faq.md).

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

1. **`/goalify <your task>`.** goalify inspects the repo, researches what it doesn't know, and asks at most one short
   batch of questions — only where there is a genuine fork.
2. **Read the brief it wrote**, and the condition it derived from that brief's definition of done.
3. **`/clear`, then paste the condition** — the whole string, not the path it names. Handing `/goal`
   the path on its own fails quietly: nothing errors, and the check does not stop running, it just
   keeps asking "is `~/acme/.goal/api-migration.md` satisfied?" — which no transcript can answer.
   Meanwhile the first turn reads the path and starts working, so the run looks healthy.

Use it for a substantial, well-specified job. Skip it for a one-line fix (just ask Claude), for
open-ended exploration with no definable end state — goalify will decline rather than write a vague
brief — and for work you want done *right now* in this session.

```text v1-antipattern
# paste the condition text itself
/goal Read and fully execute the brief at ~/acme/.goal/api-migration.md — implement every phase.
Done when npm test passes: the most recent turn must quote its output showing 0 failures and
contain ASYNC-OK. Or stop after 40 turns.

# not the path on its own — nothing errors; the check just becomes unprovable
/goal ~/acme/.goal/api-migration.md
```

Unattended runs and the headless `claude -p` form are in the
[quickstart](docs/quickstart.md#2-use-it).

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
