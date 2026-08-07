# FAQ

**Does goalify run my task?**
No. It writes the brief, derives the condition, and stops there. You start the run yourself, after
`/clear`, in a session that has nothing else in it. That split is the point. The prep happens while
Claude still has your context; the work happens with a full context of its own.

**Why a file *and* a string?**
Because two readers need two different things. The worker — the fresh session doing the job — needs
detail: absolute paths, and the research goalify cited. That is the brief, and it is allowed to run
long. The evaluator is the other reader. It decides each turn whether the work is proven, and it has
no tools and only a trimmed transcript, so it needs something short it can quote. That is the
condition. Collapsing the two into one artifact is the exact thing this design exists to prevent.

**So what actually goes wrong if I paste the path instead?**
Less than you would expect, and worse. Nothing errors: the main agent has full tools, so it opens the
brief and works. What breaks is the *stopping* check. The loop's exit test is now a string the
evaluator cannot interpret, so the run carries on past the point where the job is done. You can find
the failure if you look — running `/goal` with no argument shows the evaluator's most recent reason,
which will read something like "insufficient evidence in transcript" — but it never raises, so nobody
looks.

**What if `/goal` will not start at all?**
Two gates can block it outright, and each says so in as many words:

- `/goal is only available in trusted workspaces. Restart, accept the trust dialog, and try again.`
- `/goal can't run while hooks are restricted (disableAllHooks or allowManagedHooksOnly is set in settings or by policy).`

Both are checked before any hook is registered, so nothing half-starts. Neither is something goalify
can clear for you: the first wants the workspace trust dialog accepted, the second wants the hook
restriction lifted in settings or by whoever set the policy.

**What if the run cannot finish?**
The archive step is gated. If even one criterion is unmet, the brief stays where it is with its
checklist intact, so you can pick the work back up. You resume by pasting the same condition again.

**Why file the brief away instead of deleting it?**
So you can hold the promise and the outcome next to each other afterwards. The brief moves to
`.goal/done/` with a completion stamp, and that move runs at the same strictness — nothing is
archived unless every criterion passed.

**Why is the condition so long?**
Because anything left out of it cannot be enforced. The condition is the only text the evaluator
judges. The brief could say "run the tests" a hundred times and it would change nothing. The cap is
4,000 characters, and goalify spends them on the acceptance criteria rather than on restating the
brief.

**What happens if the condition goes over 4,000 characters?**
It is rejected out loud, at launch: `Goal condition is limited to 4000 characters (got N)`. The
length check runs *before* the hook is registered, so no goal is set and the run never starts. There
is no silent cut anywhere in that path — an oversize condition cannot quietly become a shorter one
you did not write. That is the failure mode you want, and it is why goalify checks the string it
derives rather than trusting it to fit.

**What is in the condition besides the brief's path?**
Three more things. A sentinel — a made-up word the run has to say, so the evaluator can search the
transcript for it. The exact commands whose output has to be quoted back. And a turn bound, so the
loop stays finite. The path itself opens the condition, so the worker knows where to start reading:
`~/acme/.goal/api-migration.md` in goalify's worked example. On success the brief is archived to
`.goal/done/` with a completion stamp, so the promise and the outcome stay comparable later.

**How long does each check get?**
Thirty seconds. The evaluator behind `/goal` runs under a 30-second default timeout per check, and
`/goal` registers its hook without a timeout of its own, so that default is always the one in force.
Nothing you write in the condition changes it — which is another reason the condition is a short
string to be judged rather than a body of work to be done.

**Why does it insist on a "closeout turn"?**
That is the brief's name for one final turn that reruns every check together, and it exists because
evidence ages out of the transcript. Once a session outgrows the evaluator's budget, the **oldest**
messages are dropped and a banner takes their place — and that banner tells the evaluator, in its own
words, to answer not-met if the evidence it needs might be sitting in the omitted beginning. So a
test you proved on turn 3 is not merely forgotten by turn 90; the evaluator is instructed to treat
its absence as insufficient evidence. Rerunning every check right before the evidence packet is
presented puts the raw output at the tail of the transcript, where the evaluator can still read it.

**Does it work outside Claude Code?**
Codex is directly supported, and that support was verified against the binary Codex actually ships —
see [running it under Codex](codex.md). Past that, goalify is a plain
[Agent Skill](https://agentskills.io), so it should load in any agent that implements the
[Agent Skills standard](https://code.visualstudio.com/docs/copilot/customization/agent-skills). Read
that as a structural claim rather than a tested one: this repo ships no conformance run against a
non-Claude agent.

**How is this different from other goal-runner tools?**
There are others. [supergoal](https://github.com/robzilla1738/supergoal) covers a similar niche and
also targets both tools. goalify's own bets are four: it fans research out during prep, it runs a
separate skeptic that re-derives load-bearing claims from primary sources, it locks the genuine
decisions with you before the run starts, and it derives the condition from the brief so the two stay
in step. Pick whichever fits how you work.

**Is there a plugin?**
Yes. goalify ships as a Claude Code plugin in the [**10x** marketplace](https://github.com/Aboudjem/10x)
— `claude plugin install goalify@10x` — and the skill still works on its own. Someone opened a Claude
Code issue asking [how to carry a plan across `/clear`](https://github.com/anthropics/claude-code/issues/32916);
it was closed as not planned, so goalify is one answer to it.

**Does anything in my repo change when I run `/goalify`?**
Only `.goal/` does — it gains the brief and the condition. The prep phase reads and never writes
anywhere else: goalify inspects the repo, researches what it does not know, and changes no code. The
work happens later, in the fresh session you start with the condition.

---

<sub>The `/goal` behavior described on this page — the 30-second evaluator timeout, the two startup
gates and their exact messages, the visible over-4,000-character rejection, and the oldest-first
transcript truncation — was re-derived from the shipped Claude Code 2.1.223 binary and the official
`/goal` docs, 2026.</sub>

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
