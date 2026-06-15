import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { C, FONT_UI, FONT_MONO } from "./theme";

/* ============================================================ shared helpers */
const Bg: React.FC<{ children?: React.ReactNode; flat?: boolean }> = ({ children, flat }) => (
  <AbsoluteFill
    style={{
      background: flat
        ? C.bg1
        : `radial-gradient(120% 120% at 50% 16%, ${C.bg0} 0%, ${C.bg1} 70%, #06090d 100%)`,
    }}
  >
    <AbsoluteFill
      style={{
        backgroundImage: `radial-gradient(circle at 1px 1px, #1B2230 1.3px, transparent 0)`,
        backgroundSize: "44px 44px",
        opacity: 0.35,
      }}
    />
    {children}
  </AbsoluteFill>
);

const Fade: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 7, dur - 7, dur], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const blink = (f: number, p = 30) => (f % p < p / 2 ? 1 : 0);
const typed = (t: string, f: number, start: number, cpf = 0.85) => t.slice(0, Math.max(0, Math.floor((f - start) * cpf)));
const appear = (f: number, fps: number, delay: number, d = 14) =>
  spring({ frame: f - delay, fps, config: { damping: 200 }, durationInFrames: d });

const Caret: React.FC<{ color?: string; h?: number }> = ({ color = C.clay, h = 40 }) => {
  const f = useCurrentFrame();
  return <span style={{ display: "inline-block", width: h * 0.5, height: h, marginLeft: 6, marginBottom: -h * 0.12, background: color, opacity: blink(f), borderRadius: 3 }} />;
};

const Check: React.FC<{ size?: number; color?: string }> = ({ size = 28, color = C.green2 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path d="M5 13l4 4L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Caption: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div style={{ position: "absolute", bottom: 90, left: 0, right: 0, textAlign: "center", transform: `translateY(${interpolate(s, [0, 1], [22, 0])}px)`, opacity: s, padding: "0 130px" }}>
      <span style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 60, letterSpacing: -1, color, textShadow: "0 2px 28px rgba(0,0,0,0.65)" }}>{children}</span>
    </div>
  );
};

const Caption2: React.FC<{ main: string; sub: string; color?: string }> = ({ main, sub, color = C.text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div style={{ position: "absolute", bottom: 74, left: 0, right: 0, textAlign: "center", transform: `translateY(${interpolate(s, [0, 1], [22, 0])}px)`, opacity: s, padding: "0 120px" }}>
      <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 56, letterSpacing: -1, color, textShadow: "0 2px 28px rgba(0,0,0,0.65)" }}>{main}</div>
      <div style={{ fontFamily: FONT_MONO, fontSize: 30, color: C.textDim, marginTop: 10 }}>{sub}</div>
    </div>
  );
};

const Eyebrow: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.clay }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 13 });
  const grow = spring({ frame: f - 2, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div style={{ position: "absolute", top: 116, left: 0, right: 0, textAlign: "center", opacity: s, transform: `translateY(${interpolate(s, [0, 1], [-16, 0])}px)` }}>
      <span style={{ display: "inline-flex", alignItems: "center", gap: 18, fontFamily: FONT_UI, fontWeight: 800, fontSize: 31, letterSpacing: 6, textTransform: "uppercase", color, textShadow: `0 0 30px ${color}55` }}>
        <span style={{ width: 50 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
        {children}
        <span style={{ width: 50 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
      </span>
    </div>
  );
};

const Window: React.FC<{ children: React.ReactNode; title?: string; w?: number; accent?: string; style?: React.CSSProperties }> = ({ children, title = "claude code", w = 1180, accent, style }) => (
  <div style={{ width: w, borderRadius: 18, background: C.card, border: `1px solid ${accent ?? C.line}`, boxShadow: `0 40px 120px rgba(0,0,0,0.55)${accent ? `, 0 0 0 1px ${accent}33` : ""}`, overflow: "hidden", ...style }}>
    <div style={{ height: 50, display: "flex", alignItems: "center", gap: 9, padding: "0 22px", background: "#0C1117", borderBottom: `1px solid ${C.line}` }}>
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotRed }} />
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotYellow }} />
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotGreen }} />
      <span style={{ marginLeft: 16, fontFamily: FONT_MONO, fontSize: 21, color: C.textDim }}>{title}</span>
    </div>
    <div style={{ padding: "30px 38px", fontFamily: FONT_MONO }}>{children}</div>
  </div>
);

