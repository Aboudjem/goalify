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
    {/* faint dot grid for depth */}
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
  const o = interpolate(f, [0, 6, dur - 6, dur], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const blink = (f: number, p = 30) => (f % p < p / 2 ? 1 : 0);
const typed = (t: string, f: number, start: number, cpf = 0.7) =>
  t.slice(0, Math.max(0, Math.floor((f - start) * cpf)));

const Caret: React.FC<{ color?: string; h?: number }> = ({ color = C.clay, h = 56 }) => {
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

const Check: React.FC<{ size?: number; color?: string }> = ({ size = 36, color = C.green2 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path d="M5 13l4 4L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Caption: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 16 });
  return (
    <div
      style={{
        position: "absolute",
        bottom: 88,
        left: 0,
        right: 0,
        textAlign: "center",
        transform: `translateY(${interpolate(s, [0, 1], [24, 0])}px)`,
        opacity: s,
        padding: "0 120px",
      }}
    >
      <span
        style={{
          fontFamily: FONT_UI,
          fontWeight: 800,
          fontSize: 56,
          letterSpacing: -1,
          color,
          textShadow: "0 2px 26px rgba(0,0,0,0.6)",
        }}
      >
        {children}
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
const appear = (f: number, fps: number, delay: number, d = 14) =>
  spring({ frame: f - delay, fps, config: { damping: 200 }, durationInFrames: d });

// a small agent "card" used by the fan-out + run scenes
const AgentCard: React.FC<{
  label: string;
  cx: number;
  cy: number;
  s: number; // 0..1 appear
  doneAt?: number; // frame to flip the dot to a check
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
        fontSize: 26,
        color: C.text,
        boxShadow: done ? `0 0 24px ${C.green3}33` : "none",
      }}
    >
      {done ? (
        <Check size={26} color={C.green2} />
      ) : (
        <span style={{ width: 13, height: 13, borderRadius: 99, background: color, opacity: pulse }} />
      )}
      <span style={{ whiteSpace: "nowrap" }}>{label}</span>
    </div>
  );
};

/* =================================================================== scene 1 */
// HOOK (0-1.8s): a packed session, context meter maxes out, /clear wipes it.
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const fill = interpolate(f, [0, 24], [0.7, 1], { extrapolateRight: "clamp" });
  const wipe = interpolate(f, [30, 44], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  const lines = [
    "edited 14 files…",
    "decided: use the repository pattern",
    "TODO: migrate the rest of the routes",
    "context: this whole plan lives in chat",
  ];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — a long session" w={1180}>
          {lines.map((l, i) => (
            <div key={l} style={{ fontSize: 27, color: i === 3 ? C.clay : C.textDim, lineHeight: "46px" }}>
              <span style={{ color: C.textDim }}>{">"} </span>
              {l}
            </div>
          ))}
          <div style={{ marginTop: 18, display: "flex", alignItems: "center", gap: 16 }}>
            <span style={{ fontSize: 22, color: fill > 0.95 ? C.dotRed : C.textDim }}>context</span>
            <div style={{ flex: 1, height: 14, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
              <div style={{ width: `${fill * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.dotRed})` }} />
            </div>
            <span style={{ fontSize: 22, color: C.dotRed }}>{Math.round(fill * 100)}%</span>
          </div>
        </Window>
      </AbsoluteFill>
      {/* /clear flash wipe */}
      <AbsoluteFill style={{ background: C.text, opacity: wipe < 1 ? wipe * 0.9 : 0 }} />
      <AbsoluteFill style={{ ...center, opacity: wipe > 0.6 ? 1 : 0 }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 50, color: C.clay }}>{">"} /clear</div>
      </AbsoluteFill>
      <Caption>Your plan dies at /clear.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 2 */
// goalify writes the run file.
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const card = appear(f, fps, 36, 20);
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goalify">
          <div style={{ fontSize: 32, color: C.text, height: 48 }}>
            <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
            {typed("/goalify migrate the API to async/await", f, 2, 0.8)}
            {f < 52 && <Caret h={32} />}
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
              fontSize: 28,
              color: C.clay,
            }}
          >
            ~/acme/.goal/cb-to-async.md
            <div style={{ color: C.textDim, fontSize: 22, marginTop: 8 }}>the run file — before you /clear</div>
          </div>
        </Window>
      </AbsoluteFill>
      <Caption color={C.clayHi}>First, it writes the run file.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 3 */
// FAN-OUT: parallel research agents spawn from the goalify node.
const RESEARCH = ["official docs", "community tricks", "rival tools", "gotchas"];
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nodeS = appear(f, fps, 0, 12);
  const cx = [420, 780, 1140, 1500];
  const cardY = 560;
  const nodeX = 960;
  const nodeY = 250;
  return (
    <Bg>
      {/* connecting lines */}
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {cx.map((x, i) => {
          const a = appear(f, fps, 12 + i * 6, 10);
          return (
            <line
              key={i}
              x1={nodeX}
              y1={nodeY + 36}
              x2={x}
              y2={cardY - 38}
              stroke={C.clay}
              strokeWidth={2}
              strokeOpacity={a * 0.5}
              strokeDasharray="6 8"
            />
          );
        })}
      </svg>
      {/* center node */}
      <div
        style={{
          position: "absolute",
          left: nodeX - 150,
          top: nodeY - 34,
          width: 300,
          height: 68,
          transform: `scale(${nodeS})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 12,
          borderRadius: 14,
          background: C.badgeFill,
          border: `1.5px solid ${C.clay}`,
          fontFamily: FONT_MONO,
          fontSize: 28,
          color: C.clayHi,
          fontWeight: 700,
        }}
      >
        /goalify
      </div>
      {cx.map((x, i) => (
        <AgentCard
          key={i}
          label={RESEARCH[i]}
          cx={x}
          cy={cardY}
          s={appear(f, fps, 16 + i * 6, 12)}
          doneAt={58 + i * 5}
          f={f}
          w={300}
        />
      ))}
      <Caption>Fans out research agents — in parallel.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 4 */
// SKEPTIC: a separate agent re-derives each claim from its source.
const CLAIMS = [
  "Express 4 · callback handlers",
  "node --test suite is green",
  "no DB swap — in-memory Map",
];
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scan = interpolate(f, [22, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="skeptic — re-deriving from primaries" accent={C.blue} w={1180}>
          {CLAIMS.map((c, i) => {
            const rowAt = 6 + i * 8;
            const checkedAt = 30 + i * 14;
            const reveal = appear(f, fps, rowAt, 10);
            const ok = f >= checkedAt;
            return (
              <div
                key={c}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  height: 70,
                  opacity: reveal,
                  fontSize: 28,
                  color: C.text,
                }}
              >
                <span>{c}</span>
                <span style={{ display: "flex", alignItems: "center", gap: 14 }}>
                  <span
                    style={{
                      fontSize: 20,
                      color: C.blue,
                      border: `1px solid ${C.blue}55`,
                      borderRadius: 99,
                      padding: "4px 14px",
                    }}
                  >
                    source
                  </span>
                  {ok ? (
                    <span style={{ display: "flex", alignItems: "center", gap: 8, color: C.green1, fontSize: 24 }}>
                      <Check size={26} color={C.green2} /> re-derived
                    </span>
                  ) : (
                    <span style={{ width: 26 }} />
                  )}
                </span>
              </div>
            );
          })}
          {/* scan line */}
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: `${20 + scan * 60}%`,
              height: 2,
              background: `linear-gradient(90deg, transparent, ${C.blue}, transparent)`,
              opacity: scan > 0 && scan < 1 ? 0.9 : 0,
            }}
          />
        </Window>
      </AbsoluteFill>
      <Caption color={C.blue}>A separate skeptic re-checks every claim.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 5 */
// DECISIONS locked (one quick MCQ).
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pick = f >= 26;
  const opts = ["promisify the data layer", "wrap callbacks at call sites"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 28 }}>
        <div style={{ fontFamily: FONT_UI, fontSize: 34, color: C.textDim }}>one quick decision</div>
        {opts.map((o, i) => {
          const sel = i === 0 && pick;
          const a = appear(f, fps, 4 + i * 8, 12);
          return (
            <div
              key={o}
              style={{
                width: 920,
                transform: `scale(${interpolate(a, [0, 1], [0.9, 1])})`,
                opacity: a,
                display: "flex",
                alignItems: "center",
                gap: 18,
                padding: "24px 30px",
                borderRadius: 14,
                fontFamily: FONT_MONO,
                fontSize: 30,
                background: sel ? C.badgeFill : "#0E141B",
                border: `1.5px solid ${sel ? C.badgeBorder : C.line}`,
                color: sel ? C.green1 : C.textDim,
              }}
            >
              {sel ? <Check size={28} color={C.green2} /> : <span style={{ width: 28 }} />}
              {o}
              {sel && <span style={{ marginLeft: "auto", fontSize: 26 }}>🔒</span>}
            </div>
          );
        })}
      </AbsoluteFill>
      <Caption>Locks the few real decisions.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 6 */
// CRITERIA wired to real commands.
const CRIT = [
  ['no callbacks left', 'grep "cb(" src/ → 0'],
  ["suite green", "npm test → exit 0"],
  ["contract unchanged", "separate agent ✓"],
];
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="success criteria → real commands" w={1180}>
          {CRIT.map(([k, v], i) => {
            const a = appear(f, fps, 6 + i * 10, 12);
            return (
              <div
                key={k}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 18,
                  height: 72,
                  opacity: a,
                  transform: `translateX(${interpolate(a, [0, 1], [-16, 0])}px)`,
                  fontSize: 30,
                }}
              >
                <Check size={28} color={C.green2} />
                <span style={{ color: C.text, width: 380 }}>{k}</span>
                <span style={{ color: C.clay, fontSize: 22 }}>→</span>
                <span style={{ color: C.blue, fontFamily: FONT_MONO }}>{v}</span>
              </div>
            );
          })}
        </Window>
      </AbsoluteFill>
      <Caption>The finish line is real commands.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 7 */
// /clear → your plan survives (the file persists).
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const wipe = interpolate(f, [6, 22], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  const s = spring({ frame: f - 26, fps, config: { damping: 12 } });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 46, color: C.clay, opacity: 1 - wipe }}>{">"} /clear</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.text, transform: `translateX(${interpolate(wipe, [0, 1], [-1920, 0])}px)` }} />
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 22, opacity: f > 24 ? 1 : 0 }}>
        <div
          style={{
            transform: `scale(${interpolate(s, [0, 1], [0.85, 1])})`,
            fontFamily: FONT_UI,
            fontWeight: 800,
            fontSize: 96,
            letterSpacing: -2,
            color: C.green1,
          }}
        >
          Your plan survives.
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 28, color: C.textDim }}>{">"} /goal ~/acme/.goal/cb-to-async.md</div>
      </AbsoluteFill>
    </Bg>
  );
};

/* =================================================================== scene 8 */
// Autonomous run — agents in parallel + tests + progress.
const RUN = ["routes.ts", "orders.ts", "db/pool.ts"];
const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const prog = interpolate(f, [16, dur - 24], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ticks = [0, 1, 2];
  return (
    <Bg>
      {/* three parallel worker cards */}
      {RUN.map((name, i) => (
        <AgentCard
          key={name}
          label={`editing ${name}`}
          cx={[470, 960, 1450][i]}
          cy={300}
          s={appear(f, fps, 6 + i * 5, 12)}
          doneAt={40 + i * 16}
          f={f}
          w={360}
        />
      ))}
      <AbsoluteFill style={{ ...center }}>
        <div style={{ width: 1180 }}>
          {/* test ticks */}
          <div style={{ display: "flex", gap: 40, justifyContent: "center", marginBottom: 40 }}>
            {ticks.map((i) => {
              const a = appear(f, fps, 54 + i * 12, 12);
              return (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, transform: `scale(${a})`, opacity: a }}>
                  <Check size={40} color={C.green2} />
                  <span style={{ fontFamily: FONT_MONO, fontSize: 28, color: C.text }}>{["build", "tests", "lint"][i]}</span>
                </div>
              );
            })}
          </div>
          {/* progress */}
          <div style={{ height: 18, borderRadius: 99, background: "#1A1F27", overflow: "hidden" }}>
            <div style={{ width: `${prog * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.clay}, ${C.clayHi})` }} />
          </div>
          <div style={{ marginTop: 16, textAlign: "center", fontFamily: FONT_MONO, fontSize: 26, color: C.clay }}>
            no human typing · {Math.round(prog * 100)}%
          </div>
        </div>
      </AbsoluteFill>
      <Caption>It runs the whole job — agents in parallel.</Caption>
    </Bg>
  );
};

/* =================================================================== scene 9 */
// VERIFY before done — a separate verifier re-derives the criteria.
const S9: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rows = ["no callbacks", "142 tests pass", "contract identical", "criteria 6 / 6"];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="verifier — re-derived from primaries" accent={C.blue} w={1080}>
          {rows.map((r, i) => {
            const a = appear(f, fps, 8 + i * 12, 12);
            const ok = f >= 14 + i * 12;
            return (
              <div key={r} style={{ display: "flex", alignItems: "center", gap: 16, height: 62, opacity: a, fontSize: 30, color: C.text }}>
                {ok ? <Check size={28} color={C.green2} /> : <span style={{ width: 28 }} />}
                {r}
              </div>
            );
          })}
        </Window>
      </AbsoluteFill>
      <Caption color={C.blue}>Verifies before it calls it done.</Caption>
    </Bg>
  );
};

/* ================================================================== scene 10 */
// MONEY SHOT.
const S10: React.FC = () => {
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
                <Check size={62} color={C.green2} />
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
          <span style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 100, letterSpacing: -2, color: C.green1 }}>
            GOAL COMPLETE
          </span>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ================================================================== scene 11 */
// SELF-DESTRUCT.
const S11: React.FC = () => {
  const f = useCurrentFrame();
  const path = "rm ~/acme/.goal/cb-to-async.md";
  const strike = interpolate(f, [22, 38], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dissolve = interpolate(f, [34, 46], [1, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — done" w={1020} style={{ opacity: dissolve }}>
          <div style={{ fontSize: 30, color: C.text, position: "relative" }}>
            <span style={{ color: C.clay, marginRight: 12 }}>{">"}</span>
            <span style={{ position: "relative" }}>
              {typed(path, f, 2, 0.9)}
              <span style={{ position: "absolute", left: 0, top: "52%", height: 3, width: `${strike * 100}%`, background: C.dotRed }} />
            </span>
            {f < 26 && <Caret h={30} />}
          </div>
        </Window>
      </AbsoluteFill>
      <Caption>Then it deletes itself.</Caption>
    </Bg>
  );
};

/* ================================================================== scene 12 */
// WORDMARK.
const S12: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = appear(f, fps, 0, 16);
  const underline = interpolate(f, [10, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 24 }}>
        <div style={{ opacity: s, transform: `translateY(${interpolate(s, [0, 1], [16, 0])}px)`, textAlign: "center" }}>
          <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 150, letterSpacing: -4, color: C.text }}>goalify</div>
          <div
            style={{
              height: 8,
              width: 430,
              margin: "8px auto 0",
              borderRadius: 99,
              background: C.clay,
              transform: `scaleX(${underline})`,
              transformOrigin: "left center",
            }}
          />
        </div>
        <div
          style={{
            opacity: interpolate(f, [20, 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            fontFamily: FONT_MONO,
            fontSize: 38,
            color: C.textDim,
            letterSpacing: 1,
          }}
        >
          set the goal. trust the run.
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ============================================================== composition */
const SCENES: [React.FC<any>, number, any?][] = [
  [S1, 54],
  [S2, 90],
  [S3, 96],
  [S4, 90],
  [S5, 54],
  [S6, 66],
  [S7, 60],
  [S8, 114, { dur: 114 }],
  [S9, 90],
  [S10, 78],
  [S11, 48],
  [S12, 48],
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
