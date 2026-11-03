#!/usr/bin/env python3
"""
render_preview.py: turn a goalify brief and its condition into a one-page run preview.

The page is for the human, never for the evaluator. It shows what the run will do, what
proves it is done, the caps, the locked decisions, and the full `/goal` line with a copy
button. The inline `/goal` line goalify prints in the chat stays the required step; this
page is an optional view of the same thing.

It is also the brief lint: before writing anything it checks the brief and the condition,
and it fails loudly (exit 1, one line per problem) instead of rendering a broken plan.

Standard library only. The page is self-contained: inline CSS, inline JS, inline SVG,
system fonts, and no request to any host. The only link out is the GitHub repo.

Usage:
    python3 render_preview.py <brief.md> <condition-file> [--out <page.html>]

Prints the page's file:// URL on success. Exit 0 = written, 1 = lint failed, 2 = usage.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import condition_lint  # noqa: E402
import goal_state  # noqa: E402

REPO_URL = "https://github.com/Aboudjem/goalify"
SIZE_CEILING = 60_000  # bytes; the sample renders well under it


# --------------------------------------------------------------------------- helpers

def goalify_version():
    """The version in this skill's own SKILL.md frontmatter (the single source)."""
    skill = os.path.join(os.path.dirname(HERE), "SKILL.md")
    try:
        text = open(skill, encoding="utf-8").read()
    except OSError:
        return "unknown"
    m = re.search(r"^\s+version:\s*[\"']?(\d+\.\d+\.\d+)", text, re.MULTILINE)
    return m.group(1) if m else "unknown"


def esc(text):
    return html.escape(text or "", quote=True)


def inline(text):
    """Escape, then render the two bits of Markdown briefs lean on: `code` and **bold**."""
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    return out


def plain(text):
    """Markdown markers stripped, for SVG labels and short titles."""
    return re.sub(r"[`*]", "", text or "").strip()


def clip(text, n):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1].rstrip(" ,;:.") + "…"


def first_sentence(text, limit=260):
    text = " ".join((text or "").split())
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    return clip(s, limit)


def title_html(title):
    """The title with its closing words in the drifting gradient: the parenthetical if there is
    one, otherwise the last two words."""
    m = re.match(r"^(.*?)(\s*\([^()]+\))\s*$", title)
    if m and m.group(1).strip():
        head, tail = m.group(1), m.group(2)
    else:
        words = title.split()
        if len(words) < 3:
            return f'<span class="grad">{inline(title)}</span>'
        head, tail = " ".join(words[:-2]), " " + " ".join(words[-2:])
    return f'{inline(head)}<span class="grad">{inline(tail)}</span>'


def short_title(title, n=60):
    """A <title>-sized name: the parenthetical dropped first, then cut at a word boundary."""
    t = plain(re.sub(r"\s*\([^()]*\)\s*$", "", title)) or plain(title)
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"


def node_label(title):
    """A flow-node label: the trailing parenthetical goes, the phase list keeps the full title."""
    t = plain(re.sub(r"\s*\([^()]*\)\s*\.?$", "", title)) or plain(title)
    return t.rstrip(".")


def turn_cap(condition):
    m = re.search(r"\bstop\s+after\s+(\d[\d,]*)\s+turns?", condition or "", re.IGNORECASE)
    return m.group(1) if m else None


def condition_commands(condition):
    """Commands the condition names: the text after 'quotes', up to 'passing' / ',' / 'and'."""
    found = []
    for m in re.finditer(r"\bquotes?\s+(.+?)(?=\s+passing\b|,|\s+and\s+|\s+plus\s+|\.\s|$)",
                         condition or "", re.IGNORECASE):
        phrase = m.group(1).strip()
        phrase = re.sub(r"^(?:the\s+output\s+of\s+|output\s+of\s+)", "", phrase, flags=re.I)
        # Only phrases that read like a command: a space-separated tool call or a script path.
        if re.match(r"^[a-z0-9_.\/-]+(?:\s+[^\s]+)+$", phrase) or "/" in phrase:
            if not re.match(r"^(?:every|all|each|the|its|a|an)\b", phrase, re.I):
                found.append(phrase)
    return found


# --------------------------------------------------------------------------- brief lint

