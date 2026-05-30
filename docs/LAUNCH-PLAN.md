# LAUNCH-PLAN — goalify

_Supernova Standard, Pillar 1. Dated June 2026. Strategy: borrowed-reach-first, no cold Show HN._

## The one law applied to goalify

Stars come from velocity on a channel whose audience you don't own. goalify's hook is visceral and unambiguous — "your plan survives /clear" — and the Claude Code ecosystem is a tight, active community with real borrowed-reach paths.

---

## Phase 1 — Dark build (done / in progress, May–June 2026)

- [x] Plugin manifest + installable via `claude plugin marketplace add`
- [x] README install snippet + Quick Start
- [x] Tests + eval regression guard
- [ ] `.github/workflows/validate.yml` — JSON-lint + manifest check (P2, not blocking launch)
- [ ] Submit to `hesreallyhim/awesome-claude-code` via **web-UI issue form only** (PRs auto-close)

## Phase 2 — Launch day (target: mid-June 2026, 13:00–16:00 UTC weekday)

**Primary channel (borrowed reach):** r/ClaudeAI — problem-first post, not a "look what I made" post.

> Suggested title: *"Your plan dies at /clear. I built a skill that survives it."*
> Body: describe the pain (context lost after /clear), show the two-step flow in a GIF/screenshot, link the repo. No hype.

**Stack within 2 hours of Reddit post:**

1. X/Twitter thread — lead with the GIF, thread explains the two-phase model in 3 tweets. Tag `@AnthropicAI` and relevant Claude Code accounts.
2. r/ClaudeAI post (above)
3. Merge any pending `awesome-claude-code` issue (if accepted)
4. Post on AI-agent/Claude-Code X community accounts that have followed the repo

**Do NOT cold Show HN** on launch day. If HN happens, let a third party carry it.

## Phase 3 — Second wave (2–4 weeks post-launch)

- Ship v0.2 with one concrete improvement (e.g. multi-goal tracking, resume UX improvement)
- Court a YouTuber or newsletter (TLDR AI, Changelog Nightly) with a pre-written blurb
- If Claude Code ships a `/goal`-adjacent native feature, position goalify as the complement, not a competitor

## Audience

| Channel | Audience | Why it fits |
|---------|----------|-------------|
| r/ClaudeAI | Claude Code power users | Direct pain: /clear kills context |
| X AI-agent community | Builders using Claude Code autonomously | goalify solves their exact workflow |
| awesome-claude-code | Discoverability long-tail | Drip traffic, trust signal |
| TLDR AI / Changelog | Broader dev audience | Second wave only |

## What NOT to do

- No cold Show HN from a new account
- No "just posted my project" Reddit spam
- No fake stars / fake accounts
- No launch until the install snippet is copy-paste working (now fixed)

---

_Pillar 1 source: SUPERNOVA-STANDARD.md §1 — breakout patterns P1 (borrowed reach), P2 (visceral hook), P3 (dark build), P4 (channel stacking). All confirmed from 15-repo forensics corpus._
