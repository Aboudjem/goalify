# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2026-08-04

Documentation corrections found by an independent post-release verification pass. No behavior change;
the skill, the condition contract, and the tests are identical to 2.0.0.

### Fixed

- **`.github/workflows/validate.yml` asserted an incident that never happened.** Two comments claimed a
  commit "merged green and broke HEAD's build" and that a broken `HEAD` had "shipped". Resolving every
  relative import in `video/src` against every commit reachable from all refs shows all of them clean.
  The v2.0.0 recut came one `git commit -a` away from a tree whose imports do not resolve — which is
  what the 2.0.0 entry below already says — but the near miss was never an incident, and a release
  premised on not overstating things should not have overstated this.
- **`README.md` and `SKILL.md` gave incompatible provenance for the Codex 4,000-character cap** — one
  said the limit is interpolated at runtime in the binary, the other said it is enforced server-side.
  Both now give the same account: the number is not a greppable literal, so it was established by
  probing the boundary live (4,000 accepted, 4,001 rejected).
- **The `v1-antipattern` exemption cap was `<= 4` with 3 in use**, leaving one free slot through which
  a genuine path handoff could have passed silently. It is now pinned to exactly the number in use, so
  adding one fails the build. Its failure message also claimed the test verifies each exemption is
  *prose about* the old handoff; it only counts lines, and now says so.
- **`evals/scenarios.md` still pointed the RED demo at the retired `goal-prep` file** that no longer
  exists — the exact unfalsifiable baseline 2.0.0 replaced everywhere else.
- **`evals/README.md` repeated the v1-era behavioral numbers** without the "dated record, not evidence"
  caveat `RED-baseline.md` carries.
- **`AGENTS.md` and `llms.txt` opened with the superseded one-artifact framing** before correcting
  themselves a few lines later. Both are machine-consumed entry points, so the first sentence matters.

## [2.0.0] - 2026-08-04

**goalify's central handoff was wrong, and this release fixes it.**

`/goal` takes a **completion condition, not a file path.** Every version before this one told you to
run `/goal <the-file-it-wrote>`. That path string simply *became* the condition. The evaluator behind
`/goal` has no tools and cannot read files, so on every turn it was asked whether the literal string
`/Users/you/.goal/task.md` had been satisfied — a question it can never answer from the transcript.
The run either never resolved, resolved arbitrarily, or ended early because the evaluator judged the
condition unachievable — stopping with the work unfinished. It *looked* fine because the first turn read
the path and started working; the finish-line gate goalify advertised was never actually running.

The evidence, so you can check rather than trust:

- Docs, https://code.claude.com/docs/en/goal — *"Run `/goal` followed by the condition you want
  satisfied"*, *"The condition can be up to 4,000 characters"*, and *"It doesn't run commands or read
  files independently, so write the condition as something Claude's own output can demonstrate."*
- The shipped Claude Code binary (2.1.221) contains `No goal set. Usage: `/goal <condition>`` and
  `Goal condition is limited to <N> characters`. The `/goal` handler has three branches — empty,
  clear, and "treat the rest as the raw condition". There is no file-path branch.

### Changed — BREAKING

- **The handoff is now a derived condition string, not a path.** goalify still writes a self-contained
  implementation brief, but it now also **derives a `/goal` condition from that brief's definition of
  done** and writes it to `.goal/CONDITION-<slug>.txt` so you can `pbcopy` it. The handoff became
  three steps: `/clear` → copy the condition → `/goal <paste>`, with auto mode on for an unattended
  run (it is the default in current Claude Code).
- **The generated brief separates the definition of done from the process directives.** The definition
  of done is portable and is what the condition is derived from; the process directives are what binds
  reliably in Claude Code only. This split is what makes the same brief usable under Codex.
- **Self-destruct became an archive step.** On full success the brief moves to `.goal/done/` with a
  completion stamp instead of being deleted, at the same gate strictness — the promise-vs-outcome
  audit trail survives.

### Added