def lint_brief(brief, condition):
    """Return a list of (rule id, message). Empty means the brief and condition pass."""
    problems = []
    for name in brief["missing_sections"]:
        problems.append(("missing-section", f'the brief has no "## {name}" section'))
    own = brief["own_path"]
    if not own:
        problems.append(("brief-path-not-absolute",
                         "the brief does not state its own path (\"This file's own path: ...\")"))
    elif not own.startswith("/"):
        problems.append(("brief-path-not-absolute",
                         f"the brief's own path is not absolute: {own}"))
    if not brief["dod"]:
        problems.append(("dod-empty", "the Definition of done has no checkbox items"))
    for i, item in enumerate(brief["dod"], 1):
        if item["kind"] == "none":
            problems.append(("dod-no-command",
                             f"Definition-of-done item {i} names no backticked command: "
                             f"{clip(plain(item['text']), 90)}"))
    if condition is None or not condition.strip():
        problems.append(("condition-missing", "no condition text was supplied"))
        return problems
    for rule, ok, detail in condition_lint.lint(condition):
        if not ok:
            problems.append((f"condition-{rule}", detail))
    if own:
        home = os.path.expanduser("~")
        forms = {own}
        if own.startswith(home + "/"):
            forms.add("~" + own[len(home):])
        if not any(f in condition for f in forms):
            problems.append(("condition-missing-path",
                             f"the condition does not name the brief's path {own}"))
    dod_cmds = [c for item in brief["dod"] for c in item["commands"]]
    for cmd in condition_commands(condition):
        if not any(cmd in c for c in dod_cmds):
            problems.append(("condition-command-not-in-dod",
                             f'the condition names "{cmd}", which no Definition-of-done '
                             "item runs"))
    return problems


# --------------------------------------------------------------------------- page shell

