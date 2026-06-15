# Submission packet — Claude Code community marketplace (the /plugin Discover tab)

**Goal:** get goalify listed in the in-app `/plugin` **Discover** tab so people find it from inside
Claude Code. That tab is fed by the **community marketplace** (`anthropics/claude-plugins-community`).

**Mechanism — web form, human-only.** Submit through the shortlink
**`https://clau.de/plugin-directory-submission`**. For an individual author (not a Team/Enterprise org)
that resolves to the **Console form** at **`https://platform.claude.com/plugins/submit`**. The form is
login-gated, so a human has to complete it.

> ⚠️ Do **NOT** open a pull request against `anthropics/claude-plugins-community`. That repo is a
> read-only nightly mirror and PRs are **closed automatically** — every listing flows through the
> internal review pipeline that the web form feeds. There is no `gh` CLI / API path.

> ℹ️ The **official** marketplace (`claude-plugins-official`) is curated by Anthropic at its discretion
> with no application process; the form does not add to it. The realistic target is the **community**
> marketplace, which is what Discover surfaces for third-party plugins.

## Before you submit — run the validator (passes clean)

From the repo root:

```bash
claude plugin validate .
# ✔ Validation passed
claude plugin validate . --strict   # CI-grade: warnings treated as errors
# ✔ Validation passed
```

(The validator checks `.claude-plugin/marketplace.json` schema + cross-checks the referenced
`plugin.json` versions. Both pass with no warnings as of v1.1.0.)

## Field values to paste

| Field | Value |
|---|---|
| **Plugin repository URL** (the load-bearing field) | `https://github.com/Aboudjem/goalify` |
| **Plugin name** (kebab-case, matches `plugin.json`) | `goalify` |
| **Version** | `1.1.0` |
| **Description** | goalify is a Claude Code skill that turns a big coding task into a self-contained goal file: it locks the few real decisions and wires the finish line to commands the run can check, so a fresh session (run with the built-in `/goal`) executes the whole job and verifies every criterion before the file deletes itself. |
| **Author** | Adam Boudjemaa &lt;boudjemaa.adam@gmail.com&gt; |
| **Homepage / repository** | `https://github.com/Aboudjem/goalify` |
| **License** | MIT |
| **Keywords** | claude-code, claude-code-plugin, goalify, autonomous-agents, goal-driven, task-planning, agent-skills, productivity |
| **Suggested category** | productivity |

## What happens after approval

CI pins your repo to a commit SHA in the community catalog and the public `marketplace.json` syncs
**nightly**, so goalify appears in Discover within roughly a day of approval. The local
`goalify-marketplace` (`.claude-plugin/marketplace.json`) is a personal self-hosted marketplace and is
**not** what gets submitted — the form takes the plugin repo URL, not your marketplace.

_Verified 2026-06-15 against https://code.claude.com/docs/en/plugins and the community repo README._