const AgentCard: React.FC<{ label: string; cx: number; cy: number; s: number; doneAt?: number; f: number; color?: string; w?: number }> = ({ label, cx, cy, s, doneAt, f, color = C.clay, w = 320 }) => {
  const done = doneAt != null && f >= doneAt;
  const pulse = interpolate(Math.sin(f / 5), [-1, 1], [0.5, 1]);
  return (
    <div style={{ position: "absolute", left: cx - w / 2, top: cy - 38, width: w, height: 76, transform: `scale(${s})`, opacity: s, display: "flex", alignItems: "center", gap: 16, padding: "0 22px", borderRadius: 14, background: "#0E141B", border: `1px solid ${done ? C.badgeBorder : C.line}`, fontFamily: FONT_MONO, fontSize: 24, color: C.text, boxShadow: done ? `0 0 24px ${C.green3}33` : "none" }}>
      {done ? <Check size={24} color={C.green2} /> : <span style={{ width: 13, height: 13, borderRadius: 99, background: color, opacity: pulse }} />}
      <span style={{ whiteSpace: "nowrap" }}>{label}</span>
    </div>
  );
};
const center: React.CSSProperties = { alignItems: "center", justifyContent: "center" };

/* ============================ 1 — HOOK: a vague goal gives a bad result */
const CYCLE = ["migrate the database", "upgrade to the latest version", "add tests to the whole app"];
const B1: React.FC = () => {
  const f = useCurrentFrame();
  const settled = f >= 48;
  const promptText = settled ? typed("add user login and signup", f, 48, 0.95) : CYCLE[Math.min(CYCLE.length - 1, Math.floor(f / 16))];
  const fail = f >= 72;
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code" w={1180}>
          <div style={{ fontSize: 33, color: C.text, height: 52 }}>
            <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
            {promptText}
            {f < 48 ? <Caret h={32} /> : settled && f < 70 && <Caret h={32} />}
          </div>
          <div style={{ marginTop: 20, height: 100 }}>
            {fail &&
              ["built the wrong thing", "left half of it undone"].map((l, i) => (
                <div key={l} style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 28, color: C.dotRed, lineHeight: "46px", opacity: appear(f, 30, 72 + i * 6, 9) }}>
                  <span style={{ width: 24, textAlign: "center" }}>✗</span> {l}
                </div>
              ))}
          </div>
        </Window>
      </AbsoluteFill>
      <Caption>A big task is only as good as its goal.</Caption>
    </Bg>
  );
};

/* ============================ 2 — goalify writes that goal for you */
const B2: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cmd = "/goalify add user login and signup";
  const n = typed(cmd, f, 6, 0.95);
  const has = n.startsWith("/goalify");
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goalify" w={1180}>
          <div style={{ fontSize: 34, color: C.text, height: 54, display: "flex", alignItems: "center" }}>
            <span style={{ color: C.textDim, marginRight: 12 }}>{">"}</span>
            <span style={{ color: C.clayHi, textShadow: `0 0 20px ${C.clay}99` }}>{has ? "/goalify" : n}</span>
            <span>{has ? n.slice(8) : ""}</span>
            {f < 46 && <Caret h={34} />}
          </div>
          {f >= 50 && (
            <div style={{ marginTop: 18, fontSize: 25, color: C.textDim, opacity: appear(f, fps, 50, 10) }}>
              <Check size={22} color={C.green2} /> turning it into a real, doable goal…
            </div>
          )}
        </Window>
      </AbsoluteFill>
      <Eyebrow>A free Claude Code skill</Eyebrow>
      <Caption2 main="goalify writes that goal for you." sub="even if you're not sure how." color={C.clayHi} />
    </Bg>
  );
};

