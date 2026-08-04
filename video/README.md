# goalify teaser — Remotion source

The source for the goalify Twitter/X teaser. The rendered outputs live in the repo's `assets/`
(`goalify-teaser.mp4` and `goalify-teaser.gif`); this folder is how they're produced. `node_modules/`
and render output are gitignored.

An 8-beat, 29.7s storyboard (890 frames at 30fps, 1920×1080, H.264) with baked-in captions and the
goalify brand tokens — the palette `P`, the type stack, and the shared motion primitives all live in
`src/neon.tsx`. The composition is `src/ConceptHero.tsx`, re-exported as `GoalifyTeaser` from
`src/GoalifyTeaser.tsx`; `src/Root.tsx` imports its `TEASER_FRAMES`, so the composition length can
never drift from the storyboard.

## Commands

```bash
npm install                 # install Remotion (free for individuals)
npm run dev                 # open Remotion Studio to preview
npx tsc --noEmit            # typecheck (also runs in CI)
# render the MP4 into the repo's assets/ folder:
npx remotion render src/index.ts GoalifyTeaser ../assets/goalify-teaser.mp4 --codec=h264 --crf=18
```

The GIF is derived from the MP4 with ffmpeg `palettegen`/`paletteuse` (13fps, 900px wide).

Remotion is [free for individuals and small teams](https://www.remotion.dev/docs/license); larger
for-profit companies need a company license.
