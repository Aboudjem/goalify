# goalify promo video (HyperFrames)

Source for the goalify promo. It is a [HyperFrames](https://hyperframes.heygen.com) project:
HTML + CSS + seekable GSAP timelines, rendered frame by frame to MP4.

| Output (in `../assets/`) | What |
| --- | --- |
| `goalify-promo.mp4` | main cut, 1920x1080, 58 s, music |
| `goalify-promo-vertical.mp4` | same story re-laid out for 1080x1920 (not a crop) |
| `goalify-promo-30s.mp4` | 30 s cut for social feeds |
| `goalify-promo-15s.mp4` | 15.5 s hook cut |
| `goalify-demo.mp4` / `.gif` | muted 18 s README loop (GIF 640 px, 9 fps) |
| `goalify-promo-poster.png` | 1920x1080 poster, before and after (`compositions/poster.html`) |

The story is one everyday example, a bakery website, told as two nights. In the bad night the AI
stops at 11:12 PM to ask a question and nothing is built by 7:00 AM. goalify then asks every question
up front, the AI works alone through the good night, and every finish line is checked by 7:00 AM.
The style is minimal: white captions with one soft violet accent, and no neon glow.

## Layout

```
index.html                    root composition (GENERATED: the main cut; do not hand-edit)
compositions/captions.html    the caption track (GENERATED with index.html, per cut)
compositions/sky.html         the starfield behind every scene
compositions/night.html       1-4: the bad night, from the request to 7:00 AM with nothing done
compositions/turn.html        5: Meet goalify
compositions/goal.html        6-7: the request becomes a goal with a finish line
compositions/research.html    8: it looks online for the best way
compositions/homework.html    9-10: can the plan work, then every question answered now
compositions/clear.html       11: install, /clear, the /goal line
compositions/goodnight.html   12: the good night, the AI works alone
compositions/proof.html       13: every finish line ticks, VERIFIED
compositions/done.html        14: 7:00 AM, everything is done
compositions/cta.html         15: tagline and install line
compositions/poster.html      the poster frame, not in the film
compositions/{ask,nonstop,summary,wake}.html   earlier scenes, not mounted in any cut
assets/film.css, film.js      shared tokens, captions, and seek-safe helpers
assets/toon.css, toon.js      the bedroom and the character
assets/camera-shake.js        the registry camera-shake helper, vendored (loaded by every cut)
compositions/components/      registry components installed as reference source; not mounted
assets/music-*.mp3            generated music beds
scripts/build-roots.js        the cut table AND the caption script: writes index.html + captions.html
scripts/genmusic.js           seeded procedural music (no deps, royalty-free)
scripts/render-all.sh         renders every published cut and writes ../assets
scripts/contact-sheet.py      one labelled frame per caption, to review a cut at a glance
scripts/qa.py                 checks a render: contrast, loop seams, sound effect levels
```

One master source: every shot lives once in `compositions/`. A cut is a list of scenes, slot
lengths and captions in `scripts/build-roots.js`. HyperFrames allows one root `index.html` per
project, so the script rewrites `index.html` (and the generated caption track) for the cut you
want, and `render-all.sh` puts the main cut back at the end. Scenes read `window.FILM_CUT` to play
a compressed version in the shorter cuts and the demo loop. The cuts `hook-b` and `hook-c` are two
alternative 15 s openings; they build but are not published.

The script also checks every caption before it writes anything: simple English, one idea per
caption, at most 2 lines, at most 15 characters per second, at least 2.5 s on screen (3.5 s in the
README loop), and no em dash. It refuses to build a cut that breaks a rule.

The vertical cut is a real relayout: each scene carries `@media (max-aspect-ratio: 1/1)` rules and
checks `Film.portrait()` in its timeline. Captions are fitted to the frame width at build time
(64 px in 16:9, 76 px in 9:16, never under 48 px) and sit inside the 168 to 1330 px safe band.

## Preview and edit

```bash
cd video
npx hyperframes@0.9.8 preview --background   # Studio at the printed URL; preview --stop when done
node scripts/build-roots.js vertical          # switch the preview to another cut, then refresh
node scripts/build-roots.js main              # back to the main cut (commit this one)
```

## Check

```bash
npx hyperframes@0.9.8 lint            # static, fast
npx hyperframes@0.9.8 check --json    # lint + runtime + layout + motion + contrast in Chrome
npx hyperframes@0.9.8 snapshot --at 1,4.3,30.4   # PNGs under .hyperframes/artifacts/snapshots
```

`check` passes with 0 errors. It keeps a few craft warnings on purpose: the preview page is shown
at its real UI sizes (texture, the caption carries the meaning), and lint notes that the caption
track holds 15 timed lines in one file (one clip per caption is the point of a caption track).

## Render

```bash
bash scripts/render-all.sh   # music -> every cut -> ../assets (about 3 min on an M1 Max)
# or one cut:
node scripts/build-roots.js hook && npx hyperframes@0.9.8 render --quality delivery -o renders/hook.mp4
node scripts/build-roots.js main
```

Raw renders land in `renders/` (git-ignored). The final files are re-encoded with FFmpeg: H.264
CRF 24, yuv420p, AAC 160k normalised to about -15 LUFS / -1.5 dBTP, `+faststart`.

## Music

```bash
npm run music
```

`scripts/genmusic.js` writes a seeded 44.1 kHz WAV that follows the film, with its timings from
`build-roots.js <cut> --music-args`. Every sample is computed in the script, so the bed is free to
use anywhere. `npm run music` writes one MP3 per cut in `assets/`.

## Versions used

- hyperframes CLI 0.9.8 (pinned in `package.json`), GSAP 3.15.0 (CDN, as scaffolded by `init`)
- Node 22+, FFmpeg 7+, Chrome via `npx hyperframes browser ensure`
- Fonts: the stack asks for SF Pro (`-apple-system`, `"SF Pro Display"`, `system-ui`); the renderer
  resolves it to its bundled Inter, and monospace to JetBrains Mono, so renders match on any machine.