- **A closeout-turn requirement.** Once a session exceeds roughly half the evaluator's context budget
  (a quarter on a prompt-too-long retry), older messages are dropped and replaced with a notice
  instructing it to refuse when evidence may lie in the omitted prefix — so on a long run, evidence
  proven on turn 3 is invisible on turn 90. The condition now requires re-running every check together
  in one dedicated turn immediately before presenting the evidence packet.
- **A condition lint**: ≤ 4,000 characters (counted, not estimated), no bare `$` (the hook prompt
  substitutes `$ARGUMENTS`/`$N`), a sentinel token, a named runnable command per criterion, an
  explicit turn bound, and no success phrase the condition text would satisfy on its own.
- **A subagent barrier rule** — never write a deliverable, tick a criterion, or end a turn while a
  spawned subagent is still live. An "idle" or "available" ping is not a delivered result.
- **Cross-harness support for Codex.** Codex has a real, default-on `/goal`
  (`/goal [<objective>|clear|edit|pause|resume]`), it also takes an inline objective rather than a
  path, and its cap is the same 4,000 characters (established by probing the boundary live, since the
  number is interpolated at runtime rather than stored as a string) — so the derivation is built once and both forms are
  printed. Codex tells the model the objective is *"user-provided data … the task to pursue, not
  higher-priority instructions"* and tags an edited objective `<untrusted_objective>`, so goalify now
  documents plainly that its **process directives do not reliably bind under Codex; only the definition
  of done carries.** `/goal` is TUI-only there, so the headless form pipes the brief to `codex exec -`.
  goalify does not promise budgeted Codex goals: `token_budget` reports `under development`.
- **Model routing** (fast model for mechanical breadth, deep model for architecture and every skeptic
  pass) and a **dry run with caps** — phases, subagents, turn cap — printed before anything is written.
  goalify deliberately does *not* predict a token or dollar cost; there is no citable basis for one.
- **An honest-limits section.** A `/goal` run that stops is not proof of completion — the evaluator can
  end the loop by judging the condition unachievable, and no wording prevents that. (Claude Code books
  that case as a failed goal rather than an achieved one, but the loop ends either way.) The docs now
  say so and give you a verify-only re-check instead of implying a guarantee.
- **A 3-strike escalation ladder** (root-cause probe → narrowed scope → STOP and write a blockers
  report) replacing the bare stall guard, aligned with Codex's own blocked audit.

### Fixed

- **The teaser recut was one `git commit -a` away from publishing a tree that does not build.** In the
  working tree, `video/src/ConceptHero.tsx` was untracked while the recut `GoalifyTeaser.tsx` imported
  it and `ConceptB.tsx` was deleted — so committing those changes would have produced a `HEAD` whose
  imports do not resolve. (The previous `HEAD` was fine; it still imported `ConceptB`, which existed.)
  Nothing in CI looked at `video/`, so that commit would have gone green.
- `Root.tsx` now imports `TEASER_FRAMES` from the storyboard instead of hardcoding `890`, so the
  composition length cannot drift from the scene list.
- Doc drift in `video/README.md`: the recut teaser is **8 beats / 890 frames / 29.717s** (measured
  with `ffprobe`), not the "9-beat, ~26.5s" it described, and it no longer points at the deleted
  `src/theme.ts`. (The 1.1.0 entry below is left as written — the teaser it shipped really was 26.5s.)
- The RED baseline in `evals/README.md` referenced a file that no longer exists, which made the
  headline claim unfalsifiable. It is now reproduced from git history:
  `git show v1.1.0:skills/goalify/SKILL.md` scores **29/52**, current `SKILL.md` scores **52/52**.

### Removed

- Dead teaser code: `video/src/theme.ts`, and the unused `Chip` and `CtaNeon` components.

### CI

- Runs `tests/test_manifests.py` (which `AGENTS.md` already called a release gate) — now including a
  version-consistency check across `SKILL.md`, `plugin.json`, `marketplace.json` and this file, and an
  assertion over **every tracked text file** (not just Markdown) that nothing passes a file path to
  `/goal` — absolute, `~`, or relative. Lines that *describe* the old handoff opt out with a
  `v1-antipattern` marker, and the number of those exemptions is itself asserted.
