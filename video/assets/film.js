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
          html += /^\s+$/.test(p) ? " " : '<span class="w">' + p + "</span>";
        });
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

  function portrait() {
    return window.matchMedia("(max-aspect-ratio: 1/1)").matches;
  }

  window.Film = {
    rng: rng,
    words: words,
    caption: caption,
    type: type,
    portrait: portrait,
  };
})();
