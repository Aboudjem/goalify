# goalify promo video (HyperFrames)

Source for the goalify 3.0 launch promo. It is a [HyperFrames](https://hyperframes.heygen.com)
project: HTML + CSS + seekable GSAP timelines, rendered frame by frame to MP4. It replaces the old
Remotion teaser.

| Output (in `../assets/`)     | What                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `goalify-promo.mp4`          | main cut, 1920x1080, 38.5 s, music                           |
| `goalify-promo-vertical.mp4` | same story re-laid out for 1080x1920 (not a crop)            |
| `goalify-promo-15s.mp4`      | 15.4 s cut: hook, problem, turn, proof, call to action       |
| `goalify-demo.mp4` / `.gif`  | muted 13.1 s README loop (condition, preview page, verified) |
| `goalify-promo-poster.png`   | 1920x1080 poster (the VERIFIED moment)                       |

## Layout

```
index.html              root composition (GENERATED: the main cut; do not hand-edit)
compositions/sky.html   starfield: depth layers, twinkle, flares, shooting stars, star-trail time-lapse
compositions/open.html  beats 1+2: "Claude said done." / "It wasn't."
compositions/turn.html  beat 3: the goalify mark ignites
compositions/brief.html beat 4: /goalify, research, every question up front, the brief assembles
compositions/condition.html  beat 5: /clear, then the one /goal line
compositions/preview.html    beat 6: the 3.0 run preview page (rebuilt from examples/sample-brief.html)
compositions/nonstop.html    beat 7: the run works for hours/days, checks tick
compositions/proof.html      beat 8: /goalify verify receipt, VERIFIED
compositions/cta.html        beat 9: install lines + github.com/Aboudjem/goalify
assets/film.css, film.js     shared tokens (palette, glass, captions) and tiny seek-safe helpers
assets/music-*.mp3           generated music beds
scripts/build-roots.js       the cut table: writes index.html for main | vertical | short | demo
scripts/genmusic.js          seeded procedural music (no deps, royalty-free)
scripts/render-all.sh        renders every cut and writes ../assets
```

One master source: every shot lives once in `compositions/`. A cut is only a list of scenes and
slot lengths in `scripts/build-roots.js`. HyperFrames allows one root `index.html` per project
(`lint` fails `multiple_root_compositions` otherwise), so the script rewrites `index.html` for the
cut you want and `render-all.sh` puts the main cut back at the end. The vertical cut is a real
relayout: each scene carries `@media (max-aspect-ratio: 1/1)` rules and checks
`Film.portrait()` in its timeline, so panels stack, type grows and captions move up into the
safe band (words between 168 and 1330 px).

Captions are burned in, one per beat, inside each scene (so every cut gets them for free).

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

`check` passes with 0 errors on all four cuts. It keeps a few craft warnings on purpose: the
preview page is shown at its real UI sizes (small text inside a product screenshot), and typed
command lines are not meant to be read word by word.

## Render

```bash
bash scripts/render-all.sh   # music -> all four cuts -> ../assets (about 2 min on an M1 Max)
# or one cut:
node scripts/build-roots.js short && npx hyperframes@0.9.8 render --quality delivery -o renders/short.mp4
node scripts/build-roots.js main
```

Raw renders land in `renders/` (git-ignored). The final files are re-encoded with FFmpeg: H.264
CRF 22, yuv420p, AAC 160k normalised to about -15 LUFS / -1.5 dBTP, `+faststart`.

## Music

```bash
npm run music
```

`scripts/genmusic.js --dur <s> --turn <s> --peak <s> --out <wav>` writes a seeded 44.1 kHz WAV:
a tense B-minor bed under the cold open, a sub drop when the test fails, a bell arpeggio when the
mark ignites (`--turn`), a D-A-Bm-G build with a soft kick, and a bright hit on VERIFIED
(`--peak`). Every sample is computed in the script, so the bed is free to use anywhere.
The `npm run music` script then converts both WAVs to MP3 in `assets/`.

## Versions used

- hyperframes CLI 0.9.8 (pinned in `package.json`), GSAP 3.15.0 (CDN, as scaffolded by `init`)
- Node 22+, FFmpeg 7+, Chrome via `npx hyperframes browser ensure`
- Fonts: the stack asks for SF Pro (`-apple-system`, `"SF Pro Display"`, `system-ui`); the renderer
  resolves it to its bundled Inter, and monospace to JetBrains Mono, so renders match on any machine.
