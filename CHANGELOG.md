# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [2.6.1] - 2026-09-03

A motion identity, and the literal synthwave scenery removed. No behaviour changes.

### Changed

- **Every asset is rebuilt around one principle:** the whole mark is drawn once as a muted track,
  and a single bright element travels over it, so no frame of the loop is an incomplete logo and
  the reduced-motion resting frame is the finished mark. This plugin's motion is
  a pin flying into the centre of the target, the rings pulsing once behind it.
- **The scenery is gone.** No sun disc, no horizon line, no perspective grid and no band cuts in
  any tracked SVG. The palette, the soft dual-tone wash, the restrained glow and the mono eyebrows
  stay.
- **Zero SMIL.** Every animation is now CSS, gradient colour drift included, so the
  `prefers-reduced-motion` guard reaches all of it. Verified by phase offset in a single page load,
  not by two renders at different virtual-time budgets, which gives a false negative.
- **More vibrant, still readable.** The ground is lifted off near-black and tinted with this
  plugin's own hue, every gradient drifts between two accents, and every text fill was re-measured
  against the ground it actually ships on. Tightest pair in this repo: 5.00:1.

### Added

- `assets/logo-mark-animated.svg` and `assets/logo-mark-animated-light.svg`, a 256x256 animated mark on a
  rounded tile, under 6 KB each, with dark and light variants.
- `logo-mark.png`, `logo-mark-512.png` and `social-preview.png` are now headless-Chrome renders of
  the mark's reduced-motion resting frame, so the raster is reproducible from the vector by one
  command and cannot drift from it.

## [2.6.0] - 2026-09-02

A new visual identity, a README rebuilt to the shape of the ones people actually read, four
translations, an install path for every agent, and three additions that make the condition easier
to get right.

### Added

- **A gallery of worked conditions** (`examples/conditions.md`). Eight task-to-condition pairs. Each
  pair is a condition worth shipping next to the way the same job usually comes out on the first
  try, plus one line naming the tooth the bad one loses: the bare path, the judgment call, the
  unnamed command, the self-satisfying claim, the lawyerly restatement, the missing bound, the
  ticked checkbox the evaluator cannot see, and the sentinel that is only the word "done". Eight new
  assertions in `tests/test_manifests.py` pin every pair, each verified RED on a scratch copy first.
- **A condition linter** (`skills/goalify/scripts/condition_lint.py`). Standard library only, reads
  argv or stdin, six rules: the 4,000-character ceiling, a stated finish line, the condition is a
  sentence and not a path, any stop-after clause carries a number, the last sentence bounds the
  loop, and no bare `$`. `tests/test_condition_lint.py` gives each rule its own specimen, asserts
  the exact rule ids that fire, and pins what the linter cannot see: it catches three of the eight
  gallery anti-patterns, and the other five pass every rule while still being bad conditions.
  Wired into `validate.yml`. goalify is still a skill plugin: no MCP server, no standalone CLI, no
  runtime dependency, no network call.
- **A wrap-up clause near the turn cap**, in the brief template in `skills/goalify/SKILL.md`. Within
  about five turns of the cap the run stops starting new work, finishes or reverts what is half
  done, commits what is green, ticks the checklist honestly, writes what is left into the brief, and
  says in the final report that it stopped early. The archive gate is untouched: unticked boxes
  still mean the brief stays where it is. `evals/check_skill.py` pins every step of the clause, and
  `tests/test_manifests.py` asserts `examples/sample-brief.md` carries it too.
- **The Neon Noir identity.** `assets/logo-mark.png` (1024) and `assets/logo-mark-512.png`,
  `assets/hero-dark.svg` and `assets/hero-light.svg` (1200x400 README banners),
  `assets/logo-dark.svg` and `assets/logo-light.svg` (720x200 lockups), and
  `assets/social-preview.svg`, the source for a regenerated `assets/social-preview.png` at exactly
  1280x640. The mark is three concentric rings with a pin driven through the centre on the diagonal.
- **Four translations**, `READMEs/{zh-CN,ja,es,fr}.md`, linked from a language row under the badges.
  Prose only: all seven fenced blocks are byte-identical to the English, every relative link carries
  `../`, and each file ends with a machine-assisted-translation note in its own language. One
  reviewer per language checked each file against the English for drift before it shipped.
