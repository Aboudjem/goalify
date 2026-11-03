# goalify promo video (HyperFrames)

Source for the goalify 3.0 launch promo. It is a [HyperFrames](https://hyperframes.heygen.com)
project: HTML + CSS + seekable GSAP timelines, rendered frame by frame to MP4. It replaces the old
Remotion teaser.

| Output (in `../assets/`) | What |
| --- | --- |
| `goalify-promo.mp4` | main cut, 1920x1080, 44.4 s, music |
| `goalify-promo-vertical.mp4` | same story re-laid out for 1080x1920 (not a crop) |
| `goalify-promo-15s.mp4` | 15.4 s cut: four simple lines, then the end card |
| `goalify-demo.mp4` / `.gif` | muted 18 s README loop, 4 slow captions (GIF 640 px, 10 fps, calm sky) |
| `goalify-promo-poster.png` | 1920x1080 poster (VERIFIED + the bakery "Here's what I did") |

The story and every caption follow `../.goal/video-script-v2.md` including its Round 3: one
everyday example (a bakery website) runs through the whole film, the end card is one install line
(`npx skills add Aboudjem/goalify` under "Install in one line", then "Free. Also works in Codex."), and the motion is kinetic:
spring-in captions with a glowing key word, a camera push on every scene, match cuts and carries
between scenes (chat drops into the ignition, the flag flies into the checklist, the `/goal` line
zooms into the clock, the clock shatters into VERIFIED, the result card shrinks into the install box),
particle pops, a stamp slam with shake, a day and night time-lapse, and VERIFIED with a shockwave,
star confetti and a punch-in.

## Layout

```
index.html                    root composition (GENERATED: the main cut; do not hand-edit)
compositions/captions.html    the caption track (GENERATED with index.html, per cut)
compositions/sky.html         starfield: depth layers, twinkle, flares, shooting stars, star-trail time-lapse
compositions/ask.html         1-3: "Redo my whole website", the AI keeps asking, a "Done!" that isn't
compositions/turn.html        4: Meet goalify (the mark ignites), "a free skill for your AI agent"
compositions/goal.html        5-6: three requests flip into goals; one goal up close with its finish line
compositions/homework.html    7: doable / research / precise checklist, questions answered now, the stamp
compositions/summary.html     8: the short summary in the chat + the run preview page (optional)
compositions/clear.html       9: /clear, paste one line, "You: away"
compositions/nonstop.html     10: the time-lapse clock, 0 questions, 0 interruptions
compositions/proof.html       11: VERIFIED + "Here's what I did"
compositions/cta.html         12: install lines + github.com/Aboudjem/goalify
assets/film.css, film.js      shared tokens, glass, captions, and seek-safe helpers (cap, push, burst, shake)
assets/camera-shake.js        the registry camera-shake helper, vendored (loaded by every cut)
compositions/components/      registry components installed as reference source (confetti, camera-shake,
                              notification-pileup, spring-pop); not mounted
assets/music-*.mp3            generated music beds
scripts/build-roots.js        the cut table AND the caption script: writes index.html + captions.html
scripts/genmusic.js           seeded procedural music (no deps, royalty-free)
scripts/render-all.sh         renders every cut and writes ../assets
```

One master source: every shot lives once in `compositions/`. A cut is a list of scenes, slot
lengths and captions in `scripts/build-roots.js`. HyperFrames allows one root `index.html` per
project, so the script rewrites `index.html` (and the generated caption track) for the cut you
want, and `render-all.sh` puts the main cut back at the end. Scenes read `window.FILM_CUT` to play
a compressed version in the 15 s cut and the demo loop.

The script also checks every caption before it writes anything (Round 4 rules: very simple
English, at least 0.6 s on screen per word and at least 2.5 s per caption, 3.5 s in the README
loop; a sub line is timed from when it appears; at most 7 words a line; no em dash; nothing past
the end of the cut). It refuses to build a cut that breaks a rule. Each line is fully revealed
within 0.6 s, and the film's last caption holds sharp to the final frame.

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
track holds 13 timed lines in one file (one clip per caption is the point of a caption track).

## Render

```bash
bash scripts/render-all.sh   # music -> all four cuts -> ../assets (about 2 min on an M1 Max)
# or one cut:
node scripts/build-roots.js short && npx hyperframes@0.9.8 render --quality delivery -o renders/short.mp4
node scripts/build-roots.js main
```

Raw renders land in `renders/` (git-ignored). The final files are re-encoded with FFmpeg: H.264
CRF 24, yuv420p, AAC 160k normalised to about -15 LUFS / -1.5 dBTP, `+faststart`.

## Music

```bash
npm run music
```

`scripts/genmusic.js --dur <s> --turn <s> --fail <s> --pulse <s> --peak <s> --out <wav>` writes a
seeded 44.1 kHz WAV that follows the film: a quiet start under the problem, a sub drop when the
"Done!" cracks (`--fail`, or -1 for none), a bell lift when goalify appears (`--turn`), a soft kick
pulse under the time-lapse (`--pulse` to the verdict), a big hit on VERIFIED (`--peak`) and a warm
resolve under the call to action. Every sample is computed in the script, so the bed is free to
use anywhere. `npm run music` writes both beds (main and 15 s) as MP3 in `assets/`.

## Versions used

- hyperframes CLI 0.9.8 (pinned in `package.json`), GSAP 3.15.0 (CDN, as scaffolded by `init`)
- Node 22+, FFmpeg 7+, Chrome via `npx hyperframes browser ensure`
- Fonts: the stack asks for SF Pro (`-apple-system`, `"SF Pro Display"`, `system-ui`); the renderer
  resolves it to its bundled Inter, and monospace to JetBrains Mono, so renders match on any machine.
