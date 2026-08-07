# goalify — recorded RED→GREEN baseline

> The evidence that each part of the skill fixes a real, observed failure. Skills are built
> test-first (RED → GREEN → REFACTOR): watch the failure happen *without* the skill, write the
> minimum that fixes it, prove it now behaves. This file records the baselines so a future change
> can't quietly regress them. §1 records the current baseline (re-measured **2026-08-07** at v2.5.0)
> and the original v1.0.0 one (**2026-05-29**); §2 and §3 are the v1-era behavioral runs, recorded
> **2026-05-29**.

## 1. Deterministic check (`check_skill.py`) — the artifact-level RED→GREEN

`check_skill.py` encodes the confirmed authoring edits as pass/fail assertions and runs in CI.

### Current — 78 assertions (recorded 2026-08-06 at v2.3.0; re-measured 2026-08-07 at v2.5.0)

The RED target is **this repo's own v1.1.0 skill**, reproduced from git history, so anyone with a
clone can falsify the number. v1.1.0 shipped the `/goal <file-path>` handoff <!-- v1-antipattern -->, which the tool-less
evaluator can never verify; the 49 assertions it fails are the v2 condition-string contract plus the
plain-language contract (two story assertions were re-pinned to the v2.4 wording, which moved the
RED score from the 30/78 recorded at v2.3.0 to the 29/78 measured today).

| Target | Result |
|---|---|
| `git show v1.1.0:skills/goalify/SKILL.md` (RED) | **29 / 78 pass** — fails every v2 assertion: no condition-string handoff, a file-path handoff present, no derivation from a definition of done, no 4,000-char lint, no sentinel, no closeout-turn rule, no freshly-quoted-evidence rule, no turn bound, no bare-`$` lint, no tool-less-evaluator documentation, no subagent barrier, no model routing, no dry-run/caps, no rule against inventing a predicted cost, no 3-strike ladder, no archive gate, no `--permission-mode auto`, no headless form, no "not proof of completion" caveat, no verify-only re-check, no Codex cross-harness section, no untrusted-demotion note, no definition-of-done / process-directive split. And every v2.3 assertion: no plain-words story in the description or the overview, no short-condition default, no ceiling-not-a-target framing, no canonical worked example, no four-teeth rule, no short-read lint, no rule keeping process directives out of the condition, no `/clear` + one-line handoff, no ban on a launcher or wrapper, no Done/Proof/Next report requirement, no ban on long paragraphs, no stopped-run caveat inside the template, no live-visible-progress requirement (template or PREPARE), no `in_progress → completed` rule, no read-the-deliverable-from-disk rule, no never-hand-off-while-live rule, no brief-is-a-file / condition-is-a-string vocabulary lock. |
| `skills/goalify/SKILL.md` (v2.5.0, GREEN) | **78 / 78 pass** |

Reproduce:
```bash
git show v1.1.0:skills/goalify/SKILL.md > /tmp/v1.md
mkdir -p /tmp/red/goalify && mv /tmp/v1.md /tmp/red/goalify/SKILL.md
python3 evals/check_skill.py /tmp/red/goalify/SKILL.md   # exit 1 (RED, 29/78)
python3 evals/check_skill.py skills/goalify/SKILL.md     # exit 0 (GREEN, 78/78)
```

The RED number is unchanged from the v2.1.0 recording (30) because v1.1.0 passes none of the 22 new
assertions — the delta is entirely in the denominator. One pre-existing assertion was **tightened**
rather than added: `handoff does NOT make pbcopy the required step` now also requires the handoff to
ban the copy step outright, not merely demote it. v1.1.0 failed it before and fails it now.

### v1.0.0 (recorded 2026-05-29) — 29 assertions, historical

The original baseline compared against a legacy `goal-prep` skill that lived at
`~/.claude/skills/goal-prep/SKILL.md`, outside this repo.