- **Editor install manifests and a per-agent table.** `.cursor-plugin/plugin.json` and
  `.copilot-plugin/plugin.json` mirror the Claude manifest without an `mcp` key, and both are now
  covered by the same version-parity assertion as the other four sources, so a tag can no longer
  ship a stale number inside them. `docs/editors.md` is new: the `-a` code, the project path and the
  global path for Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, OpenCode, Windsurf, Zed
  and Kimi Code CLI, read from the `vercel-labs/skills` supported-agents table on 2026-09-02, plus
  the manual copy path and what changes about the handoff outside Claude Code.
- Release workflow: pushing a `vX.Y.Z` tag now creates the GitHub release and tells the 10x
  marketplace to re-sync (`.github/workflows/release.yml`).

### Changed

- **README rewritten**, 95 lines to 168, to the plugin skeleton: a light and dark hero through
  `<picture>`, three badges, the language row, the one-sentence purpose, six jump links and the
  install block, all inside the first 30 lines, then What it does, Install, Use it, What you get,
  Works in your editor, Good to know, Learn more. The install command moves from line 45 to line 28.
  Gone: 19 em-dashes, the emoji bullets, and the numbered steps that trailed the block they
  explained. Each of the three additions above gets exactly one line.
- **`hero.svg`, `how-it-works.svg` and `two-artifacts.svg` rebuilt in place** in the new identity:
  same viewBoxes, same words, same pinned counter-examples, a dark ground instead of the paper one.
  Every shipped SVG stays self-contained and animated, with no `<script>`, no external reference,
  a reduced-motion guard, and every font stack ending in a generic family.
- **`docs/quickstart.md`** gains the `npx skills add` line and a pointer to the per-agent table.
- **`AGENTS.md`** now restates the invariant in as many words: goalify is a skill plugin with no MCP
  server, no standalone CLI, no runtime dependency and no network call, and the linter is a helper
  the skill may call.

### Fixed

- **Two wrong explanations in the conditions gallery.** Pair 1 claimed the bare path loses all four
  teeth when it still carries the brief's path, and pair 5's anti-pattern had dropped the evidence
  clause as well, so its explanation named the wrong defect. Both are corrected and the gallery now
  asserts the evidence clause and the sentinel over every worked condition.
- **The v2.6 eval assertions pinned fragments, not the clause.** The wrap-up clause could have been
  gutted to its first sentence and still passed. Every step it mandates is now pinned in both the
  template assertion and the example's.
- **`evals/RED-baseline.md` carried a wrong figure since 2026-08-07.** Running the previous checker
  against the v1.1.0 skill returns 30/78, not the 29/78 recorded. The file now states the corrected
  figure and how it was re-derived. Current baseline: RED 30/83, GREEN 83/83.
- **The em-dash in both manifest descriptions** became a comma, so `plugin.json` and
  `marketplace.json` still agree and the 10x marketplace pins a description the house style allows.
  The em-dashes inside `skills/goalify/SKILL.md` stay: `evals/check_skill.py` pins the story and the
  canonical condition byte-identically, and its vocabulary-lock assertions match on em-dash phrases.

## [2.5.0] - 2026-08-07

The simplicity redo: a brand-new visual direction anyone gets in seconds, plain-English copy with
use cases anyone can picture, and a fully re-scripted teaser.

### Changed

- **New visual direction — "Sunday Worktable" — replaces Deep Plum Neon** across all five visuals
  (hero, two-artifacts, how-it-works, social card, teaser): a warm paper field, the brief as a
  sheet of paper with a blue binding edge, the condition as an ochre capsule label, proof green
  spent once per asset. Chosen by a multi-model design battle (codex, kimi and gemini each produced
  two directions; a three-grader cross-model panel confirmed the winner; a separate judge wrote the
  implementation spec with 26 measured contrast pairs, 0 failures — lowest body-text pair 5.74:1
  against the 4.5:1 floor). Every SVG stays self-contained, animated and reduced-motion-aware, and
  renders identically on GitHub light and dark.
- **README and docs re-read in simple English**, with use cases a non-programmer can picture
  (rename one thing everywhere, move an old project onto newer code, clean up a messy project);
  every jargon word glossed in the same breath or cut; the builder-plans/inspector comparison used
  once. Two-persona judge: the non-technical reader answered 3/3 correctly from the README alone,
  and the mechanical checklist passed. The story and the 149-character condition stay
  byte-identical on every surface that carries them.