/* ============================ 3 — it studies your project (scouts) */
const SCOUTS = ["reads your code", "reads the docs", "tries each step", "challenges the plan"];
const B3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cx = [400, 740, 1180, 1520];
  return (
    <Bg>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {cx.map((x, i) => {
          const a = appear(f, fps, 12 + i * 5, 10);
          return <line key={i} x1={960} y1={306} x2={x} y2={482} stroke={C.clay} strokeWidth={2} strokeOpacity={a * 0.5} strokeDasharray="6 8" />;
        })}
      </svg>
      <div style={{ position: "absolute", left: 810, top: 250, width: 300, height: 64, transform: `scale(${appear(f, fps, 0, 12)})`, display: "flex", alignItems: "center", justifyContent: "center", borderRadius: 14, background: C.badgeFill, border: `1.5px solid ${C.clay}`, fontFamily: FONT_MONO, fontSize: 26, color: C.clayHi, fontWeight: 700 }}>
        scouts
      </div>
      {cx.map((x, i) => (
        <AgentCard key={i} label={SCOUTS[i]} cx={x} cy={520} s={appear(f, fps, 16 + i * 6, 12)} doneAt={56 + i * 5} f={f} w={300} />
      ))}
      <Eyebrow>It does the homework</Eyebrow>
      <Caption>First, it studies your project.</Caption>
    </Bg>
  );
};

/* ============================ 4 — it asks the questions that matter */
const B4: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pick = f >= 30;
  const opts = ["JSON web tokens (JWT)", "server sessions"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 26 }}>
        <div style={{ fontFamily: FONT_UI, fontSize: 34, color: C.textDim }}>How should login stay signed in?</div>
        {opts.map((o, i) => {
          const sel = i === 0 && pick;
          const a = appear(f, fps, 6 + i * 8, 12);
          return (
            <div key={o} style={{ width: 880, transform: `scale(${interpolate(a, [0, 1], [0.9, 1])})`, opacity: a, display: "flex", alignItems: "center", gap: 18, padding: "22px 30px", borderRadius: 14, fontFamily: FONT_MONO, fontSize: 30, background: sel ? C.badgeFill : "#0E141B", border: `1.5px solid ${sel ? C.badgeBorder : C.line}`, color: sel ? C.green1 : C.textDim }}>
              {sel ? <Check size={28} color={C.green2} /> : <span style={{ width: 28 }} />}
              {o}
              {sel && <span style={{ marginLeft: "auto", fontSize: 24 }}>🔒</span>}
            </div>
          );
        })}
      </AbsoluteFill>
      <Eyebrow>No interruptions</Eyebrow>
      <Caption2 main="It asks the questions that matter." sub="so the run never stops to ask." />
    </Bg>
  );
};

/* ============================ 5 — you get one clear, doable goal */
const B5: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const card = appear(f, fps, 6, 18);
  const rows = [
    ["decisions", "locked"],
    ["steps", "6, in order"],
    ["success", "npm test passes"],
  ];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <div style={{ width: 880, transform: `scale(${interpolate(card, [0, 1], [0.92, 1])})`, opacity: card, borderRadius: 16, border: `1.5px solid ${C.clay}`, background: "#140F0C", overflow: "hidden" }}>
          <div style={{ padding: "20px 28px", borderBottom: `1px solid ${C.line}`, display: "flex", alignItems: "center", justifyContent: "space-between", fontFamily: FONT_MONO }}>
            <span style={{ fontSize: 30, color: C.clayHi }}>auth.goal.md</span>
            <span style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 22, color: C.green1 }}>
              <Check size={22} color={C.green2} /> doable
            </span>
          </div>
          <div style={{ padding: "20px 28px", fontFamily: FONT_MONO }}>
            {rows.map(([k, v], i) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", fontSize: 27, lineHeight: "48px", opacity: appear(f, fps, 18 + i * 8, 10) }}>
                <span style={{ color: C.textDim }}>{k}</span>
                <span style={{ color: C.text }}>{v}</span>
              </div>
            ))}
          </div>
        </div>
      </AbsoluteFill>
      <Eyebrow>Written right</Eyebrow>
      <Caption color={C.clayHi}>You get one clear, doable goal.</Caption>
    </Bg>
  );
};

