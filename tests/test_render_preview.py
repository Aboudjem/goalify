#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/render_preview.py: the run preview and the brief lint.

Pins: a golden render of examples/sample-brief.md (byte for byte), the condition inside the
copy target byte-identical, escaping of hostile brief text, no request to any host except the
GitHub repo, a size ceiling, one broken-brief specimen per lint rule, and (when Chrome is
installed) a headless screenshot that actually renders.

Standard library only. Run: python3 tests/test_render_preview.py
Exit 0 = all pass, 1 = at least one failed.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "goalify", "scripts")
RENDER = os.path.join(SCRIPTS, "render_preview.py")
SAMPLE = os.path.join(ROOT, "examples", "sample-brief.md")
SAMPLE_COND = os.path.join(ROOT, "examples", "sample-condition.txt")
GOLDEN = os.path.join(ROOT, "examples", "sample-brief.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EXTERNAL_RE = re.compile(r'(?:src|href)\s*=\s*["\']?(https?:)?//[^"\'\s>]+', re.IGNORECASE)

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def render(brief_text, cond_text, tmp, name="b-20261103.md"):
    bp = os.path.join(tmp, name)
    cp = os.path.join(tmp, "CONDITION-b.txt")
    open(bp, "w", encoding="utf-8").write(brief_text)
    open(cp, "w", encoding="utf-8").write(cond_text)
    out = os.path.join(tmp, "out.html")
    if os.path.exists(out):
        os.remove(out)
    p = subprocess.run([sys.executable, RENDER, bp, cp, "--out", out], capture_output=True, text=True)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    rules = set(re.findall(r"^FAIL: ([a-z-]+)", p.stdout, re.MULTILINE))
    return p, page, rules


SAMPLE_TEXT = open(SAMPLE, encoding="utf-8").read()
COND = open(SAMPLE_COND, encoding="utf-8").read().strip()

# --- The sample condition file is the condition printed in the sample brief ---
blocks = re.findall(r"```text\n(.*?)\n```", SAMPLE_TEXT, re.S)
check("examples/sample-condition.txt equals the sample brief's condition block",
      bool(blocks) and blocks[-1].strip() == COND)