- **Teaser fully re-scripted** (27.9s, 836 frames) in the new direction: no terminal chrome, every
  frame a complete statement, and the `/goal` beat now shows the condition carrying all four teeth
  — the brief's path inside it, the quoted-evidence clause, the sentinel word, the turn bound —
  each underlined and captioned in plain words (closes the v2.3 adversary's S5 follow-up). GIF
  re-derived (13fps, 900px).

### Removed

- `video/src/ConceptHero.tsx` (11,895 bytes) and `video/src/neon.tsx` (7,348 bytes) — the Deep
  Plum Neon composition and palette, superseded by the self-contained `GoalifyTeaser.tsx`.
  Evidence: no tracked file imports them any more (`Root.tsx` imports `GoalifyTeaser.tsx` only,
  and CI's import-walk gate would fail on a dangling import).

### Repo hygiene

- `MIGRATION.md` is now discoverable — listed in AGENTS.md's "Where things live".
- `video/scripts/genmusic.js` is now documented in `video/README.md`'s commands block.
- `assets/social-preview.png` kept deliberately (it is the repo's GitHub social-preview image) and
  regenerated at exactly 1280×640 in the new direction.
- `.claude/` added to `.gitignore` (local session lock files; parity with `.omc/`).

## [2.4.0] - 2026-08-06

The confident-closer re-voice. One story on every surface — "Hand Claude a huge task. Come back to
proof it's done — not a promise that it is." — and a README built to land in seconds.

### Changed

- **README rewritten in the new voice.** The story up top, a short plain answer to "what is this"
  that includes a two-line explanation of the built-in `/goal` command, an eight-item
  **What you get** feature list (one-line handoff, survives `/clear`, decisions locked first, live
  progress, proof-or-nothing, resume on stop, hard turn cap, proof-then-archive), then the same
  three steps, right/wrong pair and stopped-run caveat. Copy went through a humanizer pass to strip
  AI-writing patterns.
- **The story replaced verbatim on every surface**: quickstart, `llms.txt`, `plugin.json`,
  `marketplace.json` (both fields), and the skill's frontmatter description and overview —
  with `check_skill.py`'s two verbatim-story assertions re-pinned to the new wording in the same
  commit (still 78/78; the RED baseline is unchanged at 30/78).
- **Social card re-voiced** (story plus legend glosses) and re-shot at exactly 1280×640, viewed;
  the hero's title bar now reads "hand it off · come back to proof", re-rendered two-timestamp
  (hashes differ) and viewed.
- **The contract is untouched.** Same 149-character canonical condition, byte-identical in the same
  five places; same gates, same counts, same facts.

## [2.3.0] - 2026-08-06

A README a non-technical reader gets in thirty seconds, a one-line handoff, shorter and plainer
conditions, and four hardened gates. The condition contract itself is unchanged.

### Changed

- **README radically rewritten to ~90 lines.** A two-sentence plain-words story ("You describe a
  big coding job…"), ONE image, three numbered steps carrying the literal **149-character**
  condition (down from 157), a single `[!IMPORTANT]` stopped-run caveat, and links out to docs/.
  Install variants, the with/without table and the deep two-artifacts dive moved to
  `docs/quickstart.md`. A separate two-persona judge (a smart non-technical reader plus a
  mechanical checklist) reviewed the draft; all seven required fixes were applied before ship.
- **The canonical worked condition is shorter and plainer** — "Do everything in
  ~/acme/.goal/api-migration.md and prove it — done when the last turn quotes npm test passing and
  says ASYNC-OK. Stop after 40 turns." (149 characters), byte-identical across the README sequence
  block, the README right/wrong fence, the hero's condition plate and `<desc>`, and the quickstart
  fence. Abridged renderings keep their ellipsis-marked short forms.
- **The skill authors short, plain conditions by default** (~120–150 characters, everyday words),
  with four mandatory teeth: the brief's path inside, a quoted-evidence clause naming a runnable
  command, a made-up sentinel, and a turn bound. The 4,000-character cap is now framed as a ceiling,
  not a target; heavy process directives moved into the brief, which the worker reads in full.
- **The handoff is two steps: `/clear`, then ONE short `/goal` line** with the whole condition
  inline. No file launcher, no wrapper script, no copy step — the user is never left holding only a
  path.
- **Every brief the skill authors now requires live visible progress** — one task per phase in the
  task tracker, flipped in progress → completed as work lands, plus the brief's own checklist as
  resume state — and a final report of short bullets under **Done / Proof / Next** that states
  plainly a stopped `/goal` run is not proof of completion. The PREPARE phase obeys the same two
  rules itself and never prints the handoff while a subagent is still running.
- **One story, verbatim on every surface**: README tagline, quickstart, `llms.txt`,
  `plugin.json`, `marketplace.json` and the skill's frontmatter and overview.
- **All three SVGs and the social card redesigned from scratch** through a multi-model design pass
  (two independent candidate sets, cross-checked, winners picked by a separate judge): a
  terminal-chrome system in the same Deep Plum Neon palette, artifacts coded by shape as well as
  colour (sharp folded sheet = brief, capsule = condition), `/goal` always a neutral chip outside
  the condition plate, struck counter-examples static and marked. Animation proven by two-timestamp
  headless renders; every asset viewed at 900px on dark and light and at 380px;
  `social-preview.png` regenerated at exactly 1280×640. The teaser was not re-rendered — the new
  assets match its palette and framing (its spoken condition predates the four-teeth rule).
- **The shipped example matches the new default**: its condition rewritten to the short shape
  (190 characters, all four teeth), the displaced closeout-turn / freshly-quoted / impossible-hatch
  clauses moved into its brief body, and the brief gained the live-progress and Done/Proof/Next
  directives — with `tests/test_manifests.py`'s example assertions moved in the same commit.
- **docs/faq.md and docs/limits.md record three newly verified facts**, re-derived from the shipped
  Claude Code 2.1.223 binary: the evaluator behind `/goal` has a 30-second default timeout per
  check; two hard gates can block `/goal` entirely (untrusted workspace, restricted hooks — exact
  messages quoted); an over-4,000-character condition is rejected loudly before any hook is
  registered, and on long runs the evaluator's transcript view drops the oldest messages with a
  banner instructing it to answer not-met if the evidence may sit in the dropped beginning.

### Added

- **Four gate blind spots closed in `tests/test_manifests.py`**, each proven RED on a purpose-built
  specimen in a temp tree and GREEN on the real one, with permanent in-suite self-tests so the
  specimens stay caught: attribute values (`aria-label`, `alt`, `title`, `content`, `data-*`) are
  scanned across svg/xml/html/md/tsx/json; HTML entities, NFKC compatibility forms, slash and
  common letter homoglyphs, and zero-width characters are normalised before every scan; tracked
  HTML and the SVGs are flattened with both spaced and tight joins, so a command split mid-word
  across inline tags is still seen; and
  the words-only counter-example in `two-artifacts.svg` is pinned marked-and-struck by a dedicated
  assertion. Exemptions deliberately re-pinned 10 → 15 (the five new marked specimens in the test
  file itself).
- **`evals/check_skill.py` grew 55 → 78 assertions** (+23 new v2.3 clauses, 1 tightened knowingly,
  0 deleted), pinning the short-condition default, the four teeth, the one-line handoff, the
  Done/Proof/Next template, the live-progress rules, the no-handoff-while-agents-live rule, and —
  after an adversarial pass caught the template omitting it — the closeout-turn directive inside
  the brief template itself. The RED baseline against v1.1.0 was re-run, not predicted: **30/78**.

## [2.2.0] - 2026-08-05

A mass-audience README in plain English, and a dark neon visual system that finally matches the
teaser. The condition contract itself is unchanged.

### Changed

- **README rewritten from scratch in plain, pain-first English.** It opens on the reader's problem —
  the plan dying at `/clear` — before goalify is named, shows the whole handoff in one block with the
  literal 157-character condition, and adds a with/without comparison plus a what-you-get list. The
  two-artifact distinction stays in flowing prose; the single `[!IMPORTANT]` remains reserved for the
  stopped-run caveat. A separate judging agent reviewed the draft against the voice spec before it
  shipped, and an independent codex critique rated the result **9/10**, twice in a row. (For
  calibration: the pre-v2.1.0 README rated 5/10, under an earlier and harsher critique prompt.)
- **All five visuals now share one Deep Plum Neon system** — the palette the teaser already used
  (`video/src/neon.tsx`). `hero.svg`, `two-artifacts.svg` and `how-it-works.svg` are self-contained
  dark cards with their own fill, so they render identically on both GitHub themes (a deliberate
  dark panel on light). The two-lane grammar is unchanged: warm solid rail for the brief, cool
  dashed rail for the condition, `/goal` outside the condition plate, the struck counter-example at
  full opacity in every frame. Animation proven by two-timestamp headless renders; every asset
  viewed at 900px on dark and light pages and at 380px.
- **The worked example's condition is byte-identical everywhere it appears in full** — the README
  sequence block, the right/wrong fence, the hero's condition plate and the hero's `<desc>` all
  carry the same 157 characters. Renderings that abridge it (two-artifacts, social card, teaser) now
  mark the cut with an ellipsis.
- **docs/ rewritten in the same voice with zero factual drift** — quickstart, FAQ, honest limits and
  the Codex page were each rewritten by its own agent and cross-checked line by line against the old
  page; an independent verifier then re-derived the load-bearing claims from primaries.
- **Social card and teaser re-voiced to the new copy.** `social-preview.png` regenerated at exactly
  1280×640 in the dark system; the teaser re-rendered (30.5 s) with its `/goal` beat showing the
  condition that names the brief's path.
- **Descriptions rewritten in the same voice**: `plugin.json`, `marketplace.json`, the `llms.txt`
  opening, and the README tagline — now "evidence you can check yourself", the honest form of the
  old "prove it finished".

### Fixed

- Two literal-truth defects the critique caught: the quickstart/FAQ claim that "nothing in your repo
  changes" during prep (goalify writes the two artifacts under `.goal/`), and a comparison-table
  cell that implied every stopped run reruns its checks — only a successful closeout does.

## [2.1.0] - 2026-08-05

A README rebuilt around the contract, a new visual system, and two CI gates that close the holes the
last two releases slipped through. The condition contract itself is unchanged.

### Fixed

- **The hero image still shipped the bug v2.0.0 exists to fix.** `assets/hero.svg` rendered
  `/goal  api-migration.md` — a file path — as the first thing a visitor saw, through two releases of <!-- v1-antipattern -->
  source-level review. The reason it survived is the interesting part: the string was split across
  `<tspan>` elements, so in the raw bytes `/goal` is followed by `<`, and the line-oriented regex in
  `tests/test_manifests.py` could never match it. **The test now flattens `itertext()` per `<text>`
  element, and again across the whole document**, so a command split across tags — including inside a
  `<foreignObject>`, which has no `<text>` ancestor at all — is caught. Verified the way it should
  have been the first time: the new check fails against the old asset, and against a purpose-built
  `<foreignObject>` probe.
- **The same gate was defeated by a quotation mark.** An adversarial pass proved that
  `/goal "~/path.md"`, the backtick form, the `**emphasis**` form, the `[markdown](link)` form and the <!-- v1-antipattern -->
  Windows `C:\...` form all passed while reading as unambiguous instructions to do the banned thing.
  Lines are now normalised before matching (markdown links collapse to their target, quoting and
  emphasis characters are dropped), a two-line window catches a wrapped command, and the absolute-path
  form requires a real separator so the word `/goal` is no longer mistaken for the start of a path.
  All ten forms are now caught; three legitimate forms are still correctly ignored. The one gap that
  remains — a path introduced by intervening words — is written down in the test rather than implied
  away.
- **The handoff put a file path in the user's hand at the exact moment they type `/goal`.** Step 2 of
  the printed handoff was `pbcopy < <condition file>`. `SKILL.md` now prints the **complete `/goal`
  line inline and verbatim**, ready to copy in one piece; `.goal/CONDITION-<slug>.txt` remains as a
  durable fallback and is explicitly demoted to "a convenience, never the required step".
  `evals/check_skill.py` asserts both halves of that, and fails against the old handoff.
- **Thirteen tracked files blurred the two artifacts into one imaginary one**, naming the brief as though
  it were the thing `/goal` receives. The vocabulary is now **brief** (a file) and **condition** (a
  string) everywhere, and a new gate rejects the blurred phrasing across every tracked text file. The
  worked example is renamed `examples/sample-brief.md`.

### Added

- **`assets/two-artifacts.svg`** — a new diagram whose only job is the routing rule: the brief file
  goes to the worker, the condition string goes to `/goal`'s evaluator, and the evaluator has no tools.
- **A gate asserting every shipped SVG is animated**, well-formed, script-free, free of external
  references, and that every font stack ends in a generic keyword (an unmatched stack falls back to
  *serif*, which is the loudest possible failure).
- **`docs/codex.md`, `docs/limits.md`, `docs/faq.md`** — the Codex specifics, the full honest-limits
  list, and the long-tail FAQ, split out of the README. The limit that changes behaviour stays visible
  in the README itself rather than being buried by the split.

### Changed

- **A new visual system across all five assets.** The dark-terminal-card metaphor is retired. Four
  directions were explored in parallel and judged by a separate agent (`.goal/design-directions.md`);
  the chosen one codes the two artifacts as two lanes — warm/square/solid for the file, cool/round/
  dashed for the string — so the routing survives a thumbnail, a grayscale screenshot, and
  colour-blindness. Only the two artifacts get an opaque plate; everything else sits on a transparent
  canvas in an ink (`#6E7887`) sitting essentially on the dual-safe optimum — solving
  `1.05/(L+0.05) = (L+0.05)/(L_dark+0.05)` for `#0d1117` gives `L = 0.1914` and a ceiling of
  4.35:1; the chosen ink measures `L = 0.1850`, **4.47:1 on white and 4.24:1 on `#0d1117`**. That
  clears WCAG AA Large (3:1) on both themes, which is the applicable bar for display type, and is
  short of the 4.5:1 normal-text bar — an unavoidable consequence of asking one colour to work on
  both backgrounds, which is why small text sits on a plate instead.
- **Text is legible on a phone.** The retired assets used a 1200-unit viewBox with a 12-unit type
  floor — under 4 px on a 340 px column. The new ones use a 900-unit viewBox and a 28-unit floor,
  clearing the `viewBox / 34` bar with margin.
- **Motion is gentle by construction.** `prefers-reduced-motion` does not reach an `<img>`-embedded
  SVG, so the user cannot opt out; the fastest feature is now 0.2 Hz against WCAG 2.3.1's 3 Hz limit,
  nothing meaning-bearing animates from zero, and the struck-through counter-example never animates at
  all — no single frame can show it un-negated.
- **The README is rebuilt around the reader's first question.** The v2.0.0 forensics move here; the
  two-artifact model and a real, literal condition string arrive in the first screenful instead of
  around line 111; and the brief-vs-condition distinction is flowing prose immediately before the
  `/goal` step rather than a callout, because readers skip callouts.
- **The teaser is re-cut** to the same lane coding and the same worked example, and its `/goal` beat
  now shows a condition that names the brief. 916 frames, 30.55 s.
- `assets/social-preview.png` regenerated at 1280×640 from the rebuilt `social-card.html`.

## [2.0.1] - 2026-08-04

Documentation corrections found by an independent post-release verification pass. No behavior change;
the skill, the condition contract, and the tests are identical to 2.0.0.

### Fixed

- **`.github/workflows/validate.yml` asserted an incident that never happened.** Two comments claimed a
  commit "merged green and broke HEAD's build" and that a broken `HEAD` had "shipped". Resolving every
  relative import in `video/src` against every commit reachable from all refs shows all of them clean.
  The v2.0.0 recut came one `git commit -a` away from a tree whose imports do not resolve — which is
  what the 2.0.0 entry below already says — but the near miss was never an incident, and a release
  premised on not overstating things should not have overstated this.
- **`README.md` and `SKILL.md` gave incompatible provenance for the Codex 4,000-character cap** — one
  said the limit is interpolated at runtime in the binary, the other said it is enforced server-side.
  Both now give the same account: the number is not a greppable literal, so it was established by
  probing the boundary live (4,000 accepted, 4,001 rejected).
- **The `v1-antipattern` exemption cap was `<= 4` with 3 in use**, leaving one free slot through which
  a genuine path handoff could have passed silently. It is now pinned to exactly the number in use, so
  adding one fails the build. Its failure message also claimed the test verifies each exemption is
  *prose about* the old handoff; it only counts lines, and now says so.
- **`evals/scenarios.md` still pointed the RED demo at the retired `goal-prep` file** that no longer
  exists — the exact unfalsifiable baseline 2.0.0 replaced everywhere else.
- **`evals/README.md` repeated the v1-era behavioral numbers** without the "dated record, not evidence"
  caveat `RED-baseline.md` carries.
- **`AGENTS.md` and `llms.txt` opened with the superseded one-artifact framing** before correcting
  themselves a few lines later. Both are machine-consumed entry points, so the first sentence matters.

## [2.0.0] - 2026-08-04

**goalify's central handoff was wrong, and this release fixes it.**

`/goal` takes a **completion condition, not a file path.** Every version before this one told you to
run `/goal <the-file-it-wrote>`. That path string simply *became* the condition. The evaluator behind
`/goal` has no tools and cannot read files, so on every turn it was asked whether the literal string
`/Users/you/.goal/task.md` had been satisfied — a question it can never answer from the transcript.
The run either never resolved, resolved arbitrarily, or ended early because the evaluator judged the
condition unachievable — stopping with the work unfinished. It *looked* fine because the first turn read
the path and started working; the finish-line gate goalify advertised was never actually running.

The evidence, so you can check rather than trust:

- Docs, https://code.claude.com/docs/en/goal — *"Run `/goal` followed by the condition you want
  satisfied"*, *"The condition can be up to 4,000 characters"*, and *"It doesn't run commands or read
  files independently, so write the condition as something Claude's own output can demonstrate."*
- The shipped Claude Code binary (2.1.221) contains `No goal set. Usage: `/goal <condition>`` and
  `Goal condition is limited to <N> characters`. The `/goal` handler has three branches — empty,
  clear, and "treat the rest as the raw condition". There is no file-path branch.

### Changed — BREAKING

- **The handoff is now a derived condition string, not a path.** goalify still writes a self-contained
  implementation brief, but it now also **derives a `/goal` condition from that brief's definition of
  done** and writes it to `.goal/CONDITION-<slug>.txt` as a durable copy. The handoff became
  three steps: `/clear` → copy the condition → run it, with auto mode on for an unattended
  run (it is the default in current Claude Code).
- **The generated brief separates the definition of done from the process directives.** The definition
  of done is portable and is what the condition is derived from; the process directives are what binds
  reliably in Claude Code only. This split is what makes the same brief usable under Codex.
- **Self-destruct became an archive step.** On full success the brief moves to `.goal/done/` with a
  completion stamp instead of being deleted, at the same gate strictness — the promise-vs-outcome
  audit trail survives.

### Added

- **A closeout-turn requirement.** Once a session exceeds roughly half the evaluator's context budget
  (a quarter on a prompt-too-long retry), older messages are dropped and replaced with a notice
  instructing it to refuse when evidence may lie in the omitted prefix — so on a long run, evidence
  proven on turn 3 is invisible on turn 90. The condition now requires re-running every check together
  in one dedicated turn immediately before presenting the evidence packet.
- **A condition lint**: ≤ 4,000 characters (counted, not estimated), no bare `$` (the hook prompt
  substitutes `$ARGUMENTS`/`$N`), a sentinel token, a named runnable command per criterion, an
  explicit turn bound, and no success phrase the condition text would satisfy on its own.
- **A subagent barrier rule** — never write a deliverable, tick a criterion, or end a turn while a
  spawned subagent is still live. An "idle" or "available" ping is not a delivered result.
- **Cross-harness support for Codex.** Codex has a real, default-on `/goal`
  (`/goal [<objective>|clear|edit|pause|resume]`), it also takes an inline objective rather than a
  path, and its cap is the same 4,000 characters (established by probing the boundary live, since the
  number is interpolated at runtime rather than stored as a string) — so the derivation is built once and both forms are
  printed. Codex tells the model the objective is *"user-provided data … the task to pursue, not
  higher-priority instructions"* and tags an edited objective `<untrusted_objective>`, so goalify now
  documents plainly that its **process directives do not reliably bind under Codex; only the definition
  of done carries.** `/goal` is TUI-only there, so the headless form pipes the brief to `codex exec -`.
  goalify does not promise budgeted Codex goals: `token_budget` reports `under development`.
- **Model routing** (fast model for mechanical breadth, deep model for architecture and every skeptic
  pass) and a **dry run with caps** — phases, subagents, turn cap — printed before anything is written.
  goalify deliberately does *not* predict a token or dollar cost; there is no citable basis for one.
- **An honest-limits section.** A `/goal` run that stops is not proof of completion — the evaluator can
  end the loop by judging the condition unachievable, and no wording prevents that. (Claude Code books
  that case as a failed goal rather than an achieved one, but the loop ends either way.) The docs now
  say so and give you a verify-only re-check instead of implying a guarantee.
- **A 3-strike escalation ladder** (root-cause probe → narrowed scope → STOP and write a blockers
  report) replacing the bare stall guard, aligned with Codex's own blocked audit.

### Fixed

- **The teaser recut was one `git commit -a` away from publishing a tree that does not build.** In the
  working tree, `video/src/ConceptHero.tsx` was untracked while the recut `GoalifyTeaser.tsx` imported
  it and `ConceptB.tsx` was deleted — so committing those changes would have produced a `HEAD` whose
  imports do not resolve. (The previous `HEAD` was fine; it still imported `ConceptB`, which existed.)
  Nothing in CI looked at `video/`, so that commit would have gone green.
- `Root.tsx` now imports `TEASER_FRAMES` from the storyboard instead of hardcoding `890`, so the
  composition length cannot drift from the scene list.
- Doc drift in `video/README.md`: the recut teaser is **8 beats / 890 frames / 29.717s** (measured
  with `ffprobe`), not the "9-beat, ~26.5s" it described, and it no longer points at the deleted
  `src/theme.ts`. (The 1.1.0 entry below is left as written — the teaser it shipped really was 26.5s.)
- The RED baseline in `evals/README.md` referenced a file that no longer exists, which made the
  headline claim unfalsifiable. It is now reproduced from git history:
  `git show v1.1.0:skills/goalify/SKILL.md` scores **29/52**, current `SKILL.md` scores **52/52**.

### Removed

- Dead teaser code: `video/src/theme.ts`, and the unused `Chip` and `CtaNeon` components.

### CI

- Runs `tests/test_manifests.py` (which `AGENTS.md` already called a release gate) — now including a
  version-consistency check across `SKILL.md`, `plugin.json`, `marketplace.json` and this file, and an
  assertion over **every tracked text file** (not just Markdown) that nothing passes a file path to
  `/goal` — absolute, `~`, or relative. Lines that *describe* the old handoff opt out with a
  `v1-antipattern` marker, and the number of those exemptions is itself asserted.
- Typechecks `video/` and asserts every relative import in `video/src` is tracked by git — the exact
  failure above, gated so it cannot recur.
- The secrets scanner grew from 2 patterns to 12 (GitHub, Anthropic, OpenAI, Slack, Google, Stripe,
  npm), and the markup safety gate now covers `assets/social-card.html`, not just `assets/*.svg`.

## [1.1.0] - 2026-06-15

A hardened lifecycle, wedge-led positioning, and a designed motion teaser.

### Added

- **Remotion teaser** (`assets/goalify-teaser.mp4` + `goalify-teaser.gif`): a 26.5s,
  1920×1080 / 30fps / H.264 motion teaser with baked-in captions, referenced in the README. Source
  under `video/`.
- A marketplace `description` in `marketplace.json` (clears the `claude plugin validate` warning;
  passes `--strict`).

### Changed

- **Hardened the skill lifecycle** (`SKILL.md`): the procedure now idempotently appends `.goal/` to
  `.gitignore`; the generated-MD template gains a stall guard and a self-destruct path rail; the
  one-vs-several split writes an `INDEX.md` with run order; and the handoff format gains a resume line.
- **Refreshed positioning** to lead with the wedge — lock the few real decisions, wire the finish line
  to commands the run can check, verify every criterion before done — across the README, `SKILL.md`
  `description`, `llms.txt`, `AGENTS.md`, and the GitHub About. Self-destruct is now a supporting
  feature, and the install docs point at Claude Code's built-in `/goal` for executing the file goalify
  writes.
- Repo metadata: set the homepage URL, refreshed the GitHub About, and regenerated the 1280×640 social
  preview.

## [1.0.0] - 2026-05-29

Initial public release. goalify is a Claude Code / Agent Skills skill that prepares a
self-contained, self-deleting `/goal` execution file: in one session it scopes the work,
locks the few real decisions, and writes the file, so you `/clear` and run it in a fresh,
full-context session that executes the whole job and verifies every success criterion
before deleting the file. Evolved from an internal `goal-prep` skill (see
[MIGRATION.md](MIGRATION.md)).

### Added

- The `goalify` skill (`skills/goalify/SKILL.md`): a two-phase PREPARE → EXECUTE model that
  authors the brief you run after `/clear` in a fresh session.
- A WHEN-only, disambiguated `description` (carries the `goalify` trigger, says
  author-not-execute, and disambiguates against `autopilot`/`ultrawork`/`ralph`), a quoted
  `argument-hint`, a documented `/goalify` command with `$ARGUMENTS`, and `metadata.version`.
- A hardened generated-file template: a declarative spec, verified just-in-time context with
  absolute paths, fan-out guardrails (parallel for independent discovery and verification;
  serialize builds, tests, and same-file writes), output-redirection, anti-placeholder and
  search-before-assuming rules, machine-checkable success criteria verified by a separate
  agent, a copyable progress checklist, a maximum-effort directive, and a low-freedom gated
  self-destruct with rationalization counters.
- `evals/`: a deterministic check (`check_skill.py`, run in CI) that encodes the confirmed
  edits as a RED→GREEN regression guard, plus behavioral scenarios validated on Haiku,
  Sonnet, and Opus and a recorded baseline (`RED-baseline.md`).
- A worked example brief (`examples/`), a quickstart, a terminal-themed animated SVG
  hero and "how it works" diagram, GEO files (`llms.txt`, `AGENTS.md`), and a CI workflow
  that validates frontmatter, runs the skill eval, checks relative links, scans for secrets,
  and gates the SVGs against `<script>` and external references.

[2.6.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.6.0
[2.5.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.5.0
[2.4.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.4.0
[2.3.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.3.0
[2.2.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.2.0
[2.1.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.1.0
[2.0.1]: https://github.com/Aboudjem/goalify/releases/tag/v2.0.1
[2.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v2.0.0
[1.1.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.1.0
[1.0.0]: https://github.com/Aboudjem/goalify/releases/tag/v1.0.0