/* ============================ 6 — clear, then a fresh AI runs it all */
// Calm, readable run log: two clear wins, one caught failure, then green.
const RUN = [
  { t: "writing src/login.ts", ok: true },
  { t: "writing src/signup.ts", ok: true },
  { t: "1 test failed — fixing it", fail: true },
  { t: "npm test passes", ok: true },
];
const B6: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flash = interpolate(f, [34, 42, 56], [0, 0.9, 0], clamp);
  const prog = interpolate(f, [56, dur - 16], [0, 1], clamp);
  return (
    <Bg flat>
      {/* the two commands, then they fade as the run begins */}
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 12, opacity: interpolate(f, [34, 46], [1, 0], clamp) }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 36, color: C.text }}>
          <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
          {typed("/clear", f, 4, 0.7)}
          {f >= 4 && f < 18 && <Caret h={32} />}
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 36, color: C.text }}>
          <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
          {typed("/goal auth.goal.md", f, 18, 0.7)}
          {f >= 18 && f < 34 && <Caret h={32} />}
        </div>
      </AbsoluteFill>
      {/* after the wipe: pinned file (it survived) + the autonomous run */}
      {f >= 50 && (
        <AbsoluteFill style={{ alignItems: "center", paddingTop: 150, opacity: appear(f, fps, 52, 14) }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "14px 24px", borderRadius: 12, border: `1.5px solid ${C.clay}`, background: "#140F0C", fontFamily: FONT_MONO, fontSize: 26, color: C.clayHi, marginBottom: 26 }}>
            auth.goal.md <span style={{ color: C.green1, fontSize: 22, display: "flex", alignItems: "center", gap: 6 }}><Check size={20} color={C.green2} /> survived /clear</span>
          </div>
          <div style={{ width: 1080 }}>
            <div style={{ height: 230 }}>
              {RUN.map((l, i) => {
                const at = 60 + i * 13;
                if (f < at) return null;
                const col = l.fail ? C.dotRed : l.ok ? C.text : C.textDim;
                return (
                  <div key={l.t} style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 27, lineHeight: "44px", color: col, opacity: appear(f, fps, at, 8) }}>
                    {l.ok ? <Check size={22} color={C.green2} /> : l.fail ? <span style={{ color: C.dotRed, width: 22, textAlign: "center" }}>✕</span> : <span style={{ color: C.clay, width: 22, textAlign: "center" }}>·</span>}
                    {l.t}
                  </div>
                );
              })}
            </div>
            <div style={{ height: 14, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
              <div style={{ width: `${prog * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.clayHi})` }} />
            </div>
          </div>
        </AbsoluteFill>
      )}
      <AbsoluteFill style={{ background: C.text, opacity: flash }} />
      <Eyebrow color={C.green2}>Then it runs</Eyebrow>
      <Caption>A fresh AI runs the whole job.</Caption>
    </Bg>
  );
};

/* ============================ 7 — no guessing, no self-approval */
const B7: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rows = ["every fact checked — no guessing", "a separate agent signs off"];
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center }}>
        <Window title="a second agent checks the work" accent={C.blue} w={1020}>
          {rows.map((r, i) => {
            const ok = f >= 12 + i * 16;
            return (
              <div key={r} style={{ display: "flex", alignItems: "center", gap: 16, height: 72, fontSize: 30, color: C.text, opacity: appear(f, fps, 6 + i * 16, 12) }}>
                {ok ? <Check size={28} color={C.green2} /> : <span style={{ width: 28 }} />}
                {r}
              </div>
            );
          })}
        </Window>
      </AbsoluteFill>
      <Eyebrow color={C.blue}>No self-approval</Eyebrow>
      <Caption color={C.blue}>It checks the facts. It can&rsquo;t pass itself.</Caption>
    </Bg>
  );
};

