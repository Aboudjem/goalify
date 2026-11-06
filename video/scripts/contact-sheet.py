#!/usr/bin/env python3
"""Contact sheet: one frame per caption beat, labelled with the beat and its time.

  python3 scripts/contact-sheet.py <cut> <out.png> [--video renders/x.mp4]

Without --video it snapshots the current index.html with `hyperframes snapshot` (so build the
cut first: node scripts/build-roots.js <cut>). With --video it pulls the frames from a render.
Each beat is sampled at 70% of its caption window (after the reveal, before the fade).
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    cut, out = sys.argv[1], sys.argv[2]
    video = sys.argv[sys.argv.index("--video") + 1] if "--video" in sys.argv else None
    beats = json.loads(subprocess.check_output(["node", os.path.join(HERE, "build-roots.js"), cut, "--beats"], cwd=ROOT))
    caps = beats["captions"]
    times = [round(c["start"] + 0.7 * (c["end"] - c["start"]), 2) for c in caps]
    tmp = tempfile.mkdtemp(prefix="sheet-")
    frames = []
    if video:
        for i, t in enumerate(times):
            p = os.path.join(tmp, "f%02d.png" % i)
            subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", p])
            frames.append(p)
    else:
        subprocess.check_call(
            ["npx", "--yes", "hyperframes@0.9.8", "snapshot", "--at", ",".join(str(t) for t in times), "-o", tmp],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
        pngs = sorted(f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png"))
        frames = [os.path.join(tmp, f) for f in pngs][: len(times)]
    first = Image.open(frames[0])
    W, H = first.size
    portrait = H > W
    cols = 5 if portrait else 4
    tw = 300 if portrait else 480
    th = round(tw * H / W)
    lab = 64
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + lab) + (rows + 1) * 12), (16, 14, 28))
    d = ImageDraw.Draw(sheet)
    try:
        f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        f2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    for i, (p, c, t) in enumerate(zip(frames, caps, times)):
        x = 12 + (i % cols) * (tw + 12)
        y = 12 + (i // cols) * (th + lab + 12)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 6), "beat %d  @ %.2fs  (%.2f-%.2f)" % (c["beat"], t, c["start"], c["end"]), fill=(255, 210, 63), font=f1)
        txt = c["text"]
        if len(txt) > (34 if portrait else 56):
            txt = txt[: (32 if portrait else 54)] + "..."
        d.text((x, y + th + 32), txt, fill=(241, 237, 255), font=f2)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out)
    print(out, "%d frames" % len(frames))


if __name__ == "__main__":
    main()
