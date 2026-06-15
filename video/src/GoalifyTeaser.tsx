import React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
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
  const o = interpolate(f, [0, 7, dur - 7, dur], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const blink = (f: number, p = 30) => (f % p < p / 2 ? 1 : 0);
const typed = (t: string, f: number, start: number, cpf = 0.7) =>
  t.slice(0, Math.max(0, Math.floor((f - start) * cpf)));
const appear = (f: number, fps: number, delay: number, d = 14) =>
  spring({ frame: f - delay, fps, config: { damping: 200 }, durationInFrames: d });

const Caret: React.FC<{ color?: string; h?: number }> = ({ color = C.clay, h = 50 }) => {
  const f = useCurrentFrame();
  return (
    <span
      style={{
        display: "inline-block",
        width: h * 0.5,
        height: h,
        marginLeft: 6,
        marginBottom: -h * 0.12,
        background: color,
        opacity: blink(f),
        borderRadius: 3,
      }}
    />
  );
};

const Check: React.FC<{ size?: number; color?: string }> = ({ size = 34, color = C.green2 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path d="M5 13l4 4L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

// Caption: big, simple, high-contrast, bottom-anchored (muted-safe).
const Caption: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div
      style={{
        position: "absolute",
        bottom: 92,
        left: 0,
        right: 0,
        textAlign: "center",
        transform: `translateY(${interpolate(s, [0, 1], [22, 0])}px)`,
        opacity: s,
        padding: "0 130px",
      }}
    >
      <span
        style={{
          fontFamily: FONT_UI,
          fontWeight: 800,
          fontSize: 62,
          letterSpacing: -1,
          color,
          textShadow: "0 2px 28px rgba(0,0,0,0.6)",
        }}
      >
        {children}
      </span>
    </div>
  );
};

// small uppercase label at the top of a scene
const Eyebrow: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.clay }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 13 });
  const grow = spring({ frame: f - 2, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div
      style={{
        position: "absolute",
        top: 120,
        left: 0,
        right: 0,
        textAlign: "center",
        opacity: s,
        transform: `translateY(${interpolate(s, [0, 1], [-16, 0])}px)`,
      }}
    >
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 18,
          fontFamily: FONT_UI,
          fontWeight: 800,
          fontSize: 32,
          letterSpacing: 6,
          textTransform: "uppercase",
          color,
          textShadow: `0 0 30px ${color}55`,
        }}
      >
        <span style={{ width: 52 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
        {children}
        <span style={{ width: 52 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
      </span>
    </div>
  );
};

const Window: React.FC<{
  children: React.ReactNode;
  title?: string;
  w?: number;
  accent?: string;
  style?: React.CSSProperties;
}> = ({ children, title = "claude code", w = 1180, accent, style }) => (
  <div
    style={{
      width: w,
      borderRadius: 18,
      background: C.card,
      border: `1px solid ${accent ?? C.line}`,
      boxShadow: `0 40px 120px rgba(0,0,0,0.55)${accent ? `, 0 0 0 1px ${accent}33` : ""}`,
      overflow: "hidden",
      ...style,
    }}
  >
    <div
      style={{
        height: 50,
        display: "flex",
        alignItems: "center",
        gap: 9,
        padding: "0 22px",
        background: "#0C1117",
        borderBottom: `1px solid ${C.line}`,
      }}
    >
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotRed }} />
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotYellow }} />
      <span style={{ width: 14, height: 14, borderRadius: 99, background: C.dotGreen }} />
      <span style={{ marginLeft: 16, fontFamily: FONT_MONO, fontSize: 21, color: C.textDim }}>{title}</span>
    </div>
    <div style={{ padding: "30px 38px", fontFamily: FONT_MONO }}>{children}</div>
  </div>
);

const center: React.CSSProperties = { alignItems: "center", justifyContent: "center" };

