# goalify — behavioral eval scenarios

Three scenarios that exercise the behaviors the skill must guarantee, each with a **RED**
expectation (what a model does *without* the skill) and a **GREEN** expectation (what it must do
*with* the skill). Run each scenario both ways, on **Haiku, Sonnet, and Opus** — the skill must hold
on cheaper models and under pressure, not just on the strongest one. Recorded RED→GREEN results live
in [`RED-baseline.md`](RED-baseline.md).

Scoring is behavioral (LLM-judged against the rubric) — the deterministic, in-CI half of the suite is
[`check_skill.py`](check_skill.py).

---

## Scenario 1 — substantial task (the core case)

**User prompt:** *"goalify this: migrate our Express API in this repo from callbacks to async/await,
keep behavior identical, and make sure the test suite still passes."*

**RED (no skill) — expected failure modes:**
- Starts editing code / proposes diffs immediately, instead of preparing a handoff file.
- Produces a plan that lives only in the chat (lost on `/clear`), with no absolute path and no
  self-destruct.
- No fan-out of research, no machine-checkable success criteria, no `/clear` + `/goal` handoff.

**GREEN (with skill) — must hold (rubric):**
1. Stays in PREPARE — does **not** start the migration.
2. Inspects the repo with evidence first (or states it would, given no live repo).
3. Produces a **self-contained** `/goal` MD with an **absolute path** and a **gated self-destruct**.
4. Success criteria are **machine-checkable** (wired to a named command/test, e.g. the test suite).
5. Prints the **`/clear` then `/goal <abs-path>`** handoff and stops.
6. Asks an MCQ **only** if a genuine fork exists; does not over-ask.

---

## Scenario 2 — trivial task (must decline)

**User prompt:** *"goalify this: fix the typo 'recieve' → 'receive' in README.md."*

**RED (no skill):** may dutifully produce a heavyweight `/goal` file for a one-line fix (ceremony that
doesn't scale down).

**GREEN (with skill) — must hold:**
1. Recognizes this is too small for a `/goal` file.
2. Declines to author an MD and says so (offers to just do it / that no handoff is needed).
3. Does not fabricate phases or research for a trivial change.

---

## Scenario 3 — several big independent sub-projects (must split)

**User prompt:** *"goalify this: (1) build a new billing microservice, (2) rewrite the marketing site,
and (3) migrate the data warehouse — these are independent and each is large."*

**GREEN (with skill) — must hold:**
1. Recognizes the work won't fit one fresh session.
2. Proposes the split structure: a shared **STANDARDS** MD + **one MD per sub-project** + a final
   **ALIGN** MD (run last), per the one-vs-several flowchart.
3. Each MD is still self-contained, absolute-path'd, and self-deleting.

---

## How to run

- **Deterministic (CI):** `python3 evals/check_skill.py skills/goalify/SKILL.md` → exit 0.
  RED→GREEN demo: run it against the legacy `goal-prep/SKILL.md` (fails) vs `goalify/SKILL.md` (passes).
- **Behavioral:** for each scenario, prompt a model twice — once cold (RED) and once with
  `skills/goalify/SKILL.md` prepended (GREEN) — on Haiku, Sonnet, and Opus, and judge each transcript
  against the rubric above. Results recorded in `RED-baseline.md`.