/* ============================ 8 — GOAL COMPLETE */
const B8: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 6, fps, config: { damping: 9, mass: 0.9 } });
  const glow = interpolate(Math.sin(f / 9), [-1, 1], [0.4, 0.95]);
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 44 }}>
        <div style={{ display: "flex", gap: 26 }}>
          {[0, 1, 2].map((i) => {
            const a = appear(f, fps, i * 6, 12);
            return <div key={i} style={{ transform: `scale(${a})` }}><Check size={58} color={C.green2} /></div>;
          })}
        </div>
        <div style={{ transform: `scale(${interpolate(pop, [0, 1], [0.6, 1])})`, display: "flex", alignItems: "center", gap: 28, padding: "30px 60px", borderRadius: 24, background: C.badgeFill, border: `2px solid ${C.badgeBorder}`, boxShadow: `0 0 ${60 * glow}px ${18 * glow}px rgba(63,185,80,${0.45 * glow})` }}>
          <Check size={78} color={C.green1} />
          <span style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 96, letterSpacing: -2, color: C.green1 }}>GOAL COMPLETE</span>
        </div>
      </AbsoluteFill>
      <Caption color={C.green1}>Every goal met. Proven.</Caption>
    </Bg>
  );
};

/* ============================ 9 — CTA */
const B9: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = appear(f, fps, 4, 16);
  const underline = interpolate(f, [12, 30], [0, 1], { ...clamp, easing: Easing.inOut(Easing.ease) });
  const box = appear(f, fps, 18, 16);
  return (
    <Bg flat>
      <Eyebrow>Get it free</Eyebrow>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 34 }}>
        <div style={{ opacity: s, transform: `translateY(${interpolate(s, [0, 1], [16, 0])}px)`, textAlign: "center" }}>
          <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 116, letterSpacing: -4, color: C.text }}>goalify</div>
          <div style={{ height: 7, width: 330, margin: "6px auto 0", borderRadius: 99, background: C.clay, transform: `scaleX(${underline})`, transformOrigin: "left center" }} />
        </div>
        <div style={{ opacity: box, transform: `translateY(${interpolate(box, [0, 1], [16, 0])}px)`, borderRadius: 14, border: `1px solid ${C.line}`, background: C.card, padding: "24px 38px", fontFamily: FONT_MONO, fontSize: 40, color: C.text }}>
          <span style={{ color: C.green2 }}>$</span> claude plugin install <span style={{ color: C.clayHi }}>goalify@10x</span>
          <span style={{ marginLeft: 4 }}><Caret h={36} /></span>
        </div>
        <div style={{ opacity: interpolate(f, [26, 38], [0, 1], clamp), fontFamily: FONT_MONO, fontSize: 28, color: C.textDim, letterSpacing: 1 }}>free and open source</div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ============================================================== composition */
// 7 beats, each held ≥4s to read calmly. Total 870 frames = 29.0s (under the 30s cap).
const SCENES: [React.FC<any>, number, any?][] = [
  [B1, 120],
  [B2, 120],
  [B5, 120],
  [B6, 150, { dur: 150 }],
  [B7, 120],
  [B8, 120],
  [B9, 120],
];

export const GoalifyTeaser: React.FC = () => {
  let at = 0;
  return (
    <AbsoluteFill style={{ background: C.bg1 }}>
      <Audio
        src={staticFile("music.mp3")}
        volume={(fr) => interpolate(fr, [0, 18, 828, 870], [0, 0.42, 0.42, 0], clamp)}
      />
      {SCENES.map(([Comp, dur, props], i) => {
        const from = at;
        at += dur;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Fade dur={dur}>
              <Comp dur={dur} {...(props ?? {})} />
            </Fade>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
