// Writes index.html (the one root composition HyperFrames allows per project) for a chosen cut,
// from ONE cut table, so the scene files in compositions/ stay the single source of every shot
// and the captions live in one place (BEATS below):
//   node scripts/build-roots.js [main|vertical|social|hook|loop]      (default: main)
//   node scripts/build-roots.js <cut> --music-args                     (prints genmusic.js args)
//   node scripts/build-roots.js <cut> --beats                          (prints the caption table as JSON)
// main      16:9 master, 58 s (1920x1080)
// vertical  9:16 master (1080x1920; scenes re-lay themselves out via CSS/JS, not a crop)
// social    16:9 30 s cut  (beats 1 2 3 4 9 11 13 14)
// hook      16:9 15 s cut  (beats 1 3 4 13 14)
// loop      16:9 muted README loop, 18 s (beats 3 9 11 13; loops back to the start)
// It also writes compositions/captions.html (the caption track) for the same cut.
// The committed index.html + captions.html are always the main cut.
//
// Caption rules (owner, round 5): simple English, one idea per caption, max 2 lines, at most
// 15 characters per second, every caption on screen at least 2.5 s (3.5 s in the README loop),
// the reveal done within 0.6 s (assets/film.js), zero em dashes. Checked below; a cut that
// breaks one is refused.
const fs = require("fs");
const path = require("path");

const SCENES = {
  night: "compositions/night.html", // 1-4: the bad night: the request, sleep, the questions pile up, 7:00 AM nothing done
  turn: "compositions/turn.html", // 5: Meet goalify (the mark ignites)
  goal: "compositions/goal.html", // 6-7: the same request becomes a goal; its finish line
  research: "compositions/research.html", // 8: it looks online for the best way
  homework: "compositions/homework.html", // 9-10: doable meter; the same questions, answered now
  clear: "compositions/clear.html", // 11: install, /clear, the /goal line
  goodnight: "compositions/goodnight.html", // 12: the good night: works alone, 1 -> 6 of 6
  proof: "compositions/proof.html", // 13: every finish line ticks, VERIFIED
  done: "compositions/done.html", // 14: 7:00 AM, everything is done (mirror of beat 4)
  cta: "compositions/cta.html", // 15: tagline + install
  poster: "compositions/poster.html", // the poster frame (before / after), not in the film
};

// Captions by beat. `<br class="pb">` breaks the line in 9:16 only; `<br>` in both.
const BEATS = {
  1: '11:04 PM. You give your AI<br class="pb"> a <span class="grad">big job.</span>',
  2: 'You go to sleep.<br class="pb"> It works all night... <span class="grad">right?</span>',
  3: '<span class="grad">11:12 PM.</span> It stops<br class="pb"> to ask you a question.',
  4: '7:00 AM. <span class="grad">Nothing</span> is done.',
  5: 'Meet <span class="grad">goalify.</span>',
  6: 'It turns your request<br class="pb"> into a <span class="grad">clear goal.</span>',
  7: 'A goal has a <span class="grad">finish line</span><br class="pb"> you can check.',
  8: 'It looks online for<br class="pb"> the <span class="grad">best way</span> to do it.',
  9: 'It checks that the plan<br class="pb"> can <span class="grad">really work.</span>',
  10: 'It asks <span class="grad">every question</span> now.<br>Before you sleep.',
  11: 'Clear the chat. Paste one line.<br class="pb"> <span class="grad">Go to bed.</span>',
  12: 'This time, your AI works<br class="pb"> <span class="grad">alone</span> all night.',
  13: 'At the end, it checks<br class="pb"> <span class="grad">every finish line.</span>',
  14: '7:00 AM.<br class="pb"> <span class="grad">Everything</span> is done.',
  15: 'Set the goal. Go to sleep.<br class="pb"> <span class="grad">It\'s done.</span>',
};
// which beat each scene segment carries (a scene with no segments is one beat)
const BEAT_OF = {
  "night.type": 1,
  "night.sleep": 2,
  "night.q": 3,
  "night.wake": 4,
  turn: 5,
  "goal.cards": 6,
  "goal.big": 7,
  research: 8,
  "homework.meter": 9,
  "homework.ask": 10,
  clear: 11,
  goodnight: 12,
  proof: 13,
  done: 14,
  cta: 15,
};
const CAP_OPTS = { 15: { cls: "cap-tag" } };

