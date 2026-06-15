# goalify teaser — Remotion source

The source for the goalify Twitter/X teaser. The rendered outputs live in the repo's `assets/`
(`goalify-teaser.mp4` and `goalify-teaser.gif`); this folder is how they're produced. `node_modules/`
and render output are gitignored.

A 9-beat, ~26.5s storyboard (1920×1080, 30fps, H.264) with baked-in captions and the goalify brand
tokens (see `src/theme.ts`). The composition is `src/GoalifyTeaser.tsx`.

## Commands

```bash
npm install                 # install Remotion (free for individuals)
npm run dev                 # open Remotion Studio to preview
# render the MP4 into the repo's assets/ folder:
npx remotion render src/index.ts GoalifyTeaser ../assets/goalify-teaser.mp4 --codec=h264 --crf=18
```

The GIF is derived from the MP4 with ffmpeg `palettegen`/`paletteuse` (13fps, 900px wide).

Remotion is [free for individuals and small teams](https://www.remotion.dev/docs/license); larger
for-profit companies need a company license.
