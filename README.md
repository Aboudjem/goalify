<p align="center">
  <img src="assets/hero.svg" alt="goalify writes a brief file and a condition line; the condition, never the path alone, is what you paste into /goal." width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>You describe a big coding job. goalify writes the instructions the AI works from, and the finish line it has to prove it reached.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
</p>

Hand an AI a big job — a refactor, a migration, an audit — and two things tend to go wrong:
everything you scoped together disappears when the chat is cleared, and when the work stops you
can't tell whether it finished or just stopped talking. goalify, a skill for
[Claude Code](https://code.claude.com/docs/en/goal), closes both gaps by writing the job down as
two pieces: a **brief** — a file holding everything the run needs (your decisions, the exact paths,
the order of work) — and a **condition** — one line saying what must be true, on screen, before the
run may call itself done. The whole handoff, typed in the Claude Code chat:

```text
/goalify migrate our API to async/await
    brief      ~/acme/.goal/api-migration.md      a file — the run works from it
    condition  149 chars                          one line — you paste it below

/clear
/goal Do everything in ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

It wraps on screen, but that last line is one line — you paste all of it. `~/acme/` stands in for
your own project: goalify prints this line with your real paths already in it, and that printed
line is what you paste. (The printout above is abridged.)

## Three steps

Install once, in a terminal (Claude Code 2.1.139+; more in the [quickstart](docs/quickstart.md)):

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

1. **Describe the job.** Back in the Claude Code chat, `/goalify` plus your task — goalify
   inspects your project, asks about the few real decisions, then writes the brief and the
   condition and shows you both.
2. **Clear the chat.** `/clear` — the job starts fresh, at full attention, and the brief carries
   everything across.
3. **Paste the condition.** The whole line, exactly as printed. The brief's path rides along
   *inside* it, because the automated judge behind `/goal` — the evaluator — can't open files;
   only the words you paste ever reach it.

```text v1-antipattern
# paste the condition itself — the exact line goalify printed (149 characters here)
/goal Do everything in ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.

# not the path on its own — nothing errors; the check just becomes unprovable
/goal ~/acme/.goal/api-migration.md
```

While it runs you can watch the steps tick by — the brief tells the run to keep a live task list —
and the condition caps the job (40 turns above; a turn is one reply from the AI). `ASYNC-OK` is a
made-up word the condition requires the run to print, so a run that skipped the work has to claim
it outright rather than trail off. The brief also requires a closing turn that reruns every check
and quotes the output where you (and the evaluator) can see it. When the run proves out, the brief
moves itself into `.goal/done/` — a file move you can see in any file browser; otherwise it stays
put, checklist intact, so you can resume.

> [!IMPORTANT]
> A run that stops is not proof it finished. The evaluator applies its own judgment and can end a
> run by deciding the finish line is unreachable — no wording prevents that. Before you believe a
> green result, reread the closing evidence — the quoted checks in the last reply, the brief moved
> into `.goal/done/` — or rerun the checks yourself.

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
