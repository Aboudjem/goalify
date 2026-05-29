<p align="center">
  <img src="assets/hero.svg" alt="goalify — prepare a researched, self-deleting /goal file you run after /clear in a fresh session" width="100%">
</p>

<h1 align="center">goalify</h1>

<p align="center">
  <strong>Plan your big Claude Code run <em>before</em> you <code>/clear</code>, not after. goalify researches the task, asks you the few real decisions, and writes one self-contained, self-deleting <code>/goal</code> file you launch in a fresh, full-context session.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-7c5cff" alt="Agent Skills compatible"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome"></a>
</p>

---

## What is this?

It is a [Claude Code](https://www.claude.com/product/claude-code) skill that **prepares the run, so the run goes well.**

Long autonomous tasks degrade as the context window fills, and the hardest moment is the handoff: after you plan, you `/clear` to get a clean session, and the plan is gone. (Anthropic's own tracker has this as an open question: [*"Best practice for plan-to-implementation context handoff across `/clear`?"*](https://github.com/anthropics/claude-code/issues/32916).)

goalify closes that gap. You say *"goalify this: &lt;big task&gt;"*. It reads your project, fans out research, asks you only the decisions it genuinely can't infer, and writes **one self-contained Markdown file**: a verified, right-sized execution spec with hard rules baked in. Then it hands you two commands: `/clear`, then `/goal <path>`. A fresh session runs the task at full context and **deletes the file when it's done.**

**What is a `/goal` prep?** A short, interactive pass that researches a task, locks the few real decisions, and writes a single execution file you run after `/clear`, so the work happens in a clean session instead of a context-starved one.

It only prepares the file. It does not run your task — you do, in the fresh session. And it cleans up after itself.

## Why you'd want it

Without goalify, a big run looks like this: you think out loud, you `/clear` to free up context, then you improvise a vague prompt from memory. Then you babysit it as it drifts, stubs things out, and forgets the rules halfway through.

With goalify: the research is done and cited, the real decisions are locked, the success criteria are machine-checkable, and the plan lives in a file the fresh session reads at 100% context. One file, one run, then gone. No spec rotting in your repo.

## Install

Pick whichever you prefer. Both install the same skill.

**As a Claude Code plugin:**

```text
/plugin marketplace add Aboudjem/goalify
/plugin install goalify@goalify
```

**As a drop-in skill** (no plugin system):

```bash
git clone https://github.com/Aboudjem/goalify
cp -r goalify/skills/goalify ~/.claude/skills/goalify
```

## Use it in 3 steps

1. **Install it** (above).
2. **Ask Claude:** *"goalify this: &lt;your big task&gt;"* — e.g. *"goalify this: migrate our Express API from callbacks to async/await and keep the tests green."* The skill turns on by itself.
3. **Answer the short MCQ** (only if there's a real fork), then **copy the two commands it prints:** `/clear`, then `/goal <path>`.

That's the whole thing. Nothing in your repo changes while it prepares; it only researches and writes the plan. The work happens in the fresh `/goal` session.

<p align="center">
  <img src="assets/how-it-works.svg" alt="How it works: 1 prepare — research and decide; 2 hand off — author a self-contained, self-deleting /goal file; 3 run autonomously in a fresh full-context session" width="100%">
</p>

## What you get

A single `/goal` file, ready to run. See a real one: [`examples/sample-goal-file.md`](examples/sample-goal-file.md).

- **A declarative spec**, not a brittle recipe: the desired end state and how it's verified.
- **Verified context with absolute paths**, so the fresh session is never lost.
- **Your locked decisions**, captured once so they aren't re-litigated mid-run.
- **Dependency-ordered phases** that say which work fans out in parallel and which must serialize (builds, tests, same-file writes).
- **Machine-checkable success criteria**, each wired to a named command or test, so the run knows when it's actually done.
- **A copyable progress checklist** the run ticks off, and a **gated self-destruct** that deletes the file only on full success (and leaves it to resume otherwise).

## Why you can trust it

goalify's whole job is a reliable autonomous run, so the generated file is built around rules it won't break:

1. **No hallucination.** Every load-bearing fact is verified against a primary source, cited, and labeled by confidence. A separate agent re-derives the key claims, never from another agent's summary.
2. **It asks only the genuine decisions.** One short MCQ for the real forks, then it gets out of the way. No interrogation.
3. **Full implementations only.** The run is told not to ship placeholders or stubs to make something pass, and to search before assuming code is missing.
4. **It knows when it's done.** Success criteria are pass/fail and wired to commands — not "looks good."
5. **It cleans up.** The file deletes itself only when every criterion holds; if the run can't finish, the file survives so you can resume.

These rules exist because autonomous runs reliably break them: they drift, stub, and forget instructions as context fills. The skill is validated test-first: see the recorded [RED→GREEN baseline](evals/RED-baseline.md), where a model *with* goalify went from a throwaway chat plan to a complete, self-deleting, machine-checkable handoff on Haiku, Sonnet, and Opus.

## How it compares

| | goalify | A cold `/goal` from memory | Prompting by hand each turn |
|---|---|---|---|
| Survives `/clear` (plan lives in a file) | Yes | No | No |
| Fresh session runs at full context | Yes | Yes | No (context fills as you go) |
| Research done + cited before the run | Yes | No | Rarely |
| Success criteria machine-checkable | Yes | Depends on you | Depends on you |
| Asks only the real decisions | Yes (one MCQ) | No | Ad hoc |
| Cleans up after itself | Yes (self-deletes) | No | n/a |
| Runs the task itself | No — you do, fresh | n/a | You do, in place |

goalify isn't a rival to autonomous loops. It's the front door to them: the file it writes is exactly the pre-validated spec that `/goal`, `ralph`, or an `autopilot`-style loop wants as input.

## FAQ

**How do I set up a big autonomous run in Claude Code?**
Install goalify and say *"goalify this: &lt;your task&gt;"*. It researches, asks the few real decisions, and writes one self-contained `/goal` file. Then run `/clear` and `/goal <path>`; a fresh session executes the task at full context and deletes the file when every success criterion is met.

**Does it run the task itself?**
No. goalify prepares the handoff file; you run it (after `/clear`) in a fresh session. That separation is the point: the execute session starts clean.

**Why prepare a file instead of just prompting?**
Because the plan needs to survive `/clear`. A file persists independently of the conversation, carries absolute paths and cited research, and can be re-read every loop; a chat plan can't.

**Why does the file delete itself?**
To kill drift and clutter. It's single-use. It self-destructs only on full success; if the run can't finish, the file stays so you can resume.

**What if it can't finish?**
The self-destruct is gated. If any success criterion is unmet, the file is left in place and the run can be resumed from it.

**Does it work outside Claude Code?**
The skill is a spec-correct [Agent Skill](https://agentskills.io) (`name` + `description` frontmatter + Markdown), an open standard that is [portable across agents that support it](https://code.visualstudio.com/docs/copilot/customization/agent-skills). The `/clear` + `/goal` handoff phrasing is Claude-Code-specific, so on another agent you adapt those two commands.

## How it works under the hood

The skill is in [`skills/goalify/SKILL.md`](skills/goalify/SKILL.md): a two-phase PREPARE → EXECUTE model, the procedure, the goal-MD template (with all the run-hardening clauses), the one-vs-several decision flowchart, the handoff format, and the hard rules. Heavier detail loads only when needed.

Evals live in [`evals/`](evals): a deterministic check that runs in CI plus behavioral scenarios validated on Haiku, Sonnet, and Opus.

## Contributing

Issues and PRs are welcome. The one firm rule: goalify is built test-first, so a change that adds behavior needs the failing baseline it fixes. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE). Use it, fork it, ship it.

---

<sub>Built and maintained by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. Verified against Claude Code and the Agent Skills spec in 2026. Spot a gap? <a href="https://github.com/Aboudjem/goalify/issues">Open an issue</a>.</sub>
