# goalify evals

Two layers, both built test-first (RED → GREEN → REFACTOR).

## 1. Deterministic — `check_skill.py` (runs in CI)

Encodes the confirmed authoring edits as machine-checkable assertions on `SKILL.md`. It is the
regression guard: if a future edit drops the WHEN-only description, the gated self-destruct, a
hardened-template clause, `metadata.version`, etc., CI goes red.

```bash
python3 evals/check_skill.py skills/goalify/SKILL.md        # GREEN: exit 0 (29/29)
python3 evals/check_skill.py path/to/legacy/SKILL.md        # RED:   exit 1
```

Pointed at the legacy `goal-prep` skill it scores 7/29; pointed at `goalify` it scores 29/29 — the
artifact-level RED→GREEN.

## 2. Behavioral — `scenarios.md` (judged transcripts)

Three scenarios (substantial task, trivial task, several big sub-projects), each run cold (RED) and
with the skill (GREEN) on **Haiku, Sonnet, and Opus**, scored by a separate judge against the rubric.
Recorded results: [`RED-baseline.md`](RED-baseline.md). Latest: S1 went RED 3–4/7 → **GREEN 7/7 on all
three models**; S2 declines (3/3); S3 splits (3/3).

To re-run the behavioral suite, prompt each model twice for each scenario in `scenarios.md` — once with
no skill, once with `skills/goalify/SKILL.md` active — against a real target (for S1, a small Express
repo with a test suite makes the authoring dimensions fairly testable) and score each transcript
against the rubric.
