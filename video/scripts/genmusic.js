// Procedural music bed for the goalify teaser. No deps. Reproducible (seeded RNG).
// Writes /tmp/music.wav  ->  wire to public/music.mp3 with:
//   node video/scripts/genmusic.js && ffmpeg -y -i /tmp/music.wav -c:a libmp3lame -b:a 192k video/public/music.mp3
//
// Design: calm, warm, professional, dynamic — NOT beepy.
//  - warm pad bed: a stack of slightly detuned saws through a one-pole lowpass
//  - round sub bass (sine + soft 2nd harmonic)
//  - sparse FM bells (chord tones), soft and spacious — replaces the old buzzy arp
//  - gentle kick + soft shaker, only in the middle "run" section
//  - a Schroeder reverb (4 combs + 2 allpass) on a wet bus for space/glue
//  - an intensity arc that rises into a IV->I (G->D) plagal lift right at GOAL COMPLETE,
//    then resolves on the tonic for the CTA outro.
const fs = require("fs");

const SR = 44100;
const DUR = 30.0;
const N = Math.floor(SR * DUR);
const BPM = 80;
const SPB = 60 / BPM;       // 0.75s per beat
const BAR = SPB * 4;        // 3.0s per bar

// dry + wet (reverb-send) buses, stereo
const dryL = new Float32Array(N), dryR = new Float32Array(N);
const wetL = new Float32Array(N), wetR = new Float32Array(N);

// deterministic RNG so the render is fully reproducible
let _s = 0x2f6e2b1 >>> 0;
const rnd = () => { _s ^= _s << 13; _s ^= _s >>> 17; _s ^= _s << 5; _s >>>= 0; return _s / 4294967296; };

const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, t) => { const x = clamp01((t - a) / (b - a)); return x * x * (3 - 2 * x); };

// I-V-vi-IV in D major: D A Bm G, looping, then resolving D D.
// (root midi, chord-tone midis for the pad/bell)
const CH = {
  D:  { root: 38, notes: [50, 54, 57, 62] }, // D F# A D
  A:  { root: 33, notes: [49, 52, 57, 61] }, // C# E A C#'
  Bm: { root: 35, notes: [50, 54, 59, 62] }, // D F# B D
  G:  { root: 31, notes: [50, 55, 59, 62] }, // D G B D
};
const PROG = ["D", "A", "Bm", "G", "D", "A", "Bm", "G", "D", "D"]; // 10 bars = 30s
const chordAt = (bar) => CH[PROG[Math.min(PROG.length - 1, bar)]];

// Overall arc: soft intro -> build -> peak lift at GOAL COMPLETE (~21-25s) -> settle.
function intensity(t) {
  // base rise from 0.42 to 1.0 across the first 21s, hold, then ease to 0.62 for outro
  let v = 0.42 + 0.58 * smooth(0, 21, t);
  if (t > 24.6) v = 1.0 - 0.40 * smooth(24.6, 30, t); // gentle outro, never silent
  return clamp01(v);
}

// ---- voices ---------------------------------------------------------------
function saw(ph) { return 2 * (ph - Math.floor(ph + 0.5)); }

// Warm pad: 3 detuned saws/voice through a per-render one-pole lowpass, slow attack/release.
function pad(t0, dur, midis, amp) {
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  const det = [0.0, 0.0018, -0.0016];
  for (const m of midis) {
    const fr = mtof(m);
    let lp = 0;
    // cutoff opens slightly with register-independent warmth
    const a = 0.16;
    for (let i = i0; i < i1; i++) {
      const tt = (i - i0) / SR;
      const env = Math.min(1, tt / 0.30) * Math.min(1, (dur - tt) / 0.45); // soft attack + release
      let s = 0;
      for (const d of det) s += saw((fr * (1 + d) * (i / SR)) % 1);
      s /= det.length;
      lp += a * (s - lp);                 // one-pole lowpass -> warm
      const lfo = 1 + 0.05 * Math.sin(2 * Math.PI * 0.12 * (i / SR)); // slow movement
      const v = lp * env * amp * lfo;
      // gentle stereo spread per voice
      const pan = 0.5 + 0.18 * Math.sin(m);
      dryL[i] += v * (1 - pan) * 1.1;
      dryR[i] += v * pan * 1.1;
      wetL[i] += v * (1 - pan) * 0.5;
      wetR[i] += v * pan * 0.5;
    }
  }
}

// Round sub bass.
function bass(t0, dur, midi, amp) {
  const fr = mtof(midi);
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.min(1, tt / 0.02) * Math.exp(-tt / (dur * 0.7));
    const s = (Math.sin(2 * Math.PI * fr * tt) + 0.18 * Math.sin(4 * Math.PI * fr * tt)) * env * amp;
    dryL[i] += s; dryR[i] += s;
  }
}

