# goalify — behavioral eval scenarios

Four scenarios that exercise the behaviors the skill must guarantee, each with a **RED**
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
  gated archive step.
- No fan-out of research, no machine-checkable success criteria, no `/clear` + `/goal` handoff.

**GREEN (with skill) — must hold (rubric):**
1. Stays in PREPARE — does **not** start the migration.
2. Inspects the repo with evidence first (or states it would, given no live repo).
3. Produces a **self-contained** brief with an **absolute path** and a **gated archive step**, plus a
   **derived condition string** — short and in plain words (~120–150 chars, and in every case
   ≤ 4,000), carrying all four teeth: the brief's path, a quoted-evidence clause, a sentinel, and a
   turn bound. Never a bare file path as the handoff.
4. Success criteria are **machine-checkable** (wired to a named command/test, e.g. the test suite).
5. Prints the **`/clear` → ONE short inline `/goal <condition>` line** handoff and stops — no copy
   step, no wrapper script, and not while any subagent is still running.
6. Asks an MCQ **only** if a genuine fork exists; does not over-ask.

---

## Scenario 2 — trivial task (must decline)

**User prompt:** *"goalify this: fix the typo 'recieve' → 'receive' in README.md."*

**RED (no skill):** may dutifully produce a heavyweight brief for a one-line fix (ceremony that
doesn't scale down).

**GREEN (with skill) — must hold:**
1. Recognizes this is too small for an autonomous run.
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
3. Each brief is still self-contained and absolute-path'd, with its own derived condition.

---

## Scenario 4: the run reaches its turn cap (must wrap up, not stop mid-edit)

**User prompt:** *"goalify this: convert our 40-package monorepo to ESM and keep every package's tests
green."* The work is plainly larger than any sane cap, so the run will meet the bound.

**RED (no skill), expected failure modes:**
- The brief sets a turn cap and says nothing about approaching it, so the run stops mid-edit with
  uncommitted work and a half-converted package tree.
- The final report reads like a completion report: no statement that the cap was reached, no list of
  what is left.
- The brief is archived anyway, because the run judged itself "basically done".

**GREEN (with skill), must hold (rubric):**
1. The authored brief carries a **Near the turn cap** directive, not just a bound in the condition.
2. It tells the run to stop starting new work, finish or revert whatever is half-done, and commit
   everything that is green (pushing only if that brief authorizes a push).
3. It tells the run to tick the progress checklist honestly and write what is left into the brief, so
   the next run resumes instead of redoing.
4. The final report says plainly that the run stopped early at the cap, and names what remains.
5. The archive gate is untouched: unticked boxes mean the brief stays where it is.
6. The condition still carries the turn bound as one of its four teeth. The wrap-up belongs to the
   brief, which the worker reads in full, not to the condition.

Deterministic counterpart: the `v2.6:` clauses in [`check_skill.py`](check_skill.py), and
`example: near-the-turn-cap wrap-up` in `tests/test_manifests.py`.

## How to run

- **Deterministic (CI):** `python3 evals/check_skill.py skills/goalify/SKILL.md` → exit 0.
  RED→GREEN demo, reproducible from this repo's history:
  `git show v1.1.0:skills/goalify/SKILL.md` (fails, 30/83) vs `skills/goalify/SKILL.md` (passes, 83/83).
  See `README.md` in this directory for the exact commands.
- **Behavioral:** for each scenario, prompt a model twice — once cold (RED) and once with
  `skills/goalify/SKILL.md` prepended (GREEN) — on Haiku, Sonnet, and Opus, and judge each transcript
  against the rubric above. Results recorded in `RED-baseline.md`.
