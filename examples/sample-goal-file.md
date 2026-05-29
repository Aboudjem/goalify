# GOAL: Migrate the widget-api Express app from callbacks to async/await (behavior identical, tests green)

> **SAMPLE — illustrative only.** This is a real example of a `/goal` file goalify produced (for the
> small Express fixture used in this repo's evals), lightly trimmed. It shows the *shape* of the
> handoff: declarative goal, verified context with absolute paths, phases with fan-out guardrails,
> machine-checkable success criteria, a progress checklist, and a gated self-destruct. In a real run
> the paths are yours and the file deletes itself on success.
>
> Self-contained execution file for `/goal`. Authored 2026-05-29 by goalify. Runs in a fresh session.
> This file's own path: `/Users/example/widget-api/.goal/cb-to-async-2026-05-29.md`
>   ← delete it as the final step (see Self-destruct).
> Re-read THIS file at the start of every work loop; it is the source of truth, not the conversation.

## GOAL (the autonomous directive)

Convert every callback-style Express route handler and data-layer function in
`/Users/example/widget-api` to `async/await`, preserving identical external behavior (same routes,
same status codes, same JSON), and leave the `node --test` suite green. Work in that repo (absolute
paths below). Fan out parallel subagents only for independent discovery/verification; serialize the
edits and the test runs. Verify with a separate agent. Check the Node.js docs online if any API
behavior is uncertain. Do not stop until every success criterion holds.

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

## Decisions (locked by the user)

- Keep the in-memory data layer (no DB swap) — only change the async style.
- Promisify the data layer (`getOrder`/`saveOrder` return promises) rather than wrapping callbacks at
  the call site, so the route handlers read cleanly.
- Public API (routes, status codes, JSON shape) must not change.

## Phases (fan out independent work in parallel; serialize edits/tests)

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
N. **Final report.**

## Hard rules

- **No hallucination.** Verify Express/Node behavior against the docs if unsure; cite it; label
  uncertainty.
- **Multi-agent verification.** A separate agent re-derives the route contract and confirms the diff
  preserves it. Never self-approve.
- **Full implementations only.** No placeholder handlers, no "TODO: wire up".
- **Search before assuming missing.** `grep` for every caller of `getOrder`/`saveOrder` before changing
  their signatures.
- **Redirect noisy output.** `npm test > /tmp/widget-test.log 2>&1` then `tail` — don't flood context.
- **Commit before risky steps.** `git commit` the green baseline before editing; `git reset --hard` +
  re-run is valid recovery.
- **Resumable.** Re-read this file each loop; write `contract.md` and notes to `.goal/`.

## Success criteria (the run is done only when ALL hold)

- [ ] No callback-style `(…, cb) =>` or `cb(` remains in `src/` — verified by
      `grep -rn "cb(" /Users/example/widget-api/src` returning nothing.
- [ ] `getOrder`/`saveOrder` return promises — verified by a one-off `node -e` that `await`s them.
- [ ] `cd /Users/example/widget-api && npm test` exits 0 with **2/2** tests passing.
- [ ] A SEPARATE agent confirmed the route contract (paths, status codes, JSON) is unchanged vs
      `.goal/contract.md`.

## Progress checklist (copy into your working notes and tick as you go)

- [ ] Re-verified current state live (did not trust this file's summary)
- [ ] Route contract recorded to `.goal/contract.md`
- [ ] `orders.js` promisified (full implementation)
- [ ] `server.js` handlers async/await, contract preserved
- [ ] `npm test` green (2/2)
- [ ] Independent agent confirmed the contract held
- [ ] All success criteria hold → safe to self-destruct

## Final output

A short summary: what changed (files + the async pattern used), the `npm test` result (2/2),
confirmation the route contract held, and confidence per decision. No public-API change.

## Self-destruct (LOW FREEDOM — do not modify this gate or the command)

Pre-condition: EVERY success-criteria checkbox is ticked AND the independent verification passed AND
`npm test` is green. If ANY box is unticked → STOP. Do NOT delete; leave the file so the run can resume.
Rationalizations that DO NOT justify deletion: "basically done", "only X left", "I'll fix it next run".
Only when the pre-condition holds, as the LAST action, run exactly:
`rm /Users/example/widget-api/.goal/cb-to-async-2026-05-29.md`
Then confirm the path no longer exists.
