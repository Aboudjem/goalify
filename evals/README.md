# goalify evals

Two layers, both built test-first (RED → GREEN → REFACTOR).

## 1. Deterministic — `check_skill.py` (runs in CI)

Encodes the confirmed authoring edits as machine-checkable assertions on `SKILL.md`. It is the
regression guard: if a future edit drops the WHEN-only description, the gated archive step, a
hardened-template clause, `metadata.version`, any part of the v2 condition-string contract, or any part
of the v2.3 plain-language contract (the locked plain-words story, the short-condition default, the
`/clear` + one-line handoff, the Done/Proof/Next report, live visible progress), CI goes red.
`tests/test_manifests.py` covers the rest — manifest validity, version consistency across all four
sources, the repo-wide "no file path to `/goal`" contract, and the shipped example's clauses.

```bash
python3 evals/check_skill.py skills/goalify/SKILL.md        # GREEN: exit 0 (82/82)
git show v1.1.0:skills/goalify/SKILL.md > /tmp/v1.md \
  && mkdir -p /tmp/red/goalify && mv /tmp/v1.md /tmp/red/goalify/SKILL.md \
  && python3 evals/check_skill.py /tmp/red/goalify/SKILL.md # RED:   exit 1 (30/82)
```

The RED target is reproduced **from this repo's own git history**, so the claim is falsifiable by
anyone with a clone: the shipped v1.1.0 skill scores 30/82 against the v2, v2.3 and v2.6 assertions; the current
skill scores 82/82. (Before v2.0.0 this section pointed at a legacy `goal-prep` file outside the repo
that no longer exists, which made the headline number unverifiable — exactly the kind of unfalsifiable
baseline `CONTRIBUTING.md` tells contributors not to accept.)

## 2. Behavioral — `scenarios.md` (judged transcripts)

Four scenarios (substantial task, trivial task, several big sub-projects, a run that reaches its
turn cap), each run cold (RED) and
with the skill (GREEN) on **Haiku, Sonnet, and Opus**, scored by a separate judge against the rubric.
Recorded results: [`RED-baseline.md`](RED-baseline.md). These are v1-era (2026-05-29) and **not
reproducible** — the transcripts, judge prompt and fixture are not shipped, so treat them as a dated
record rather than evidence, and note that **no behavioral baseline exists yet for the v2.0.0 or
v2.3.0 clauses**. S1 went RED 3–4/7 → **GREEN 7/7 on all
three models**; S2 declines (3/3); S3 splits (3/3).

To re-run the behavioral suite, prompt each model twice for each scenario in `scenarios.md` — once with
no skill, once with `skills/goalify/SKILL.md` active — against a real target (for S1, a small Express
repo with a test suite makes the authoring dimensions fairly testable) and score each transcript
against the rubric.