CSS = r"""
:root{--bg:#07060f;--ink:#f1edff;--mute:#a59cc9;--dim:#8a82b6;--line:rgba(255,255,255,.10);
--glass:rgba(255,255,255,.045);--glass-hi:rgba(255,255,255,.18);
--purple:#9b6bff;--cyan:#2ee6ff;--pink:#ff3d9a;--yellow:#ffd23f;--green:#3dffa8;--red:#ff6b8b}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:radial-gradient(1200px 700px at 80% -10%,#2a1563 0%,transparent 60%),radial-gradient(900px 600px at -10% 20%,#0b3a52 0%,transparent 55%),var(--bg);
color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",system-ui,sans-serif;
letter-spacing:-.005em;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh}
code,.mono{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:.88em}
p code,li code,td code{background:rgba(255,255,255,.07);padding:1px 6px;border-radius:6px;word-break:break-word}
a{color:var(--cyan)}
#sky{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}
main{position:relative;z-index:1;max-width:1040px;margin:0 auto;padding:0 20px 80px}
section{margin-top:96px}
.eyebrow{font:600 12px/1 -apple-system,"SF Pro Text",system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--cyan);margin-bottom:14px;opacity:.9}
h2{font-size:clamp(26px,4vw,38px);line-height:1.1;letter-spacing:-.03em;font-weight:650;margin-bottom:12px}
.lede{color:var(--mute);max-width:660px}
.grad{background:linear-gradient(90deg,var(--purple),var(--pink),var(--yellow),var(--cyan),var(--purple));background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:drift 10s linear infinite}
@keyframes drift{to{background-position:300% 0}}
.glass{background:var(--glass);border:1px solid var(--line);-webkit-backdrop-filter:blur(22px) saturate(160%);backdrop-filter:blur(22px) saturate(160%);
box-shadow:inset 0 1px 0 var(--glass-hi),0 10px 40px -20px rgba(0,0,0,.6);border-radius:24px}
.rv{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.8,.2,1)}
.rv.in{opacity:1;transform:none}
.static .rv{opacity:1;transform:none;transition:none}
.hero{min-height:min(82vh,760px);display:flex;flex-direction:column;justify-content:center;padding-top:48px}
.badge{display:inline-flex;align-self:flex-start;align-items:center;gap:10px;padding:7px 14px;border-radius:999px;font:600 13px -apple-system,system-ui,sans-serif;margin-bottom:26px}
.badge i{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green)}
.hero h1{font-size:clamp(34px,6.4vw,72px);line-height:1.02;letter-spacing:-.045em;font-weight:700;max-width:940px;overflow-wrap:anywhere}
.hero h1.long{font-size:clamp(30px,4.6vw,56px);line-height:1.06}
.hero p{font-size:clamp(17px,2vw,20px);color:var(--mute);margin-top:22px;max-width:680px}
.pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.pill{padding:8px 14px;border-radius:999px;font-size:14px}
.pill b{color:var(--yellow)}
.cue{margin-top:56px;color:var(--dim);font-size:13px;animation:bob 2s infinite}
@keyframes bob{50%{transform:translateY(6px)}}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.band{padding:34px;position:relative;overflow:hidden;border-radius:28px;background:linear-gradient(135deg,rgba(155,107,255,.10),rgba(46,230,255,.06))}
.band:before{content:"";position:absolute;inset:-2px;background:conic-gradient(from var(--a,0deg),transparent 0 70%,var(--cyan),var(--pink),transparent 90%);animation:spin 6s linear infinite;z-index:0;opacity:.22;filter:blur(20px)}
@property --a{syntax:"<angle>";inherits:false;initial-value:0deg}
@keyframes spin{to{--a:360deg}}
.band>*{position:relative;z-index:1}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:26px}
.step{padding:16px;border-radius:18px}
.step .t{font:600 11px ui-monospace,Menlo,monospace;color:var(--yellow);letter-spacing:.1em}
.step h4{margin:6px 0 4px;font-size:17px;font-weight:650}
.step p{color:var(--mute);font-size:14px}
.runbar{margin-top:22px;height:8px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;position:relative}
.runbar span{position:absolute;inset:0;width:30%;background:linear-gradient(90deg,var(--purple),var(--cyan),var(--green));border-radius:99px;animation:run 5s ease-in-out infinite}
@keyframes run{0%{width:4%}80%,100%{width:100%}}
.runlbl{display:flex;justify-content:space-between;gap:10px;font:12px ui-monospace,Menlo,monospace;color:var(--dim);margin-top:8px}
.flow{margin-top:26px;padding:18px}
.flow svg{display:block;width:100%;height:auto}
.dash{stroke-dasharray:6 8;animation:dash 1.2s linear infinite}
@keyframes dash{to{stroke-dashoffset:-14}}
.phases{margin-top:18px;display:grid;gap:10px}
.phase{display:grid;grid-template-columns:44px 1fr;gap:14px;align-items:start;padding:14px 16px;border-radius:18px}
.phase .n{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font:600 14px ui-monospace,Menlo,monospace;background:rgba(155,107,255,.18);color:#d9c9ff}
.phase h4{font-size:16px;font-weight:650}
.phase p{color:var(--mute);font-size:14px;margin-top:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:26px;align-items:start}
.card{padding:22px;transition:transform .25s,border-color .25s,box-shadow .25s}
.card:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.22);box-shadow:inset 0 1px 0 var(--glass-hi),0 24px 60px -28px var(--c,var(--purple))}
.card h3{font-size:15px;font-weight:650;margin-bottom:8px;color:var(--c,var(--ink))}
.card p,.card li{color:var(--mute);font-size:15px}
.card ul{list-style:none;display:grid;gap:8px}
.card li{display:flex;gap:10px}
.card li:before{content:"";flex:none;width:6px;height:6px;margin-top:9px;border-radius:50%;background:var(--c,var(--purple))}
.big{font:700 34px/1 -apple-system,system-ui,sans-serif;letter-spacing:-.03em;color:var(--ink)}
.checks{margin-top:26px;display:grid;gap:10px}
.check{display:grid;grid-template-columns:28px 1fr;gap:14px;padding:16px 18px;border-radius:18px}
.check .ok{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;border:1.5px solid var(--green);color:var(--green);font-size:13px}
.check .txt{color:var(--ink);font-size:15px}
.cmds{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.cmd{font:12.5px ui-monospace,Menlo,monospace;padding:5px 10px;border-radius:10px;background:rgba(46,230,255,.08);border:1px solid rgba(46,230,255,.22);color:var(--cyan);overflow-wrap:anywhere}
.cmd.agent{background:rgba(255,210,63,.08);border-color:rgba(255,210,63,.25);color:var(--yellow)}
.arrow{color:var(--dim);font-size:13px;margin-right:2px}
.launch{margin-top:26px;padding:26px}
.tabs{display:flex;gap:6px;margin-bottom:18px;padding:4px;border-radius:999px;background:rgba(255,255,255,.05);width:max-content;max-width:100%}
.tab{border:0;cursor:pointer;padding:8px 16px;border-radius:999px;background:transparent;color:var(--mute);font:600 14px -apple-system,system-ui,sans-serif}
.tab[aria-selected=true]{background:rgba(255,255,255,.92);color:#0a0818}
.panel[hidden]{display:none}
.stepno{font:600 12px ui-monospace,Menlo,monospace;color:var(--dim);margin:16px 0 8px;letter-spacing:.08em}
.line{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;border-radius:16px;background:rgba(10,8,24,.55);border:1px solid rgba(155,107,255,.35)}
.line code{flex:1;font-size:13.5px;line-height:1.6;white-space:pre-wrap;word-break:break-word;color:var(--ink)}
.btn{flex:none;border:0;cursor:pointer;font:600 13px -apple-system,system-ui,sans-serif;padding:9px 16px;border-radius:999px;background:rgba(255,255,255,.92);color:#0a0818;transition:transform .15s,background .15s}
.btn:hover{background:#fff}.btn:active{transform:scale(.95)}
.note{color:var(--dim);font-size:13.5px;margin-top:12px}
footer{margin-top:110px;text-align:center;color:var(--dim);font-size:14px}
footer a{display:inline-flex;gap:8px;align-items:center;color:var(--ink);text-decoration:none;padding:10px 18px;border-radius:999px;margin-top:12px;transition:border-color .2s,box-shadow .2s}
footer a:hover{border-color:var(--purple);box-shadow:0 0 30px #9b6bff66}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;color:var(--dim);font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:10px 12px}
td{padding:12px;border-top:1px solid var(--line);vertical-align:top;color:var(--mute)}
td.k{color:var(--ink)}
.st{display:inline-block;padding:3px 10px;border-radius:999px;font:600 12px ui-monospace,Menlo,monospace}
.st.pass,.st.done{background:rgba(61,255,168,.12);color:var(--green)}
.st.fail,.st.blocked{background:rgba(255,107,139,.14);color:var(--red)}
.st.skip,.st.orphan{background:rgba(255,255,255,.08);color:var(--mute)}
.st.open{background:rgba(46,230,255,.12);color:var(--cyan)}
pre.out{margin-top:10px;padding:12px 14px;border-radius:12px;background:rgba(0,0,0,.35);font:12px/1.5 ui-monospace,Menlo,monospace;color:var(--mute);white-space:pre-wrap;word-break:break-word;max-height:220px;overflow:auto}
.verdict{display:inline-flex;align-items:center;gap:12px;padding:12px 22px;border-radius:999px;font:700 clamp(18px,3vw,26px)/1 -apple-system,system-ui,sans-serif;letter-spacing:.04em;margin-top:6px}
.verdict.ok{color:var(--green);background:rgba(61,255,168,.10);border:1px solid rgba(61,255,168,.4);box-shadow:0 0 50px -10px rgba(61,255,168,.5)}
.verdict.no{color:var(--red);background:rgba(255,107,139,.10);border:1px solid rgba(255,107,139,.4)}
.verdict.un{color:var(--yellow);background:rgba(255,210,63,.08);border:1px solid rgba(255,210,63,.35)}
.scroll-x{overflow-x:auto}
@media (max-width:760px){.steps{grid-template-columns:1fr 1fr}.band,.launch{padding:22px}section{margin-top:72px}}
.flow .v{display:none}
@media (max-width:600px){.flow .h{display:none}.flow .v{display:block;max-width:340px;margin:0 auto}}
@media (max-width:460px){.steps{grid-template-columns:1fr}.line{flex-direction:column}.btn{align-self:flex-end}}
@media (prefers-reduced-motion:reduce){*,*:before{animation:none!important;transition:none!important}.rv{opacity:1;transform:none}}
"""

