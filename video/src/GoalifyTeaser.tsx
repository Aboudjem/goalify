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
const typed = (t: string, f: number, start: number, cpf = 0.8) =>
  t.slice(0, Math.max(0, Math.floor((f - start) * cpf)));
const appear = (f: number, fps: number, delay: number, d = 14) =>
  spring({ frame: f - delay, fps, config: { damping: 200 }, durationInFrames: d });

const Caret: React.FC<{ color?: string; h?: number }> = ({ color = C.clay, h = 44 }) => {
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

const Check: React.FC<{ size?: number; color?: string }> = ({ size = 30, color = C.green2 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path d="M5 13l4 4L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Caption: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div
      style={{
        position: "absolute",
        bottom: 90,
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
          fontSize: 60,
          letterSpacing: -1,
          color,
          textShadow: "0 2px 28px rgba(0,0,0,0.65)",
        }}
      >
        {children}
      </span>
    </div>
  );
};

const Eyebrow: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.clay }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 13 });
  const grow = spring({ frame: f - 2, fps, config: { damping: 200 }, durationInFrames: 18 });
  return (
    <div
      style={{
        position: "absolute",
        top: 118,
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
          fontSize: 31,
          letterSpacing: 6,
          textTransform: "uppercase",
          color,
          textShadow: `0 0 30px ${color}55`,
        }}
      >
        <span style={{ width: 50 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
        {children}
        <span style={{ width: 50 * grow, height: 4, borderRadius: 2, background: color, opacity: 0.8 }} />
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

// the goal file as a small card (used to show it being written, pinned, dissolving)
const FileCard: React.FC<{ s: number; subtitle?: string; badge?: string; style?: React.CSSProperties }> = ({
  s,
  subtitle,
  badge,
  style,
}) => (
  <div
    style={{
      transform: `scale(${interpolate(s, [0, 1], [0.9, 1])})`,
      opacity: s,
      borderRadius: 14,
      border: `1.5px solid ${C.clay}`,
      background: "#140F0C",
      padding: "20px 26px",
      display: "flex",
      alignItems: "center",
      gap: 18,
      fontFamily: FONT_MONO,
      ...style,
    }}
  >
    <span style={{ fontSize: 30, color: C.clayHi }}>checkout.goal.md</span>
    {subtitle && <span style={{ fontSize: 22, color: C.textDim }}>{subtitle}</span>}
    {badge && (
      <span style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 22, color: C.green1, marginLeft: "auto" }}>
        <Check size={22} color={C.green2} /> {badge}
      </span>
    )}
  </div>
);

const center: React.CSSProperties = { alignItems: "center", justifyContent: "center" };
const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

/* ===================================== 1 — PROBLEM: too big for one chat */
const B1: React.FC = () => {
  const f = useCurrentFrame();
  const fill = interpolate(f, [6, 40], [0.55, 1], clamp);
  const full = fill > 0.97;
  const lines = ["build the new checkout", "migrate the database", "fix the failing tests", "add the email flow"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — one long chat" w={1180}>
          {lines.map((l, i) => (
            <div key={l} style={{ fontSize: 28, color: C.textDim, lineHeight: "46px", opacity: appear(f, 30, 4 + i * 4, 8) }}>
              <span>{">"} </span>
              {l}
            </div>
          ))}
          <div style={{ marginTop: 20, display: "flex", alignItems: "center", gap: 16 }}>
            <span style={{ fontSize: 22, color: full ? C.dotRed : C.textDim }}>{full ? "CONTEXT FULL" : "memory"}</span>
            <div style={{ flex: 1, height: 16, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
              <div style={{ width: `${fill * 100}%`, height: "100%", background: full ? C.dotRed : `linear-gradient(90deg, ${C.green3}, ${C.clay}, ${C.dotRed})` }} />
            </div>
            <span style={{ fontSize: 22, color: full ? C.dotRed : C.textDim }}>{Math.round(fill * 100)}%</span>
          </div>
        </Window>
      </AbsoluteFill>
      <Eyebrow color={C.dotRed}>The problem</Eyebrow>
      <Caption>A big task is too big for one AI chat.</Caption>
    </Bg>
  );
};

/* ===================================== 2 — PROBLEM: /clear loses the plan */
const B2: React.FC = () => {
  const f = useCurrentFrame();
  const flash = interpolate(f, [22, 30, 46], [0, 0.95, 0], clamp);
  const planOut = interpolate(f, [40, 62], [1, 0], clamp);
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 46, color: C.clay, opacity: interpolate(f, [34, 44], [1, 0], clamp) }}>
          {">"} {typed("/clear", f, 2, 0.6)}
          {f < 26 && <Caret h={42} />}
        </div>
      </AbsoluteFill>
      {/* fresh empty terminal revealed, with the plan fading out */}
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 30, opacity: interpolate(f, [44, 56], [0, 1], clamp) }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 30, color: C.textDim, opacity: planOut, border: `1px dashed ${C.line}`, borderRadius: 10, padding: "14px 22px" }}>
          your plan
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 40, color: C.textDim }}>
          {">"} <Caret h={36} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.text, opacity: flash }} />
      <Eyebrow color={C.dotRed}>The problem</Eyebrow>
      <Caption>You clear the chat. Your plan is gone.</Caption>
    </Bg>
  );
};

