# Contributing to goalify

Thanks for wanting to help. `goalify` is a Claude Code skill that prepares a self-contained,
self-deleting `/goal` execution file. Because its whole value is **reliable behavior in a fresh
autonomous session**, it is built carefully and tested-first. This guide explains how to add to it
without breaking that contract.

Contributions of every size are welcome: a sharper trigger, a tighter template clause, a new eval
scenario, a clearer doc, a typo fix. Open an issue first if you want to discuss a larger change.

## Repo layout

```
skills/goalify/
  SKILL.md              the skill: two-phase model, procedure, goal-MD template,
                        one-vs-several decision, handoff format, hard rules
evals/
  check_skill.py        deterministic assertions on SKILL.md (runs in CI)
  scenarios.md          behavioral scenarios + rubrics
  RED-baseline.md       recorded RED->GREEN baseline (Haiku/Sonnet/Opus)
assets/                 animated SVG hero + how-it-works + social card
examples/               a worked, redacted example goal file
docs/                   quickstart + build audit trail
AGENTS.md               instructions for AI agents working in / invoking this repo
README.md               human-facing overview
LICENSE                 MIT
```

`AGENTS.md` is the source of truth for how the skill behaves and the rules it enforces. Read it before
changing anything in `skills/`.

## We build TEST-FIRST (RED → GREEN → REFACTOR)

This skill exists to fix specific, observed failures — for example, a description that *summarized* the
workflow caused models to skip reading the body, and vague tool nouns failed to resolve in a fresh
session. Every guarantee traces back to a failure we watched happen first.

**The rule: no new behavioral guarantee lands without a failing baseline first.**

1. **RED — watch it fail.** Before you write skill text, run the scenario against a model that does
   *not* have your change (or doesn't have the skill at all) and record what it does wrong, verbatim.
   Test the weak case too — the skill must hold on cheaper models, not just Opus. See
   [`evals/RED-baseline.md`](evals/RED-baseline.md) for the format.
2. **GREEN — write the minimum that fixes it.** Add the skill text / clause / gate that makes that
   exact failure stop. Re-run the same scenario and show it now behaves. If the change is
   statically checkable, add an assertion to `evals/check_skill.py`.
3. **REFACTOR — tighten.** Clean up wording, keep the body under 500 lines (push heavy detail into a
   one-level-deep `references/` file with a table of contents if needed), deduplicate — without
   changing behavior. Re-run to confirm.

A PR that adds behavior but cites no baseline failure it fixes will be sent back for a RED step.
"I think a model might…" is not a baseline; "here is the model doing it" is.

## Hard rules you must keep

These mirror the skill's rules in `AGENTS.md` / `SKILL.md`. Don't look for loopholes.

- **Description stays WHEN-only.** Do not re-introduce a workflow summary into the `description` (it
  becomes a shortcut models follow instead of reading the body). Keep the disambiguation line that
  separates goalify from `autopilot`/`ultrawork`/`ralph`.
- **Tool references resolve in a fresh session.** Use a capability + fallback, or fully-qualified tool
  names — never a vague noun a stranger session can't resolve.
- **The self-destruct stays gated and low-freedom.** Don't weaken the pre-condition or edit the `rm`.
- **No hallucination, anywhere.** No invented flags, behaviors, metrics, or "works with X" claims
  without a primary source. Don't bake unverified third-party star/usage numbers into docs.
- **Keep the SVGs GitHub-safe.** No `<script>`, no external references; well-formed XML. CI enforces it.
- **Frontmatter stays spec-clean.** `name` matches the directory and `^[a-z0-9-]+$`; `description`
  ≤ 1024 chars; version lives under `metadata`.

## Testing locally

```bash
# 1. The deterministic eval must pass.
python3 evals/check_skill.py skills/goalify/SKILL.md     # expect: exit 0, all checks pass

# 2. Run the skill for real: drop it in and exercise the path you changed.
cp -r skills/goalify ~/.claude/skills/goalify
#   then ask Claude Code: "goalify this: <a task that hits your change>"
```

For a behavioral change, re-run the relevant `scenarios.md` case cold (RED) and with the skill (GREEN)
and paste the before/after into your PR.

## Commit and PR etiquette

- Branch off the default branch; don't commit directly to it.
- Keep commits focused; messages say what changed and *why* (link the baseline failure your change fixes).
- One logical change per PR. Smaller PRs get reviewed faster.
- In the PR description include: the RED baseline (the failure you observed), the GREEN fix, and how you
  verified it (`check_skill.py` output and/or a sample run).
- Be kind in review — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## CI must pass

Every PR runs CI: frontmatter check, the `check_skill.py` eval, the SVG safety gate, a
secrets scan, and a relative-link check. It must be green before merge. If CI fails, read the log and
push a fix; don't ask for a merge override.

Thanks again — careful contributions to a tool people point at their real, big tasks genuinely matter.
