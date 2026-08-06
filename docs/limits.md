# Honest limits

This is everything goalify does not promise, in one place. The short version lives in the
[README](../README.md). This page is the full list.

## A `/goal` run that stops is not proof the work is done

The evaluator applies its own judgment every turn. One of the calls it can make is that your
condition can never be met, and that call ends the loop.

From the outside it looks fine. The hook outcome is literally named `success`, so nothing blocks
and the loop stops. But the goal itself is recorded `met:false, failed:true` — **failed, not
achieved**. So a run can stop with the work unfinished, and tooling wrapped around that run may not
draw the distinction.

No wording in the condition prevents this. goalify does write an anti-impossible clause, but that
clause is best-effort, and it speaks to the worker, not to the evaluator.

**What to do instead.** Open a fresh session and run only the commands in the brief's definition of
done. Or reread the closeout evidence packet yourself. goalify makes that check cheap. It cannot
make it unnecessary.

## The evaluator may never see your earliest evidence

The evaluator behind `/goal` judges a transcript, and on a long run that transcript is trimmed to
fit its budget. The **oldest** messages go first, replaced by a banner — and the banner instructs
the evaluator to answer not-met when the evidence it needs might be sitting in the omitted
beginning. So proof that scrolled off the top is not neutral. It counts against you.

goalify's answer is the closeout turn: rerun every check together at the end, so the output lands
where it can still be read. That is a mitigation for a constraint goalify does not control, and it
only works if the run actually reaches the closeout turn.

## Each check gets 30 seconds, and goalify cannot extend it

The evaluator runs under a 30-second default timeout per check. `/goal` registers its hook without a
timeout of its own, so that default always applies, and nothing you can put in the condition changes
it. Write the condition as something judged quickly from quoted output — not as an analysis the
evaluator has to perform.

## `/goal` can be blocked before it starts

Two gates are checked before any hook is registered, and either one stops the run at launch:

- `/goal is only available in trusted workspaces. Restart, accept the trust dialog, and try again.`
- `/goal can't run while hooks are restricted (disableAllHooks or allowManagedHooksOnly is set in settings or by policy).`

goalify can author a brief and a condition in a workspace where neither gate will ever open. It has
no way to detect that for you, and no way to clear it — the first wants the trust dialog accepted,
the second wants the restriction lifted in settings or by whoever set the policy.

## The brief and the condition are two specs, and they can drift

goalify derives the condition from the brief's definition of done, then lints it. That keeps the two
in step. It is a mitigation, not a proof. Whatever the condition leaves out is unenforceable, no
matter how firmly the brief states it.

The 4,000-character cap is the one part of this that fails cleanly: a condition over the limit is
rejected at launch with `Goal condition is limited to 4000 characters (got N)`, before any hook
exists. Nothing is truncated behind your back, so a too-long condition can never quietly become a
weaker one. The drift that matters is the kind that fits.

## A turn cap is a stopping rule, not a completion rule

A run that hits the cap is not a finished run. The cap is there so the loop stays finite and stays
yours.

## Process directives do not bind under other harnesses

Codex tags the objective as user-provided data. So the process lines — "maximum effort", "never
self-approve", "pause before destructive actions" — do not reliably carry. Only the definition of
done does. The specifics are in [running it under Codex](codex.md).

## The eval baseline is a static diff, not a behavioral one

goalify is built test-first, against a baseline you can reproduce. Measured by today's 55-assertion
check, this repo's own v1.1.0 skill scores **30/55** and the current skill scores **55/55**
([baseline](../evals/RED-baseline.md)).

Read that number for what it is: a **static regression diff**. The v2 clauses do not yet have a
recorded behavioral RED, and the baseline says so rather than implying otherwise.

## Agent Skills portability is a structural claim, not a tested one

goalify is a plain [Agent Skill](https://agentskills.io) — `name` and `description` frontmatter,
then Markdown. On that basis it should load in any agent that implements the
[Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills).

This repo ships **no conformance run against a non-Claude agent**. The brief travels as a spec. The
handoff commands are the part you adapt.

## What goalify does not do

It does not run your task. It does not fetch remote content and execute it. It does not delete the
brief — it archives it, gated on full success, so the promise and the outcome stay comparable
([security](../SECURITY.md)).

---

<sub>The `/goal` constraints on this page — the 30-second evaluator timeout, the two startup gates
and their exact messages, the visible over-4,000-character rejection, and the oldest-first
transcript truncation — were re-derived from the shipped Claude Code 2.1.223 binary and the official
`/goal` docs, 2026.</sub>

Back to the [README](../README.md) · [FAQ](faq.md) · [quickstart](quickstart.md)
