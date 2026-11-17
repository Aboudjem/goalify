# GOAL: Make slugify keep digits and collapse symbols, with every test passing

> Self-contained implementation brief. Authored 2026-11-17 by hand for the goalify demo, in the shape goalify writes.
> This file's own path: `__DEMO_DIR__/.goal/slugify-20261117.md`
> **This file is the brief, not the stop condition.** `/goal` takes a condition string and cannot read
> files: the condition derived from this brief is in `CONDITION-slugify.txt`, next to it.

## GOAL (the autonomous directive)

End state: `slugify()` in `__DEMO_DIR__/slugify.py` lowercases a title, keeps letters and digits, and
joins the words with single hyphens. The three tests in `__DEMO_DIR__/test_slugify.py` pass.

## Context (verified: re-confirm live; don't trust this summary)

- The project is two files: `__DEMO_DIR__/slugify.py` and `__DEMO_DIR__/test_slugify.py`.
- The tests use the standard library only. They run with `python3 -m unittest -q test_slugify`.

## Decisions (locked by the user: do not re-litigate)

- Standard library only. No new dependency.
- The function name and its one argument stay as they are.

## Phases

1. **Read.** Read both files and run the tests once.
2. **Fix.** Change `slugify()` until the three tests pass. Full implementation, no stub.
3. **Prove.** Rerun every Definition-of-done check and quote the output.

## Process directives

- **Closeout turn.** Immediately before the final report, rerun every Definition-of-done check in one
  dedicated turn and quote each command's fresh output in that same turn.
- **No hallucination.** Never state a result you did not just see a command print.
- **3-strike escalation.** After three failed attempts on one problem, stop and say BLOCKED.

## Definition of done (portable: the condition is derived from exactly this list)

- [x] Every test passes, verified by `python3 -m unittest -q test_slugify` (exit 0).
- [x] No unfinished marker is left in the code, verified by `grep -n "TODO" slugify.py` printing nothing.

## Progress checklist (tick these IN THIS FILE as you go: this is the resume state)

- [x] Read both files, ran the tests once
- [x] slugify() fixed
- [x] Closeout turn done
- [x] All criteria hold: safe to archive

## Final output (short bullets under Done / Proof / Next, no long paragraphs)

- **Done**: what changed. One bullet per thing.
- **Proof**: each check that was run and its actual quoted output.
- **Next**: the user's next commands, plus anything still open.

Then state plainly: a `/goal` run that stopped is not proof of completion, because the evaluator can
end the loop by judging the condition unachievable. Give the verify-only re-check.

## Archive gate (LOW FREEDOM: do not modify this gate or the command)

Pre-condition: EVERY Definition-of-done checkbox is ticked AND the checks are green. If ANY box is
unticked: STOP. Do NOT archive; leave the file in place so the run can resume.
Only when the pre-condition holds, as the LAST action, append a completion stamp to this file and run exactly:
`mkdir -p __DEMO_DIR__/.goal/done && mv __DEMO_DIR__/.goal/slugify-20261117.md __DEMO_DIR__/.goal/done/slugify-20261117.md`
