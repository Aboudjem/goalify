# Submission packet — ComposioHQ/awesome-claude-skills

**Mechanism — Pull Request** (not an issue). Fork, add the README line under the right category, open a
PR. The repo's **default branch is `master`** (not `main`).

## The exact steps (per CONTRIBUTING.md)

```bash
# 1. Fork ComposioHQ/awesome-claude-skills on GitHub, then:
git clone https://github.com/<your-fork>/awesome-claude-skills
cd awesome-claude-skills
git checkout -b add-goalify
# 2. Edit README.md — add the line below under "### Productivity & Organization", in alphabetical order
git commit -am "Add Goalify skill"
git push origin add-goalify
# 3. Open a Pull Request titled "Add Goalify skill"
```

## The README line to add

Category: **Productivity & Organization**. goalify lives in its own repo, so use the **external-skill**
variant (full GitHub URL + author attribution), matching live entries like `n8n-skills`. Place it
alphabetically (lowercase `goalify` sorts near the top of the section). No emojis, one sentence,
consistent punctuation:

```markdown
- [goalify](https://github.com/Aboudjem/goalify) - Turns a big coding task into a self-contained /goal file that a fresh Claude Code session executes and verifies before it self-deletes. *By [@Aboudjem](https://github.com/Aboudjem)*
```

## PR description (required content)

The CONTRIBUTING guide asks the PR body to cover four things:

- **What problem it solves:** a plan made in chat dies at `/clear`; goalify writes a self-contained,
  resumable `/goal` file so a fresh, full-context session can execute and verify the whole task.
- **Who uses this workflow:** Claude Code users running substantial autonomous jobs (refactors,
  migrations, audits) who want machine-checkable success criteria instead of vibes.
- **Attribution / inspiration:** original work by Adam Boudjemaa (@Aboudjem); MIT licensed.
- **Example:** `goalify this: migrate our Express API from callbacks to async/await and keep the tests
  green` → goalify writes `~/repo/.goal/<task>.md`; you `/clear` then `/goal <path>`.

> Note: the repo also asks that contributed skills ship a `SKILL.md` with `name` + `description`
> frontmatter. goalify already has a spec-correct one at `skills/goalify/SKILL.md`, so linking the repo
> (external variant) satisfies this — you do **not** need to copy a folder into the Composio repo unless
> you prefer the in-repo `./goalify/` variant.

_Verified 2026-06-15 against `master` branch README.md + CONTRIBUTING.md (the `main` raw URLs 404)._
