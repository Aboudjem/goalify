// Writes index.html (the one root composition HyperFrames allows per project) for a chosen cut,
// from ONE cut table, so the scene files in compositions/ stay the single source of every shot
// and the captions live in one place (the CAPTIONS below):
//   node scripts/build-roots.js [main|vertical|short|demo]     (default: main)
// main      16:9 main cut  (1920x1080)
// vertical  9:16 main cut  (1080x1920; scenes re-lay themselves out via CSS/JS, not a crop)
// short     16:9 15 s cut
// demo      16:9 muted README loop
// It also writes compositions/captions.html (the caption track) for the same cut.
// The committed index.html + captions.html are always the main cut; scripts/render-all.sh restores them.
//
// Caption rules (owner): plain words, no em dashes, max 2 lines of about 7 words (a <br> marks
// the break), and every caption on screen at least 0.35 s per word (checked below).
const fs = require("fs");
const path = require("path");

const SCENES = {
  ask: "compositions/ask.html", // 1-3: big job, it keeps asking, "Done!" that isn't
  turn: "compositions/turn.html", // 4: Meet goalify (the mark ignites)
  goal: "compositions/goal.html", // 5-6: requests become goals; what a goal is
  homework: "compositions/homework.html", // 7: doable, research, precise, every question now
  summary: "compositions/summary.html", // 8: short summary in Claude + the detail page
  clear: "compositions/clear.html", // 9: /clear, paste one line, walk away
  nonstop: "compositions/nonstop.html", // 10: works alone (time-lapse)
  proof: "compositions/proof.html", // 11: VERIFIED + what it did
  cta: "compositions/cta.html", // 12: install
};

const MAIN = [
  ["ask", 8.4],
  ["turn", 1.9],
  ["goal", 9.05],
  ["homework", 5.45],
  ["summary", 3.95],
  ["clear", 2.9],
  ["nonstop", 3.25],
  ["proof", 4.3],
  ["cta", 5.6],
];
// [start, end, html, sub?, opts?] in seconds on the cut's clock. A sub line appears SUB_DELAY s
// after its caption and is checked as its own caption (0.35 s per word from when it appears).
// <br class="pb"> breaks only in 9:16 (a line too long for a phone-width frame).
const MAIN_CAPS = [
  [0.15, 2.3, "You give AI a <span class='grad'>big job.</span>"],
  [2.4, 5.6, "It stops to ask you stuff.<br>Again and <span class='grad'>again.</span>"],
  [5.7, 8.2, 'Or it says "Done!"...<br>and it <span class="grad">isn\'t.</span>'],
  [8.55, 10.2, 'Meet <span class="grad">goalify.</span>'],
  [10.4, 12.9, 'It turns any request<br>into a <span class="grad">goal.</span>'],
  // honesty (release verifier): a run also ends at the turn limit, so never "can't stop"
  [13.0, 19.3, 'A goal is a clear <span class="grad">finish line.</span><br>The AI keeps going until it\'s proven, <br class="pb">or hits your limit.', null, { maxWords: 11, tall: true }],
  [19.4, 21.2, 'First, it does the <span class="grad">homework.</span>'],
  [21.25, 24.78, "It checks it's doable, researches,<br>and asks <span class='grad'>every question</span> now."],
  [24.85, 28.72, 'You get a short <span class="grad">summary,</span><br>and a page with every detail.'],
  [28.8, 31.62, 'Clear the chat. Paste one line.<br><span class="grad">Walk away.</span>'],
  [31.7, 34.87, 'Your AI works alone. Hours.<br>Even days. <span class="grad">Zero interruptions.</span>'],
  [34.95, 39.17, 'Then it checks everything, <span class="grad">proves it,</span><br>and tells you what it did.'],
  [39.25, 44.8, 'Hand your AI a huge task.<br>Come back to <span class="grad">proof.</span>'],
];

// The 15 s cut reads at the same 0.35 s a word as the main cut. To fit 15.5 s it keeps five
// lines: "And it proves it's done." is dropped and the brand promise plays over VERIFIED and the
// end card ("Come back to proof" lands on the proof).
const SHORT = [
  ["ask", 2.4],
  ["turn", 2.5],
  ["homework", 1.85],
  ["goal", 2.05],
  ["nonstop", 2.3],
  ["proof", 1.35],
  ["cta", 3.0],
];
const SHORT_CAPS = [
  [0.1, 3.25, 'You give AI a big job.<br>It keeps <span class="grad">stopping.</span>'],
  [3.3, 4.9, 'Meet <span class="grad">goalify.</span>'],
  [4.95, 8.85, 'It asks everything first.<br>Then turns your request into a <span class="grad">goal.</span>'],
  [8.88, 11.68, 'Your AI works alone for hours.<br><span class="grad">Zero interruptions.</span>'],
  [11.72, 15.45, 'Hand your AI a huge task.<br>Come back to <span class="grad">proof.</span>'],
];

const DEMO = [
  ["goal", 2.4],
  ["homework", 2.2],
  ["nonstop", 2.4],
  ["proof", 2.8],
];
const DEMO_CAPS = [
  [0.1, 2.3, 'Any request becomes a <span class="grad">goal.</span>'],
  [2.45, 4.5, '<span class="grad">Every question</span> asked first.'],
  [4.65, 6.75, 'Then it works <span class="grad">alone.</span>'],
  [6.9, 9.8, 'And <span class="grad">proves</span> it\'s done.'],
];
const SUB_DELAY = 0.9;

