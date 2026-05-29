<p align="center">
  <img src="assets/hero.svg" alt="goalify — an arrow landing in a bullseye: prepare a /goal file, then hit the goal in a fresh Claude Code session" width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>Aim your big Claude Code run before you fire it.</strong><br>
  goalify researches the task, asks you the few real decisions, and writes one self-contained,
  self-deleting <code>/goal</code> file you <code>/clear</code> and run in a fresh, full-context session.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-7c5cff" alt="Agent Skills compatible"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome"></a>
</p>

---

You type one line. goalify hands you two:

```text
you  ▸  goalify this: migrate our API from callbacks to async/await, keep tests green
       ┊ (goalify researches the repo, asks ~1 real question, writes the file)
goalify ▸  1.  /clear
           2.  /goal /Users/you/project/.goal/api-migration.md
```

> [!IMPORTANT]
> goalify **prepares** the run; it doesn't run your task. You run it (in a fresh session), and the file deletes itself once the run succeeds.

## The problem it solves

Big autonomous runs rot as the context window fills. The worst moment is the handoff: you plan, you `/clear` for a clean session, and your plan is gone. goalify does the research and the decisions **now**, writes them to one file, and that fresh session reads it at full context, then runs the task at maximum effort and cleans up after itself.

## Install

It's a skill — no plugin required. Drop it in:

```bash
git clone https://github.com/Aboudjem/goalify
mkdir -p ~/.claude/skills
cp -r goalify/skills/goalify ~/.claude/skills/goalify
```

Then say **`goalify this: <your task>`** in Claude Code. It triggers on its own.

## What you get

One `/goal` file — [see a real one](examples/sample-goal-file.md):

- **A declarative spec:** the end state and how it's verified, not a brittle recipe.
- **Verified, cited context** with absolute paths, so the fresh session is never lost.
- **Machine-checkable success criteria** wired to real commands, so the run knows when it's done.
- **Max-effort + fan-out directives**, a progress checklist, and a **gated self-destruct** that deletes only on full success (and survives to resume otherwise).

## goalify vs. winging it

| | goalify | A cold `/goal` from memory | Prompting by hand |
|---|:--:|:--:|:--:|
| Plan survives `/clear` | ✅ | ❌ | ❌ |
| Runs at full context | ✅ | ✅ | ❌ |
| Research done + cited first | ✅ | ❌ | rarely |
| Knows when it's done | ✅ | depends | depends |
| Cleans up after itself | ✅ | ❌ | — |

## Why you can trust it

- **No hallucination:** every load-bearing fact is cited; a separate agent re-derives the key claims.
- **Tested:** built test-first, RED→GREEN on Haiku, Sonnet, and Opus ([the baseline](evals/RED-baseline.md)).
- **Safe:** read-mostly prep, a gated self-destruct, no remote fetch-and-execute ([SECURITY](SECURITY.md)).

## FAQ

**Does it run my task?** No. It writes the `/goal` file; you run it after `/clear`, in a fresh session. That separation is the point.

**Why a file instead of just prompting?** The plan has to survive `/clear`. A file persists, carries absolute paths and cited research, and the run re-reads it every loop. A chat plan can't.

<details>
<summary>More questions</summary>

**What if it can't finish?** The self-destruct is gated: if any success criterion is unmet, the file stays put so you can resume from it.

**Does it work outside Claude Code?** It's a spec-correct [Agent Skill](https://agentskills.io), [portable across agents that support the standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills). The `/clear` + `/goal` handoff is Claude-Code-specific; adapt those two commands on another agent.

**When should I *not* use it?** A one-line fix (just ask Claude), or open-ended exploration with no definable end state. goalify will decline.
</details>

## How it works

<p align="center">
  <img src="assets/how-it-works.svg" alt="How it works: 1 prepare — research and decide; 2 hand off — author a self-contained, self-deleting /goal file; 3 run autonomously in a fresh session" width="100%">
</p>

The skill lives in [`skills/goalify/SKILL.md`](skills/goalify/SKILL.md) (two-phase PREPARE → EXECUTE model, the goal-file template, hard rules). Evals are in [`evals/`](evals); first run, the [quickstart](docs/quickstart.md).

## Contributing & license

Issues and PRs welcome. goalify is built test-first ([CONTRIBUTING](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)). [MIT](LICENSE).

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. Verified against Claude Code and the Agent Skills spec, 2026. <a href="https://github.com/Aboudjem/goalify/issues">Spot a gap?</a></sub>
