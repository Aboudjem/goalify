# LAUNCH-PLAN — goalify

_Supernova Standard, Pillar 1. June 2026. Strategy: borrowed-reach-first, no cold Show HN._

## The one law

Stars come from velocity on a channel whose audience you don't own yet. goalify's hook is blunt — "your plan survives /clear" — and the Claude Code community is tight enough that borrowed-reach works.

---

## Phase 1 — Dark build (done / in progress, May–June 2026)

- [x] Plugin manifest + installable via `claude plugin marketplace add`
- [x] README install snippet + Quick Start
- [x] Tests + eval regression guard
- [ ] `.github/workflows/validate.yml` — JSON-lint + manifest check (P2, not blocking)
- [ ] Submit to `hesreallyhim/awesome-claude-code` via **web-UI issue form only** (PRs auto-close)

## Phase 2 — Launch day (target: mid-June 2026, 13:00–16:00 UTC weekday)

**Primary channel:** r/ClaudeAI — problem-first, not "look what I made".

> Suggested title: *"Your plan dies at /clear. I built a skill that survives it."*
> Body: name the pain (context lost after /clear), show the two-step flow in a GIF/screenshot, link the repo. No hype.

**Stack within 2 hours of the Reddit post:**

1. X/Twitter thread — lead with the GIF, 3 tweets on the two-phase model, tag `@AnthropicAI` and active Claude Code accounts.
2. r/ClaudeAI post (above)
3. Merge any pending `awesome-claude-code` issue if accepted
4. Post to AI-agent/Claude-Code X accounts that already follow the repo

**Do NOT cold Show HN** on launch day. If it gets posted to HN, let someone else carry it.

## Phase 3 — Second wave (2–4 weeks post-launch)

- Ship v0.2 with one concrete improvement (e.g. multi-goal tracking, resume UX)
- Reach out to a YouTuber or newsletter (TLDR AI, Changelog Nightly) with a short pre-written blurb
- If Claude Code ships a `/goal`-adjacent native feature, lean into "complement, not competitor"

## Audience

| Channel | Audience | Why it fits |
|---------|----------|-------------|
| r/ClaudeAI | Claude Code power users | Direct pain: /clear kills context |
| X AI-agent community | Builders using Claude Code autonomously | goalify solves their exact workflow |
| awesome-claude-code | Discoverability long-tail | Drip traffic, trust signal |
| TLDR AI / Changelog | Broader dev audience | Second wave only |

## What not to do

- No cold Show HN from a new account
- No "just posted my project" Reddit spam
- No fake stars or fake accounts
- Don't launch until the install snippet is copy-paste working (now fixed)

---

_Pillar 1 source: SUPERNOVA-STANDARD.md §1 — patterns P1 (borrowed reach), P2 (visceral hook), P3 (dark build), P4 (channel stacking). Confirmed from 15-repo forensics corpus._
