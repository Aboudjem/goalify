#!/usr/bin/env bash
# Render every cut and write the final deliverables into ../assets.
# Needs Node 22+, FFmpeg, and Chrome (npx hyperframes browser ensure).
set -euo pipefail
cd "$(dirname "$0")/.."
HF="npx --yes hyperframes@0.9.8"
A=../assets
mkdir -p renders

npm run -s music

for cut in main vertical social hook loop; do
  node scripts/build-roots.js "$cut"
  $HF render --quality delivery -o "renders/$cut.mp4"
done

enc() { # in out: H.264 CRF 22 yuv420p, AAC loudness-normalised to -15 LUFS / -1.5 dBTP, faststart
  ffmpeg -v error -y -i "$1" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p \
    -af loudnorm=I=-15:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false -ar 48000 -c:a aac -b:a 160k -movflags +faststart "$2"
}
enc renders/main.mp4 "$A/goalify-promo.mp4"
enc renders/vertical.mp4 "$A/goalify-promo-vertical.mp4"
enc renders/social.mp4 "$A/goalify-promo-30s.mp4"
enc renders/hook.mp4 "$A/goalify-promo-15s.mp4"

# README loop: muted, 1280 wide, plus a GIF (palettegen/paletteuse)
ffmpeg -v error -y -i renders/loop.mp4 -an -vf "scale=1280:-2:flags=lanczos" \
  -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart "$A/goalify-demo.mp4"
ffmpeg -v error -y -i renders/loop.mp4 -vf "fps=9,scale=640:-1:flags=lanczos,palettegen=max_colors=96:stats_mode=diff" renders/pal.png
ffmpeg -v error -y -i renders/loop.mp4 -i renders/pal.png \
  -lavfi "fps=9,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop 0 "$A/goalify-demo.gif"

# poster: the before / after frame (compositions/poster.html)
node scripts/build-roots.js poster
$HF snapshot --at 1.0 -o renders/poster > /dev/null
cp renders/poster/frame-00-at-1s.png "$A/goalify-promo-poster.png"
node scripts/build-roots.js main   # the committed index.html is always the main cut

ls -la "$A"/goalify-promo* "$A"/goalify-demo*
