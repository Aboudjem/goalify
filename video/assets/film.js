/* goalify promo: tiny shared helpers for scene timelines. Everything is a function of
   timeline time; nothing here reads the clock or unseeded randomness. */
(function () {
  function rng(seed) {
    // mulberry32
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // split an element's text into .w spans (once)
  function words(el) {
    if (!el || el.dataset.split) return el ? el.querySelectorAll(".w") : [];
    var html = "";
    el.childNodes.forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (p) {
          if (!p) return;
          html += /^\s+$/.test(p) ? "&nbsp;" : '<span class="w">' + p + "</span>";
        });
      } else if (n.nodeName === "BR") {
        html += n.outerHTML;
      } else {
        html += '<span class="w">' + n.outerHTML + "</span>";
      }
    });
    el.innerHTML = html;
    el.dataset.split = "1";
    return el.querySelectorAll(".w");
  }

  // caption: words blur in (0.14 s, 70 ms apart), hard kill at `end`
  function caption(tl, el, start, end) {
    var ws = words(el);
    tl.fromTo(el, { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);
    tl.fromTo(
      ws,
      { opacity: 0, filter: "blur(8px)" },
      {
        opacity: 1,
        filter: "blur(0px)",
        duration: 0.16,
        ease: "power3.out",
        stagger: 0.07,
      },
      start,
    );
    if (end != null) {
      tl.to(
        el,
        { opacity: 0, filter: "blur(6px)", duration: 0.16, ease: "power2.in" },
        end - 0.16,
      );
    }
  }

  // type text into an element (character reveal) between t0 and t0+dur
  function type(tl, el, t0, dur) {
    var full = el.getAttribute("data-text") || el.textContent;
    el.setAttribute("data-text", full);
    var o = { n: 0 };
    tl.fromTo(
      o,
      { n: 0 },
      {
        n: full.length,
        duration: dur,
        ease: "none",
        onUpdate: function () {
          el.textContent = full.slice(0, Math.round(o.n));
        },
      },
      t0,
    );
    el.textContent = "";
  }

  // burned-in caption on the root timeline: fit the longest line to the frame, then words blur
  // in (70 ms apart) and the line blurs out just before its clip ends
  function fitCaption(el) {
    var inner = el.querySelector(".capin");
    var avail = el.clientWidth - 2 * (portrait() ? 50 : 140);
    var base = parseFloat(getComputedStyle(inner).fontSize);
    var w = inner.offsetWidth;
    if (w > avail) inner.style.fontSize = Math.max(48, Math.floor((base * avail) / w)) + "px";
  }
  // kinetic caption: words spring in one by one (scale + rise + blur), the key word (.grad)
  // lands last-ish with a glow pulse; the line blurs out just before its clip ends
  function cap(tl, el, start, end, hold) {
    var inner = el.querySelector(".capin");
    var sub = el.querySelector(".capsub");
    var ws = words(inner);
    // the whole line is readable within 0.6 s: 0.3 s per word, the last word starts by 0.3 s
    var gap = Math.min(0.06, 0.3 / Math.max(1, ws.length - 1));
    tl.fromTo(
      ws,
      { opacity: 0, y: 14, scale: 0.88, filter: "blur(4px)" },
      { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "back.out(1.4)", stagger: gap },
      start
    );
    if (sub) tl.fromTo(sub, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, start + (window.FILM_SUB_DELAY || 0.9));
    var g = el.querySelectorAll(".grad");
    if (g.length) {
      tl.fromTo(g, { backgroundPosition: "0% 0" }, { backgroundPosition: "100% 0", duration: Math.max(1, end - start), ease: "none" }, start);
      var kw = [];
      g.forEach(function (x) {
        kw.push(x.closest(".w") || x);
      });
      var tk = start + 0.65;
      tl.fromTo(kw, { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, tk);
      tl.fromTo(g, { filter: "drop-shadow(0 0 0px rgba(155,107,255,0))" }, { filter: "drop-shadow(0 0 18px rgba(155,107,255,0.85))", duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, tk);
    }
    if (!hold) tl.to(sub ? [inner, sub] : inner, { opacity: 0, y: -8, filter: "blur(6px)", duration: 0.16, ease: "power2.in" }, end - 0.18);
  }

  // a slow camera push on a scene's wrapper so no frame is ever dead still
  function push(tl, sel, dur, from, to) {
    tl.fromTo(sel, { scale: from || 1, transformOrigin: "50% 45%" }, { scale: to || 1.045, duration: dur, ease: "none" }, 0);
  }

  // particle pop: n small sparks (or 4-point stars) burst from (x, y) inside `box` at time t.
  // opts: { n, colors, dist, star, gravity, size, seed, dur }
  function burst(tl, box, x, y, t, opts) {
    opts = opts || {};
    var R = rng(opts.seed || 1);
    var cols = opts.colors || ["#3dffa8", "#ffffff", "#2ee6ff"];
    var n = opts.n || 10,
      dist = opts.dist || 90,
      dur = opts.dur || 0.6;
    for (var i = 0; i < n; i++) {
      var d = document.createElement("div");
      var sz = (opts.size || 6) * (0.6 + R() * 0.8);
      var c = cols[(R() * cols.length) | 0];
      d.style.cssText =
        "position:absolute;pointer-events:none;left:" + (x - sz / 2) + "px;top:" + (y - sz / 2) + "px;width:" + sz + "px;height:" + sz + "px;background:" + c + ";" +
        (opts.star ? "clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%);" : "border-radius:50%;box-shadow:0 0 " + (6 + sz) + "px " + c + ";");
      box.appendChild(d);
      var a = R() * Math.PI * 2,
        r = dist * (0.45 + R() * 0.7);
      var dx = Math.cos(a) * r,
        dy = Math.sin(a) * r;
      if (opts.gravity) {
        tl.fromTo(d, { x: 0, opacity: 0, rotation: 0 }, { x: dx, rotation: (R() - 0.5) * 720, duration: dur, ease: "power1.out" }, t);
        tl.fromTo(d, { y: 0 }, { keyframes: [{ y: dy - dist * 0.35, duration: dur * 0.4, ease: "power2.out" }, { y: dy + opts.gravity, duration: dur * 0.6, ease: "power2.in" }] }, t);
        tl.fromTo(d, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.05 }, { opacity: 1, duration: dur * 0.6 }, { opacity: 0, duration: dur * 0.35 }] }, t);
      } else {
        tl.fromTo(d, { x: 0, y: 0, opacity: 0, scale: 1 }, { x: dx, y: dy, scale: 0.3, duration: dur, ease: "power3.out" }, t);
        tl.fromTo(d, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.04 }, { opacity: 1, duration: dur * 0.45 }, { opacity: 0, duration: dur * 0.5 }] }, t);
      }
    }
  }

  // short camera shake on a wrapper: seeded jitter that decays to rest (x, y, roll), zero
  // outside its window. (The registry camera-shake helper is vendored in assets/camera-shake.js
  // for longer handheld moves; for a 0.3 s impact this decaying jitter reads cleaner.)
  function shake(tl, sel, t, dur, intensity) {
    var R = rng(Math.round(t * 1000) + 7);
    var n = 8,
      k = intensity || 1.5;
    for (var i = 0; i < n; i++) {
      var f = 1 - i / n;
      tl.to(sel, { x: (R() - 0.5) * 28 * k * f, y: (R() - 0.5) * 18 * k * f, rotation: (R() - 0.5) * 1.6 * k * f, duration: (dur || 0.32) / n, ease: "none" }, t + (i * (dur || 0.32)) / n);
    }
    tl.to(sel, { x: 0, y: 0, rotation: 0, duration: 0.12, ease: "power2.out" }, t + (dur || 0.32));
  }

  // which cut is being rendered (set by the generated index.html)
  function cut() {
    return window.FILM_CUT || "main";
  }

  function portrait() {
    return window.matchMedia("(max-aspect-ratio: 1/1)").matches;
  }

  window.Film = {
    rng: rng,
    words: words,
    caption: caption,
    type: type,
    portrait: portrait,
    fitCaption: fitCaption,
    cap: cap,
    push: push,
    burst: burst,
    shake: shake,
    cut: cut,
  };
})();
