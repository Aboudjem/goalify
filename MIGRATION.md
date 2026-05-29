# Migration: `goal-prep` → `goalify`

`goalify` is the renamed, hardened successor to an internal skill called `goal-prep`. The rename
happened before any public release, so there is no compatibility shim to maintain — this note exists
only for completeness.

## What changed

| | `goal-prep` (internal) | `goalify` (this repo) |
|---|---|---|
| Skill name / directory | `goal-prep` | `goalify` |
| Invocation | "goal prep", "prep a goal" | the same **plus** "goalify", "goalify this", "goalify <task>" |
| `description` | summarized the workflow (research + MCQ + fan-out) | WHEN-only, with a disambiguation line vs `autopilot`/`ultrawork`/`ralph` |
| Tool references | vague nouns ("the Workflow tool") | a capability + fallback that resolves in a fresh session |
| Self-destruct | prose `rm` | a LOW-freedom gated block with rationalization counters |
| Generated-MD template | strong, but missing several run-hardening clauses | adds output-redirection, anti-placeholder, search-before-assuming, machine-checkable criteria, a progress checklist, just-in-time identifiers, and fan-out guardrails |
| `metadata.version` | absent | `1.0.0` |
| Evals | none shipped | `evals/` (deterministic + behavioral, RED→GREEN on Haiku/Sonnet/Opus) |

Why these specific changes: see [`evals/RED-baseline.md`](evals/RED-baseline.md) for the observed
failures each one fixes.

## If you used `goal-prep`

Replace the old skill directory with the new one:

```bash
rm -rf ~/.claude/skills/goal-prep
git clone https://github.com/Aboudjem/goalify
cp -r goalify/skills/goalify ~/.claude/skills/goalify
```

Then invoke it by saying **"goalify this: &lt;task&gt;"** (the old "prep a goal" phrasing still triggers it).
Behavior is the same two-phase model — PREPARE here, then `/clear` and `/goal <path>` to EXECUTE — just
more reliable.