/* ===================================== 3 — MEET GOALIFY (what it is) */
const B3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = appear(f, fps, 4, 16);
  const underline = interpolate(f, [14, 32], [0, 1], { ...clamp, easing: Easing.inOut(Easing.ease) });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 22 }}>
        <div style={{ opacity: s, transform: `translateY(${interpolate(s, [0, 1], [16, 0])}px)`, textAlign: "center" }}>
          <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 150, letterSpacing: -4, color: C.text }}>goalify</div>
          <div style={{ height: 8, width: 380, margin: "8px auto 0", borderRadius: 99, background: C.clay, transform: `scaleX(${underline})`, transformOrigin: "left center" }} />
        </div>
        <div style={{ opacity: interpolate(f, [20, 32], [0, 1], clamp), fontFamily: FONT_MONO, fontSize: 32, color: C.textDim, letterSpacing: 1 }}>
          free and open source
        </div>
      </AbsoluteFill>
      <Eyebrow>Meet goalify</Eyebrow>
      <Caption>A free skill for Claude Code.</Caption>
    </Bg>
  );
};

/* ===================================== 4 — STEP 1: type your task once */
const B4: React.FC = () => {
  const f = useCurrentFrame();
  const cmd = "/goalify build the new checkout";
  const n = typed(cmd, f, 6, 0.85);
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code" w={1180}>
          <div style={{ fontSize: 38, color: C.text, height: 56, display: "flex", alignItems: "center" }}>
            <span style={{ color: C.textDim, marginRight: 14 }}>{">"}</span>
            <span style={{ color: C.clayHi, textShadow: `0 0 22px ${C.clay}99` }}>{n.startsWith("/goalify") ? "/goalify" : n}</span>
            <span style={{ color: C.text }}>{n.startsWith("/goalify") ? n.slice(8) : ""}</span>
            <Caret h={38} />
          </div>
        </Window>
      </AbsoluteFill>
      <Eyebrow>Step 1</Eyebrow>
      <Caption>Type your big task one time.</Caption>
    </Bg>
  );
};

/* ===================================== 5 — STEP 1: it writes one plan file */
const B5: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const steps = ["reading your project…", "locking the key decisions…", "writing the success checks…"];
  const card = appear(f, fps, 50, 18);
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goalify" w={1180}>
          {steps.map((s, i) => {
            const at = 6 + i * 13;
            if (f < at) return <div key={s} style={{ height: 46 }} />;
            return (
              <div key={s} style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 28, color: C.text, lineHeight: "46px", opacity: appear(f, fps, at, 10) }}>
                <Check size={24} color={C.green2} /> {s}
              </div>
            );
          })}
          <div style={{ marginTop: 18 }}>
            <FileCard s={card} badge="npm test passes" style={{ borderColor: C.clay }} />
          </div>
        </Window>
      </AbsoluteFill>
      <Eyebrow>Step 1</Eyebrow>
      <Caption color={C.clayHi}>goalify writes the whole plan to one file.</Caption>
    </Bg>
  );
};

/* ===================================== 6 — STEP 2: clear, then run the file */
const B6: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c1 = typed("/clear", f, 6, 0.7);
  const c2 = typed("/goal checkout.goal.md", f, 26, 0.7);
  const flash = interpolate(f, [48, 56, 70], [0, 0.9, 0], clamp);
  const pinned = appear(f, fps, 60, 16);
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 14, opacity: interpolate(f, [46, 58], [1, 0], clamp) }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 38, color: C.text }}>
          <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
          {c1}
          {f >= 6 && f < 24 && <Caret h={34} />}
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 38, color: C.text }}>
          <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
          {c2}
          {f >= 26 && f < 48 && <Caret h={34} />}
        </div>
      </AbsoluteFill>
      {/* after the wipe, the file is still pinned at the top */}
      <div style={{ position: "absolute", top: 250, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: pinned, transform: `translateY(${interpolate(pinned, [0, 1], [-16, 0])}px)` }}>
        <FileCard s={1} badge="still here" />
      </div>
      <AbsoluteFill style={{ ...center, opacity: interpolate(f, [62, 72], [0, 1], clamp) }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 34, color: C.textDim }}>
          fresh session {">"} <Caret h={30} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.text, opacity: flash }} />
      <Eyebrow color={C.green2}>Step 2</Eyebrow>
      <Caption>Clear the chat. Run the file.</Caption>
    </Bg>
  );
};

