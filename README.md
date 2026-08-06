<p align="center">
  <img src="assets/hero.svg" alt="goalify writes a brief file and a condition line; the condition, never the path alone, is what you paste into /goal." width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>Hand Claude a huge task. Come back to proof it's done — not a promise that it is.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
</p>

goalify is a Claude Code skill for work too big to babysit: a refactor, a migration, an audit. It
preps the whole run while Claude still has your context, then hands you one line to paste. Behind
that line sit a **brief** — a file holding everything the run needs (your decisions, the exact
paths, the order of work) — and a **condition** — one line that says what done must look like.
`/goal` is Claude Code's built-in stop-check: hand it a condition and the session keeps working,
judged every turn, until that condition is proven. goalify writes both pieces.

## What you get

- ⚡ **One-line handoff** — `/clear`, paste one line, walk away.
- 🧠 **Survives `/clear`** — the brief carries your decisions and context into the fresh session.
- 🔒 **Decisions locked first** — the few real choices are settled with you before the run starts.
- 📋 **Live progress** — the run keeps a task list ticking; glance at it, don't babysit it.
- ✅ **Proof-or-nothing** — the last turn has to quote the checks passing and print a made-up word
  (`ASYNC-OK` below); a run that skipped the work has to claim it outright.
- 🔁 **Nothing lost on a stop** — the brief stays put, checklist intact; you resume, not restart.
- ⏱️ **A hard turn cap** — the run ends on time; it never wanders for hours.
- 📦 **Proof, then archive** — success reruns every check in one closing turn, quotes the output,
  and files the brief into `.goal/done/` — a file move you can see in any file browser.

## Three steps

Install once, in a terminal (Claude Code 2.1.139+; more in the [quickstart](docs/quickstart.md)):

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Then, in the Claude Code chat:

```text
/goalify migrate our API to async/await
    brief      ~/acme/.goal/api-migration.md      a file — the run works from it
    condition  149 chars                          one line — you paste it below

/clear
/goal Do everything in ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

1. **Describe the job.** `/goalify` plus your task. goalify digs through your project, asks about
   the few real decisions, then writes the brief and the condition and shows you both.
2. **Clear the chat.** The run starts fresh, at full attention.
3. **Paste the condition.** The whole line — it wraps on screen, paste all of it. The brief's path
   rides along *inside* it, because the evaluator behind `/goal` can't open files; only the words
   you paste reach it. `~/acme/` stands in for your project: goalify prints this line with your
   real paths already in it.

```text v1-antipattern
# the condition itself — the exact line goalify printed (149 characters)
/goal Do everything in ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.

# not the path on its own — nothing errors; the check just becomes unprovable
/goal ~/acme/.goal/api-migration.md
```

> [!IMPORTANT]
> A run that stops is not proof it finished. The evaluator judges for itself and can end a run by
> deciding the finish line is unreachable. Before you trust a green result, reread the closing
> evidence — the quoted checks in the last reply, the brief moved into `.goal/done/` — or rerun
> the checks yourself.

## Learn more

- [Quickstart](docs/quickstart.md) — first run, install variants, headless use
- [A worked example](examples/sample-brief.md) — a real brief and the condition derived from it
- [Honest limits](docs/limits.md) — everything goalify does not promise
- [FAQ](docs/faq.md) · [Running it under Codex](docs/codex.md) · [Changelog](CHANGELOG.md) ·
  [the skill itself](skills/goalify/SKILL.md)

<p align="center"><sub><a href="assets/goalify-teaser.mp4">▶ Watch the 30-second teaser</a> · <a href="assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. `/goal` behavior
re-derived from the shipped Claude Code 2.1.223 binary, 2026.
<a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
