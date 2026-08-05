# FAQ

**Does it run my task?**
No. It writes the brief and derives the condition; you start the run after `/clear`, in a fresh
session. That separation is the point.

**Why a file *and* a string?**
They have different readers. The worker needs detail, absolute paths and cited research — that's the
brief, and it can be long. The evaluator gets no tools and a truncated transcript, so it needs a
short, quotable condition. Collapsing the two is the mistake this design exists to prevent.

**What if the run can't finish?**
The archive step is gated. If any criterion is unmet, the brief stays in place with its checklist so
you can resume — rerun the same condition.

**Why archive the brief instead of deleting it?**
So the promise and the outcome can be compared afterwards. The brief moves to `.goal/done/` with a
completion stamp, at the same gate strictness.

**Why is the condition so long?**
Because anything left out of it is unenforceable. The condition is the only thing the evaluator
judges; the brief could say "run the tests" a hundred times and it would not matter. The cap is 4,000
characters, and goalify spends them on the acceptance criteria rather than restating the brief.

**What else is in the condition besides the brief's path?**
A sentinel token the evaluator can search for, the exact commands whose output has to be quoted, and
a turn bound. On success the brief is archived to `.goal/done/` with a completion stamp, so the
promise and the outcome can be compared later.

**Why does it insist on a "closeout turn"?**
Once a session grows past roughly half the evaluator's context budget, older messages are dropped and
replaced with a notice telling it to refuse when the evidence might sit in the omitted prefix. So
evidence proven on turn 3 is invisible on turn 90. The closeout turn is the fix: rerun everything
together right before presenting the packet, so the raw output lands at the tail of the transcript
where the evaluator can still see it.

**Does it work outside Claude Code?**
Codex is directly supported and verified against its shipped binary — see
[running it under Codex](codex.md). Beyond that, goalify is a plain
[Agent Skill](https://agentskills.io), so it should load in any agent implementing the
[Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills). That
is a structural claim, not a tested one; this repo ships no conformance run against a non-Claude
agent.

**How is this different from other goal-runner tools?**
There are others — [supergoal](https://github.com/robzilla1738/supergoal) covers a similar niche and
also targets both harnesses. goalify's distinct bets are the research fan-out during prep, a separate
skeptic re-deriving load-bearing claims from primaries, locking the genuine decisions with you before
the run starts, and deriving the condition from the brief so the two stay in step. Pick whichever
fits how you work.

**Is there a plugin?**
Yes — goalify ships as a Claude Code plugin in the [**10x** marketplace](https://github.com/Aboudjem/10x)
(`claude plugin install goalify@10x`), and the skill still works standalone. Someone opened a Claude
Code issue asking [how to carry a plan across `/clear`](https://github.com/anthropics/claude-code/issues/32916);
it was closed as not planned, so goalify is one answer.

**Does anything in my repo change when I run `/goalify`?**
No. The prep phase is read-mostly: it inspects, researches, and writes the brief plus the condition
under `.goal/`. The work happens later, in the fresh `/goal` session.

---

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
