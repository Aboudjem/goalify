# Submission packet — hesreallyhim/awesome-claude-code (~46.5k★)

**Mechanism — GitHub issue form ONLY.** This list accepts submissions *only* through the
`recommend-resource` issue template. CONTRIBUTING says verbatim: *"Do not open a PR. Just fill out the
form,"* and *"ALL RECOMMENDATIONS MUST BE MADE USING THE WEB UI ISSUE FORM TEMPLATE, OR YOU RISK BEING
BANNED."* PRs are auto-closed by a workflow. A bot validates the issue; if it passes maintainer review,
a PR is auto-created for you.

**Open the form here (web UI only):**
`https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml`

> ⚠️ **Eligibility gates to satisfy first** (the checklist enforces them):
> - It must be **over one week** since goalify's first public commit. (First release was 2026-05-29, so this is satisfied.)
> - You must have **no other open issue** in that repo when you file.

## Field values to paste

| Form field | Value |
|---|---|
| **Title** (overwrite the placeholder) | `[Resource]: goalify` |
| **Display Name** | `goalify` |
| **Category** (dropdown — exact) | `Agent Skills` |
| **Sub-Category** | _(leave blank — optional)_ |
| **Primary Link** | `https://github.com/Aboudjem/goalify` |
| **Author Name** | `Adam Boudjemaa` |
| **Author Link** | `https://github.com/Aboudjem` |
| **License** (dropdown) | `MIT` |
| **Other License** | _(leave blank)_ |
| **Description** (1–3 sentences, no emojis) | goalify is a Claude Code skill that prepares a big coding task to run autonomously across a `/clear`. In one session it researches the repo, locks the few real decisions, and writes a self-contained `/goal` file whose success criteria are wired to real commands; you then run `/goal <path>` in a fresh session that executes the whole job, verifies every criterion, and deletes the file on success. |

### Mandatory-for-skills fields (the three "Validate Claims" boxes)

> The schema marks these optional, but an in-form note makes them **required for skills/plugins**.

- **Validate Claims:** Clone the repo and run `python3 evals/check_skill.py skills/goalify/SKILL.md`
  and `python3 tests/test_manifests.py` — both exit 0 and assert the skill's structure and the gated
  self-destruct. The recorded RED→GREEN baseline (Haiku/Sonnet/Opus) is in `evals/RED-baseline.md`.
- **Specific Task(s):** Prepare an autonomous run that migrates an Express callback API to async/await
  without losing the plan across `/clear` (a fresh session should execute and verify it, then the goal
  file deletes itself).
- **Specific Prompt(s):** `goalify this: migrate our Express API from callbacks to async/await and keep the tests green`

| **Additional Comments** | _(optional)_ Ships as a Claude Code plugin in the 10x marketplace and as a drop-in skill; MIT; built test-first with a CI eval. |

### Recommendation Checklist — tick all 5 (all required)

- [x] I have checked that this resource hasn't already been submitted
- [x] It has been over one week since the first public commit to the repo
- [x] All provided links are working and publicly accessible
- [x] I do NOT have any other open issues in this repository
- [x] I am primarily composed of human-y stuff and not electrical circuits

_Verified 2026-06-15 against the live `recommend-resource.yml` and `docs/CONTRIBUTING.md`. Category list
and License list are the exact dropdown options._