const CUTS = [
  {
    name: "main",
    title: "goalify promo (16:9)",
    w: 1920,
    h: 1080,
    seq: MAIN,
    caps: MAIN_CAPS,
    music: "assets/music-main.mp3",
    shots: [8.75, 24.0, 39.6],
    warp: ["nonstop"],
  },
  {
    name: "vertical",
    title: "goalify promo (9:16)",
    w: 1080,
    h: 1920,
    seq: MAIN,
    caps: MAIN_CAPS,
    music: "assets/music-main.mp3",
    shots: [8.75, 24.0, 39.6],
    warp: ["nonstop"],
  },
  {
    name: "short",
    title: "goalify promo (15 s)",
    w: 1920,
    h: 1080,
    seq: SHORT,
    caps: SHORT_CAPS,
    music: "assets/music-short.mp3",
    shots: [2.75, 13.0],
    warp: ["nonstop"],
  },
  {
    name: "demo",
    title: "goalify demo loop",
    w: 1920,
    h: 1080,
    seq: DEMO,
    caps: DEMO_CAPS,
    music: null,
    shots: [7.2],
    warp: ["nonstop"],
  },
];

const r2 = (x) => Math.round(x * 100) / 100;
const plain = (h) => h.replace(/<br>/g, " ").replace(/<[^>]+>/g, "");

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
{
  let t = 0;
  const hosts = [];
  const warp = [];
  c.seq.forEach(([id, dur], i) => {
    hosts.push(
      `      <div id="${id}" data-composition-id="${id}" data-composition-src="${SCENES[id]}" data-start="${r2(t)}" data-duration="${dur}" data-track-index="${i + 1}" data-track-kind="graphics" data-width="${c.w}" data-height="${c.h}" style="z-index: ${i + 2}"></div>`,
    );
    if (c.warp.includes(id)) warp.push(r2(t + 0.1), r2(t + dur - 0.1));
    t += dur;
  });
  const D = r2(t);

  // caption checks: reading time, line length, no em dash
  const problems = [];
  const PW = c.perWord || 0.35, MIN = c.minCap || 1.6, SD = c.subDelay || SUB_DELAY;
  const EM_DASH = String.fromCharCode(0x2014);
  const count = (h) => plain(h).split(/\s+/).filter(Boolean).length;
  c.caps.forEach(([s, e, html, sub, opts], i) => {
    const text = plain(html) + (sub ? " " + plain(sub) : "");
    const words = count(html);
    if (e - s < Math.max(MIN, PW * words) - 1e-6)
      problems.push(`caption ${i + 1} on screen ${r2(e - s)} s < ${r2(PW * words)} s (${words} words)`);
    if (sub && e - s - SD < Math.max(MIN, PW * count(sub)) - 1e-6)
      problems.push(`caption ${i + 1} sub line on screen ${r2(e - s - SD)} s < ${r2(PW * count(sub))} s`);
    // about 7 words a line (the smaller sub line may run to 8)
    html.split("<br>").forEach((line) => {
      const max = (opts && opts.maxWords) || 7;
      if (count(line) > max) problems.push(`caption ${i + 1} line over ${max} words: ${plain(line)}`);
    });
    (sub ? sub.split("<br>") : []).forEach((line) => {
      if (count(line) > 8) problems.push(`caption ${i + 1} sub line over 8 words: ${plain(line)}`);
    });
    if (text.includes(EM_DASH)) problems.push(`caption ${i + 1} has an em dash`);
    if (e > D + 1e-6) problems.push(`caption ${i + 1} ends after the cut (${e} > ${D})`);
  });
  if (problems.length) {
    console.error(problems.join("\n"));
    process.exit(1);
  }
  const caps = c.caps
    .map(
      ([s, e, html, sub, opts], i) =>
        `    <div id="cap-${i + 1}" class="clip" data-start="${s}" data-duration="${r2(e - s)}" data-track-index="31"><div class="cap${sub ? " cap-sub" : ""}${opts && opts.tall ? " cap-tall" : ""}"><span class="capin">${html}</span>${sub ? `<span class="capsub">${sub}</span>` : ""}</div></div>`,
    )
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
    <script src="assets/film.js"></script>
    <script src="assets/camera-shake.js"></script>
    <script>
      window.FILM_CUT = ${JSON.stringify(c.name === "vertical" ? "main" : c.name)};
      window.FILM_SUB_DELAY = ${c.subDelay || SUB_DELAY};
      window.FILM_SKY = ${JSON.stringify({ dur: D, shots: c.shots, warp })};
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
${caps}
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
        window.Film.cap(tl, el, s, s + d, i === all.length - 1);
      });
      window.__timelines["captions"] = tl;
    })();
  </script>
</template>
`;
  fs.writeFileSync(path.join(__dirname, "..", "compositions", "captions.html"), capsHtml);
  fs.writeFileSync(path.join(__dirname, "..", "index.html"), html);
  console.log(
    `index.html <- ${c.name}: ${c.w}x${c.h}, ${D}s, scenes: ${c.seq.map((s) => s[0]).join(" > ")}, ${c.caps.length} captions`,
  );
}
