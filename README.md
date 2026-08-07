<p align="center">
  <img src="assets/hero.svg" alt="goalify writes a brief (a file) and a condition (a line); the condition, not the path, is what you paste into /goal." width="100%">
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

goalify is a Claude Code skill for jobs too big to sit and watch: renaming one thing across hundreds
of files, moving an old project onto a newer version of the code it is built on, going through a
messy project to clean up one kind of problem. You describe the job. goalify writes down what the
run — the session that does the work — has to do, and what done has to look like, while Claude
still has your context, then hands you one line to paste.

It writes two things. A **brief** — a file holding everything the run needs: your decisions, the
exact paths, the order of work. And a **condition** — one line you paste into `/goal`, Claude Code's
built-in stop-check, which keeps the session working and judges every turn until that line is proven.
Picture a building site: the brief is the plans a builder works from, and the condition is the
checklist an inspector signs off against. The inspector never reads the plans and never visits the
site — they judge only the evidence the builder shows them.

## What you get

- ⚡ **One line to hand over** — clear the chat, paste one line, walk away.
- 🧠 **Your context survives the reset** — the brief carries your decisions into the fresh session.
- 🔒 **Decisions settled first** — the few real choices get made with you, before the run starts.
- 📋 **Progress you can glance at** — the run ticks off a task list as it goes; no hovering needed.
- ✅ **Proof, not a promise** — the last turn has to quote the checks passing and print a made-up word (`ASYNC-OK` below); a run that skipped the work has to claim it outright.
- 🔁 **A stop costs you nothing** — the brief stays put, checklist intact; you resume, not restart.
- ⏱️ **A hard turn limit** — a cap on how many replies the run gets; it ends on time.
- 📦 **Proof, then filing** — success reruns every check in one closing turn, quotes the output, and moves the brief into `.goal/done/` — a file move you can see in any file browser.

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

1. **Describe the job.** `/goalify` plus your task. goalify reads your project, asks about the few
   real decisions, then writes the brief and the condition and shows you both.
2. **Clear the chat.** `/clear` wipes the conversation, so the run starts fresh, at full attention.
3. **Paste the condition.** The whole line — it wraps on screen, so grab all of it. The brief's path
   rides along *inside* it, because the evaluator behind `/goal` — the judge that decides each turn
   whether you are done — has no tools and cannot open files. Only the words you paste reach it.
   `~/acme/` stands in for your project: goalify prints this line with your real paths already in it.

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

- [Quickstart](docs/quickstart.md) — your first run, other ways to install, running without a terminal
- [A worked example](examples/sample-brief.md) — a real brief and the condition derived from it
- [Honest limits](docs/limits.md) — everything goalify does not promise
- [FAQ](docs/faq.md) · [Under Codex](docs/codex.md) · [Changelog](CHANGELOG.md) · [The skill itself](skills/goalify/SKILL.md)

<p align="center"><sub><a href="assets/goalify-teaser.mp4">▶ Watch the 28-second teaser</a> · <a href="assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. `/goal` behavior re-derived
from the shipped Claude Code 2.1.223 binary, 2026. <a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
