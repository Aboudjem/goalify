# Security Policy

`goalify` writes a local Markdown file and is used to set up **autonomous** Claude Code runs, so its
safety properties matter. Security is part of its design, not an afterthought.

## How the skill is built to be safe

- **It only authors local artifacts.** The PREPARE phase researches, asks the user the genuine
  decisions, and writes an implementation brief (Markdown) plus the derived `/goal` condition string to
  local paths. It does not run the task itself.
- **No remote fetch-and-execute.** The skill and the file it generates must never download and run
  remote instructions or code. Everything the run does is described in the local file and grounded in
  the user's own repo.
- **No secrets shipped.** This repo contains no credentials, API keys, or tokens, and the skill writes
  none. In a repo that already has a `.gitignore`, the skill appends `.goal/` to it so generated briefs
  (which contain absolute paths and project context) are not committed — note it does **not** create a
  `.gitignore` where none exists, so in that case `.goal/` is unprotected until you add one.
- **No telemetry, and your repository is never uploaded.** The skill runs locally inside Claude Code.
  It does not phone home and does not transmit your source tree. It is **not** fully offline, though:
  the PREPARE phase's research step issues outbound web searches and documentation fetches whose
  queries are derived from your task, so those queries reach third parties (search engines, docs sites,
  forums). If that matters for your work, say so up front and goalify will skip the web research.
- **The archive step is gated.** The brief moves to `.goal/done/` **only** after every success
  criterion is met and verification passed — otherwise it is left in place so the run can resume. The
  `mv` is a low-freedom, do-not-modify command with a path rail restricting it to the brief's own
  absolute path under `.goal/`. Since v2.0.0 it archives rather than deletes, which also means a failed
  or misjudged run destroys nothing.
- **Destructive actions are gated in the generated run.** The template instructs the autonomous run to
  pause for destructive/irreversible/outward-facing actions unless explicitly pre-approved.

## What counts as a security issue here

Please report any of the following:

- A path by which the skill (or a generated `/goal` file) could **fetch and execute remote
  instructions or code**.
- A way the archive `mv` could fire on the **wrong path** or before its success-criteria gate.
- Anything that could **leak credentials**, tokens, or a user's private project data off the machine.
- A generated file that is **not** self-contained / not absolute-path'd in a way that could cause a
  fresh session to act on the wrong target.

## Reporting a vulnerability

**Please do not open a public issue for a security problem.**

Email **boudjemaa.adam@gmail.com** with:

- A description of the issue and its impact.
- Steps to reproduce.

You will get a response within 48 hours. Once a fix is ready, the issue will be disclosed
responsibly with credit to the reporter if wanted.

## Your responsibility when running it

- Review the generated brief before you start the run — it is plain Markdown, meant to be read — and
  read the condition string too, since that is what actually decides when the run may stop.
- Remember that a stopped `/goal` run is not proof of completion: the evaluator can end a run by
  judging the condition unachievable. Verify the outcome yourself before acting on it.
- Treat the autonomous run like any agent with tool access: run it on work you own, and keep the
  destructive-action gate intact.
