// Procedural music bed for the goalify promo. No deps, seeded, reproducible, royalty-free
// (every sample is computed here). Writes a 16-bit stereo 44.1 kHz WAV.
//
//   node scripts/genmusic.js --dur 37.7 --turn 4.6 --fail 1.47 --peak 29.3 --out renders/music-main.wav
//   node scripts/genmusic.js --dur 15 --turn 4.6 --fail 1.47 --peak 8.8 --out renders/music-short.wav
//
// The arc follows the film:
//   0 .. turn    "Claude said done. It wasn't."  a held B-minor pad, one bell on "Done.",
//                a low sub drop when the test fails (--fail, ~1.47 s)
//   turn         the goalify mark ignites: a bell arpeggio + sub hit on the pin strike (turn+0.66)
//   turn .. peak D A Bm G in D major, soft kick from turn+2 s, intensity builds
//   peak         VERIFIED: a bright chord, bell cascade and sub hit, then the bed settles
//   peak .. end  plagal G -> D under the call to action, fade out
const fs = require("fs");
const path = require("path");

function arg(name, def) {
  const i = process.argv.indexOf("--" + name);
  return i > 0 ? process.argv[i + 1] : def;
}
const DUR = parseFloat(arg("dur", "37.7"));
const TURN = parseFloat(arg("turn", "4.6"));
const PEAK = parseFloat(arg("peak", "29.3"));
const OUT = arg("out", "assets/music-main.wav");
const FAIL = parseFloat(arg("fail", "1.47"));

const SR = 44100;
const N = Math.floor(SR * DUR);
const BPM = 80;
const SPB = 60 / BPM;
const BAR = SPB * 4; // 3.0 s

const dryL = new Float32Array(N),
  dryR = new Float32Array(N);
const wetL = new Float32Array(N),
  wetR = new Float32Array(N);

const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, t) => {
  const x = clamp01((t - a) / (b - a));
  return x * x * (3 - 2 * x);
};

const CH = {
  D: { root: 38, notes: [50, 54, 57, 62] },
  A: { root: 33, notes: [49, 52, 57, 61] },
  Bm: { root: 35, notes: [50, 54, 59, 62] },
  G: { root: 31, notes: [50, 55, 59, 62] },
};
const PROG = ["D", "A", "Bm", "G"];

// 0..1 energy across the film
function intensity(t) {
  if (t < TURN) return 0.32;
  let v = 0.5 + 0.5 * smooth(TURN, PEAK, t);
  if (t > PEAK + 1.5) v = 1.0 - 0.35 * smooth(PEAK + 1.5, DUR, t);
  return clamp01(v);
}

function saw(ph) {
  return 2 * (ph - Math.floor(ph + 0.5));
}

function pad(t0, dur, midis, amp, cutoff) {
  const i0 = Math.max(0, Math.floor(t0 * SR)),
    i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  const det = [0.0, 0.0018, -0.0016];
  for (const m of midis) {
    const fr = mtof(m);
    let lp = 0;
    const a = cutoff || 0.15;
    for (let i = i0; i < i1; i++) {
      const tt = (i - i0) / SR;
      const env = Math.min(1, tt / 0.34) * Math.min(1, (dur - tt) / 0.5);
      let s = 0;
      for (const d of det) s += saw((fr * (1 + d) * (i / SR)) % 1);
      s /= det.length;
      lp += a * (s - lp);
      const lfo = 1 + 0.05 * Math.sin(2 * Math.PI * 0.11 * (i / SR));
      const v = lp * env * amp * lfo;
      const pan = 0.5 + 0.18 * Math.sin(m);
      dryL[i] += v * (1 - pan) * 1.1;
      dryR[i] += v * pan * 1.1;
      wetL[i] += v * (1 - pan) * 0.55;
      wetR[i] += v * pan * 0.55;
    }
  }
}

function bass(t0, dur, midi, amp) {
  const fr = mtof(midi);
  const i0 = Math.max(0, Math.floor(t0 * SR)),
    i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.min(1, tt / 0.025) * Math.exp(-tt / (dur * 0.7));
    // second + third harmonics so it still reads on a phone speaker
    const s =
      (Math.sin(2 * Math.PI * fr * tt) +
        0.3 * Math.sin(4 * Math.PI * fr * tt) +
        0.12 * Math.sin(6 * Math.PI * fr * tt)) *
      env *
      amp;
    dryL[i] += s;
    dryR[i] += s;
  }
}

