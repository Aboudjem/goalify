#!/usr/bin/env python3
"""Round 6 QA on rendered files: squint test, caption/key-text contrast, loop seams, SFX levels.

  python3 scripts/qa.py <render dir>      (e.g. renders/v6)

Writes into <render dir>/qa/: squint-main.png, contrast.json, seam-main.png, seam-loop.png,
sfx.json, and prints a summary. Needs ffmpeg and Pillow.
"""
import json
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def beats(cut):
    return json.loads(subprocess.check_output(["node", os.path.join(HERE, "build-roots.js"), cut, "--beats"], cwd=ROOT))


def frame(video, t, out):
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % t, "-i", video, "-frames:v", "1", out])
    return Image.open(out).convert("RGB")


def lum(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def box_contrast(img, box):
    """bg = 20th percentile luminance in the box, text = the bright text pixels (97th percentile),
    dim = the dimmest real text pixel (10th percentile of pixels clearly above the background)."""
    crop = img.crop(box)
    px = [lum(p) for p in crop.getdata()]
    px.sort()
    n = len(px)
    bg = px[int(n * 0.2)]
    txt = px[int(n * 0.97)]
    # text pixels: well above the background (the core of the glyphs, not the antialiased edge)
    thr = bg + (txt - bg) * 0.6
    tp = [v for v in px if v >= thr]
    dim = tp[int(len(tp) * 0.1)] if tp else txt
    return round(ratio(txt, bg), 2), round(ratio(dim, bg), 2), round(bg, 4)


# key text per beat in the 16:9 master (x0, y0, x1, y1), from the scene layouts
KEY = {
    1: ("laptop: the request bubble", (1340, 255, 1825, 565)),
    2: ("laptop: request + On it!", (1340, 255, 1825, 565)),
    3: ("the questions with their times", (230, 250, 1300, 700)),
    4: ("laptop: 0 of 6 pages built / 4 questions waiting", (1340, 255, 1825, 565)),
    5: ("goalify wordmark", (890, 320, 1620, 540)),
    6: ("goal card: Bakery website live", (560, 330, 1360, 560)),
    7: ("goal title + finish line rows", (470, 120, 1450, 700)),
    8: ("search bar + card titles", (420, 100, 1500, 190)),
    9: ("Can the plan work?", (420, 150, 1500, 260)),
    10: ("question card", (470, 180, 1450, 560)),
    11: ("terminal lines", (220, 180, 1540, 620)),
    12: ("laptop: n of 6 pages built / Questions asked: 0", (1340, 255, 1825, 565)),
    13: ("VERIFIED badge", (700, 96, 1220, 260)),
    14: ("laptop: Little Oven Bakery / 6 of 6 pages built", (1340, 255, 1825, 565)),
    15: ("install line", (420, 520, 1500, 660)),
}


def caption_box(cut, beat, w, h):
    if beat == 15:  # the tagline sits high on the end card
        return (100, 262, w - 100, 380) if w > h else (40, 540, w - 40, 760)
    return (100, 925, w - 100, 1040) if w > h else (30, 1100, w - 30, 1340)


def contact_frames(video, cut, tmp):
    caps = beats(cut)["captions"]
    out = []
    for i, c in enumerate(caps):
        t = round(c["start"] + 0.7 * (c["end"] - c["start"]), 2)
        out.append((c, t, frame(video, t, os.path.join(tmp, "%s-%02d.png" % (cut, i)))))
    return out


def font(sz, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial%s.ttf" % (" Bold" if bold else ""), sz)
    except OSError:
        return ImageFont.load_default()


def squint(frames, out):
    """320 px wide, gaussian blur: what still stands out is what the eye lands on first. Also
    reports where the strongest bright-on-dark blob sits (thirds of the frame)."""
    tiles = []
    notes = []
    for c, t, img in frames:
        sm = img.resize((320, round(320 * img.height / img.width)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
        g = sm.convert("L")
        W, H = g.size
        # saliency: brightness relative to the frame's median, summed over a 3x3 grid
        px = list(g.getdata())
        med = sorted(px)[len(px) // 2]
        cells = {}
        for y in range(H):
            for x in range(W):
                v = max(0, px[y * W + x] - med)
                k = (min(2, x * 3 // W), min(2, y * 3 // H))
                cells[k] = cells.get(k, 0) + v * v
        best = max(cells, key=cells.get)
        where = ["top", "middle", "bottom"][best[1]] + "-" + ["left", "centre", "right"][best[0]]
        notes.append({"beat": c["beat"], "t": t, "strongest_cell": where})
        tiles.append((c, t, sm))
    cols = 4
    th = tiles[0][2].height
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 330 + 10, rows * (th + 30) + 10), (16, 14, 28))
    d = ImageDraw.Draw(sheet)
    for i, (c, t, sm) in enumerate(tiles):
        x, y = 10 + (i % cols) * 330, 10 + (i // cols) * (th + 30)
        sheet.paste(sm, (x, y))
        d.text((x, y + th + 4), "beat %d @ %.2fs" % (c["beat"], t), fill=(255, 210, 63), font=font(16, True))
    sheet.save(out)
    return notes


def seam(video, out, dur):
    tmp = tempfile.mkdtemp()
    a = frame(video, 0, os.path.join(tmp, "first.png"))
    b = frame(video, dur - 1 / 30 - 0.001, os.path.join(tmp, "last.png"))
    diff = sum(abs(p - q) for pa, pb in zip(a.getdata(), b.getdata()) for p, q in zip(pa, pb)) / (a.width * a.height * 3)
    w = 960
    h = round(w * a.height / a.width)
    sheet = Image.new("RGB", (2 * w + 30, h + 50), (16, 14, 28))
    sheet.paste(b.resize((w, h), Image.LANCZOS), (10, 40))
    sheet.paste(a.resize((w, h), Image.LANCZOS), (w + 20, 40))
    d = ImageDraw.Draw(sheet)
    d.text((10, 10), "LAST frame (%.3f s)" % (dur - 1 / 30), fill=(255, 210, 63), font=font(20, True))
    d.text((w + 20, 10), "FIRST frame (0 s)   mean abs diff %.1f / 255" % diff, fill=(255, 210, 63), font=font(20, True))
    sheet.save(out)
    return round(diff, 2)


def wav_mono(path):
    import wave
    import array

    w = wave.open(path)
    sr, n = w.getframerate(), w.getnframes()
    a = array.array("h", w.readframes(n))
    return sr, [max(abs(a[2 * i]), abs(a[2 * i + 1])) / 32768 for i in range(n)]


def db(x):
    return 20 * math.log10(max(x, 1e-9))


def lufs(path, t0, dur):
    r = subprocess.run(
        ["ffmpeg", "-nostats", "-ss", "%.3f" % t0, "-t", "%.3f" % dur, "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    lines = [l for l in r.stderr.splitlines() if l.strip().startswith("I:")]
    try:
        return float(lines[-1].split()[1])
    except (IndexError, ValueError):
        return None


FX_LEN = {"alarm": 1.6, "whoosh": 0.42, "ping": 0.4, "slap": 0.2, "pop": 0.1, "tick": 0.06, "click": 0.03, "stamp": 0.4, "snore": 3.2, "hit": 0.9, "chime": 0.8}


def sfx(cut, tmp):
    """Stems at the full mix's gain: music only, effects only. Per event: the effect's peak and
    loudness (its own window, at least 0.4 s), against the music stem's overall peak."""
    args = subprocess.check_output(["node", os.path.join(HERE, "build-roots.js"), cut, "--music-args"], cwd=ROOT).decode().split()
    full = os.path.join(tmp, "full.wav")
    out = subprocess.check_output(["node", os.path.join(HERE, "genmusic.js")] + args + ["--out", full], cwd=ROOT).decode()
    gain = out.split("gain ")[1].split(")")[0]
    mus = os.path.join(tmp, "music.wav")
    fxw = os.path.join(tmp, "fx.wav")
    subprocess.check_call(["node", os.path.join(HERE, "genmusic.js")] + args + ["--norm", gain, "--nofx", "--out", mus], cwd=ROOT, stdout=subprocess.DEVNULL)
    subprocess.check_call(["node", os.path.join(HERE, "genmusic.js")] + args + ["--norm", gain, "--nomusic", "--out", fxw], cwd=ROOT, stdout=subprocess.DEVNULL)
    sr, m = wav_mono(mus)
    _, f = wav_mono(fxw)
    mpk = db(max(m))
    evs = args[args.index("--fx") + 1].split(",")
    rows = []
    for e in evs:
        name, at = e.split("@")
        at = float(at)
        ln = FX_LEN.get(name, 0.4)
        i0, i1 = int(at * sr), int((at + ln) * sr)
        pk = db(max(f[i0:i1] or [0]))
        local = db(max(m[max(0, i0 - sr // 2) : i1] or [0]))
        win = max(0.4, ln)
        rows.append(
            {
                "fx": name,
                "t": at,
                "peak_dBFS": round(pk, 1),
                "lufs": lufs(fxw, at, win),
                "under_music_peak_dB": round(mpk - pk, 1),
                "music_local_peak_dBFS": round(local, 1),
            }
        )
    return {"cut": cut, "music_peak_dBFS": round(mpk, 1), "music_lufs": lufs(mus, 0, 600), "fx_lufs": lufs(fxw, 0, 600), "events": rows}


def main():
    d = sys.argv[1]
    q = os.path.join(d, "qa")
    os.makedirs(q, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="qa-")
    report = {}
    fm = contact_frames(os.path.join(d, "main-58s.mp4"), "main", tmp)
    fv = contact_frames(os.path.join(d, "main-vertical.mp4"), "vertical", tmp)
    report["squint"] = squint(fm, os.path.join(q, "squint-main.png"))
    squint(fv, os.path.join(q, "squint-vertical.png"))
    con = []
    for cut, frames in (("main", fm), ("vertical", fv)):
        for c, t, img in frames:
            cap = box_contrast(img, caption_box(cut, c["beat"], img.width, img.height))
            row = {"cut": cut, "beat": c["beat"], "t": t, "caption_text_vs_bg": cap[0], "caption_dimmest_text_vs_bg": cap[1]}
            if cut == "main" and c["beat"] in KEY:
                k = box_contrast(img, KEY[c["beat"]][1])
                row.update({"key": KEY[c["beat"]][0], "key_text_vs_bg": k[0], "key_dimmest_vs_bg": k[1]})
            con.append(row)
    report["contrast"] = con
    report["seam_main_diff"] = seam(os.path.join(d, "main-58s.mp4"), os.path.join(q, "seam-main.png"), 58.0)
    report["seam_loop_diff"] = seam(os.path.join(d, "readme-loop.mp4"), os.path.join(q, "seam-loop.png"), 18.0)
    report["sfx"] = [sfx(c, tmp) for c in ("main", "social", "hook", "hook-b", "hook-c")]
    json.dump(report, open(os.path.join(q, "qa.json"), "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
