# Install goalify in your editor

goalify is one Agent Skill: a `SKILL.md` with `name` and `description` frontmatter and Markdown
underneath. There is no server to run and nothing to compile. Claude Code has a first-party path;
every other agent installs the same file through the skills CLI.

## Claude Code

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Then say "goalify this: `<your task>`" or run `/goalify <task>`.

## Any other agent, in one line

```bash
npx skills add Aboudjem/goalify -a <agent>
```

The agent codes below were read from the supported-agents table in
[vercel-labs/skills](https://github.com/vercel-labs/skills#supported-agents) on 2026-09-02, along
with the directory each agent reads. That table lists 77 codes in all, so if yours is not here, it is
almost certainly in the table.

| Agent | `-a` code | Project path | Global path |
| --- | --- | --- | --- |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Zed | `zed` | `.agents/skills/` | `~/.agents/skills/` |
| Kimi Code CLI | `kimi-code-cli` | `.agents/skills/` | `~/.agents/skills/` |

So, for Cursor:

```bash
npx skills add Aboudjem/goalify -a cursor
```

Three flags worth knowing:

- `-g` installs to the global path in the table instead of the project one.
- `-y` skips the confirmation prompts, which is what you want in a script.
- `--list` prints what a repository offers and installs nothing. For this repo it reports one skill.

## Copy it in by hand

The skill is a directory. Copying it works anywhere, and it is the fallback if the CLI does not know
your agent:

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Swap the destination for your own agent's path from the table above. Nothing else in the repository
is needed at run time.

## What changes outside Claude Code

The skill itself is portable. The two-step handoff it prints is not: `/clear` and `/goal` are Claude
Code commands. Two things to know:

- **Codex** has its own `/goal`, and it also takes an inline objective under the same 4,000-character
  cap, so the condition transfers as written. What does not transfer is the brief's process
  directives, because Codex tells the model the objective is user-provided data rather than
  higher-priority instructions. Only the definition of done carries. The details, including the
  headless form, are in [running it under Codex](codex.md).
- **Everywhere else**, keep the two artifacts and adapt the two commands: start a fresh session in
  place of `/clear`, and give that session the condition in whatever way your agent accepts a
  standing objective. If it has no such mechanism, paste the condition as the first message and
  re-state it when the run drifts.

## Next

- [Quickstart](quickstart.md), a first run end to end.
- [Worked conditions](../examples/conditions.md), eight good ones and eight to avoid.
- [Honest limits](limits.md), what a stopped run does and does not prove.
