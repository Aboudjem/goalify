# goalify teaser — Remotion source

The source for the goalify Twitter/X teaser. The rendered outputs live in the repo's `assets/`
(`goalify-teaser.mp4` and `goalify-teaser.gif`); this folder is how they're produced. `node_modules/`
and render output are gitignored.

An 8-beat, 27.9s storyboard (836 frames at 30fps, 1920×1080, H.264) with baked-in captions on the
goalify "Sunday Worktable" paper system. The composition is `src/GoalifyTeaser.tsx` and it is
self-contained — the palette `W`, the type stacks, the motion helpers and every beat live in that
one file. `src/Root.tsx` imports its `TEASER_FRAMES`, so the composition length can never drift
from the storyboard.

## Commands

```bash
npm install                 # install Remotion (free for individuals)
npm run dev                 # open Remotion Studio to preview
npx tsc --noEmit            # typecheck (also runs in CI)
# render the MP4 into the repo's assets/ folder:
npx remotion render src/index.ts GoalifyTeaser ../assets/goalify-teaser.mp4 --codec=h264 --crf=18
# regenerate the music bed (seeded, reproducible; writes /tmp/music.wav, then encode it):
node scripts/genmusic.js && ffmpeg -y -i /tmp/music.wav -c:a libmp3lame -b:a 192k public/music.mp3
```

The GIF is derived from the MP4 with ffmpeg `palettegen`/`paletteuse` (13fps, 900px wide).

Remotion is [free for individuals and small teams](https://www.remotion.dev/docs/license); larger
for-profit companies need a company license.
