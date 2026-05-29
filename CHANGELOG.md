# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