// the question bubbles' times inside the questions shot (night.html uses the same rule)
const qTimes = (len, cold) =>
  cold ? [0, 0, 1.0, 1.8].map((x) => x * Math.min(1, len / 3)) : [0.5, 1.3, 2.1, 2.9].map((x) => x * Math.min(1, len / 4));

// Sound effects, on each scene's own clock (seconds from the segment's start). A function gets the
// segment length and whether the segment opens the film; it returns one time or a list.
const SFX = {
  "night.type": [["pop", 1.0]],
  "night.sleep": [
    ["click", 0.9], // the lamp
    ["snore", 1.2],
  ],
  "night.q": [
    ["ping", (len, cold) => (cold ? 0.5 : qTimes(len, cold)[0])],
    ["pop", (len, cold) => qTimes(len, cold).slice(1).filter((x) => x > 0.01)],
  ],
  "night.wake": [
    ["alarm", 0.15],
    ["slap", (len) => Math.min(2.2, len - 0.5)], // the facepalm
  ],
  "goal.cards": [["pop", 1.2]],
  "goal.big": [["whoosh", -0.15]],
  research: [
    ["tick", 1.3],
    ["tick", 1.9],
    ["tick", 2.5],
  ],
  "homework.meter": [["tick", 2.2]],
  "homework.ask": [
    ["click", 1.0],
    ["click", 1.8],
    ["stamp", 2.6],
  ],
  clear: [["click", 0.62]], // enter on the install line
  goodnight: [
    ["snore", 0.3],
    ["tick", (len) => len - 0.55], // 6 of 6
  ],
  proof: [
    ["tick", 0.35],
    ["tick", 0.75],
    ["tick", 1.15],
    ["hit", 1.6],
  ],
  done: [
    ["alarm", 0.15],
    ["chime", 0.9],
  ],
};

// scene, slot length, segments [start, end, beat?] on the scene clock
const MAIN = [
  ["night", 14, { type: [0, 3.5], sleep: [3.5, 6.5], q: [6.5, 10.5], wake: [10.5, 14] }],
  ["turn", 2.5],
  ["goal", 8, { cards: [0, 4], big: [4, 8] }],
  ["research", 4],
  ["homework", 7, { meter: [0, 3], ask: [3, 7] }],
  ["clear", 3.5],
  ["goodnight", 4],
  ["proof", 4],
  ["done", 4],
  ["cta", 7],
];
const SOCIAL = [
  ["night", 9.5, { type: [0, 3], q: [3, 6.5], wake: [6.5, 9.5] }],
  ["turn", 2.5],
  ["homework", 3.6, { ask: [0, 3.6] }],
  ["goodnight", 3.6],
  ["done", 3.6],
  ["cta", 7.2],
];
// hook a: the night, compressed (1, 3, 4), then 5, 14, 15
const HOOK = [
  ["night", 7.8, { type: [0, 2.5], q: [2.5, 5.3], wake: [5.3, 7.8] }],
  ["turn", 2.5],
  ["done", 2.5],
  ["cta", 2.7],
];
// hook b: cold open on the pile of questions, then 4, 5, 14, 15
const HOOK_B = [
  ["night", 5.5, { q: [0, 3], wake: [3, 5.5] }],
  ["turn", 2.5],
  ["done", 2.5],
  ["cta", 5.0],
];
// hook c: opens on the result (14), then 5, 12, 15
const HOOK_C = [
  ["done", 3.0],
  ["turn", 2.5],
  ["goodnight", 3.5],
  ["cta", 6.0],
];
const POSTER = [["poster", 2]];
const LOOP = [
  ["night", 4.5, { q: [0, 4.5] }],
  ["homework", 4.5, { ask: [0, 4.5] }],
  ["goodnight", 4.5],
  ["done", 4.5],
];