const AgentCard: React.FC<{
  label: string;
  cx: number;
  cy: number;
  s: number;
  doneAt?: number;
  f: number;
  color?: string;
  w?: number;
}> = ({ label, cx, cy, s, doneAt, f, color = C.clay, w = 300 }) => {
  const done = doneAt != null && f >= doneAt;
  const pulse = interpolate(Math.sin(f / 5), [-1, 1], [0.5, 1]);
  return (
    <div
      style={{
        position: "absolute",
        left: cx - w / 2,
        top: cy - 38,
        width: w,
        height: 76,
        transform: `scale(${s})`,
        opacity: s,
        display: "flex",
        alignItems: "center",
        gap: 16,
        padding: "0 22px",
        borderRadius: 14,
        background: "#0E141B",
        border: `1px solid ${done ? C.badgeBorder : C.line}`,
        fontFamily: FONT_MONO,
        fontSize: 25,
        color: C.text,
        boxShadow: done ? `0 0 24px ${C.green3}33` : "none",
      }}
    >
      {done ? <Check size={25} color={C.green2} /> : <span style={{ width: 13, height: 13, borderRadius: 99, background: color, opacity: pulse }} />}
      <span style={{ whiteSpace: "nowrap" }}>{label}</span>
    </div>
  );
};

/* ============================================ 1 — HOOK: the AI forgets the task */
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const fill = interpolate(f, [4, 30], [0.62, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wipe = interpolate(f, [40, 56], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  const lines = ["build the new checkout", "migrate the database", "fix the failing tests", "…a big, multi-step job"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code" w={1120}>
          {lines.map((l, i) => (
            <div key={l} style={{ fontSize: 28, color: i === 3 ? C.clay : C.textDim, lineHeight: "48px" }}>
              <span>{">"} </span>
              {l}
            </div>
          ))}
          <div style={{ marginTop: 18, display: "flex", alignItems: "center", gap: 16 }}>
            <span style={{ fontSize: 22, color: fill > 0.95 ? C.dotRed : C.textDim }}>memory</span>
            <div style={{ flex: 1, height: 14, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
              <div style={{ width: `${fill * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.dotRed})` }} />
            </div>
            <span style={{ fontSize: 22, color: C.dotRed }}>full</span>
          </div>
        </Window>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.text, opacity: wipe < 1 ? wipe * 0.92 : 0 }} />
      <AbsoluteFill style={{ ...center, opacity: wipe > 0.6 ? 1 : 0 }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 48, color: C.clay }}>{">"} /clear</div>
      </AbsoluteFill>
      <Caption>Big task. Your AI forgets it all.</Caption>
    </Bg>
  );
};

/* ============================================ 2 — you babysit every step (FOMO) */
const NAG = [
  ["are you done?", "not yet…"],
  ["keep going", "…lost the thread"],
  ["no — do it again", "starting over"],
];
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="you · checking every step" w={1020}>
          {NAG.map(([u, a], i) => {
            const at = 6 + i * 22;
            if (f < at) return <div key={i} style={{ height: 84 }} />;
            const ap = appear(f, fps, at, 10);
            return (
              <div key={i} style={{ opacity: ap, marginBottom: 18 }}>
                <div style={{ fontSize: 30, color: C.clay }}>
                  {">"} {u}
                </div>
                <div style={{ fontSize: 25, color: C.textDim, marginLeft: 30 }}>{a}</div>
              </div>
            );
          })}
        </Window>
      </AbsoluteFill>
      <Caption>So you repeat yourself, step by step.</Caption>
    </Bg>
  );
};

/* ============================================ 3 — SOLUTION: goalify writes a plan */
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const card = appear(f, fps, 40, 20);
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goalify">
          <div style={{ fontSize: 32, color: C.text, height: 48 }}>
            <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
            {typed("/goalify build the new checkout", f, 2, 0.8)}
            {f < 48 && <Caret h={32} />}
          </div>
          <div
            style={{
              marginTop: 22,
              opacity: card,
              transform: `translateY(${interpolate(card, [0, 1], [20, 0])}px)`,
              borderRadius: 12,
              border: `1px solid ${C.line}`,
              background: "#0C1015",
              padding: "22px 26px",
            }}
          >
            <div style={{ fontSize: 28, color: C.clay }}>checkout.goal.md</div>
            <div style={{ color: C.textDim, fontSize: 23, marginTop: 8 }}>one file · the whole plan</div>
          </div>
        </Window>
      </AbsoluteFill>
      <Caption color={C.clayHi}>goalify writes the plan. You walk away.</Caption>
    </Bg>
  );
};