// Soft FM bell (chord tone). Sine carrier + decaying modulator -> bell attack, pure tail.
function bell(t0, midi, amp, pan) {
  const fr = mtof(midi), dur = 1.6;
  const i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.exp(-tt / 0.55) * (1 - Math.exp(-tt / 0.004));
    const mod = Math.exp(-tt / 0.18) * 2.2 * Math.sin(2 * Math.PI * fr * 2.0 * tt);
    const s = Math.sin(2 * Math.PI * fr * tt + mod) * env * amp;
    dryL[i] += s * (1 - pan); dryR[i] += s * pan;
    wetL[i] += s * (1 - pan) * 0.7; wetR[i] += s * pan * 0.7;
  }
}

// Gentle kick (pitch-drop sine).
function kick(t0, amp) {
  const dur = 0.16, i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const fr = 110 * Math.exp(-tt / 0.035) + 42;
    const env = Math.exp(-tt / 0.11);
    const s = Math.sin(2 * Math.PI * fr * tt) * env * amp;
    dryL[i] += s; dryR[i] += s;
  }
}

// Soft shaker (filtered noise).
function shaker(t0, amp) {
  const dur = 0.06, i0 = Math.floor(t0 * SR), i1 = Math.min(N, Math.floor((t0 + dur) * SR));
  let last = 0;
  for (let i = i0; i < i1; i++) {
    const tt = (i - i0) / SR;
    const env = Math.min(1, tt / 0.005) * Math.exp(-tt / 0.022);
    const w = rnd() * 2 - 1;
    const hp = w - last; last = w;
    const s = hp * env * amp;
    dryL[i] += s * 0.9; dryR[i] += s * 1.0;
  }
}

// ---- arrangement ----------------------------------------------------------
const nBars = Math.ceil(DUR / BAR);
for (let bar = 0; bar < nBars; bar++) {
  const t0 = bar * BAR;
  if (t0 >= DUR) break;
  const ch = chordAt(bar);
  const it = intensity(t0 + BAR / 2);

  // pad: full bar, voiced; brighter/fuller as intensity grows
  pad(t0, BAR + 0.15, ch.notes.slice(0, 3), 0.085 * (0.55 + 0.45 * it));
  if (it > 0.8) pad(t0, BAR + 0.15, [ch.notes[3] + 12], 0.04 * it); // sparkle octave at the peak

  // bass: from bar 1 (t>=3). root on beat 1, light fifth pickup on beat 3 when fuller.
  if (bar >= 1) {
    bass(t0, SPB * 2.1, ch.root, 0.26 * (0.7 + 0.3 * it));
    if (it > 0.6) bass(t0 + SPB * 2, SPB * 2.0, ch.root + 7, 0.16 * it);
  }

  // bells: sparse chord tones. denser & higher as we build.
  if (bar >= 2) {
    const top = ch.notes;
    bell(t0, top[2] + 12, 0.10 * (0.6 + 0.4 * it), 0.40);
    bell(t0 + SPB * 2, top[1] + 12, 0.085 * (0.6 + 0.4 * it), 0.60);
    if (it > 0.65) bell(t0 + SPB * 3, top[3] + 12, 0.075 * it, 0.5);
    if (it > 0.9) bell(t0 + SPB, top[3] + 24, 0.06 * it, 0.5); // high sparkle at the lift
  }

  // soft percussion only through the "run" + payoff (t ~12..25)
  if (t0 >= 12 && t0 < 25.2) {
    for (let b = 0; b < 4; b++) {
      const tb = t0 + b * SPB;
      if (b % 2 === 0) kick(tb, 0.42 * it);          // beats 1 & 3
      shaker(tb + SPB / 2, 0.05 * it);               // offbeats
      if (it > 0.85) shaker(tb, 0.03 * it);
    }
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
  for (const dl of c) { const o = comb(buf, dl, 0.84, 0.4); for (let i = 0; i < N; i++) acc[i] += o[i] * 0.25; }
  acc = allpass(acc, 0.005, 0.7);
  acc = allpass(acc, 0.0017, 0.7);
  return acc;
}
const rL = reverb(wetL), rR = reverb(wetR);

// ---- master ---------------------------------------------------------------
const WET = 0.26;
const out = new Float32Array(N * 2);
let peak = 0;
const mix = new Float32Array(N * 2);
for (let i = 0; i < N; i++) {
  let l = dryL[i] + rL[i] * WET;
  let r = dryR[i] + rR[i] * WET;
  mix[2 * i] = l; mix[2 * i + 1] = r;
  peak = Math.max(peak, Math.abs(l), Math.abs(r));
}
const norm = peak > 0 ? 0.78 / peak : 1;
const fi = 0.6, fo = 2.2;
for (let i = 0; i < N; i++) {
  const tt = i / SR;
  let g = 1;
  if (tt < fi) g = tt / fi;
  if (tt > DUR - fo) g = Math.max(0, (DUR - tt) / fo);
  // gentle saturation for glue, then fade
  let l = Math.tanh(mix[2 * i] * norm * 1.05) * g;
  let r = Math.tanh(mix[2 * i + 1] * norm * 1.05) * g;
  out[2 * i] = l; out[2 * i + 1] = r;
}

// ---- WAV (16-bit PCM stereo) ----------------------------------------------
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
