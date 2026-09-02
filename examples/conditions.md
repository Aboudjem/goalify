# Worked conditions

Writing the condition is the hardest step goalify asks of you. The brief is a file you can take your
time over; the condition is one line you paste into `/goal`, and it is the only thing the evaluator
ever judges. Anything you leave out of it is unenforceable, however firmly the brief states it.

Eight worked pairs follow. The first block in each pair is a condition worth shipping. The second is
the same job written the way it usually comes out on the first try, with one line saying what it
loses. The rules behind them live in
[`skills/goalify/SKILL.md`](../skills/goalify/SKILL.md); a full brief that one of these was derived
from is in [`sample-brief.md`](sample-brief.md).

## What every condition on this page carries

1. **The brief's path**, named inside the sentence. That is how the run finds the work.
2. **A quoted-evidence clause** naming a command whose output the last turn has to quote. The
   evaluator runs nothing and reads no files, so this is the only kind of proof it can see.
3. **A sentinel**, one made-up string no ordinary summary produces by accident.
4. **A turn bound**, so the loop stays finite and yours.

Say each one once, in the words you would use out loud. The 4,000-character limit is a ceiling, not
a target: every clause past these four is one more thing the evaluator can score as unmet.

---

## 1. Migrate an Express API from callbacks to async/await

```text
Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

```text anti-pattern
~/acme/.goal/api-migration.md
```

Loses all four teeth at once. A path is not a finish line, and the evaluator cannot open it, so every
turn it is asked whether a literal string of characters is satisfied. This is the mistake goalify v2
exists to prevent.

## 2. Upgrade an app to React 19

```text
Work through ~/shop/.goal/upgrade-react-19.md, done when the last turn quotes pnpm build and pnpm test both passing and says REACT19-OK. Stop after 30 turns.
```

```text anti-pattern
Upgrade the app to React 19 and make sure everything still works.
```

Loses the brief, the named commands, the sentinel and the bound. "Everything still works" is a
judgment call, and a judgment call is what you were trying to avoid.

## 3. Hunt down flaky tests

```text
Follow ~/api/.goal/flaky-tests.md, done when the last turn quotes go test ./... -count=5 passing five runs in a row and says FLAKE-FREE. Stop after 50 turns.
```

```text anti-pattern
Follow ~/api/.goal/flaky-tests.md, done when the test suite is no longer flaky. Stop after 50 turns.
```

Loses the quoted-evidence clause. "No longer flaky" names no command, so nothing that appears in the
transcript can prove it and nothing can disprove it either.

## 4. Rebuild a documentation site

```text
Do the work in ~/site/.goal/docs-rebuild.md, done when the last turn quotes npm run build and npm run linkcheck both exiting 0 and says DOCS-GREEN. Stop after 25 turns.
```

```text anti-pattern
Do the work in ~/site/.goal/docs-rebuild.md, done when you report that the docs are rebuilt and say DOCS-GREEN. Stop after 25 turns.
```

Loses the evidence. The run satisfies this condition by claiming it is satisfied. Never make the
assistant's own summary the test.

## 5. Split a Terraform monolith

```text
Do everything in ~/infra/.goal/terraform-split.md, done when the last turn quotes terraform validate and terraform plan reporting no changes and says TF-CLEAN. Stop after 60 turns.
```

```text anti-pattern
Do everything described in the brief at ~/infra/.goal/terraform-split.md at maximum effort, fanning out parallel subagents for independent discovery while serializing all state operations, never self-approving any verification, following the 3-strike escalation ladder on failure, committing before every risky step, and not declaring the goal impossible in order to escape it, done when terraform validate and terraform plan report no changes and says TF-CLEAN. Stop after 60 turns.
```

Everything after the fourth tooth is process, and process belongs in the brief, which the run reads
in full. Here it is surface area: the evaluator can score any one of those clauses as unmet and hold
the loop open.

## 6. Turn on TypeScript strict mode across a monorepo

```text
Run ~/mono/.goal/typescript-strict.md to the end, done when the last turn quotes tsc --noEmit exiting 0 with zero errors and says STRICT-OK. Stop after 45 turns.
```

```text anti-pattern
Run ~/mono/.goal/typescript-strict.md to the end, done when the last turn quotes tsc --noEmit exiting 0 with zero errors and says STRICT-OK.
```

Loses the turn bound. Without one the loop is open-ended, and the only thing that ends it is the
evaluator deciding the condition is unachievable, which is recorded as a failure.

## 7. Generate invoice PDFs

```text
Do the work in ~/billing/.goal/invoice-pdf.md, done when the last turn quotes pytest -q passing and says PDF-OK. Stop after 35 turns.
```

```text anti-pattern
Do the work in ~/billing/.goal/invoice-pdf.md, done when every box in that file is ticked. Stop after 35 turns.
```

Loses the evidence again, in the way that looks most reasonable. The evaluator has no file access, so
a ticked checkbox in a Markdown file is invisible to it no matter how honestly it was ticked.

## 8. Rewrite a search backend

```text
Work through ~/crm/.goal/search-rewrite.md, done when the last turn quotes make test passing and says SEARCH-REWRITE-OK. Stop after 40 turns.
```

```text anti-pattern
Work through ~/crm/.goal/search-rewrite.md, done when the last turn quotes make test passing and says done. Stop after 40 turns.
```

Loses the sentinel. "Done" turns up in ordinary summaries all the time, so the marker fires on a turn
that proved nothing. Pick a string that appears nowhere else.

---

## Check one before you paste it

```bash
python3 skills/goalify/scripts/condition_lint.py "Work through ~/crm/.goal/search-rewrite.md, done when the last turn quotes make test passing and says SEARCH-REWRITE-OK. Stop after 40 turns."
```

The linter reads a condition from its argument or from stdin and exits non-zero if a rule fails. It
checks the length, that a finish line is stated, that the condition is a sentence rather than a path,
that a stop rule is present with a number in it, and that no bare `$` is left for the hook prompt to
rewrite.

It catches three of the eight anti-patterns on this page. The other five pass every rule and are
still bad conditions: an unnamed command, a self-satisfying claim, a lawyerly restatement of the
brief, a ticked checkbox the evaluator cannot see, and a sentinel that is only the word "done". No
mechanical check sees those, which is why the four teeth are worth reading for yourself before you
paste.

See [`docs/quickstart.md`](../docs/quickstart.md) for where the brief and the condition fit in a run,
and [`docs/faq.md`](../docs/faq.md) for what happens when a run stops early.
