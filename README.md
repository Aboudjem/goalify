<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
    <img src="assets/hero-dark.svg" alt="goalify: autonomous run prep. Come back to proof, not a promise." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=8E7BFF" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=8E7BFF" alt="GitHub stars"></a>
</p>

<p align="center">
  <b>English</b> · <a href="READMEs/zh-CN.md">简体中文</a> · <a href="READMEs/ja.md">日本語</a> · <a href="READMEs/es.md">Español</a> · <a href="READMEs/fr.md">Français</a>
</p>

<p align="center">
  <strong>Hand Claude a huge task. Come back to proof it's done, not a promise that it is.</strong>
</p>

<p align="center">
  <a href="#what-it-does">What it does</a> · <a href="#install">Install</a> · <a href="#use-it">Use it</a> · <a href="#what-you-get">What you get</a> · <a href="#works-in-your-editor">Works in your editor</a> · <a href="#good-to-know">Good to know</a>
</p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

## What it does

Some jobs are too big to sit and watch. Renaming one thing across hundreds of files. Moving an old
project onto a newer version of the code it is built on. Going through a messy project to clean up
one kind of problem. You describe the job while Claude still has your context, and goalify writes
down what the run has to do and what done has to look like. Then it hands you one line to paste.

- **The brief** is a file holding everything the run needs: your decisions, the exact paths, the
  order of work.
- **The condition** is one line you paste into `/goal`, Claude Code's built-in stop-check, which
  keeps the session working and judges every turn against that line.

Picture a building site. The brief is the plans a builder works from. The condition is the checklist
an inspector signs off against, and that inspector never reads the plans and never visits the site.
They judge only the evidence the builder shows them.

## Install

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Any other agent, in one line:

```bash
npx skills add Aboudjem/goalify
```

<details>
<summary>Copy it in by hand</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Nothing else in the repository is needed at run time. You want Claude Code 2.1.139 or newer, because
that is the release `/goal` landed in. The [quickstart](docs/quickstart.md) covers the rest.
</details>

## Use it

**1. Describe the job.** Run `/goalify` plus your task in Claude Code. goalify reads your project,
asks about the few real decisions, then writes the brief and prints the condition.

```text
/goalify migrate our API to async/await
    Brief:     ~/acme/.goal/api-migration.md
    Condition: 149 chars, under the 4,000 limit
```

**2. Clear the chat.** `/clear` wipes the conversation, so the run starts fresh, at full attention.

**3. Paste the condition.** The whole line. It wraps on screen, so grab all of it.

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it - done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

The brief's path rides along inside that line, because the evaluator behind `/goal` has no tools and
cannot open files. It reads the line you paste and a trimmed transcript of the run, never the brief
itself. Handing it the path on its own errors nothing and proves nothing, which is why it is the
easiest mistake to make:

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

Unsure about a line before you paste it?
`python3 skills/goalify/scripts/condition_lint.py "<your condition>"` checks it against six
mechanical rules and names the ones it fails. The judgment calls stay with you.

<p align="center">
  <img src="assets/hero.svg" alt="Four steps: describe the job, get a brief and a condition, paste the condition, come back to proof." width="72%">
</p>

## What you get

- **One line to hand over.** Clear the chat, paste one line, walk away.
- **Your context survives the reset.** The brief carries your decisions into the fresh session.
- **Progress you can glance at.** The run ticks a checklist inside the brief as it goes.
- **Proof, not a promise.** The last turn has to quote the checks passing and print a made-up word,
  `ASYNC-OK` above, so a run that skipped the work would have to lie outright.
- **A tidy ending at the cap.** Nearing its turn limit the run stops starting new work, finishes or
  reverts what is half-done, and says in the final report that it stopped early.
- **A stop keeps your progress.** The brief stays put with its checklist intact. You resume by
  pasting the same line, you do not restart.
- **Filing on success only.** The closing turn reruns every check, quotes the output, and moves the
  brief into `.goal/done/`, a file move you can see in any file browser.

## Works in your editor

Works in Claude Code, Cursor, Codex, Copilot, Gemini CLI, and 70+ other agents through
`npx skills add`. The skill is plain Markdown, so nothing in it is tied to one model.

| Agent | One-line install |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| Any of 70+ agents | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| Everything else | the agent codes and paths in [docs/editors.md](docs/editors.md) |

`/clear` and `/goal` are Claude Code commands. Elsewhere, start a fresh session in place of `/clear`
and give it the condition as a standing objective. Codex has a `/goal` of its own, and
[running it under Codex](docs/codex.md) covers what carries over and what does not.

## Good to know

> [!IMPORTANT]
> A run that stops is not proof it finished. The evaluator judges for itself and can end a run by
> deciding the finish line is unreachable. Before you trust a green result, reread the closing
> evidence, the quoted checks in the last reply and the brief moved into `.goal/done/`, or rerun the
> checks yourself.

- **goalify authors, it never executes.** It writes the two artifacts in this session and stops. You
  start the run.
- **Nothing runs in the background.** One Markdown skill, no server, no dependency to install, no
  network call of its own.
- **Everything it does not promise** is written down under [honest limits](docs/limits.md).

## Learn more

- [Quickstart](docs/quickstart.md), a first run end to end, plus the other ways to install.
- [Worked conditions](examples/conditions.md), eight worth shipping and eight to avoid, each with a
  line naming what the bad one loses.
- [A worked example](examples/sample-brief.md), a real brief and the condition derived from it.
- [Install in your editor](docs/editors.md) · [FAQ](docs/faq.md) · [Under Codex](docs/codex.md)
- [Honest limits](docs/limits.md) · [Changelog](CHANGELOG.md) · [The skill itself](skills/goalify/SKILL.md) · [LICENSE](LICENSE)

<p align="center"><sub><a href="assets/goalify-teaser.mp4">Watch the 28-second teaser</a> · <a href="assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. MIT licensed. `/goal` behavior
re-derived from the shipped Claude Code 2.1.223 binary, 2026.
<a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