- Typechecks `video/` and asserts every relative import in `video/src` is tracked by git — the exact
  failure above, gated so it cannot recur.
- The secrets scanner grew from 2 patterns to 12 (GitHub, Anthropic, OpenAI, Slack, Google, Stripe,
  npm), and the markup safety gate now covers `assets/social-card.html`, not just `assets/*.svg`.

## [1.1.0] - 2026-06-15

A hardened lifecycle, wedge-led positioning, and a designed motion teaser.

### Added

- **Remotion teaser** (`assets/goalify-teaser.mp4` + `goalify-teaser.gif`): a 26.5s,
  1920×1080 / 30fps / H.264 motion teaser with baked-in captions, referenced in the README. Source
  under `video/`.
- A marketplace `description` in `marketplace.json` (clears the `claude plugin validate` warning;
  passes `--strict`).

### Changed

- **Hardened the skill lifecycle** (`SKILL.md`): the procedure now idempotently appends `.goal/` to
  `.gitignore`; the generated-MD template gains a stall guard and a self-destruct path rail; the
  one-vs-several split writes an `INDEX.md` with run order; and the handoff format gains a resume line.
- **Refreshed positioning** to lead with the wedge — lock the few real decisions, wire the finish line
  to commands the run can check, verify every criterion before done — across the README, `SKILL.md`
  `description`, `llms.txt`, `AGENTS.md`, and the GitHub About. Self-destruct is now a supporting
  feature, and the install docs point at Claude Code's built-in `/goal` for executing the file goalify
  writes.
- Repo metadata: set the homepage URL, refreshed the GitHub About, and regenerated the 1280×640 social
  preview.

## [1.0.0] - 2026-05-29

Initial public release. goalify is a Claude Code / Agent Skills skill that prepares a
self-contained, self-deleting `/goal` execution file: in one session it scopes the work,
locks the few real decisions, and writes the file, so you `/clear` and run it in a fresh,
full-context session that executes the whole job and verifies every success criterion
before deleting the file. Evolved from an internal `goal-prep` skill (see
[MIGRATION.md](MIGRATION.md)).

### Added

- The `goalify` skill (`skills/goalify/SKILL.md`): a two-phase PREPARE → EXECUTE model that
  authors the `/goal` file you run after `/clear` in a fresh session.
- A WHEN-only, disambiguated `description` (carries the `goalify` trigger, says
  author-not-execute, and disambiguates against `autopilot`/`ultrawork`/`ralph`), a quoted
  `argument-hint`, a documented `/goalify` command with `$ARGUMENTS`, and `metadata.version`.
- A hardened generated-file template: a declarative spec, verified just-in-time context with
  absolute paths, fan-out guardrails (parallel for independent discovery and verification;
  serialize builds, tests, and same-file writes), output-redirection, anti-placeholder and
  search-before-assuming rules, machine-checkable success criteria verified by a separate
  agent, a copyable progress checklist, a maximum-effort directive, and a low-freedom gated
  self-destruct with rationalization counters.
- `evals/`: a deterministic check (`check_skill.py`, run in CI) that encodes the confirmed
  edits as a RED→GREEN regression guard, plus behavioral scenarios validated on Haiku,
  Sonnet, and Opus and a recorded baseline (`RED-baseline.md`).
- A worked example `/goal` file (`examples/`), a quickstart, a terminal-themed animated SVG
  hero and "how it works" diagram, GEO files (`llms.txt`, `AGENTS.md`), and a CI workflow
  that validates frontmatter, runs the skill eval, checks relative links, scans for secrets,
  and gates the SVGs against `<script>` and external references.

[2.0.1]: https://github.com/Aboudjem/goalify/releases/tag/v2.0.1
[2.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.0.0
[1.1.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.1.0
[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