# The approved canvas starfield: depth layers, soft twinkle, flares on the brightest stars and
# an occasional shooting star with a gradient tail. One still frame under reduced motion.
STARFIELD_JS = r"""
(function(){
  if(location.hash==='#static')document.documentElement.classList.add('static');
  var c=document.getElementById('sky'),x=c.getContext('2d'),W,H,D=Math.min(window.devicePixelRatio||1,2),stars=[],shots=[],still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var tints=['255,255,255','200,220,255','190,170,255','255,220,240','255,240,200'];
  function size(){W=innerWidth;H=innerHeight;c.width=W*D;c.height=H*D;x.setTransform(D,0,0,D,0,0);
    stars=[];var n=Math.round(W*H/5200);
    for(var i=0;i<n;i++){var z=Math.random();stars.push({x:Math.random()*W,y:Math.random()*H,z:z,r:z<.9?.35+z*.7:1+Math.random()*.8,
      b:.25+Math.random()*.55,ph:Math.random()*6.28,sp:.4+Math.random()*1.4,t:tints[Math.random()*tints.length|0],flare:z>.97});}
    if(still)frame(0);}
  function star(s,a){x.fillStyle='rgba('+s.t+','+a+')';x.beginPath();x.arc(s.x,s.y,s.r,0,6.283);x.fill();
    if(s.r>1){var g=x.createRadialGradient(s.x,s.y,0,s.x,s.y,s.r*5);g.addColorStop(0,'rgba('+s.t+','+a*.35+')');g.addColorStop(1,'rgba('+s.t+',0)');x.fillStyle=g;x.beginPath();x.arc(s.x,s.y,s.r*5,0,6.283);x.fill();}
    if(s.flare){x.strokeStyle='rgba('+s.t+','+a*.45+')';x.lineWidth=.6;var L=s.r*7*a;x.beginPath();x.moveTo(s.x-L,s.y);x.lineTo(s.x+L,s.y);x.moveTo(s.x,s.y-L);x.lineTo(s.x,s.y+L);x.stroke();}}
  var last=0,next=4000;
  function frame(t){x.clearRect(0,0,W,H);var dt=Math.min(t-last,50);last=t;
    for(var i=0;i<stars.length;i++){var s=stars[i];
      s.y-=s.z*s.z*.012*dt;s.x+=s.z*s.z*.004*dt;if(s.y<-4){s.y=H+4;s.x=Math.random()*W}if(s.x>W+4)s.x=-4;
      var a=s.b*(.55+.45*Math.sin(t*.001*s.sp+s.ph));star(s,a);}
    next-=dt;if(!still&&next<0){next=5000+Math.random()*7000;var ang=.35+Math.random()*.25;shots.push({x:Math.random()*W*.7,y:Math.random()*H*.35,vx:Math.cos(ang)*.9,vy:Math.sin(ang)*.9,life:0,max:900});}
    for(var j=shots.length-1;j>=0;j--){var h=shots[j];h.life+=dt;h.x+=h.vx*dt;h.y+=h.vy*dt;var k=h.life/h.max,al=Math.sin(Math.PI*Math.min(k,1));
      var tx=h.x-h.vx*140,ty=h.y-h.vy*140,g=x.createLinearGradient(h.x,h.y,tx,ty);g.addColorStop(0,'rgba(255,255,255,'+al+')');g.addColorStop(.3,'rgba(46,230,255,'+al*.5+')');g.addColorStop(1,'rgba(155,107,255,0)');
      x.strokeStyle=g;x.lineWidth=1.4;x.lineCap='round';x.beginPath();x.moveTo(h.x,h.y);x.lineTo(tx,ty);x.stroke();if(k>=1)shots.splice(j,1);}
    if(!still)requestAnimationFrame(frame);}
  size();addEventListener('resize',size);
  if(!still)requestAnimationFrame(function(t){last=t;frame(t)});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.08});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});}else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')})}
  document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    var t=document.getElementById(b.getAttribute('data-copy')).textContent,lbl=b.textContent;
    function ok(){b.textContent='Copied';var l=document.getElementById('live');if(l)l.textContent='Copied to the clipboard';setTimeout(function(){b.textContent=lbl},1600)}
    function fb(){var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove();ok()}
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,fb)}else fb();});});
  var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
  function pick(tb){tabs.forEach(function(o){var on=o===tb;o.setAttribute('aria-selected',on?'true':'false');o.tabIndex=on?0:-1;document.getElementById(o.getAttribute('aria-controls')).hidden=!on;});tb.focus();}
  tabs.forEach(function(tb,i){tb.addEventListener('click',function(){pick(tb)});tb.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();pick(tabs[(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length]);}});});
})();
"""