// sub "drop": a falling sine thud (the failed test, the pin strike, the verdict)
function drop(t0, f0, f1, amp, len) {
  const i0 = Math.max(0, Math.floor(t0 * SR)),
    i1 = Math.min(N, Math.floor((t0 + len) * SR));
  let ph = 0;
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const fr = f1 + (f0 - f1) * Math.exp(-tt / 0.08);
    ph += (2 * Math.PI * fr) / SR;
    const env = Math.min(1, tt / 0.004) * Math.exp(-tt / (len * 0.35));
    const s = (Math.sin(ph) + 0.25 * Math.sin(2 * ph)) * env * amp;
    dryL[i] += s;
    dryR[i] += s;
    wetL[i] += s * 0.2;
    wetR[i] += s * 0.2;
  }
}

function bell(t0, midi, amp, pan) {
  const fr = mtof(midi),
    dur = 1.8;
  const i0 = Math.max(0, Math.floor(t0 * SR)),
    i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.exp(-tt / 0.6) * (1 - Math.exp(-tt / 0.004));
    const mod =
      Math.exp(-tt / 0.2) * 2.0 * Math.sin(2 * Math.PI * fr * 2.0 * tt);
    const s = Math.sin(2 * Math.PI * fr * tt + mod) * env * amp;
    dryL[i] += s * (1 - pan);
    dryR[i] += s * pan;
    wetL[i] += s * (1 - pan) * 0.75;
    wetR[i] += s * pan * 0.75;
  }
}

function kick(t0, amp) {
  const dur = 0.17,
    i0 = Math.floor(t0 * SR),
    i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const fr = 105 * Math.exp(-tt / 0.04) + 44;
    const env = Math.exp(-tt / 0.12);
    const s = Math.sin(2 * Math.PI * fr * tt) * env * amp;
    dryL[i] += s;
    dryR[i] += s;
  }
}

// soft shaker on the off-beats while the run works (adds forward motion, no harsh hats)
let _s = 0x2f6e2b1 >>> 0;
const rnd = () => {
  _s ^= _s << 13;
  _s ^= _s >>> 17;
  _s ^= _s << 5;
  _s >>>= 0;
  return _s / 4294967296;
};
function shaker(t0, amp) {
  const dur = 0.07,
    i0 = Math.floor(t0 * SR),
    i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  let hp = 0,
    prev = 0;
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const n = rnd() * 2 - 1;
    hp = 0.85 * (hp + n - prev);
    prev = n;
    const s = hp * Math.exp(-tt / 0.018) * amp;
    dryL[i] += s * 0.7;
    dryR[i] += s;
  }
}

// ---- 1. the cold open: Bm pad, a bell on "Done.", a drop on the failing test ----
pad(0, TURN + 0.3, [47, 50, 54], 0.075, 0.08);
bass(0, TURN, 35, 0.12);
bell(0.1, 78, 0.07, 0.55); // "Claude said done." lands
drop(FAIL, 120, 42, 0.42, 0.9); // "It wasn't."
pad(FAIL, TURN - FAIL + 0.3, [46], 0.03, 0.06); // a tense flat-6 colour under the reveal

// ---- 2. the turn: ignition arpeggio + strike ----
const arp = [62, 66, 69, 74, 78];
arp.forEach((m, k) => bell(TURN + 0.05 + k * 0.09, m, 0.075, 0.3 + k * 0.1));
drop(TURN + 0.66, 160, 50, 0.38, 0.8);

// ---- 3. the build, bar by bar from the turn ----
for (let bar = 0; ; bar++) {
  const t0 = TURN + bar * BAR;
  if (t0 >= DUR) break;
  let ch = CH[PROG[bar % 4]];
  // after the verdict: G -> D plagal settle
  if (t0 >= PEAK - 0.01)
    ch = CH[Math.floor((t0 - PEAK) / BAR) % 2 === 0 ? "D" : "G"];
  const it = intensity(t0 + BAR / 2);
  const len = Math.min(BAR + 0.18, DUR - t0);

  pad(t0, len, ch.notes.slice(0, 3), 0.085 * (0.6 + 0.4 * it));
  if (it > 0.8) pad(t0, len, [ch.notes[3] + 12], 0.035 * it);

  bass(t0, SPB * 2.2, ch.root, 0.26 * (0.7 + 0.3 * it));
  if (it > 0.6) bass(t0 + SPB * 2, SPB * 2.1, ch.root + 7, 0.15 * it);

  bell(t0, ch.notes[2] + 12, 0.1 * (0.6 + 0.4 * it), 0.4);
  bell(t0 + SPB * 2, ch.notes[1] + 12, 0.08 * (0.6 + 0.4 * it), 0.6);
  if (it > 0.7) bell(t0 + SPB * 3, ch.notes[3] + 12, 0.07 * it, 0.5);
  if (it > 0.88) bell(t0 + SPB, ch.notes[3] + 24, 0.05 * it, 0.5);

  for (let b = 0; b < 4; b++) {
    const tb = t0 + b * SPB;
    if (tb >= TURN + 2 && tb < PEAK + 1.6) {
      if (b % 2 === 0) kick(tb, 0.36 * it);
      shaker(tb + SPB / 2, 0.05 * it);
    }
  }
}

