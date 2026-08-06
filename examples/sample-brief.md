# GOAL: Migrate the widget-api Express app from callbacks to async/await (behavior identical, tests green)

> **SAMPLE — illustrative only.** This is a real example of the brief goalify produces (for the small
> Express fixture used in this repo's evals), lightly trimmed. It shows the *shape* of the handoff:
> a declarative goal, verified context with absolute paths, phases with fan-out guardrails, process
> directives kept separate from the definition of done, machine-checkable criteria, a progress
> checklist, a gated archive step, and — at the bottom — the one short sentence derived from it that
> the user actually pastes into `/goal`. In a real run the paths are yours.
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
5. **Closeout + final report (serialize).** Re-run every Definition-of-done command together in one
   dedicated turn, then present the evidence packet and the Done / Proof / Next report in that same
   turn (see the Closeout turn directive and Final output below).

## Process directives (reliable in Claude Code; see docs/codex.md for what survives in Codex)

- **Live visible progress.** At the start, create ONE task per phase in the task tracker
  (`TaskCreate`, or this environment's equivalent). Flip each one `in_progress` → `completed` as it
  lands — never in one batch at the end — and tick this file's progress checklist below as you go;
  that checklist IS the resume state. A silent run is indistinguishable from a stalled one.
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
- **Closeout turn.** Immediately before you report, rerun every Definition-of-done check together in
  one dedicated turn and quote the fresh output. The whole evidence packet — the sentinel
  `WIDGET_ASYNC_EVIDENCE`, each command and its output, and "unresolved failures: none" or the list of
  them — must land in the single most recent assistant turn. Do not rely on results proven in earlier
  turns: on a long run the evaluator sees only a recent window of the transcript and rejects evidence
  it cannot quote. Claims without freshly quoted command output are not evidence.
- **3-strike escalation.** On failure: (1) retry with a root-cause probe; (2) retry with a narrowed fix
  scope; (3) STOP, write `.goal/BLOCKERS-<stamp>.md`, and say BLOCKED explicitly. Do not treat
  inability, difficulty, or partial progress as completion, and do not declare this goal impossible in
  order to finish.
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
- [ ] Closeout turn done: every check rerun together and freshly quoted in one turn
- [ ] All criteria hold → safe to archive

## Final output (short bullets under Done / Proof / Next — no long paragraphs)

Exactly these three headers, a few short bullets under each, and nothing else.

- **Done** — what changed: `orders.js` promisified, both route handlers on async/await, no
  public-API change. One bullet per thing.
- **Proof** — every check as rerun in the closeout turn, with its actual quoted output: the `grep`
  returning nothing, `npm test` at 2/2, the separate agent's contract confirmation. Confidence per
  decision (confirmed · likely · uncertain · blocked · needs-approval).
- **Next** — the user's next commands, plus anything still open.

Then state plainly, in the report itself: a `/goal` run that stopped is not proof of completion — the
evaluator can end the loop by judging the condition unachievable — and give the verify-only re-check:
open a fresh session and run only the Definition-of-done commands above.

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

Derived from Definition of done above; 190 characters, far under the 4,000-character limit
(`tests/test_manifests.py` asserts the limit and re-counts this block, so the number cannot drift).
One plain sentence carrying the four teeth and nothing more: this file's absolute path, a
quoted-evidence clause naming a runnable command, a made-up sentinel, and a turn bound. Every heavy
directive — the closeout turn, the freshly-quoted rule, "do not declare this goal impossible",
maximum effort — lives in the brief above, which the worker reads in full. The condition only has to
be checkable by an evaluator that has no tools and cannot read files.

```text
Do everything in /Users/example/widget-api/.goal/cb-to-async-2026-05-29.md and prove it — done when the last turn quotes npm test passing and says WIDGET_ASYNC_EVIDENCE. Stop after 40 turns.
```

The user runs `/clear`, then pastes that string into `/goal` (with `--permission-mode auto` for an
unattended run; auto mode is the default in current Claude Code). A `/goal` run that stops is not proof
of completion — re-run the Definition-of-done commands yourself to confirm.