def page(title, body, description=""):
    """A whole self-contained HTML document around `body` (already escaped HTML)."""
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<meta name=\"color-scheme\" content=\"dark\">\n"
        f"<title>{esc(title)}</title>\n"
        + (f"<meta name=\"description\" content=\"{esc(description)}\">\n" if description else "")
        + f"<style>{CSS}</style>\n</head>\n<body>\n"
        "<canvas id=\"sky\" aria-hidden=\"true\"></canvas>\n<div id=\"live\" class=\"sr\" aria-live=\"polite\"></div>\n<main>\n"
        + body
        + footer()
        + "</main>\n<script>" + STARFIELD_JS + "</script>\n</body>\n</html>\n"
    )


def footer():
    return (
        "<footer class=\"rv\">\n<p>Made by goalify " + esc(goalify_version())
        + ". Nothing on this page phones home.</p>\n"
        f"<a class=\"glass\" href=\"{REPO_URL}\">"
        "<svg width=\"18\" height=\"18\" viewBox=\"0 0 16 16\" aria-hidden=\"true\" fill=\"currentColor\">"
        "<path d=\"M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01"
        "-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 "
        "1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82"
        "-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 "
        "2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73"
        ".54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z\"/></svg>"
        "Aboudjem/goalify on GitHub</a>\n</footer>\n"
    )


def write_page(path, document):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(document)
    return os.path.abspath(path)


# --------------------------------------------------------------------------- the flow SVG

def _wrap(text, width, max_lines=3):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = clip(lines[-1] + " …", width)
    return [clip(ln, width) for ln in lines]


def _flow(nodes, per, bw, gx, gy, label_width, ident):
    """One snake-shaped SVG: `per` nodes a row, odd rows run right to left, arrows show the way."""
    pad = 14
    wrapped = [_wrap(title, label_width) for _, title in nodes]
    bh = 96 if any(len(w) == 3 for w in wrapped) else 82
    rows = (len(nodes) + per - 1) // per
    width = pad * 2 + per * bw + (per - 1) * gx
    height = pad * 2 + rows * bh + (rows - 1) * gy
    pos = []
    for i in range(len(nodes)):
        r, c = divmod(i, per)
        if r % 2 == 1:
            c = per - 1 - c
        pos.append((pad + c * (bw + gx), pad + r * (bh + gy)))
    gap = 7
    paths = []
    for i in range(len(nodes) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            if x2 > x1:
                paths.append(f"M{x1 + bw + gap} {y1 + bh / 2} H{x2 - gap}")
            else:
                paths.append(f"M{x1 - gap} {y1 + bh / 2} H{x2 + bw + gap}")
        else:
            cx = x1 + bw / 2
            paths.append(f"M{cx} {y1 + bh + gap} V{y2 - gap}")
    out = [
        f'<svg class="{ident}" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="The run, phase by phase">',
        f'<defs><linearGradient id="fg-{ident}" gradientUnits="userSpaceOnUse" x1="0" y1="0" '
        f'x2="{width}" y2="{height}"><stop offset="0" stop-color="#9b6bff"/>'
        '<stop offset="1" stop-color="#2ee6ff"/></linearGradient>'
        f'<marker id="ah-{ident}" viewBox="0 0 8 8" refX="6" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
        'markerHeight="9" orient="auto"><path d="M0 0L8 4L0 8z" fill="#2ee6ff"/></marker></defs>',
        f'<g fill="none" stroke="url(#fg-{ident})" stroke-width="2.2" stroke-linecap="round" '
        f'class="dash">'
        + "".join(f'<path d="{d}" marker-end="url(#ah-{ident})"/>' for d in paths) + "</g>",
        '<g font-family="-apple-system,system-ui,sans-serif">',
    ]
    for i, ((num, _), lines, (x, y)) in enumerate(zip(nodes, wrapped, pos)):
        last = i == len(nodes) - 1
        stroke = "#3dffa8" if last else "rgba(255,255,255,.16)"
        fill = "rgba(61,255,168,.08)" if last else "rgba(255,255,255,.05)"
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="20" fill="{fill}" '
                   f'stroke="{stroke}"/>')
        out.append(f'<circle cx="{x + 26}" cy="{y + bh / 2}" r="13" '
                   f'fill="{"#3dffa833" if last else "rgba(155,107,255,.22)"}"/>')
        out.append(f'<text x="{x + 26}" y="{y + bh / 2 + 4.5}" text-anchor="middle" font-size="12" '
                   f'font-weight="700" fill="{"#3dffa8" if last else "#d9c9ff"}">{esc(num)}</text>')
        y0 = y + bh / 2 - (len(lines) - 1) * 8.5 + 4.5
        for k, ln in enumerate(lines):
            out.append(f'<text x="{x + 50}" y="{y0 + k * 17}" font-size="13.5" font-weight="600" '
                       f'fill="#f1edff">{esc(ln)}</text>')
    out.append("</g></svg>")
    return "".join(out)


