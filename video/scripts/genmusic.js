// Procedural music bed for the goalify teaser. No deps. Reproducible (seeded RNG).
// Writes /tmp/music.wav  ->  wire to public/music.mp3 with:
//   node video/scripts/genmusic.js && ffmpeg -y -i /tmp/music.wav -c:a libmp3lame -b:a 192k video/public/music.mp3
//
// Calm, warm, demonstrative cut: NO percussion (kept gentle and uncluttered).
//  - warm pad bed (stack of slightly detuned saws through a one-pole lowpass)
//  - round sub bass
//  - sparse FM bells on chord tones
//  - a Schroeder reverb (4 combs + 2 allpass) for space
//  - an intensity arc that lifts into a IV->I (G->D) plagal resolution right at
//    GOAL COMPLETE (~11-15s), then settles for the install outro.
const fs = require("fs");

const SR = 44100;
const DUR = 26.5;
const N = Math.floor(SR * DUR);
const BPM = 80;
const SPB = 60 / BPM;
const BAR = SPB * 4; // 3.0s per bar

const dryL = new Float32Array(N), dryR = new Float32Array(N);
const wetL = new Float32Array(N), wetR = new Float32Array(N);

let _s = 0x2f6e2b1 >>> 0;
const rnd = () => { _s ^= _s << 13; _s ^= _s >>> 17; _s ^= _s << 5; _s >>>= 0; return _s / 4294967296; };

const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, t) => { const x = clamp01((t - a) / (b - a)); return x * x * (3 - 2 * x); };

// I-V-vi-IV in D major (D A Bm G), resolving G -> D into the GOAL COMPLETE beat.
const CH = {
  D:  { root: 38, notes: [50, 54, 57, 62] },
  A:  { root: 33, notes: [49, 52, 57, 61] },
  Bm: { root: 35, notes: [50, 54, 59, 62] },
  G:  { root: 31, notes: [50, 55, 59, 62] },
};
const PROG = ["D", "A", "Bm", "G", "D", "A", "Bm", "G", "D"]; // ~9 bars over 26.5s
const chordAt = (bar) => CH[PROG[Math.min(PROG.length - 1, bar)]];

// soft intro -> peak on the verify climax (~16s) -> sustain through advantages -> outro
function intensity(t) {
  let v = 0.46 + 0.54 * smooth(0, 16, t);
  if (t > 22.5) v = 1.0 - 0.40 * smooth(22.5, 26.5, t);
  return clamp01(v);
}

function saw(ph) { return 2 * (ph - Math.floor(ph + 0.5)); }

function pad(t0, dur, midis, amp) {
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  const det = [0.0, 0.0018, -0.0016];
  for (const m of midis) {
    const fr = mtof(m);
    let lp = 0;
    const a = 0.15;
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
      dryL[i] += v * (1 - pan) * 1.1; dryR[i] += v * pan * 1.1;
      wetL[i] += v * (1 - pan) * 0.55; wetR[i] += v * pan * 0.55;
    }
  }
}

function bass(t0, dur, midi, amp) {
  const fr = mtof(midi);
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.min(1, tt / 0.025) * Math.exp(-tt / (dur * 0.7));
    const s = (Math.sin(2 * Math.PI * fr * tt) + 0.18 * Math.sin(4 * Math.PI * fr * tt)) * env * amp;
    dryL[i] += s; dryR[i] += s;
  }
}

function bell(t0, midi, amp, pan) {
  const fr = mtof(midi), dur = 1.8;
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.exp(-tt / 0.6) * (1 - Math.exp(-tt / 0.004));
    const mod = Math.exp(-tt / 0.2) * 2.0 * Math.sin(2 * Math.PI * fr * 2.0 * tt);
    const s = Math.sin(2 * Math.PI * fr * tt + mod) * env * amp;
    dryL[i] += s * (1 - pan); dryR[i] += s * pan;
    wetL[i] += s * (1 - pan) * 0.75; wetR[i] += s * pan * 0.75;
  }
}

// soft, round kick — gentle forward motion (only through the middle, kept low)
function kick(t0, amp) {
  const dur = 0.17, i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const fr = 105 * Math.exp(-tt / 0.04) + 44;
    const env = Math.exp(-tt / 0.12);
    const s = Math.sin(2 * Math.PI * fr * tt) * env * amp;
    dryL[i] += s; dryR[i] += s;
  }
}