/* ===================================== 7 — RESULT: a fresh AI does it alone */
const RUN = [
  { t: "writing checkout.tsx", ok: true },
  { t: "writing api/pay.ts", ok: true },
  { t: "running npm test…", run: true },
  { t: "1 test failed — fixing…", fail: true },
  { t: "npm test passes", ok: true },
];
const B7: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const prog = interpolate(f, [10, dur - 18], [0, 1], clamp);
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="fresh session — /goal" w={1180}>
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 18 }}>
            <span style={{ fontSize: 22, color: C.green2 }}>memory</span>
            <div style={{ flex: 1, height: 14, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
              <div style={{ width: "100%", height: "100%", background: C.green3 }} />
            </div>
            <span style={{ fontSize: 22, color: C.green2 }}>fresh</span>
          </div>
          <div style={{ height: 250 }}>
            {RUN.map((l, i) => {
              const at = 12 + i * 16;
              if (f < at) return null;
              const a = appear(f, fps, at, 9);
              const col = l.fail ? C.dotRed : l.ok ? C.text : C.textDim;
              return (
                <div key={l.t} style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 28, lineHeight: "46px", color: col, opacity: a }}>
                  {l.ok ? <Check size={24} color={C.green2} /> : l.fail ? <span style={{ color: C.dotRed, width: 24, textAlign: "center" }}>✕</span> : <span style={{ color: C.clay, width: 24, textAlign: "center" }}>·</span>}
                  {l.t}
                </div>
              );
            })}
          </div>
          <div style={{ height: 14, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
            <div style={{ width: `${prog * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.clayHi})` }} />
          </div>
        </Window>
      </AbsoluteFill>
      <Eyebrow>The result</Eyebrow>
      <Caption>A fresh AI does the whole job alone.</Caption>
    </Bg>
  );
};

/* ===================================== 8 — PROOF: a checker confirms it */
const B8: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rows = ["checkout works", "every test passes", "nothing else broke"];
  const badge = spring({ frame: f - 50, fps, config: { damping: 9, mass: 0.9 } });
  const glow = interpolate(Math.sin(f / 9), [-1, 1], [0.4, 0.95]);
  const showBadge = f >= 48;
  return (
    <Bg flat>
      {!showBadge && (
        <AbsoluteFill style={{ ...center }}>
          <Window title="a second agent checks the work" accent={C.blue} w={980} style={{ opacity: interpolate(f, [40, 48], [1, 0], clamp) }}>
            {rows.map((r, i) => {
              const ok = f >= 8 + i * 11;
              return (
                <div key={r} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", height: 64, fontSize: 30, color: C.text, opacity: appear(f, fps, 4 + i * 11, 10) }}>
                  <span style={{ display: "flex", alignItems: "center", gap: 14 }}>
                    {ok ? <Check size={26} color={C.green2} /> : <span style={{ width: 26 }} />}
                    {r}
                  </span>
                  {ok && <span style={{ fontSize: 20, color: C.blue, letterSpacing: 2 }}>CHECKED</span>}
                </div>
              );
            })}
          </Window>
        </AbsoluteFill>
      )}
      {showBadge && (
        <AbsoluteFill style={{ ...center }}>
          <div
            style={{
              transform: `scale(${interpolate(badge, [0, 1], [0.6, 1])})`,
              display: "flex",
              alignItems: "center",
              gap: 28,
              padding: "30px 60px",
              borderRadius: 24,
              background: C.badgeFill,
              border: `2px solid ${C.badgeBorder}`,
              boxShadow: `0 0 ${60 * glow}px ${18 * glow}px rgba(63,185,80,${0.45 * glow})`,
            }}
          >
            <Check size={78} color={C.green1} />
            <span style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 96, letterSpacing: -2, color: C.green1 }}>GOAL COMPLETE</span>
          </div>
        </AbsoluteFill>
      )}
      <Eyebrow color={C.blue}>The proof</Eyebrow>
      <Caption color={showBadge ? C.green1 : C.blue}>A checker confirms every goal is real.</Caption>
    </Bg>
  );
};

/* ===================================== 9 — CTA: get it free */
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
        <div
          style={{
            opacity: box,
            transform: `translateY(${interpolate(box, [0, 1], [16, 0])}px)`,
            borderRadius: 14,
            border: `1px solid ${C.line}`,
            background: C.card,
            padding: "24px 38px",
            fontFamily: FONT_MONO,
            fontSize: 40,
            color: C.text,
          }}
        >
          <span style={{ color: C.green2 }}>$</span> claude plugin install <span style={{ color: C.clayHi }}>goalify@10x</span>
          <span style={{ marginLeft: 4 }}>
            <Caret h={36} />
          </span>
        </div>
        <div style={{ opacity: interpolate(f, [26, 38], [0, 1], clamp), fontFamily: FONT_MONO, fontSize: 28, color: C.textDim, letterSpacing: 1 }}>
          free and open source
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ============================================================== composition */
const SCENES: [React.FC<any>, number, any?][] = [
  [B1, 90],
  [B2, 90],
  [B3, 84],
  [B4, 90],
  [B5, 102, { dur: 102 }],
  [B6, 108],
  [B7, 108, { dur: 108 }],
  [B8, 108],
  [B9, 90],
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
