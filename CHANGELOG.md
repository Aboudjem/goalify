# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-05-29

### Changed

- **New high-energy hero** (`assets/hero.svg`): an arrow strikes the target and it erupts — a glowing
  power core, a radiating energy burst, and synced impact shockwaves. Rebuilt `assets/how-it-works.svg`
  to match (glowing step nodes, an energized connector). Both animate via CSS `@keyframes` with
  fully-visible static base states, verified on the live GitHub page.
- **Rewrote the README with more energy**, kept plain: a "point it and walk away" hook that shows the
  power through concrete capability (fans out sub-agents, tests as it goes, won't stop until the success
  criteria pass), the literal what-it-does first line intact, and punchier section headers — same honest
  claims, no fabricated metrics.

## [1.2.0] - 2026-05-29

### Changed

- **Rebuilt both SVGs** (`assets/hero.svg`, `assets/how-it-works.svg`) to animate via CSS `@keyframes`
  with a fully-visible static base state. The hero arrow no longer depends on SMIL (which left it
  invisible wherever that animation is ignored) — it's now a neon arrow with a glowing, clearly-visible
  shaft that strikes a bullseye, plus impact rings; "how it works" is a cleaner three-step flow with
  distinct icons.
- **Rewrote the README pain-first.** The literal first sentence now states exactly what goalify does
  (no metaphor), a "Sound familiar?" pain→fix table makes the problem concrete, and both invocation
  methods are documented: `goalify this: <task>` and the `/goalify <task>` slash command.
- **Made the `/goalify` command self-explanatory.** The skill `description` leads with a plain
  what-it-does sentence (still WHEN-only), declares an `argument-hint`, and the body documents
  `$ARGUMENTS`.

### Added

- Two `check_skill.py` assertions (an `argument-hint` is declared; `$ARGUMENTS`/`/goalify` are documented
  in the body) — the deterministic eval is now **29/29**.

## [1.1.0] - 2026-05-29

### Added

- A **maximum-effort directive** baked into both phases: goalify's own PREPARE phase and the generated
  `/goal` file now push all-out execution — aggressive parallel fan-out for independent work, exhaustive
  verification, correctness over speed/cost — and name a max-effort mode (ultracode/ultrawork) when the
  environment has one. Covered by two new `check_skill.py` assertions.

### Changed

- **Distribution is now skill-only.** Removed the plugin wrapper (`.claude-plugin/` manifests) and the
  JSON-validity CI step. For a single skill with no agents/hooks/MCP, a plugin added no capability — only
  install/update convenience — so goalify ships as a drop-in skill: `git clone` + copy into
  `~/.claude/skills/goalify`. (Verified against the Claude Code plugin docs.)
- **Redesigned the README** to be short, scannable, and self-explanatory: an arrow-into-bullseye hook, a
  show-don't-tell command block, a single GitHub `[!IMPORTANT]` callout, a comparison table, and FAQ
  overflow tucked into `<details>` (≈142 → ≈95 lines).
- **New animated hero** (`assets/hero.svg`): an arrow arcs into a bullseye — the "goal," hit on the
  first shot — replacing the abstract prep-line motif.

### Fixed

- `assets/how-it-works.svg` steps no longer render blank where CSS animation is ignored (static fallback:
  base `opacity:1`, reveal driven by the keyframes).

## [1.0.0] - 2026-05-29

Initial public release. Evolved from the internal `goal-prep` skill (renamed to `goalify`;
see [MIGRATION.md](MIGRATION.md)).

### Added

- The `goalify` skill (`skills/goalify/SKILL.md`): a two-phase PREPARE → EXECUTE model that authors a
  self-contained, self-deleting `/goal` execution file you run after `/clear` in a fresh session.
- A WHEN-only, disambiguated `description` (so it stops summarizing its own workflow and stops
  colliding with `autopilot`/`ultrawork`/`ralph`), plus a `goalify` trigger keyword and
  `metadata.version`.
- A hardened generated-MD template: re-orient-from-disk, declarative spec, just-in-time identifiers,
  fan-out guardrails (parallel for independent discovery/verify; serialize builds/tests/same-file
  writes), output-redirection, anti-placeholder + search-before-assuming-missing rules, machine-checkable
  success criteria verified by a separate agent, a copyable progress checklist, and a LOW-freedom gated
  self-destruct with rationalization counters.
- `evals/`: a deterministic check (`check_skill.py`, also run in CI) that encodes the confirmed edits as
  a RED→GREEN regression guard, plus behavioral scenarios (`scenarios.md`) validated on Haiku, Sonnet,
  and Opus and a recorded baseline (`RED-baseline.md`).
- Two install paths: a Claude Code plugin (`marketplace.json` + `plugin.json`, GitHub self-source) and a
  drop-in skill; aligned to the Agent Skills open standard.
- A worked example goal file (`examples/`), a quickstart, GEO/AEO files (`llms.txt`, `AGENTS.md`), an
  animated SVG hero and "how it works" diagram, a social preview card, and a CI workflow that validates
  frontmatter, runs the skill eval, checks JSON + relative links, scans for secrets, and gates the SVGs
  against `<script>` / external references.

[Unreleased]: https://github.com/Aboudjem/goalify/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/Aboudjem/goalify/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Aboudjem/goalify/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Aboudjem/goalify/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
