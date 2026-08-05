# Honest limits

Everything goalify does not promise, in one place. The short version lives in the
[README](../README.md#honest-limits); this is the full list.

## A `/goal` run that stops is not proof of completion

The evaluator applies independent judgment and can end the loop by deciding the condition is
unachievable. The hook outcome is literally named `success`, so nothing blocks and the loop stops —
but the goal itself is recorded `met:false, failed:true`: **failed, not achieved**. Net effect, a run
can stop with the work unfinished, and tooling wrapped around it may not make the distinction.

No condition wording prevents this. goalify's anti-impossible clause is best-effort and aimed at the
worker, not the evaluator.

**What to do instead:** open a fresh session and run only the brief's definition-of-done commands, or
reread the closeout evidence packet yourself. goalify makes that cheap. It cannot make it
unnecessary.

## The brief and the condition are two specs that can drift

Deriving the condition from the brief's definition of done and linting it is a mitigation, not a
proof. Anything omitted from the condition is unenforceable no matter how firmly the brief states it.

## A turn cap is a stopping rule, not a completion rule

A timed-out run is not a finished run. The cap exists so the loop stays finite and yours.

## Process directives do not bind under other harnesses

Codex tags the objective as user-provided data, so "maximum effort", "never self-approve" and
"pause before destructive actions" do not reliably carry. Only the definition of done does. Details
in [running it under Codex](codex.md).

## The eval baseline is a static diff, not a behavioral one

goalify is built test-first with a reproducible baseline: against today's 55-assertion check, this
repo's own v1.1.0 skill scores **30/55** and the current skill scores **55/55**
([baseline](../evals/RED-baseline.md)). That is a **static regression diff**. The v2 clauses do not
yet have a recorded behavioral RED, and the baseline says so rather than implying otherwise.

## Agent Skills portability is a structural claim, not a tested one

goalify is a plain [Agent Skill](https://agentskills.io) — `name` + `description` frontmatter and
Markdown — so it should load in any agent implementing the
[Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills). This
repo ships **no conformance run against a non-Claude agent**. The brief is portable as a spec; the
handoff commands are what you adapt.

## What goalify does not do

It does not run your task. It does not fetch and execute remote content. It does not delete the
brief — it archives it, gated on full success, so the promise and the outcome stay comparable
([security](../SECURITY.md)).

---

Back to the [README](../README.md) · [FAQ](faq.md) · [quickstart](quickstart.md)