def flow_svg(phases):
    """The brief's phases as a flow, ending in a proof node: a snake for wide screens and a
    single column for phones. CSS shows one of the two."""
    nodes = [(str(p["num"]), node_label(p["title"])) for p in phases] + [("✓", "Proven, then archived")]
    rows_needed = (len(nodes) + 3) // 4
    per = (len(nodes) + rows_needed - 1) // rows_needed  # balance the rows: 6 nodes = 3 + 3
    wide = _flow(nodes, per, 196, 44, 46, 19, "h")
    tall = _flow(nodes, 1, 300, 0, 30, 30, "v")
    return wide + tall


# --------------------------------------------------------------------------- preview body

def render_preview(brief, condition):
    cap = turn_cap(condition)
    goal_line = "/goal " + condition
    headless = f'claude -p "/goal {condition}" --permission-mode auto'
    own = brief["own_path"]
    objective = first_sentence(brief["objective"]) or brief["title"]
    n_checks = len(brief["dod"])
    n_cmds = sum(len(i["commands"]) for i in brief["dod"])

    pills = [
        f'<span class="pill glass"><b>{len(brief["phases"])}</b> phases</span>',
        f'<span class="pill glass"><b>{n_checks}</b> checks to pass</span>',
        f'<span class="pill glass"><b>{n_cmds}</b> commands quoted at the end</span>',
    ]
    if cap:
        pills.append(f'<span class="pill glass">turn cap <b>{esc(cap)}</b></span>')
    if brief["decisions"]:
        pills.append(f'<span class="pill glass"><b>{len(brief["decisions"])}</b> decisions locked</span>')

    hero = (
        '<header class="hero">\n'
        f'<span class="badge glass rv"><i></i>Run preview · ready to launch</span>\n'
        f'<h1 class="rv{" long" if len(brief["title"]) > 56 else ""}">{title_html(brief["title"])}</h1>\n'
        f'<p class="rv">{inline(objective)}</p>\n'
        f'<div class="pills rv">{"".join(pills)}</div>\n'
        '<div class="cue rv" aria-hidden="true">↓ scroll for the plan</div>\n'
        "</header>\n"
    )

    band = (
        '<section class="rv"><div class="band glass">\n'
        '<div class="eyebrow">Why you can walk away</div>\n'
        '<h2>Every question is already answered. <span class="grad">Now it just works.</span></h2>\n'
        '<p class="lede">The research, your decisions and the finish line are all in the brief. '
        "After <code>/clear</code>, a fresh session works through it without stopping to ask you "
        "anything. Hours if it takes hours. Days if it takes days. It only stops when the proof "
        "is on screen, or when it hits the turn cap.</p>\n"
        '<div class="steps">'
        '<div class="step glass"><div class="t">DONE · BEFORE</div><h4>Homework</h4>'
        "<p>Can it work? Docs read, real test commands found.</p></div>"
        '<div class="step glass"><div class="t">DONE · BEFORE</div><h4>Questions, once</h4>'
        "<p>Your few real choices are locked below.</p></div>"
        '<div class="step glass"><div class="t">YOU · /CLEAR</div><h4>Fresh brain</h4>'
        "<p>A clean session spends all its context on the job.</p></div>"
        '<div class="step glass"><div class="t">RUN · NON-STOP</div><h4>Work, check, repeat</h4>'
        "<p>It ends on quoted proof, not on a promise.</p></div>"
        "</div>\n"
        '<div class="runbar"><span></span></div>\n'
        f'<div class="runlbl"><span>/goal started</span><span>{n_checks} checks · proven</span></div>\n'
        "</div></section>\n"
    )

    phase_rows = "".join(
        f'<div class="phase glass"><span class="n">{p["num"]}</span><div>'
        f'<h4>{inline(clip(p["title"], 90))}</h4>'
        + (f'<p>{inline(clip(p["text"], 240))}</p>' if p["text"] else "")
        + "</div></div>"
        for p in brief["phases"]
    )
    plan = (
        '<section class="rv">\n<div class="eyebrow">The plan</div>\n'
        "<h2>What the run will do</h2>\n"
        '<p class="lede">Straight from the brief, in order. Independent work fans out to parallel '
        "agents; builds, tests and git stay one at a time.</p>\n"
        f'<div class="flow glass">{flow_svg(brief["phases"])}</div>\n'
        f'<div class="phases">{phase_rows}</div>\n</section>\n'
    )

    deliverables = [i["text"] for i in brief["checklist"]
                    if not re.search(r"safe to archive|re-?verified current state", i["text"], re.I)]
    cards = []
    if deliverables:
        cards.append(
            '<div class="card glass" style="--c:var(--cyan)"><h3>What you get</h3><ul>'
            + "".join(f"<li><span>{inline(clip(d, 160))}</span></li>" for d in deliverables[:12])
            + "</ul></div>")
    caps = [f'<div class="big">{esc(cap)}</div><p>turns at most. A cap is a stopping rule, '
            "not a finish line: near it, the run wraps up cleanly and says what is left.</p>"
            if cap else "<p>No turn cap found in the condition.</p>"]
    caps.append('<p style="margin-top:12px">No cost estimate here on purpose. goalify never '
                "guesses a dollar or token figure; the caps are the honest control.</p>")
    cards.append('<div class="card glass" style="--c:var(--yellow)"><h3>Caps</h3>'
                 + "".join(caps) + "</div>")
    if brief["decisions"]:
        cards.append(
            '<div class="card glass" style="--c:var(--pink)"><h3>Locked decisions</h3><ul>'
            + "".join(f"<li><span>{inline(clip(d, 200))}</span></li>" for d in brief["decisions"][:10])
            + "</ul></div>")
    overview = ('<section class="rv">\n<div class="eyebrow">At a glance</div>\n'
                "<h2>Deliverables, caps, and what is already decided</h2>\n"
                f'<div class="grid">{"".join(cards)}</div>\n</section>\n')

    rows = []
    for item in brief["dod"]:
        text = item["text"]
        if item["commands"]:
            chips = "".join(f'<span class="cmd">{esc(c)}</span>' for c in item["commands"])
        elif item["kind"] == "agent":
            chips = '<span class="cmd agent">checked by a separate agent</span>'
        else:
            chips = ""
        rows.append(
            '<div class="check glass"><span class="ok" aria-hidden="true">✓</span><div>'
            f'<div class="txt">{inline(clip(display_text(text, item["commands"]), 320))}</div>'
            + (f'<div class="cmds"><span class="arrow">proved by</span>{chips}</div>' if chips else "")
            + "</div></div>")
    done = ('<section class="rv">\n<div class="eyebrow">Done when</div>\n'
            "<h2>The finish line, check by check</h2>\n"
            '<p class="lede">The run is only done when its last turn reruns these and quotes the '
            "output. The evaluator behind <code>/goal</code> reads that transcript, nothing else.</p>\n"
            f'<div class="checks">{"".join(rows)}</div>\n</section>\n')

    codex_obj = "/goal " + condition
    codex_pipe = f"cat {own} | codex exec -"
    launch = (
        '<section class="rv" id="launch">\n<div class="eyebrow">Launch it</div>\n'
        "<h2>Two steps. Then walk away.</h2>\n"
        f'<p class="lede">The condition is {len(condition):,} characters, under the 4,000 limit. '
        "It names the brief's path, so the run finds the plan without <code>/goal</code> ever "
        "getting a bare path.</p>\n"
        '<div class="launch glass">\n'
        '<div class="tabs" role="tablist">'
        '<button class="tab" role="tab" aria-selected="true" aria-controls="p-cc" id="t-cc">Claude Code</button>'
        '<button class="tab" role="tab" aria-selected="false" aria-controls="p-cx" id="t-cx" tabindex="-1">Codex</button>'
        "</div>\n"
        '<div class="panel" id="p-cc" role="tabpanel" aria-labelledby="t-cc">'
        '<div class="stepno">STEP 1</div><div class="line"><code>/clear</code></div>'
        '<div class="stepno">STEP 2 · PASTE THIS WHOLE LINE</div>'
        f'<div class="line"><code id="goal-line">{esc(goal_line)}</code>'
        '<button class="btn" type="button" data-copy="goal-line">Copy</button></div>'
        '<div class="stepno">OR HEADLESS</div>'
        f'<div class="line"><code id="headless-line">{esc(headless)}</code>'
        '<button class="btn" type="button" data-copy="headless-line">Copy</button></div>'
        '<p class="note">Unattended? Make sure auto mode is on (the default in current Claude Code). '
        "Type <code>/goal</code> on its own any time to see how the run is going.</p>"
        "</div>\n"
        '<div class="panel" id="p-cx" role="tabpanel" aria-labelledby="t-cx" hidden>'
        '<div class="stepno">CODEX INTERACTIVE</div>'
        f'<div class="line"><code id="codex-line">{esc(codex_obj)}</code>'
        '<button class="btn" type="button" data-copy="codex-line">Copy</button></div>'
        '<div class="stepno">CODEX HEADLESS (PIPES THE BRIEF)</div>'
        f'<div class="line"><code id="codex-pipe">{esc(codex_pipe)}</code>'
        '<button class="btn" type="button" data-copy="codex-pipe">Copy</button></div>'
        '<p class="note">Codex treats the objective as data, so only the Definition of done '
        "binds there; the process rules in the brief may not.</p>"
        "</div>\n</div>\n"
        '<p class="note">A <code>/goal</code> run that stopped is not proof by itself. To check '
        "later, run <code>/goalify verify</code> on this brief.</p>\n"
        "</section>\n"
    )

    body = hero + band + plan + overview + done + launch
    return page(f"{short_title(brief['title'])} · goalify run preview", body,
                "What this /goal run will do, what proves it is done, and the line to launch it.")


