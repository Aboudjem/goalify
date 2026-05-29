# Security Policy

`goalify` writes a local Markdown file and is used to set up **autonomous** Claude Code runs, so its
safety properties matter. Security is part of its design, not an afterthought.

## How the skill is built to be safe

- **It only authors a file.** The PREPARE phase researches, asks the user the genuine decisions, and
  writes one `/goal` Markdown file to a local path. It does not run the task itself.
- **No remote fetch-and-execute.** The skill and the file it generates must never download and run
  remote instructions or code. Everything the run does is described in the local file and grounded in
  the user's own repo.
- **No secrets shipped.** This repo contains no credentials, API keys, or tokens, and the skill writes
  none. Generated `/goal` files (which contain absolute paths and project context) are git-ignored.
- **No data leaves your machine.** The skill runs locally inside Claude Code. It has no telemetry and
  sends your project data to no third party.
- **Self-destruct is gated.** The generated file deletes itself **only** after every success criterion
  is met and verification passed — otherwise it is left in place so the run can resume. The `rm` is a
  low-freedom, do-not-modify command.
- **Destructive actions are gated in the generated run.** The template instructs the autonomous run to
  pause for destructive/irreversible/outward-facing actions unless explicitly pre-approved.

## What counts as a security issue here

Please report any of the following:

- A path by which the skill (or a generated `/goal` file) could **fetch and execute remote
  instructions or code**.
- A way the self-destruct `rm` could fire on the **wrong path** or before its success-criteria gate.
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

- Review the generated `/goal` file before you run it — it is plain Markdown, meant to be read.
- Treat the autonomous run like any agent with tool access: run it on work you own, and keep the
  destructive-action gate intact.