// ---- 4. the verdict ----
drop(PEAK, 190, 46, 0.5, 1.1);
pad(PEAK, 2.6, [62, 66, 69, 74], 0.05, 0.22);
[74, 78, 81, 86].forEach((m, k) =>
  bell(PEAK + 0.02 + k * 0.07, m, 0.08, 0.25 + k * 0.17),
);

// ---- Schroeder reverb on the wet bus ----
function comb(buf, delaySec, fb, damp) {
  const d = Math.floor(delaySec * SR),
    out = new Float32Array(N);
  const store = new Float32Array(d);
  let lp = 0,
    idx = 0;
  for (let i = 0; i < N; i++) {
    const y = store[idx];
    lp = y * (1 - damp) + lp * damp;
    store[idx] = buf[i] + lp * fb;
    out[i] = y;
    if (++idx >= d) idx = 0;
  }
  return out;
}
function allpass(buf, delaySec, g) {
  const d = Math.floor(delaySec * SR),
    out = new Float32Array(N);
  const store = new Float32Array(d);
  let idx = 0;
  for (let i = 0; i < N; i++) {
    const bufout = store[idx];
    out[i] = -buf[i] + bufout;
    store[idx] = buf[i] + bufout * g;
    if (++idx >= d) idx = 0;
  }
  return out;
}
function reverb(buf) {
  let acc = new Float32Array(N);
  for (const dl of [0.0297, 0.0371, 0.0411, 0.0437]) {
    const o = comb(buf, dl, 0.85, 0.4);
    for (let i = 0; i < N; i++) acc[i] += o[i] * 0.25;
  }
  acc = allpass(acc, 0.005, 0.7);
  return allpass(acc, 0.0017, 0.7);
}
const rL = reverb(wetL),
  rR = reverb(wetR);

// ---- master: normalise, soft clip, fades ----
const WET = 0.3;
let peak = 0;
const mix = new Float32Array(N * 2);
for (let i = 0; i < N; i++) {
  mix[2 * i] = dryL[i] + rL[i] * WET;
  mix[2 * i + 1] = dryR[i] + rR[i] * WET;
  peak = Math.max(peak, Math.abs(mix[2 * i]), Math.abs(mix[2 * i + 1]));
}
const norm = peak > 0 ? 0.8 / peak : 1;
const fi = 0.05,
  fo = Math.min(2.4, DUR * 0.12);
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0);
buf.writeUInt32LE(36 + N * 4, 4);
buf.write("WAVE", 8);
buf.write("fmt ", 12);
buf.writeUInt32LE(16, 16);
buf.writeUInt16LE(1, 20);
buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24);
buf.writeUInt32LE(SR * 4, 28);
buf.writeUInt16LE(4, 32);
buf.writeUInt16LE(16, 34);
buf.write("data", 36);
buf.writeUInt32LE(N * 4, 40);
let o = 44;
for (let i = 0; i < N; i++) {
  const tt = i / SR;
  let g = 1;
  if (tt < fi) g = tt / fi;
  if (tt > DUR - fo) g = Math.max(0, (DUR - tt) / fo);
  for (let ch = 0; ch < 2; ch++) {
    const v = Math.tanh(mix[2 * i + ch] * norm * 1.05) * g;
    buf.writeInt16LE((Math.max(-1, Math.min(1, v)) * 32767) | 0, o);
    o += 2;
  }
}
fs.mkdirSync(path.dirname(path.resolve(OUT)), { recursive: true });
fs.writeFileSync(OUT, buf);
console.log(
  `wrote ${OUT} ${DUR.toFixed(1)}s turn=${TURN} peak=${PEAK} (pre-norm peak ${peak.toFixed(3)})`,
);
