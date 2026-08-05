# FAQ

**Does goalify run my task?**
No. It writes the brief, derives the condition, and stops there. You start the run yourself, after
`/clear`, in a session that has nothing else in it. That split is the point. The prep happens while
Claude still has your context; the work happens with a full context of its own.

**Why a file *and* a string?**
Because two readers need two different things. The worker — the fresh session doing the job — needs
detail: absolute paths, and the research goalify cited. That is the brief, and it is allowed to run
long. The evaluator is the other reader. It decides each turn whether the
work is proven, and it has no tools and only a truncated transcript, so it needs something short it
can quote. That is the condition. Collapsing the two into one artifact is the exact thing this
design exists to prevent.

**What if the run cannot finish?**
The archive step is gated. If even one criterion is unmet, the brief stays where it is with its
checklist intact, so you can pick the work back up. You resume by pasting the same condition again.

**Why archive the brief instead of deleting it?**
So you can hold the promise and the outcome next to each other afterwards. The brief moves to
`.goal/done/` with a completion stamp, and that move runs at the same gate strictness — nothing is
archived unless every criterion passed.

**Why is the condition so long?**
Because anything left out of it cannot be enforced. The condition is the only text the evaluator
judges. The brief could say "run the tests" a hundred times and it would change nothing. The cap is
4,000 characters, and goalify spends them on the acceptance criteria rather than on restating the
brief.

**What is in the condition besides the brief's path?**
Three more things. A sentinel — a made-up token the run has to say, so the evaluator can search the
transcript for it. The exact commands whose output has to be quoted back. And a turn bound, so the
loop stays finite. The path itself opens the condition, so the worker knows where to start reading:
`~/acme/.goal/api-migration.md` in goalify's worked example. On success the brief is archived to
`.goal/done/` with a completion stamp, so the promise and the outcome stay comparable later.

**Why does it insist on a "closeout turn"?**
Because evidence ages out of the transcript. Once a session grows past roughly half the evaluator's
context budget, the oldest messages are dropped and replaced with a notice telling it to refuse when
the evidence might sit in that dropped beginning. A test you proved on turn 3 is invisible on turn 90. The
closeout turn is the fix: rerun every check together right before the evidence packet is presented,
so the raw output lands at the tail of the transcript, where the evaluator can still read it.

**Does it work outside Claude Code?**
Codex is directly supported, and that support was verified against the binary Codex actually ships —
see [running it under Codex](codex.md). Past that, goalify is a plain
[Agent Skill](https://agentskills.io), so it should load in any agent that implements the
[Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills). Read
that as a structural claim rather than a tested one: this repo ships no conformance run against a
non-Claude agent.

**How is this different from other goal-runner tools?**
There are others. [supergoal](https://github.com/robzilla1738/supergoal) covers a similar niche and
also targets both harnesses. goalify's own bets are four: it fans research out during prep, it runs a
separate skeptic that re-derives load-bearing claims from primary sources, it locks the genuine
decisions with you before the run starts, and it derives the condition from the brief so the two stay
in step. Pick whichever fits how you work.

**Is there a plugin?**
Yes. goalify ships as a Claude Code plugin in the [**10x** marketplace](https://github.com/Aboudjem/10x)
— `claude plugin install goalify@10x` — and the skill still works on its own. Someone opened a Claude
Code issue asking [how to carry a plan across `/clear`](https://github.com/anthropics/claude-code/issues/32916);
it was closed as not planned, so goalify is one answer to it.

**Does anything in my repo change when I run `/goalify`?**
Only `.goal/` does — it gains the brief and the condition. The prep phase is otherwise read-only:
goalify inspects the repo, researches what it does not know, and changes no code. The work happens
later, in the fresh session you start with the condition.

---

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
