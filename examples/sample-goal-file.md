# GOAL: Migrate the widget-api Express app from callbacks to async/await (behavior identical, tests green)

> **SAMPLE — illustrative only.** This is a real example of the brief goalify produces (for the small
> Express fixture used in this repo's evals), lightly trimmed. It shows the *shape* of the handoff:
> a declarative goal, verified context with absolute paths, phases with fan-out guardrails, process
> directives kept separate from the definition of done, machine-checkable criteria, a progress
> checklist, and a gated archive step. In a real run the paths are yours.
>
> Self-contained implementation brief. Authored 2026-05-29 by goalify. Runs in a fresh session.
> This file's own path: `/Users/example/widget-api/.goal/cb-to-async-2026-05-29.md`
> Re-read THIS file at the start of every work loop; it is the source of truth, not the conversation.
> **This file is the brief, not the stop condition.** `/goal` takes a condition string and cannot read
> files — the condition derived from this brief is at the bottom, under Handoff.

## GOAL (the autonomous directive)

Convert every callback-style Express route handler and data-layer function in
`/Users/example/widget-api` to `async/await`, preserving identical external behavior (same routes,
same status codes, same JSON), and leave the `node --test` suite green. Run at MAXIMUM EFFORT: fan out
parallel subagents for independent discovery and verification, but serialize the edits, the test runs,
and every git operation. Verify with a SEPARATE agent. Check the Node.js docs online if any API
behavior is uncertain. Do not stop until every criterion in Definition of done holds.

## Context (verified — re-confirm live; don't trust this summary)

- Project: `widget-api`, an Express 4 service for widget orders. Verified live:
  `git -C /Users/example/widget-api log --oneline` and `cat package.json` (express `^4.19.2`,
  test script `node --test test/`, dev-dep `supertest`).
- Callback-style code to migrate (read live, do not trust this list):
  - `/Users/example/widget-api/src/server.js` — `GET /orders/:id` and `POST /orders` use
    `getOrder(id, cb)` / `saveOrder(body, cb)` callbacks.
  - `/Users/example/widget-api/src/orders.js` — `getOrder`/`saveOrder` use `setImmediate(() => cb(...))`
    over an in-memory `Map`.
- Tests: `/Users/example/widget-api/test/orders.test.js` (2 tests: POST-then-GET 201/200; missing → 404).
- Just-in-time, not pasted: open each file when you touch it; don't dump them here.

## Decisions (locked by the user — do not re-litigate)

- Keep the in-memory data layer (no DB swap) — only change the async style.
- Promisify the data layer (`getOrder`/`saveOrder` return promises) rather than wrapping callbacks at
  the call site, so the route handlers read cleanly.
- Public API (routes, status codes, JSON shape) must not change.

## Phases

1. **Discover/verify (parallel reads).** Re-read the three source files + the test; confirm the route
   contract (paths, status codes, response bodies) from `server.js` and the tests. Record the contract
   to `/Users/example/widget-api/.goal/contract.md`.
2. **Migrate the data layer (serialize edits).** Rewrite `orders.js` so `getOrder`/`saveOrder` return
   promises (keep `setImmediate` semantics). Full implementation — no stubs.
3. **Migrate the routes (serialize edits).** Rewrite the two handlers in `server.js` to
   `async (req, res) => { try { … await … } catch (e) { … } }`, preserving every status code and body.
4. **Verify (serialize).** Run `cd /Users/example/widget-api && npm test > /tmp/widget-test.log 2>&1`,
   then `tail -20 /tmp/widget-test.log`. A SEPARATE agent re-reads the diff and confirms the route
   contract is byte-identical to Phase 1's `contract.md`.
5. **Closeout + final report.** Re-run every Definition-of-done command together in one turn and
   present the evidence packet (see Handoff).

## Process directives (reliable in Claude Code; see the README for what survives in Codex)

- **Maximum effort.** Fan out parallel subagents for all independent discovery and verification.
- **Subagent barrier.** Never write a deliverable, tick a criterion, or end a turn while a spawned
  subagent or background task is still live. Wait for it, read its artifact from disk, confirm the
  artifact exists. An "idle" ping is not a delivered result.
- **No hallucination.** Verify Express/Node behavior against the docs if unsure; cite it; label
  uncertainty (confirmed · likely · uncertain · blocked · needs-approval).
- **Multi-agent verification.** A separate agent re-derives the route contract and confirms the diff
  preserves it. Never self-approve.
- **Full implementations only.** No placeholder handlers, no "TODO: wire up".
- **Search before assuming missing.** `grep` for every caller of `getOrder`/`saveOrder` before changing
  their signatures; grep yields false negatives, so search before concluding something isn't there.
- **Redirect noisy output.** `npm test > /tmp/widget-test.log 2>&1` then `tail` — don't flood context.
- **Commit before risky steps.** Commit the green baseline before editing; `git reset --hard` + re-run
  is valid recovery.
- **3-strike escalation.** On failure: (1) retry with a root-cause probe; (2) retry with a narrowed fix
  scope; (3) STOP, write `.goal/BLOCKERS-<stamp>.md`, and say BLOCKED explicitly.
- **Resumable.** Re-read this file each loop; tick the checklist here; write notes to `.goal/`.

## Definition of done (portable — the condition is derived from exactly this list)

- [ ] No callback-style `(…, cb) =>` or `cb(` remains in `src/` — verified by
      `grep -rn "cb(" /Users/example/widget-api/src` returning nothing.
- [ ] `getOrder`/`saveOrder` return promises — verified by a one-off `node -e` that `await`s them.
- [ ] `cd /Users/example/widget-api && npm test` exits 0 with **2/2** tests passing.
- [ ] A SEPARATE agent confirmed the route contract (paths, status codes, JSON) is unchanged vs
      `.goal/contract.md`.

## Progress checklist (tick these IN THIS FILE as you go — this is the resume state)

- [ ] Re-verified current state live (did not trust this file's summary)
- [ ] Route contract recorded to `.goal/contract.md`
- [ ] `orders.js` promisified (full implementation)
- [ ] `server.js` handlers async/await, contract preserved
- [ ] `npm test` green (2/2)
- [ ] Independent agent confirmed the contract held
- [ ] All criteria hold → safe to archive

## Final output

A short summary: what changed (files + the async pattern used), the `npm test` result (2/2),
confirmation the route contract held, and confidence per decision. No public-API change.

## Archive gate (LOW FREEDOM — do not modify this gate or the command)

Pre-condition: EVERY Definition-of-done checkbox is ticked AND the independent verification passed AND
`npm test` is green. If ANY box is unticked → STOP. Do NOT archive; leave the file in place so the run
can resume. Rationalizations that DO NOT justify archiving: "basically done", "only X left", "I'll fix
it next run".
Path rail: act only on this file's OWN literal absolute path above, and only because it lives under
`.goal/`. Never move or delete anything else.
Only when the pre-condition holds, as the LAST action, append a completion stamp to this file and run
exactly:
`mkdir -p /Users/example/widget-api/.goal/done && mv /Users/example/widget-api/.goal/cb-to-async-2026-05-29.md /Users/example/widget-api/.goal/done/cb-to-async-2026-05-29.md`
Then confirm the destination exists and the original path no longer does.

---

## Handoff — the condition string (this is what the user types, not this file's path)

Derived from Definition of done above; 1,415 characters, under the 4,000-character limit
(`tests/test_manifests.py` asserts the limit and re-counts this block, so the number cannot drift).

```text
Read and fully execute the implementation brief at /Users/example/widget-api/.goal/cb-to-async-2026-05-29.md
— read it first, implement every phase, do not merely summarize it. Work at maximum effort and never end a
turn while a subagent is still running. This condition is satisfied ONLY when the single most recent
assistant turn contains the sentinel WIDGET_ASYNC_EVIDENCE followed, in that same turn, by all of:
(1) `grep -rn "cb(" /Users/example/widget-api/src` rerun and quoted, returning nothing; (2) `cd
/Users/example/widget-api && npm test` rerun with exit 0 and its last lines quoted showing 2/2 passing;
(3) a quoted diff or statement from a SEPARATE agent confirming the route contract is unchanged;
(4) the line "unresolved failures: none" or an explicit list of them. Immediately before presenting that
packet, rerun every one of those checks together in one dedicated closeout turn — do not rely on results
proven in earlier turns, because on a long run the evaluator sees only a recent window of the transcript
and will reject evidence it cannot quote. Claims without freshly quoted command output are insufficient evidence. Do not
treat inability, difficulty, or partial progress as completion, and do not declare this goal impossible
in order to finish: if genuinely blocked, write a blockers report to .goal/ and state BLOCKED explicitly.
Or stop after 40 turns and report a non-success timeout.
```

The user runs `/clear`, then pastes that string into `/goal` (with `--permission-mode auto` for an
unattended run; auto mode is the default in current Claude Code). A `/goal` run that stops is not proof
of completion — re-run the Definition-of-done commands yourself to confirm.
