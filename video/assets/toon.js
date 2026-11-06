/* goalify promo, round 7: the bedroom and the character, as a modern flat illustration in the film
   palette (night purples, cyan, pink, warm sunrise). Every prop is plain SVG / CSS built once at
   setup; every change (lamp, sky, pose, expression, laptop screen) is a timeline tween, so the film
   stays seekable. Positions live in assets/toon.css (16:9 first, then the 9:16 relayout). */
(function () {
  var INK = "#2a1c4a",
    SKIN = "#ffd3b6",
    SKIN2 = "#f4b48f",
    HAIR = "#3a2363";

  // the character: head + shoulders. Every expression is a group; Toon.mood() shows one set.
  function face() {
    return (
      '<svg class="toon-face" viewBox="0 0 400 460" overflow="visible">' +
      "<defs>" +
      '<linearGradient id="tf-skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe0c8"/><stop offset="1" stop-color="' +
      SKIN +
      '"/></linearGradient>' +
      '<linearGradient id="tf-hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#57358f"/><stop offset="1" stop-color="' +
      HAIR +
      '"/></linearGradient>' +
      '<linearGradient id="tf-pj" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fd6e8"/><stop offset="1" stop-color="#2a8fc0"/></linearGradient>' +
      "</defs>" +
      // shoulders in pyjamas
      '<g class="c-body"><path d="M78 470 C80 380 122 336 200 336 C278 336 320 380 322 470 Z" fill="url(#tf-pj)"/>' +
      '<path d="M166 338 L200 382 L234 338" fill="none" stroke="#e8fbff" stroke-width="9" stroke-linejoin="round"/>' +
      '<rect x="178" y="292" width="44" height="52" rx="18" fill="' +
      SKIN2 +
      '"/>' +
      '<circle cx="200" cy="410" r="5" fill="#e8fbff"/><circle cx="200" cy="440" r="5" fill="#e8fbff"/></g>' +
      // hair behind the head
      '<ellipse cx="200" cy="176" rx="132" ry="124" fill="url(#tf-hair)"/>' +
      '<circle cx="76" cy="200" r="24" fill="' +
      SKIN2 +
      '"/><circle cx="324" cy="200" r="24" fill="' +
      SKIN2 +
      '"/>' +
      '<ellipse cx="200" cy="198" rx="122" ry="116" fill="url(#tf-skin)"/>' +
      // fringe
      '<path class="c-hair" d="M78 182 C72 96 132 52 204 52 C276 52 332 94 324 180 C306 140 276 118 240 112 C222 134 178 142 138 126 C114 138 92 156 78 182 Z" fill="url(#tf-hair)"/>' +
      // morning bed hair: three soft tufts and a loose strand
      '<g class="c-messy" fill="' +
      HAIR +
      '"><path d="M118 92 C86 70 92 34 124 46 C118 64 126 80 140 86 Z"/><path d="M196 58 C186 18 220 4 236 30 C216 30 208 44 214 60 Z"/>' +
      '<path d="M276 86 C296 52 334 56 334 84 C314 74 298 82 290 98 Z"/><path d="M232 56 C260 22 300 30 296 52" fill="none" stroke="' +
      HAIR +
      '" stroke-width="9" stroke-linecap="round"/></g>' +
      // brows
      '<g class="c-brows" stroke="' +
      HAIR +
      '" stroke-width="9" stroke-linecap="round" fill="none"><path d="M126 150 Q150 138 174 148"/><path d="M226 148 Q250 138 274 150"/></g>' +
      '<g class="c-brows-up" stroke="' +
      HAIR +
      '" stroke-width="9" stroke-linecap="round" fill="none"><path d="M124 132 Q150 112 176 126"/><path d="M224 126 Q250 112 276 132"/></g>' +
      // eyes
      '<g class="e-open"><ellipse cx="150" cy="194" rx="25" ry="28" fill="#fff"/><ellipse cx="250" cy="194" rx="25" ry="28" fill="#fff"/>' +
      '<circle cx="160" cy="198" r="14" fill="' +
      INK +
      '"/><circle cx="260" cy="198" r="14" fill="' +
      INK +
      '"/><circle cx="165" cy="191" r="5" fill="#fff"/><circle cx="265" cy="191" r="5" fill="#fff"/></g>' +
      '<g class="e-wide"><ellipse cx="150" cy="190" rx="29" ry="34" fill="#fff"/><ellipse cx="250" cy="190" rx="29" ry="34" fill="#fff"/>' +
      '<circle cx="150" cy="192" r="10" fill="' +
      INK +
      '"/><circle cx="250" cy="192" r="10" fill="' +
      INK +
      '"/><circle cx="154" cy="187" r="3.5" fill="#fff"/><circle cx="254" cy="187" r="3.5" fill="#fff"/></g>' +
      '<g class="e-half"><ellipse cx="150" cy="200" rx="24" ry="17" fill="#fff"/><ellipse cx="250" cy="200" rx="24" ry="17" fill="#fff"/>' +
      '<circle cx="153" cy="206" r="11" fill="' +
      INK +
      '"/><circle cx="253" cy="206" r="11" fill="' +
      INK +
      '"/>' +
      '<path d="M124 202 A26 22 0 0 1 176 202 Z" fill="' +
      SKIN2 +
      '"/><path d="M224 202 A26 22 0 0 1 276 202 Z" fill="' +
      SKIN2 +
      '"/>' +
      '<path d="M124 202 L176 202 M224 202 L276 202" stroke="' +
      INK +
      '" stroke-width="6" stroke-linecap="round"/></g>' +
      '<g class="e-closed" stroke="' +
      INK +
      '" stroke-width="7" fill="none" stroke-linecap="round"><path d="M126 200 Q150 216 174 200"/><path d="M226 200 Q250 216 274 200"/></g>' +
      '<g class="e-happy" stroke="' +
      INK +
      '" stroke-width="8" fill="none" stroke-linecap="round"><path d="M126 206 Q150 180 174 206"/><path d="M226 206 Q250 180 274 206"/></g>' +
      // nose, cheeks
      '<ellipse cx="200" cy="228" rx="10" ry="7" fill="#eda283"/>' +
      '<g class="c-cheek" fill="#ff8fb8"><ellipse cx="124" cy="240" rx="22" ry="14"/><ellipse cx="276" cy="240" rx="22" ry="14"/></g>' +
      // mouths
      '<path class="m-neutral" d="M182 262 Q200 272 218 262" stroke="' +
      INK +
      '" stroke-width="7" fill="none" stroke-linecap="round"/>' +
      '<path class="m-sleep" d="M186 264 Q200 272 214 264" stroke="' +
      INK +
      '" stroke-width="6" fill="none" stroke-linecap="round"/>' +
      '<path class="m-flat" d="M180 268 Q190 262 200 268 Q210 274 220 268" stroke="' +
      INK +
      '" stroke-width="6" fill="none" stroke-linecap="round"/>' +
      '<g class="m-yawn"><ellipse cx="200" cy="268" rx="17" ry="23" fill="#6b2346"/><ellipse cx="200" cy="282" rx="10" ry="7" fill="#ff7d98"/></g>' +
      '<g class="m-o"><ellipse cx="200" cy="270" rx="15" ry="19" fill="#6b2346"/></g>' +
      '<g class="m-smile"><path d="M164 252 Q200 300 236 252 Q200 266 164 252 Z" fill="#6b2346"/><path d="M182 274 Q200 286 218 274 Q200 268 182 274 Z" fill="#ff7d98"/></g>' +
      '<path class="m-softsmile" d="M178 258 Q200 280 222 258" stroke="' +
      INK +
      '" stroke-width="7" fill="none" stroke-linecap="round"/>' +
      // facepalm hand
      '<g class="c-hand"><g transform="rotate(-14 200 180)" fill="' +
      SKIN2 +
      '" stroke="#d98d6a" stroke-width="4">' +
      '<rect x="110" y="88" width="34" height="112" rx="17"/><rect x="146" y="72" width="34" height="128" rx="17"/><rect x="182" y="74" width="34" height="126" rx="17"/><rect x="218" y="90" width="34" height="108" rx="17"/>' +
      '<rect x="104" y="146" width="154" height="122" rx="52"/><rect x="58" y="206" width="90" height="34" rx="17" transform="rotate(-32 102 222)"/></g></g>' +
      "</svg>"
    );
  }

  var GROUPS = [
    "e-open",
    "e-wide",
    "e-half",
    "e-closed",
    "e-happy",
    "c-brows",
    "c-brows-up",
    "c-messy",
    "c-cheek",
    "m-neutral",
    "m-sleep",
    "m-flat",
    "m-yawn",
    "m-o",
    "m-smile",
    "m-softsmile",
  ];
  var MOODS = {
    focused: ["e-open", "c-brows", "m-neutral"],
    sleep: ["e-closed", "m-sleep"],
    smilesleep: ["e-closed", "m-softsmile", "c-cheek"],
    sleepy: ["e-half", "c-brows", "c-messy", "m-flat"],
    yawn: ["e-half", "c-brows", "c-messy", "m-yawn"],
    shocked: ["e-wide", "c-brows-up", "c-messy", "m-o"],
    happy: ["e-happy", "c-brows", "c-cheek", "m-smile"],
    // round 6 names kept for older scenes
    groggy: ["e-half", "c-brows", "c-messy", "m-flat"],
    dream: ["e-closed", "m-softsmile", "c-cheek"],
  };
  // show one expression from time t (an immediate set at 0, a zero-length tween later)
  function mood(tl, scope, name, t) {
    var on = MOODS[name] || [];
    GROUPS.forEach(function (g) {
      var els = scope.querySelectorAll("." + g);
      if (!els.length) return;
      var v = on.indexOf(g) >= 0 ? (g === "c-cheek" ? 0.5 : 1) : 0;
      if (t <= 0) gsap.set(els, { opacity: v });
      else tl.set(els, { opacity: v }, t);
    });
  }

  // the laptop: a bezel in SVG, the screen in real text (big enough for a phone). Screen states:
  // lp-chat (the request), lp-wait (the frozen run), lp-prog (the good run), lp-done (the site)
  function laptop() {
    return (
      '<svg viewBox="0 0 360 240"><defs><linearGradient id="lp-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3b86"/><stop offset="1" stop-color="#2c2258"/></linearGradient></defs>' +
      '<rect x="20" y="0" width="320" height="212" rx="16" fill="url(#lp-body)"/>' +
      '<rect x="31" y="11" width="298" height="190" rx="8" fill="#0c0a1d"/>' +
      '<g class="lp-site"><rect x="31" y="11" width="298" height="190" rx="8" fill="#2a1840"/><rect x="31" y="11" width="298" height="12" fill="#ff8fb8"/></g>' +
      '<path d="M0 214 L360 214 L346 234 Q344 238 338 238 L22 238 Q16 238 14 234 Z" fill="#5a4aa0"/><rect x="146" y="214" width="68" height="7" rx="3.5" fill="#3a2e70"/>' +
      "</svg>" +
      '<div class="lp-ui lp-chat"><div class="lp-me">Build a website for my bakery.</div><div class="lp-ai"><span class="lp-dots"><i></i><i></i><i></i></span><span class="lp-on">On it!</span></div></div>' +
      '<div class="lp-ui lp-wait"><div class="lp-n">0 of 6 pages built</div><div class="lp-bar"></div><div class="lp-st">4 questions waiting</div></div>' +
      '<div class="lp-ui lp-prog"><div class="lp-n"><span class="lp-k">1</span> of 6 pages built</div><div class="lp-bar"><b></b></div><div class="lp-st">Questions asked: 0</div></div>' +
      '<div class="lp-ui lp-done"><div class="lp-site-t">Little Oven Bakery</div><div class="lp-n">6 of 6 pages built</div><div class="lp-bar"></div></div>'
    );
  }

  function mug() {
    return (
      '<svg viewBox="0 0 120 140">' +
      '<g class="mg-steam" stroke="#f1edff" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.7">' +
      '<path class="mg-s" d="M38 30 q-8 -12 0 -22"/><path class="mg-s" d="M56 28 q8 -12 0 -24"/><path class="mg-s" d="M74 30 q-8 -12 0 -22"/></g>' +
      '<path d="M92 64 h8 a18 18 0 0 1 0 36 h-8" stroke="#ff8fb8" stroke-width="10" fill="none"/>' +
      '<rect x="16" y="42" width="80" height="90" rx="20" fill="#ff8fb8"/><rect x="16" y="42" width="80" height="22" rx="11" fill="#ffb3cc"/>' +
      '<ellipse cx="56" cy="46" rx="36" ry="7" fill="#6a3a24"/>' +
      "</svg>"
    );
  }

  // the bedroom; `p` prefixes the ids a scene animates
  function room(p) {
    var stars = "";
    var R = window.Film.rng(77);
    for (var i = 0; i < 26; i++)
      stars +=
        '<i style="left:' +
        (R() * 96).toFixed(1) +
        "%;top:" +
        (R() * 70).toFixed(1) +
        "%;width:" +
        (2 + R() * 3).toFixed(1) +
        "px;height:" +
        (2 + R() * 3).toFixed(1) +
        'px"></i>';
    return (
      '<div class="rm" id="' +
      p +
      '-room">' +
      '<div class="rm-bg" id="' +
      p +
      '-bg">' +
      '<div class="rm-wall"></div><div class="rm-sun-wall" id="' +
      p +
      '-sunwall"></div>' +
      '<div class="rm-win"><div class="rm-sky"></div><div class="rm-sky2" id="' +
      p +
      '-sky2"></div>' +
      '<div class="rm-stars" id="' +
      p +
      '-stars">' +
      stars +
      "</div>" +
      '<div class="rm-moon" id="' +
      p +
      '-moon"></div><div class="rm-sun" id="' +
      p +
      '-sun"></div>' +
      '<div class="rm-cloud c1"></div><div class="rm-cloud c2"></div><div class="rm-hill"></div><div class="rm-hill b"></div><div class="rm-mull"></div></div>' +
      '<div class="rm-curt l"></div><div class="rm-curt r"></div>' +
      "</div>" +
      '<div class="rm-floor"></div><div class="rm-rug"></div>' +
      '<div class="rm-fg" id="' +
      p +
      '-fg">' +
      '<div class="rm-ns"><i></i></div>' +
      '<svg class="rm-lamp" id="' +
      p +
      '-lamp" viewBox="0 0 160 240"><rect x="52" y="214" width="56" height="18" rx="9" fill="#5a4aa0"/><rect x="74" y="120" width="12" height="100" rx="6" fill="#7a68c8"/>' +
      '<path class="lamp-shade" d="M34 30 L126 30 L150 124 L10 124 Z" fill="#ffcf8a"/><path d="M34 30 L126 30 L132 54 L28 54 Z" fill="#fff1d6" opacity="0.6"/></svg>' +
      '<div class="rm-headb"><i></i><i></i><i></i></div>' +
      '<div class="rm-pillow"></div>' +
      '<div class="rm-char" id="' +
      p +
      '-char">' +
      face() +
      "</div>" +
      '<div class="rm-duvet"><i class="f1"></i><i class="f2"></i></div>' +
      '<div class="rm-table"><i></i></div>' +
      '<div class="rm-mug" id="' +
      p +
      '-mug">' +
      mug() +
      "</div>" +
      "</div>" +
      '<div class="rm-shade" id="' +
      p +
      '-shade"></div>' +
      '<div class="rm-clock" id="' +
      p +
      '-clock"><span class="rm-t" id="' +
      p +
      '-t">11:04</span><span class="rm-ap" id="' +
      p +
      '-ap">PM</span>' +
      '<svg class="rm-ring" id="' +
      p +
      '-ring" viewBox="0 0 400 200"><g stroke="#efe4cc" stroke-width="6" stroke-linecap="round" fill="none"><path d="M30 64 q-20 36 0 72"/><path d="M8 46 q-30 54 0 108"/><path d="M370 64 q20 36 0 72"/><path d="M392 46 q30 54 0 108"/></g></svg></div>' +
      '<div class="rm-cone" id="' +
      p +
      '-cone"></div>' +
      '<div class="rm-scr" id="' +
      p +
      '-scr"></div>' +
      '<div class="rm-laptop" id="' +
      p +
      '-laptop">' +
      laptop() +
      "</div>" +
      "</div>"
    );
  }

  // a wall-clock text tween: minutes from midnight, a -> b (seek-safe)
  function clock(tl, p, a, b, t, dur, init) {
    var tEl = document.getElementById(p + "-t"),
      apEl = document.getElementById(p + "-ap");
    var o = { m: a };
    function show(m) {
      m = ((Math.round(m) % 1440) + 1440) % 1440;
      var h = Math.floor(m / 60);
      tEl.textContent = (h % 12 || 12) + ":" + ("0" + (m % 60)).slice(-2);
      apEl.textContent = h < 12 ? "AM" : "PM";
    }
    if (init) show(a);
    tl.fromTo(
      o,
      { m: a },
      {
        m: b,
        duration: Math.max(0.01, dur),
        ease: "power1.inOut",
        immediateRender: false,
        onUpdate: function () {
          show(o.m);
        },
      },
      t,
    );
  }

  // frame 0 of the film (also the end-card dissolve, so the main cut loops): night, lamp on,
  // he sits in bed looking at the laptop, the request already on its screen
  function night0(p) {
    var q = function (s) {
      return document.querySelectorAll(
        s
          .split(",")
          .map(function (x) {
            return "#" + p + "-room " + x.trim();
          })
          .join(", "),
      );
    };
    gsap.set(q(".lp-wait, .lp-prog, .lp-done, .lp-site, .lp-on"), {
      opacity: 0,
    });
    gsap.set(q(".lp-chat, .lp-dots"), { opacity: 1 });
    gsap.set("#" + p + "-sky2", { opacity: 0 });
    gsap.set(
      [
        "#" + p + "-sun",
        "#" + p + "-sunwall",
        "#" + p + "-ring",
        "#" + p + "-mug",
      ],
      { opacity: 0 },
    );
    gsap.set(["#" + p + "-stars", "#" + p + "-moon"], { opacity: 1 });
    gsap.set(q(".rm-cloud"), { opacity: 0 });
    gsap.set("#" + p + "-shade", { opacity: 0.42 });
    gsap.set(["#" + p + "-cone", "#" + p + "-scr"], { opacity: 1 });
    gsap.set("#" + p + "-lamp .lamp-shade", { fill: "#ffcf8a" });
    gsap.set("#" + p + "-char", { y: 0, rotation: 0 });
    gsap.set(q(".c-hand"), { opacity: 0 });
    var c = document.getElementById(p + "-t");
    c.textContent = "11:04";
    document.getElementById(p + "-ap").textContent = "PM";
  }

  window.Toon = {
    face: face,
    mood: mood,
    room: room,
    laptop: laptop,
    mug: mug,
    clock: clock,
    night0: night0,
  };
})();