const CUTS = [
  { name: "main", title: "goalify promo (16:9)", w: 1920, h: 1080, seq: MAIN, music: "assets/music-main.mp3", seam: true },
  { name: "vertical", title: "goalify promo (9:16)", w: 1080, h: 1920, seq: MAIN, music: "assets/music-main.mp3", seam: true },
  { name: "social", title: "goalify promo (30 s)", w: 1920, h: 1080, seq: SOCIAL, music: "assets/music-social.mp3" },
  { name: "hook", title: "goalify hook a, night (15 s)", w: 1920, h: 1080, seq: HOOK, music: "assets/music-hook.mp3" },
  { name: "hook-b", title: "goalify hook b, cold open (15 s)", w: 1920, h: 1080, seq: HOOK_B, music: "assets/music-hook-b.mp3" },
  { name: "hook-c", title: "goalify hook c, result first (15 s)", w: 1920, h: 1080, seq: HOOK_C, music: "assets/music-hook-c.mp3" },
  { name: "poster", title: "goalify poster", w: 1920, h: 1080, seq: POSTER, music: null, calmSky: true },
  { name: "loop", title: "goalify README loop", w: 1920, h: 1080, seq: LOOP, music: null, minCap: 3.5, calmSky: true, seam: true },
];

const r2 = (x) => Math.round(x * 100) / 100;
const plain = (h) =>
  h
    .replace(/<br[^>]*>/g, " ")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();

const want = process.argv[2] || "main";
const c = CUTS.find((x) => x.name === want);
if (!c) {
  console.error(
    "unknown cut " +
      want +
      "; use one of " +
      CUTS.map((x) => x.name).join(", "),
  );
  process.exit(1);
}

// lay the cut out: scene hosts, segments, captions, sound effects
let t = 0;
const hosts = [];
const slots = {};
const segs = {};
const caps = []; // [start, end, beat]
const fx = []; // [name, time]
let warp = [];
let turnAt = -1,
  pulseAt = -1,
  peakAt = -1,
  doneAt = -1;
c.seq.forEach(([id, dur, sg], i) => {
  hosts.push(
    `      <div id="${id}" data-composition-id="${id}" data-composition-src="${SCENES[id]}" data-start="${r2(t)}" data-duration="${dur}" data-track-index="${i + 1}" data-track-kind="graphics" data-width="${c.w}" data-height="${c.h}" style="z-index: ${i + 2}"></div>`,
  );
  slots[id] = dur;
  if (sg) segs[id] = sg;
  const parts = sg ? Object.entries(sg) : [[null, [0, dur]]];
  parts.forEach(([name, [a, b, beat]]) => {
    const key = name ? id + "." + name : id;
    if (beat || BEAT_OF[key]) caps.push([r2(t + a), r2(t + b), beat || BEAT_OF[key]]);
    const cold = t + a < 0.05;
    (SFX[key] || []).forEach(([n, o]) => {
      const v = typeof o === "function" ? o(b - a, cold) : o;
      [].concat(v).forEach((x) => fx.push([n, r2(t + a + x)]));
    });
  });
  if (id === "goodnight") pulseAt = r2(t);
  if (id === "nonstop") {
    if (!c.calmSky) warp.push(r2(t + 0.1), r2(t + dur - 0.1)); // the README loop keeps a still sky (small GIF)
    pulseAt = r2(t);
  }
  if (id === "turn") turnAt = r2(t);
  if (id === "proof") peakAt = r2(t + 1.6);
  if (id === "done") doneAt = r2(t);
  t += dur;
});
const D = r2(t);
caps.sort((x, y) => x[0] - y[0]);
// loop seam: the last caption leaves 0.3 s before the end, so the last frame matches frame 0
if (c.seam && caps.length) caps[caps.length - 1][1] = r2(D - 0.3);
if (peakAt < 0) peakAt = doneAt >= 0 ? r2(doneAt + 0.3) : D - 2;
if (pulseAt < 0) pulseAt = D + 10;

if (process.argv.includes("--music-args")) {
  const out = [
    "--dur",
    D,
    "--turn",
    turnAt,
    "--fail",
    -1,
    "--pulse",
    pulseAt,
    "--peak",
    peakAt,
    "--fx",
    fx.map(([n, at]) => n + "@" + at).join(","),
  ];
  console.log(out.join(" "));
  process.exit(0);
}

// caption checks
const problems = [];
const MIN = c.minCap || 2.5,
  MAXCPS = 15;
