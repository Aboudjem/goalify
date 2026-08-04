# goalify evals

Two layers, both built test-first (RED → GREEN → REFACTOR).

## 1. Deterministic — `check_skill.py` (runs in CI)

Encodes the confirmed authoring edits as machine-checkable assertions on `SKILL.md`. It is the
regression guard: if a future edit drops the WHEN-only description, the gated archive step, a
hardened-template clause, `metadata.version`, or any part of the v2 condition-string contract, CI goes
red. `tests/test_manifests.py` covers the rest — manifest validity, version consistency across all four
sources, the repo-wide "no file path to `/goal`" contract, and the shipped example's clauses.

```bash
python3 evals/check_skill.py skills/goalify/SKILL.md        # GREEN: exit 0 (52/52)
git show v1.1.0:skills/goalify/SKILL.md > /tmp/v1.md \
  && mkdir -p /tmp/red/goalify && mv /tmp/v1.md /tmp/red/goalify/SKILL.md \
  && python3 evals/check_skill.py /tmp/red/goalify/SKILL.md # RED:   exit 1 (29/52)
```

The RED target is reproduced **from this repo's own git history**, so the claim is falsifiable by
anyone with a clone: the shipped v1.1.0 skill scores 29/52 against the v2 assertions; the current
skill scores 52/52. (Before v2.0.0 this section pointed at a legacy `goal-prep` file outside the repo
that no longer exists, which made the headline number unverifiable — exactly the kind of unfalsifiable
baseline `CONTRIBUTING.md` tells contributors not to accept.)

## 2. Behavioral — `scenarios.md` (judged transcripts)

Three scenarios (substantial task, trivial task, several big sub-projects), each run cold (RED) and
with the skill (GREEN) on **Haiku, Sonnet, and Opus**, scored by a separate judge against the rubric.
Recorded results: [`RED-baseline.md`](RED-baseline.md). Latest: S1 went RED 3–4/7 → **GREEN 7/7 on all
three models**; S2 declines (3/3); S3 splits (3/3).

To re-run the behavioral suite, prompt each model twice for each scenario in `scenarios.md` — once with
no skill, once with `skills/goalify/SKILL.md` active — against a real target (for S1, a small Express
repo with a test suite makes the authoring dimensions fairly testable) and score each transcript
against the rubric.