const nBars = Math.ceil(DUR / BAR);
for (let bar = 0; bar < nBars; bar++) {
  const t0 = bar * BAR;
  if (t0 >= DUR) break;
  const ch = chordAt(bar);
  const it = intensity(t0 + BAR / 2);

  pad(t0, BAR + 0.18, ch.notes.slice(0, 3), 0.09 * (0.6 + 0.4 * it));
  if (it > 0.82) pad(t0, BAR + 0.18, [ch.notes[3] + 12], 0.04 * it);

  bass(t0, SPB * 2.2, ch.root, 0.26 * (0.7 + 0.3 * it));
  if (it > 0.6) bass(t0 + SPB * 2, SPB * 2.1, ch.root + 7, 0.15 * it);

  // sparse, soft bells
  bell(t0, ch.notes[2] + 12, 0.11 * (0.6 + 0.4 * it), 0.4);
  bell(t0 + SPB * 2, ch.notes[1] + 12, 0.09 * (0.6 + 0.4 * it), 0.6);
  if (it > 0.7) bell(t0 + SPB * 3, ch.notes[3] + 12, 0.075 * it, 0.5);
  if (it > 0.9) bell(t0 + SPB, ch.notes[3] + 24, 0.06 * it, 0.5);

  // gentle kick on beats 1 & 3 through the build/payoff/advantages (~9-23s)
  if (t0 >= 9 && t0 < 23) {
    kick(t0, 0.34 * it);
    kick(t0 + SPB * 2, 0.34 * it);
  }
}

// ---- Schroeder reverb on the wet bus --------------------------------------
function comb(buf, delaySec, fb, damp) {
  const d = Math.floor(delaySec * SR), out = new Float32Array(N);
  const store = new Float32Array(d); let lp = 0, idx = 0;
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
  const d = Math.floor(delaySec * SR), out = new Float32Array(N);
  const store = new Float32Array(d); let idx = 0;
  for (let i = 0; i < N; i++) {
    const bufout = store[idx];
    const y = -buf[i] + bufout;
    store[idx] = buf[i] + bufout * g;
    out[i] = y;
    if (++idx >= d) idx = 0;
  }
  return out;
}
function reverb(buf) {
  const c = [0.0297, 0.0371, 0.0411, 0.0437];
  let acc = new Float32Array(N);
  for (const dl of c) { const o = comb(buf, dl, 0.85, 0.4); for (let i = 0; i < N; i++) acc[i] += o[i] * 0.25; }
  acc = allpass(acc, 0.005, 0.7);
  acc = allpass(acc, 0.0017, 0.7);
  return acc;
}
const rL = reverb(wetL), rR = reverb(wetR);

// ---- master ---------------------------------------------------------------
const WET = 0.3;
const mix = new Float32Array(N * 2);
let peak = 0;
for (let i = 0; i < N; i++) {
  const l = dryL[i] + rL[i] * WET;
  const r = dryR[i] + rR[i] * WET;
  mix[2 * i] = l; mix[2 * i + 1] = r;
  peak = Math.max(peak, Math.abs(l), Math.abs(r));
}
const norm = peak > 0 ? 0.76 / peak : 1;
const out = new Float32Array(N * 2);
const fi = 0.7, fo = 2.4;
for (let i = 0; i < N; i++) {
  const tt = i / SR;
  let g = 1;
  if (tt < fi) g = tt / fi;
  if (tt > DUR - fo) g = Math.max(0, (DUR - tt) / fo);
  out[2 * i] = Math.tanh(mix[2 * i] * norm * 1.03) * g;
  out[2 * i + 1] = Math.tanh(mix[2 * i + 1] * norm * 1.03) * g;
}

const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVE", 8);
buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
let o = 44;
for (let i = 0; i < N * 2; i++) {
  buf.writeInt16LE((Math.max(-1, Math.min(1, out[i])) * 32767) | 0, o);
  o += 2;
}
fs.writeFileSync("/tmp/music.wav", buf);
console.log("wrote /tmp/music.wav", DUR.toFixed(1) + "s", "peak(pre-norm)=" + peak.toFixed(3));