tmp = tempfile.mkdtemp(prefix="goalify-preview-")
try:
    # --- Golden render: the committed sample page is exactly what the renderer writes ---
    out = os.path.join(tmp, "sample.html")
    p = subprocess.run([sys.executable, RENDER, SAMPLE, SAMPLE_COND, "--out", out],
                       capture_output=True, text=True)
    check("sample: renders, exit 0", p.returncode == 0, p.stdout[-300:])
    check("sample: prints a file:// URL on its own line",
          p.stdout.strip() == "file://" + os.path.abspath(out), p.stdout)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    golden = open(GOLDEN, encoding="utf-8").read() if os.path.exists(GOLDEN) else None
    check("sample: output is byte-identical to examples/sample-brief.html (the golden)",
          page == golden, "re-run render_preview.py on the sample and commit it")

    m = re.search(r'<code id="goal-line">(.*?)</code>', page, re.S)
    check("copy target: holds '/goal ' + the condition, byte for byte",
          bool(m) and html.unescape(m.group(1)) == "/goal " + COND)
    check("copy target: a copy button points at it", 'data-copy="goal-line"' in page)
    check("copy: navigator.clipboard with an execCommand fallback",
          "navigator.clipboard" in page and "execCommand('copy')" in page)
    hm = re.search(r'<code id="headless-line">(.*?)</code>', page, re.S)
    check("headless line: double-quoted claude -p with the same condition",
          bool(hm) and html.unescape(hm.group(1)) ==
          f'claude -p "/goal {COND}" --permission-mode auto')
    check("codex tab: present with the pipe form",
          'id="codex-pipe"' in page and "codex exec -" in page)

    ext = [x.group(0) for x in EXTERNAL_RE.finditer(page)
           if "github.com/Aboudjem/goalify" not in x.group(0)]
    check("no src=/href= to any host except github.com/Aboudjem/goalify", not ext, f"{ext}")
    check("no external stylesheet, font or script tag",
          not re.search(r"<link\b|@import|<script\s+src|fonts\.googleapis", page))
    check("the GitHub link sits in the footer",
          re.search(r"<footer.*https://github.com/Aboudjem/goalify.*</footer>", page, re.S)
          is not None)
    check(f"size ceiling: under 60,000 bytes (got {len(page.encode()):,})",
          len(page.encode()) < 60_000)
    check("canvas starfield with a shooting star", '<canvas id="sky"' in page and "shots.push" in page)
    check("prefers-reduced-motion is respected (CSS and JS)",
          "prefers-reduced-motion:reduce" in page and "prefers-reduced-motion: reduce" in page)
    check("glass panels: backdrop-filter blur 22px with saturate",
          "backdrop-filter:blur(22px) saturate(160%)" in page)
    check("the phase flow: a wide and a phone SVG, each with one node per phase plus the proof node",
          page.count('<rect x=') == 12 and '<svg class="h"' in page and '<svg class="v"' in page)
    check("the flow has direction arrows", 'marker-end="url(#ah-h)"' in page)
    check("the DoD row drops the 'verified by' tail when the chip shows the command",
          "No callback-style" in page and "returning nothing" not in page.split('id="launch"')[0]
          .split("The finish line")[1])
    check("no cost or token estimate on the page",
          not re.search(r"\$\s?\d|\d+\s?(?:k\s)?tokens|estimated cost", page, re.I))

    # --- Hostile brief text is escaped everywhere it lands ---
    evil = SAMPLE_TEXT.replace(
        "# GOAL: Migrate the widget-api", "# GOAL: <script>alert(1)</script> Migrate the widget-api", 1)
    evil = evil.replace("- Keep the in-memory data layer",
                        '- <img src=x onerror=alert(2)> Keep the in-memory data layer', 1)
    evil = evil.replace("1. **Discover/verify (parallel reads).**",
                        '1. **Discover <svg onload=alert(3)>.**', 1)
    p, epage, rules = render(evil, COND, tmp, "cb-to-async-2026-05-29.md")
    check("xss: the hostile brief still renders", p.returncode == 0, p.stdout[-300:])
    check("xss: no live <script>alert, <img onerror or <svg onload in the page",
          "<script>alert" not in epage and "<img src=x" not in epage and "<svg onload" not in epage)
    check("xss: the payloads appear escaped",
          "&lt;script&gt;alert(1)&lt;/script&gt;" in epage and "&lt;img src=x" in epage)
    check("xss: only one <script> element, the page's own",
          epage.count("<script") == 1, f"{epage.count('<script')}")

    # --- Brief lint: one specimen per rule, each naming the rule that must fire ---
    def without_section(text, heading):
        return re.sub(rf"\n## {re.escape(heading)}.*?(?=\n## )", "\n", text, count=1, flags=re.S)

    specimens = [
        ("missing-section", without_section(SAMPLE_TEXT, "Decisions"), COND),
        ("brief-path-not-absolute",
         SAMPLE_TEXT.replace("This file's own path: `/Users/example/widget-api/.goal/",
                             "This file's own path: `widget-api/.goal/", 1), COND),
        ("dod-no-command",
         SAMPLE_TEXT.replace("- [ ] `getOrder`/`saveOrder` return promises — verified by a one-off "
                             "`node -e` that `await`s them.",
                             "- [ ] getOrder and saveOrder return promises.", 1), COND),
        ("dod-empty",
         re.sub(r"(## Definition of done[^\n]*\n).*?(?=\n## )", r"\1\nNothing yet.\n", SAMPLE_TEXT,
                count=1, flags=re.S), COND),
        ("condition-missing-path", SAMPLE_TEXT,
         COND.replace("/Users/example/widget-api/.goal/cb-to-async-2026-05-29.md", "the brief")),
        ("condition-command-not-in-dod", SAMPLE_TEXT,
         COND.replace("quotes npm test passing", "quotes cargo test passing")),
        ("condition-shell-quote", SAMPLE_TEXT, COND.replace("npm test", "`npm test`")),
        ("condition-stop-rule", SAMPLE_TEXT, COND.replace(" Stop after 40 turns.", "")),
        ("condition-missing", SAMPLE_TEXT, "   "),
    ]
    for rule, btext, ctext in specimens:
        p, spage, rules = render(btext, ctext, tmp, "cb-to-async-2026-05-29.md")
        check(f"lint: {rule} fires, exit 1, no page written",
              p.returncode == 1 and rule in rules and not spage,
              f"exit={p.returncode} rules={sorted(rules)}")
    check("lint: the failure output says no preview was written",
          "no preview written" in p.stdout)

    # --- A ~ form of the brief path in the condition is accepted ---
    home = os.path.expanduser("~")
    hb = SAMPLE_TEXT.replace("/Users/example/widget-api", home + "/widget-api")
    hc = COND.replace("/Users/example/widget-api", "~/widget-api")
    p, _, rules = render(hb, hc, tmp, "cb-to-async-2026-05-29.md")
    check("lint: a ~/ form of the brief's path counts as naming it", p.returncode == 0,
          f"{sorted(rules)}")

    # --- Usage errors ---
    p = subprocess.run([sys.executable, RENDER], capture_output=True, text=True)
    check("usage: no arguments exits 2", p.returncode == 2)

    # --- Headless Chrome: the page actually paints ---
    if os.path.exists(CHROME):
        shot = os.path.join(tmp, "shot.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1280,2400", "--virtual-time-budget=4000",
                        f"--screenshot={shot}", "file://" + out + "#static"],
                       capture_output=True, timeout=120)
        ok = os.path.exists(shot) and os.path.getsize(shot) > 50_000
        check("headless Chrome renders a non-trivial screenshot of the sample preview", ok,
              f"{os.path.getsize(shot) if os.path.exists(shot) else 'missing'}")
    else:
        print("SKIP: headless Chrome not installed, screenshot check skipped")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
