# goalify — recorded RED→GREEN baseline

> The evidence that each part of the skill fixes a real, observed failure. Skills are built
> test-first (RED → GREEN → REFACTOR): watch the failure happen *without* the skill, write the
> minimum that fixes it, prove it now behaves. This file records the baselines so a future change
> can't quietly regress them. Recorded **2026-05-29** on this machine.

## 1. Deterministic check (`check_skill.py`) — the artifact-level RED→GREEN

`check_skill.py` encodes the confirmed authoring edits as 25 pass/fail assertions and runs in CI.
Pointed at the **legacy `goal-prep`** SKILL.md vs the **improved `goalify`** SKILL.md:

| Target | Result |
|---|---|
| `~/.claude/skills/goal-prep/SKILL.md` (legacy, RED) | **7 / 25 pass** — missing `metadata.version`, WHEN-only/disambiguated description, the `goalify` trigger, the capability+fallback for tool fan-out, every hardened-template clause (output-redirection, anti-placeholder, search-before-assuming, machine-checkable criteria, progress checklist, just-in-time identifiers, serialize-builds guardrail, separate-agent verification, commit-before-risky, re-read-each-loop), the LOW-freedom gated self-destruct, and the never-run-`/clear`-yourself rule. |
| `skills/goalify/SKILL.md` (improved, GREEN) | **25 / 25 pass** |

Reproduce:
```bash
python3 evals/check_skill.py ~/.claude/skills/goal-prep/SKILL.md   # exit 1 (RED, 7/25)
python3 evals/check_skill.py skills/goalify/SKILL.md               # exit 0 (GREEN, 25/25)
```

## 2. Behavioral RED→GREEN on Haiku, Sonnet, and Opus

Each scenario was run twice per model — once **cold** (no skill, RED) and once with `goalify` active
(GREEN) — and scored by a **separate** Opus judge against the scenario rubric (never self-approved).
Scenarios and rubrics are in [`scenarios.md`](scenarios.md).

### Scenario 1 — substantial task (migrate a real callback-style Express API to async/await)

Run against a real fixture repo (`/tmp/goalify-eval-fixture`: Express 4, callback handlers, a
`node --test` suite) so the authoring dimensions were achievable and the inspection was real.

| Model | RED (no skill) | GREEN (goalify) |
|---|---:|---:|
| Haiku  | 3 / 7 | **7 / 7** |
| Sonnet | 4 / 7 | **7 / 7** |
| Opus   | 3 / 7 | **7 / 7** |

- **RED misses (all models):** no self-contained `/goal` MD authored, no absolute-path file with a
  gated self-destruct, no `/clear` + `/goal` handoff. (RED models *did* stay in PREPARE and inspect
  with evidence — the baseline isn't reckless, it just doesn't produce the durable, resumable,
  self-deleting handoff artifact the skill guarantees.)
- **GREEN (every model):** stayed in PREPARE; inspected the repo with cited evidence (real
  `src/server.js`, `orders.js`, `test/orders.test.js`); authored a self-contained `/goal` MD at an
  absolute path with a gated low-freedom self-destruct; success criteria wired to a named command
  (`npm test` / `node --test`); printed the `/clear` then `/goal <abs-path>` handoff and stopped; did
  not over-ask. `green_beats_red_each_model: true`.

### Scenario 2 — trivial task (fix one typo) → must decline

GREEN (Sonnet): **3 / 3** — recognized the task is too small for a `/goal` file, declined to author an
MD, offered to just do it, fabricated no phases or research.

### Scenario 3 — three big independent sub-projects → must split

GREEN (Sonnet): **3 / 3** — recognized the work won't fit one fresh session and proposed the split
(shared STANDARDS md + one md per sub-project + a final ALIGN md), each self-contained,
absolute-path'd, and self-deleting.

## 3. The earlier "false-premise" run (kept as a note, not a failure)

An initial S1 run pointed the prompt at "this repo" while the eval agents' working dir was *not* an
Express project. GREEN Sonnet/Opus **correctly refused to fabricate a goal MD**, inspected with
evidence, found no Express API, and asked the single genuine clarifying question — i.e. the skill's
no-hallucination rule fired exactly as intended. The fixture run above replaced it so the authoring
dimensions were fairly testable. Worth keeping in mind: a high score on the authoring rubric is only
correct when the target actually exists; declining is the right answer when it doesn't.
