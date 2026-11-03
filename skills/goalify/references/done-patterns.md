# Definition-of-done patterns by job type

Loaded just in time from PREPARE step 2. These are **finish-line patterns only**: extra checks to
add on top of the ones `scripts/detect_checks.py` found in the repo. They are not phase templates
and not whole briefs, so the research still has to happen. Every command below is a shape: swap
in the repo's real paths and tools, and only keep a check the repo can actually run.

Each line follows the template's form: a pass/fail criterion, then `verified by` a named command
whose output the closeout turn can quote.

## Migration (API, framework, language feature)

- Zero uses of the old API remain, verified by `grep -rn "<old call>" <src dir>` printing nothing.
- The new API is in use where the old one was, verified by `grep -rc "<new call>" <src dir>`
  showing the expected count.
- The suite still passes, verified by the detected test command exiting 0.
- Sentinel idea: `MIGRATION-OK`.

## Refactor (behavior must not change)

- The public surface is unchanged, verified by a diff of the exported names or routes before and
  after (`git diff <base> -- <api file>` empty, or a contract file compared by a separate agent).
- The suite passes with the same test count as the baseline, verified by the test command and its
  summary line quoted next to the baseline from Context.
- Sentinel idea: `REFACTOR-OK`.

## Test coverage

- Coverage meets the target, verified by the coverage command printing a total at or above it
  (`npx vitest run --coverage`, `python3 -m pytest --cov=<pkg> --cov-fail-under=<n>`).
- No test is skipped to get there, verified by `grep -rn "skip\|xit(\|xdescribe" <tests dir>`
  showing no new hits against the baseline.
- Sentinel idea: `COVERAGE-OK`.

## Docs

- Every relative link resolves, verified by the repo's link checker or a short script quoted in
  full.
- The examples in the docs still run, verified by running each example command once.
- Sentinel idea: `DOCS-OK`.

## Dependency upgrade

- The manifest pins the new version, verified by `grep '"<pkg>"' package.json` (or the lockfile
  equivalent) showing it.
- The lockfile is consistent, verified by `npm ci` (or `pnpm install --frozen-lockfile`) exiting 0.
- Build and tests pass, verified by the detected build and test commands exiting 0.
- Sentinel idea: `UPGRADE-OK`.

## Release

- The tag and the release exist, verified by `gh release view <tag> --json tagName,url`.
- CI on the default branch is green, verified by `gh run list --branch main --limit 1`.
- The published version matches every manifest, verified by the repo's version-consistency test.
- Sentinel idea: `RELEASE-OK`.

## Always, whatever the job

- A SEPARATE agent re-derived every load-bearing claim from primaries.
- The closeout turn reran every check above and quoted the output in one turn.
