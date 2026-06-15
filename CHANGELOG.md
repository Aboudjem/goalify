# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-15

A hardened lifecycle, wedge-led positioning, and a designed motion teaser.

### Added

- **Remotion teaser** (`assets/goalify-teaser.mp4` + `goalify-teaser.gif`): a 26.5s,
  1920×1080 / 30fps / H.264 motion teaser with baked-in captions, referenced in the README. Source
  under `video/`.
- **Submission packets** (`docs/submissions/`): paste-ready field values for the claude-community
  Discover form, awesome-claude-code (issue form), and awesome-claude-skills (PR) — all
  human-web-UI-only, plus an index.
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

[1.1.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.1.0
[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
