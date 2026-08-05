# Honest limits

This is everything goalify does not promise, in one place. The short version lives in the
[README](../README.md#honest-limits). This page is the full list.

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

## The brief and the condition are two specs, and they can drift

goalify derives the condition from the brief's definition of done, then lints it. That keeps the two
in step. It is a mitigation, not a proof. Whatever the condition leaves out is unenforceable, no
matter how firmly the brief states it.

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

Back to the [README](../README.md) · [FAQ](faq.md) · [quickstart](quickstart.md)