/* ============================================ 4 — it researches + checks the facts */
const RESEARCH = ["read the docs", "ask the community", "check the code"];
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cx = [520, 960, 1400];
  return (
    <Bg>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {cx.map((x, i) => {
          const a = appear(f, fps, 12 + i * 6, 10);
          return <line key={i} x1={960} y1={306} x2={x} y2={482} stroke={C.clay} strokeWidth={2} strokeOpacity={a * 0.5} strokeDasharray="6 8" />;
        })}
      </svg>
      <div
        style={{
          position: "absolute",
          left: 810,
          top: 250,
          width: 300,
          height: 64,
          transform: `scale(${appear(f, fps, 0, 12)})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 14,
          background: C.badgeFill,
          border: `1.5px solid ${C.clay}`,
          fontFamily: FONT_MONO,
          fontSize: 27,
          color: C.clayHi,
          fontWeight: 700,
        }}
      >
        /goalify
      </div>
      {cx.map((x, i) => (
        <AgentCard key={i} label={RESEARCH[i]} cx={x} cy={520} s={appear(f, fps, 16 + i * 6, 12)} doneAt={54 + i * 6} f={f} w={320} />
      ))}
      <Eyebrow color={C.blue}>No hallucinations</Eyebrow>
      <Caption color={C.blue}>It researches and checks every fact.</Caption>
    </Bg>
  );
};

/* ============================================ 5 — your plan survives /clear */
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flash = interpolate(f, [8, 16, 34], [0, 0.95, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const clearOut = interpolate(f, [0, 10], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const s = spring({ frame: f - 30, fps, config: { damping: 12 } });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 44, color: C.clay, opacity: clearOut }}>{">"} /clear</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 24, opacity: interpolate(f, [26, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
        <div style={{ transform: `scale(${interpolate(s, [0, 1], [0.85, 1])})`, fontFamily: FONT_UI, fontWeight: 800, fontSize: 92, letterSpacing: -2, color: C.green1 }}>
          Your plan stays.
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 27, color: C.textDim }}>checkout.goal.md — still here</div>
      </AbsoluteFill>
      {/* quick white flash = the /clear wipe, then it's gone */}
      <AbsoluteFill style={{ background: C.text, opacity: flash }} />
      <Eyebrow color={C.green2}>Survives /clear</Eyebrow>
      <Caption>You clear the chat. The plan stays.</Caption>
    </Bg>
  );
};

/* ============================================ 6 — it runs the whole job, alone */
const RUN = ["checkout.tsx", "cart.ts", "api/pay.ts"];
const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const prog = interpolate(f, [16, dur - 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Bg>
      {RUN.map((name, i) => (
        <AgentCard key={name} label={`writing ${name}`} cx={[470, 960, 1450][i]} cy={320} s={appear(f, fps, 6 + i * 5, 12)} doneAt={42 + i * 14} f={f} w={360} />
      ))}
      <AbsoluteFill style={{ ...center }}>
        <div style={{ width: 1120 }}>
          <div style={{ display: "flex", gap: 48, justifyContent: "center", marginBottom: 40 }}>
            {[0, 1, 2].map((i) => {
              const a = appear(f, fps, 52 + i * 12, 12);
              return (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, transform: `scale(${a})`, opacity: a }}>
                  <Check size={38} color={C.green2} />
                  <span style={{ fontFamily: FONT_MONO, fontSize: 28, color: C.text }}>{["build", "tests", "lint"][i]}</span>
                </div>
              );
            })}
          </div>
          <div style={{ height: 18, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
            <div style={{ width: `${prog * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.clayHi})` }} />
          </div>
          <div style={{ marginTop: 16, textAlign: "center", fontFamily: FONT_MONO, fontSize: 26, color: C.clay }}>no help needed · {Math.round(prog * 100)}%</div>
        </div>
      </AbsoluteFill>
      <Eyebrow>Fully autonomous</Eyebrow>
      <Caption>It runs the whole job, alone.</Caption>
    </Bg>
  );
};

/* ============================================ 7 — it checks its own work */
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rows = ["new checkout works", "every test passes", "nothing else broke", "all goals met"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="a second agent checks the work" accent={C.blue} w={1020}>
          {rows.map((r, i) => {
            const a = appear(f, fps, 8 + i * 11, 12);
            const ok = f >= 14 + i * 11;
            return (
              <div key={r} style={{ display: "flex", alignItems: "center", gap: 16, height: 62, opacity: a, fontSize: 30, color: C.text }}>
                {ok ? <Check size={28} color={C.green2} /> : <span style={{ width: 28 }} />}
                {r}
              </div>
            );
          })}
        </Window>
      </AbsoluteFill>
      <Eyebrow color={C.blue}>Double-checked</Eyebrow>
      <Caption color={C.blue}>It checks its own work, twice.</Caption>
    </Bg>
  );
};

/* ============================================ 8 — PAYOFF: you come back, it's done */
const S8: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 6, fps, config: { damping: 9, mass: 0.9 } });
  const glow = interpolate(Math.sin(f / 9), [-1, 1], [0.4, 0.95]);
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 46 }}>
        <div style={{ display: "flex", gap: 26 }}>
          {[0, 1, 2].map((i) => {
            const a = appear(f, fps, i * 6, 12);
            return (
              <div key={i} style={{ transform: `scale(${a})` }}>
                <Check size={60} color={C.green2} />
              </div>
            );
          })}
        </div>
        <div
          style={{
            transform: `scale(${interpolate(pop, [0, 1], [0.6, 1])})`,
            display: "flex",
            alignItems: "center",
            gap: 30,
            padding: "32px 64px",
            borderRadius: 24,
            background: C.badgeFill,
            border: `2px solid ${C.badgeBorder}`,
            boxShadow: `0 0 ${64 * glow}px ${20 * glow}px rgba(63,185,80,${0.45 * glow})`,
          }}
        >
          <Check size={84} color={C.green1} />
          <span style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 100, letterSpacing: -2, color: C.green1 }}>GOAL COMPLETE</span>
        </div>
      </AbsoluteFill>
      <Caption color={C.green1}>You come back. It&rsquo;s done.</Caption>
    </Bg>
  );
};

/* ============================================ 9 — tested, verified, clean */
const S9: React.FC = () => {
  const f = useCurrentFrame();
  const path = "rm checkout.goal.md";
  const strike = interpolate(f, [16, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dissolve = interpolate(f, [28, 40], [1, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — done" w={920} style={{ opacity: dissolve }}>
          <div style={{ fontSize: 30, color: C.text, position: "relative" }}>
            <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
            <span style={{ position: "relative" }}>
              {typed(path, f, 2, 1.1)}
              <span style={{ position: "absolute", left: 0, top: "52%", height: 3, width: `${strike * 100}%`, background: C.dotRed }} />
            </span>
          </div>
        </Window>
      </AbsoluteFill>
      <Caption>Tested. Verified. Clean.</Caption>
    </Bg>
  );
};

/* ============================================ 10 — CTA: try it free */
const S10: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = appear(f, fps, 4, 16);
  const underline = interpolate(f, [14, 32], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.ease) });
  const box = appear(f, fps, 24, 16);
  return (
    <Bg flat>
      <Eyebrow>Free · open source</Eyebrow>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 30 }}>
        <div style={{ opacity: s, transform: `translateY(${interpolate(s, [0, 1], [16, 0])}px)`, textAlign: "center" }}>
          <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 128, letterSpacing: -4, color: C.text }}>goalify</div>
          <div style={{ height: 7, width: 360, margin: "6px auto 0", borderRadius: 99, background: C.clay, transform: `scaleX(${underline})`, transformOrigin: "left center" }} />
        </div>
        <div style={{ opacity: interpolate(f, [18, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), fontFamily: FONT_MONO, fontSize: 34, color: C.textDim, letterSpacing: 1 }}>
          set the goal. trust the run.
        </div>
        <div
          style={{
            opacity: box,
            transform: `translateY(${interpolate(box, [0, 1], [16, 0])}px)`,
            marginTop: 14,
            borderRadius: 14,
            border: `1px solid ${C.line}`,
            background: C.card,
            padding: "22px 34px",
            fontFamily: FONT_MONO,
            fontSize: 30,
            color: C.text,
          }}
        >
          <span style={{ color: C.green2 }}>$</span> claude plugin install <span style={{ color: C.clayHi }}>goalify@10x</span>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ============================================================== composition */
const SCENES: [React.FC<any>, number, any?][] = [
  [S1, 84],
  [S2, 84],
  [S3, 96],
  [S4, 84],
  [S5, 90],
  [S6, 102, { dur: 102 }],
  [S7, 84],
  [S8, 84],
  [S9, 54],
  [S10, 108],
];

export const GoalifyTeaser: React.FC = () => {
  let at = 0;
  return (
    <AbsoluteFill style={{ background: C.bg1 }}>
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
