# Submission packets (you submit these — they are human-web-UI-only)

These are **ready-to-paste** field values for getting goalify discovered. Every one below is
**human-web-UI-only**: it must be filed by a person through a website form or a GitHub PR. None of them
can be done with the `gh` CLI / API, and goalify's release run does **not** auto-submit them.

| Packet | Where it goes | Mechanism | You do |
|---|---|---|---|
| [`claude-community.md`](claude-community.md) | Claude Code in-app **/plugin Discover** tab (community marketplace) | Web form at `clau.de/plugin-directory-submission` → Console form for individual authors | Fill the form |
| [`awesome-claude-code.md`](awesome-claude-code.md) | `hesreallyhim/awesome-claude-code` (~46.5k★) | **Issue form only** — `recommend-resource.yml`. PRs are auto-closed. | Open the issue |
| [`awesome-claude-skills.md`](awesome-claude-skills.md) | `ComposioHQ/awesome-claude-skills` | **Pull request** (default branch is `master`) | Fork + open PR |

Already done for you (no action needed):
- **Repo metadata** — homepage URL set and the GitHub About description refreshed to lead with the wedge
  (`gh repo edit`); 20 topics kept (they already include `claude-skill` and `context-management`).
- **Social preview image** — `assets/social-preview.png` (1280×640) is regenerated with the new
  positioning. **One manual step:** upload it under the repo **Settings → Social preview** (that upload
  has no API; it is a web-UI drag-and-drop).
- **Teaser** — `assets/goalify-teaser.mp4` is attached to the GitHub release; drag it into a tweet to
  post natively (X autoplays native uploads muted, so the baked-in captions carry it).

All facts below were verified against primary sources on 2026-06-15 (issue templates, CONTRIBUTING
files, and the Claude Code plugin docs). Re-check the live forms before filing; star counts and form
fields drift.