const EM_DASH = String.fromCharCode(0x2014);
const rows = caps.map(([s, e, beat], i) => {
  const html = BEATS[beat];
  const text = plain(html);
  const chars = text.length;
  const dur = r2(e - s);
  const cps = Math.round((chars / dur) * 10) / 10;
  if (dur < MIN - 1e-6)
    problems.push(`beat ${beat} on screen ${dur} s < ${MIN} s`);
  if (cps > MAXCPS)
    problems.push(`beat ${beat} reads at ${cps} chars/s > ${MAXCPS}`);
  const landLines = html.split(/<br>/).length;
  const portLines = html.split(/<br[^>]*>/).length;
  if (landLines > 2 || portLines > 2)
    problems.push(`beat ${beat} has more than 2 lines`);
  if (text.includes(EM_DASH)) problems.push(`beat ${beat} has an em dash`);
  if (e > D + 1e-6)
    problems.push(`beat ${beat} ends after the cut (${e} > ${D})`);
  return { beat, text, start: s, end: e, dur, chars, cps };
});
if (process.argv.includes("--beats")) {
  console.log(
    JSON.stringify({ cut: c.name, duration: D, captions: rows, fx }, null, 1),
  );
  process.exit(0);
}
if (problems.length) {
  console.error(problems.join("\n"));
  process.exit(1);
}

const capsHtmlRows = caps
  .map(([s, e, beat], i) => {
    const o = CAP_OPTS[beat] || {};
    return `    <div id="cap-${i + 1}" class="clip" data-start="${s}" data-duration="${r2(e - s)}" data-track-index="31"><div class="cap${o.cls ? " " + o.cls : ""}"><span class="capin">${BEATS[beat]}</span></div></div>`;
  })
  .join("\n");

const audio = c.music
  ? `\n      <audio id="music" src="${c.music}" data-start="0" data-duration="${D}" data-track-index="20" data-volume="1"></audio>`
  : "";
const html = `<!doctype html>
<!-- GENERATED by scripts/build-roots.js (cut: ${c.name}): edit the cut table there, not this file. -->
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${c.w}, height=${c.h}" />
    <title>${c.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/film.css" />
    <link rel="stylesheet" href="assets/toon.css" />
    <script src="assets/film.js"></script>
    <script src="assets/toon.js"></script>
    <script src="assets/camera-shake.js"></script>
    <script>
      window.FILM_CUT = ${JSON.stringify(c.name === "vertical" ? "main" : c.name)};
      window.FILM_SLOTS = ${JSON.stringify(slots)};
      window.FILM_SEGS = ${JSON.stringify(segs)};
      window.FILM_SEAM = ${!!c.seam};
      window.FILM_SKY = ${JSON.stringify({ dur: D, shots: c.calmSky ? [] : [r2(turnAt + 0.4), pulseAt < D ? r2(pulseAt + 1.2) : r2(D - 3)], warp, calm: !!c.calmSky })};
    </script>
    <style>
      html,
      body {
        width: ${c.w}px;
        height: ${c.h}px;
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${D}" data-width="${c.w}" data-height="${c.h}">
      <div id="sky" data-composition-id="sky" data-composition-src="compositions/sky.html" data-start="0" data-duration="${D}" data-track-index="0" data-track-kind="graphics" data-width="${c.w}" data-height="${c.h}" style="z-index: 1"></div>
${hosts.join("\n")}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="${D}" data-track-index="30" data-track-kind="captions" data-width="${c.w}" data-height="${c.h}" style="z-index: 40"></div>${audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
`;
const capsHtml = `<!-- GENERATED by scripts/build-roots.js (cut: ${c.name}): the caption script lives there. -->
<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      width: 100% !important;
      height: 100% !important;
      pointer-events: none;
    }
  </style>
  <div id="root" data-composition-id="captions" data-width="${c.w}" data-height="${c.h}">
${capsHtmlRows}
  </div>
  <script>
    (function () {
      var tl = gsap.timeline({ paused: true });
      var all = document.querySelectorAll('[data-composition-id="captions"] .cap');
      all.forEach(function (el, i) {
        var host = el.parentNode;
        var s = parseFloat(host.getAttribute("data-start")),
          d = parseFloat(host.getAttribute("data-duration"));
        window.Film.fitCaption(el);
        // the film's last line holds sharp to the final frame
        window.Film.cap(tl, el, s, s + d, ${c.seam ? "false" : "i === all.length - 1"});
      });
      window.__timelines["captions"] = tl;
    })();
  </script>
</template>
`;
fs.writeFileSync(
  path.join(__dirname, "..", "compositions", "captions.html"),
  capsHtml,
);
fs.writeFileSync(path.join(__dirname, "..", "index.html"), html);
console.log(
  `index.html <- ${c.name}: ${c.w}x${c.h}, ${D}s, scenes: ${c.seq.map((s) => s[0]).join(" > ")}, ${caps.length} captions`,
);