def display_text(text, commands):
    """The criterion without its 'verified by `cmd`' tail when the chips below already show it."""
    if not commands:
        return text
    cut = re.search(r"\s*[—–-]*\s*,?\s*verified by\b", text, re.IGNORECASE)
    if cut and all(c in text[cut.start():] for c in commands):
        head = text[:cut.start()].rstrip(" ,;:—–-")
        if head:
            return head + "."
    return text


def preview_path_for(brief_path):
    stem = os.path.splitext(os.path.abspath(brief_path))[0]
    return stem + ".html"


# --------------------------------------------------------------------------- status index

def write_status_index(goal_dir, rows):
    """`/goalify status --html`: .goal/index.html with one row per brief."""
    trs = []
    for r in rows:
        cls = {"OPEN": "open", "BLOCKED": "blocked", "DONE": "done"}.get(r["state"], "orphan")
        links = []
        if r["path"]:
            prev = preview_path_for(r["path"])
            if os.path.exists(prev):
                links.append(f'<a href="{esc(os.path.relpath(prev, goal_dir))}">preview</a>')
            gdir = goal_state.goal_dir_of(r["path"])
            for n in sorted(os.listdir(gdir)):
                if n.startswith(f"RECEIPT-{r['slug']}-") and n.endswith(".html"):
                    links.append(f'<a href="{esc(os.path.relpath(os.path.join(gdir, n), goal_dir))}">'
                                 "receipt</a>")
        ticks = f"{r['ticks'][0]}/{r['ticks'][1]}" if r["path"] else "-"
        resume = ""
        if r["state"] in ("OPEN", "BLOCKED") and r["condition"]:
            ident = "c-" + re.sub(r"[^a-z0-9-]", "-", r["slug"].lower())
            resume = (f'<div class="line" style="margin-top:10px"><code id="{ident}">'
                      f'{esc("/goal " + r["condition"])}</code>'
                      f'<button class="btn" type="button" data-copy="{ident}">Copy</button></div>')
        trs.append(
            f'<tr><td class="k"><b>{esc(r["slug"])}</b><br>{inline(clip(r["title"], 120))}{resume}</td>'
            f'<td><span class="st {cls}">{esc(r["state"])}</span></td>'
            f'<td class="mono">{esc(ticks)}</td><td class="mono">{esc(r["age"])}</td>'
            f'<td>{" · ".join(links) or "-"}</td></tr>')
    body = (
        '<header class="hero" style="min-height:46vh">\n'
        '<span class="badge glass rv"><i></i>goalify status</span>\n'
        '<h1 class="rv">Every run in <span class="grad">.goal/</span></h1>\n'
        '<p class="rv">Open runs come with their full <code>/goal</code> line, so resuming is a '
        "paste. This page is read-only and never launches anything.</p>\n</header>\n"
        '<section class="rv"><div class="glass scroll-x" style="padding:8px 6px">'
        "<table><thead><tr><th>Brief</th><th>State</th><th>Ticks</th><th>Age</th><th>Pages</th>"
        f"</tr></thead><tbody>{''.join(trs)}</tbody></table></div></section>\n"
    )
    return write_page(os.path.join(goal_dir, "index.html"),
                      page("goalify status", body, "Every goalify brief in this folder."))


# --------------------------------------------------------------------------- CLI

def main(argv):
    args = argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out")
        if i + 1 >= len(args):
            print("usage: render_preview.py <brief.md> <condition-file> [--out <page.html>]")
            return 2
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    if len(args) != 2:
        print("usage: render_preview.py <brief.md> <condition-file> [--out <page.html>]")
        return 2
    brief_path, cond_path = args
    for p in (brief_path, cond_path):
        if not os.path.isfile(p):
            print(f"no such file: {p}")
            return 2
    brief = goal_state.parse_brief(brief_path)
    condition = goal_state.read_condition(cond_path)
    problems = lint_brief(brief, condition)
    if problems:
        print(f"BRIEF LINT FAILED: {len(problems)} problem(s), no preview written.")
        for rule, msg in problems:
            print(f"FAIL: {rule}  ({msg})")
        return 1
    document = render_preview(brief, condition)
    path = write_page(out or preview_path_for(brief_path), document)
    print("file://" + path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