| Target | Result |
|---|---|
| `~/.claude/skills/goal-prep/SKILL.md` (legacy, RED) | **7 / 29 pass** — missing `metadata.version`, WHEN-only/disambiguated description, the `goalify` trigger, the capability+fallback for tool fan-out, every hardened-template clause (output-redirection, anti-placeholder, search-before-assuming, machine-checkable criteria, progress checklist, just-in-time identifiers, serialize-builds guardrail, separate-agent verification, commit-before-risky, re-read-each-loop, the maximum-effort directive, a portable max-effort mode), the LOW-freedom gated self-destruct, the never-run-`/clear`-yourself rule, a self-explanatory `argument-hint`, and a documented `$ARGUMENTS`/`/goalify` invocation. |
| `skills/goalify/SKILL.md` (v1.0.0, GREEN) | **29 / 29 pass** |

> **This one is no longer reproducible.** That legacy file has since been removed from the machine it
> was recorded on, so the 7/29 figure cannot be re-derived by a reader — it is kept as a dated record,
> not as evidence. The v2 baseline above replaces it precisely because it *is* reproducible from git.

## 2. Behavioral RED→GREEN on Haiku, Sonnet, and Opus

> **Same reproducibility caveat as the retired 7/29 figure above.** These are LLM-judged transcripts
> from 2026-05-29; the transcripts and judge prompt are not shipped and the fixture at
> `/tmp/goalify-eval-fixture` is gone, so a reader cannot re-derive these numbers. They are kept as a
> dated record, not as evidence. **No behavioral baseline has been recorded for the v2.0.0 or v2.3.0
> clauses** — §1's table is a static re-scoring of the v1.1.0 file, which is a regression diff, not an
> observed model failure. Recording one is the top open task for the next release. The S1 rubric in
> `scenarios.md` was also reworded for v2.3.0 (short plain condition; one-line handoff; no hand-off
> while a subagent is live) without changing the number of dimensions, so the `/7` figures below were
> scored against the v1-era wording of those same dimensions.

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

- **RED misses (all models):** no self-contained brief authored, no absolute-path file with a
  gated self-destruct, no `/clear` + `/goal` handoff. (RED models *did* stay in PREPARE and inspect
  with evidence — the baseline isn't reckless, it just doesn't produce the durable, resumable handoff
  artifact the skill guarantees. *v1-era wording: at the time this was recorded that artifact deleted
  itself; since v2.0.0 it is archived instead.*)
- **GREEN (every model):** stayed in PREPARE; inspected the repo with cited evidence (real
  `src/server.js`, `orders.js`, `test/orders.test.js`); authored a self-contained brief at an
  absolute path with a gated low-freedom self-destruct; success criteria wired to a named command
  (`npm test` / `node --test`); printed the `/clear` then the v1 file-path handoff and stopped; did
  not over-ask. `green_beats_red_each_model: true`. (That handoff step is exactly what v2.0.0 replaced
  with a derived condition string — the rubric dimension survived, the syntax it scored did not.)

### Scenario 2 — trivial task (fix one typo) → must decline

GREEN (Sonnet): **3 / 3** — recognized the task is too small for an autonomous run, declined to author an
MD, offered to just do it, fabricated no phases or research.

### Scenario 3 — three big independent sub-projects → must split

GREEN (Sonnet): **3 / 3** — recognized the work won't fit one fresh session and proposed the split
(shared STANDARDS md + one md per sub-project + a final ALIGN md), each self-contained,
absolute-path'd, and self-deleting. *(v1-era: those files are archived, not deleted, since v2.0.0.)*

## 3. The earlier "false-premise" run (kept as a note, not a failure)

An initial S1 run pointed the prompt at "this repo" while the eval agents' working dir was *not* an
Express project. GREEN Sonnet/Opus **correctly refused to fabricate a goal MD**, inspected with
evidence, found no Express API, and asked the single genuine clarifying question — i.e. the skill's
no-hallucination rule fired exactly as intended. The fixture run above replaced it so the authoring
dimensions were fairly testable. Worth keeping in mind: a high score on the authoring rubric is only
correct when the target actually exists; declining is the right answer when it doesn't.
