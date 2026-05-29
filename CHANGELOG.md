# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/Aboudjem/goalify/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
