#!/usr/bin/env bash
# Render every cut and write the final deliverables into ../assets.
# Needs Node 22+, FFmpeg, and Chrome (npx hyperframes browser ensure).
set -euo pipefail
cd "$(dirname "$0")/.."
HF="npx --yes hyperframes@0.9.8"
A=../assets
mkdir -p renders

npm run -s music

for cut in main vertical short demo; do
  node scripts/build-roots.js "$cut"
  $HF render --quality delivery -o "renders/$cut.mp4"
done
node scripts/build-roots.js main   # the committed index.html is always the main cut

enc() { # in out: H.264 CRF 22 yuv420p, AAC loudness-normalised to -15 LUFS / -1.5 dBTP, faststart
  ffmpeg -v error -y -i "$1" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p \
    -af loudnorm=I=-15:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false -ar 48000 -c:a aac -b:a 160k -movflags +faststart "$2"
}
enc renders/main.mp4 "$A/goalify-promo.mp4"
enc renders/vertical.mp4 "$A/goalify-promo-vertical.mp4"
enc renders/short.mp4 "$A/goalify-promo-15s.mp4"

# README loop: muted, 1280 wide, plus a GIF (palettegen/paletteuse)
ffmpeg -v error -y -i renders/demo.mp4 -an -vf "scale=1280:-2:flags=lanczos" \
  -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart "$A/goalify-demo.mp4"
ffmpeg -v error -y -i renders/demo.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,palettegen=max_colors=96:stats_mode=diff" renders/pal.png
ffmpeg -v error -y -i renders/demo.mp4 -i renders/pal.png \
  -lavfi "fps=10,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop 0 "$A/goalify-demo.gif"

# poster: the VERIFIED moment
ffmpeg -v error -y -ss 37.6 -i renders/main.mp4 -frames:v 1 "$A/goalify-promo-poster.png"
ls -la "$A"/goalify-promo* "$A"/goalify-demo*
