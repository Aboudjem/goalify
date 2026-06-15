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

/* ------------------------------------------------------------------ helpers */

const Bg: React.FC<{ children?: React.ReactNode; flat?: boolean }> = ({
  children,
  flat,
}) => (
  <AbsoluteFill
    style={{
      background: flat
        ? C.bg1
        : `radial-gradient(120% 120% at 50% 18%, ${C.bg0} 0%, ${C.bg1} 70%, #06090d 100%)`,
    }}
  >
    {children}
  </AbsoluteFill>
);

const Fade: React.FC<{ dur: number; children: React.ReactNode }> = ({
  dur,
  children,
}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 7, dur - 7, dur], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const blink = (f: number, period = 30) => (f % period < period / 2 ? 1 : 0);

const typed = (text: string, f: number, start: number, cpf = 0.55) => {
  const n = Math.max(0, Math.floor((f - start) * cpf));
  return text.slice(0, n);
};

const Caret: React.FC<{ color?: string; h?: number }> = ({
  color = C.clay,
  h = 64,
}) => {
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

const Check: React.FC<{ size?: number; color?: string }> = ({
  size = 40,
  color = C.green2,
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M5 13l4 4L19 7"
      stroke={color}
      strokeWidth={3}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

// Caption: large, high-contrast, muted-safe. Bottom-anchored.
const Caption: React.FC<{ children: React.ReactNode; clay?: boolean }> = ({
  children,
  clay,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 18 });
  const y = interpolate(s, [0, 1], [26, 0]);
  return (
    <div
      style={{
        position: "absolute",
        bottom: 96,
        left: 0,
        right: 0,
        textAlign: "center",
        transform: `translateY(${y}px)`,
        opacity: s,
        padding: "0 120px",
      }}
    >
      <span
        style={{
          fontFamily: FONT_UI,
          fontWeight: 700,
          fontSize: 58,
          letterSpacing: -1,
          color: clay ? C.clayHi : C.text,
          textShadow: "0 2px 24px rgba(0,0,0,0.55)",
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
  style?: React.CSSProperties;
}> = ({ children, title = "claude code", w = 1180, style }) => (
  <div
    style={{
      width: w,
      borderRadius: 18,
      background: C.card,
      border: `1px solid ${C.line}`,
      boxShadow: "0 40px 120px rgba(0,0,0,0.55)",
      overflow: "hidden",
      ...style,
    }}
  >
    <div
      style={{
        height: 52,
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "0 22px",
        background: "#0C1117",
        borderBottom: `1px solid ${C.line}`,
      }}
    >
      <span style={{ width: 15, height: 15, borderRadius: 99, background: C.dotRed }} />
      <span style={{ width: 15, height: 15, borderRadius: 99, background: C.dotYellow }} />
      <span style={{ width: 15, height: 15, borderRadius: 99, background: C.dotGreen }} />
      <span
        style={{
          marginLeft: 16,
          fontFamily: FONT_MONO,
          fontSize: 22,
          color: C.textDim,
        }}
      >
        {title}
      </span>
    </div>
    <div style={{ padding: "34px 40px", fontFamily: FONT_MONO }}>{children}</div>
  </div>
);

const center: React.CSSProperties = {
  alignItems: "center",
  justifyContent: "center",
};

/* ------------------------------------------------------------------- scene 1 */
// HOOK (0-2s): clay prompt types the hook line.
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const line = "Big task. Context's about to run out.";
  return (
    <Bg>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 40 }}>
        <div
          style={{
            fontFamily: FONT_MONO,
            fontSize: 70,
            color: C.text,
            maxWidth: 1500,
            textAlign: "center",
            lineHeight: 1.25,
          }}
        >
          <span style={{ color: C.clay, marginRight: 18 }}>&gt;</span>
          {typed(line, f, 6, 0.85)}
          <Caret h={62} />
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 2 */
// (2-4s): "One session isn't enough." + a near-full context meter.
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const fill = interpolate(f, [0, 38], [0.62, 0.99], { extrapolateRight: "clamp" });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 56 }}>
        <div
          style={{
            fontFamily: FONT_UI,
            fontWeight: 800,
            fontSize: 96,
            letterSpacing: -2,
            color: C.text,
          }}
        >
          One session isn&rsquo;t enough.
        </div>
        <div style={{ width: 760 }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontFamily: FONT_MONO,
              fontSize: 24,
              color: C.textDim,
              marginBottom: 14,
            }}
          >
            <span>context window</span>
            <span style={{ color: fill > 0.9 ? C.dotRed : C.textDim }}>
              {Math.round(fill * 100)}%
            </span>
          </div>
          <div
            style={{
              height: 18,
              borderRadius: 99,
              background: "#1A1F27",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${fill * 100}%`,
                height: "100%",
                background: `linear-gradient(90deg, ${C.clay}, ${C.dotRed})`,
              }}
            />
          </div>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 3 */
// (4-7s): /goalify writes the goal.md — decisions + finish line stream in.
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cmd = "/goalify migrate the API to async/await";
  const rows = [
    { t: "scope locked", k: "·" },
    { t: "decisions locked", k: "·" },
    { t: "success criteria → npm test", k: "·" },
  ];
  const cardS = spring({ frame: f - 40, fps, config: { damping: 200 }, durationInFrames: 22 });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goalify">
          <div style={{ fontSize: 34, color: C.text, height: 52 }}>
            <span style={{ color: C.clay, marginRight: 14 }}>&gt;</span>
            {typed(cmd, f, 2, 0.7)}
            {f < 60 && <Caret h={34} />}
          </div>
          <div
            style={{
              marginTop: 26,
              opacity: cardS,
              transform: `translateY(${interpolate(cardS, [0, 1], [22, 0])}px)`,
              borderRadius: 12,
              border: `1px solid ${C.line}`,
              background: "#0C1015",
              padding: "24px 28px",
            }}
          >
            <div style={{ fontSize: 28, color: C.clay, marginBottom: 18 }}>
              ~/acme/.goal/cb-to-async.md
            </div>
            {rows.map((r, i) => {
              const a = spring({
                frame: f - (58 + i * 16),
                fps,
                config: { damping: 200 },
                durationInFrames: 14,
              });
              return (
                <div
                  key={r.t}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 16,
                    fontSize: 30,
                    color: C.text,
                    opacity: a,
                    transform: `translateX(${interpolate(a, [0, 1], [-18, 0])}px)`,
                    marginBottom: 12,
                  }}
                >
                  <Check size={30} color={C.green2} />
                  {r.t}
                </div>
              );
            })}
          </div>
        </Window>
      </AbsoluteFill>
      <Caption clay>goalify locks the decisions &amp; the finish line.</Caption>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 4 */
// (7-9s): /clear — white wipe to a fresh empty session.
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const wipe = interpolate(f, [22, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 64, color: C.text }}>
          <span style={{ color: C.clay, marginRight: 16 }}>&gt;</span>
          {typed("/clear", f, 2, 0.55)}
          {f < 24 && <Caret h={58} />}
        </div>
      </AbsoluteFill>
      {/* wipe panel */}
      <AbsoluteFill
        style={{
          background: C.text,
          transform: `translateX(${interpolate(wipe, [0, 1], [-1920, 0])}px)`,
        }}
      />
      {/* fresh empty session revealed under the trailing edge */}
      <AbsoluteFill
        style={{
          background: C.bg1,
          transform: `translateX(${interpolate(wipe, [0, 1], [-1920, 0])}px)`,
          opacity: wipe > 0.98 ? 1 : 0,
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 80,
            left: 90,
            fontFamily: FONT_MONO,
            fontSize: 40,
            color: C.textDim,
          }}
        >
          <span style={{ color: C.clay }}>&gt;</span> <Caret h={36} />
        </div>
      </AbsoluteFill>
      <Caption>Then you /clear.</Caption>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 5 */
// (9-10s): "Your plan survives." — the file persists.
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12, mass: 0.8 } });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 28 }}>
        <div
          style={{
            transform: `scale(${interpolate(s, [0, 1], [0.8, 1])})`,
            fontFamily: FONT_UI,
            fontWeight: 800,
            fontSize: 110,
            letterSpacing: -3,
            color: C.green1,
          }}
        >
          Your plan survives.
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 30, color: C.textDim }}>
          /goal ~/acme/.goal/cb-to-async.md
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 6 */
// (10-18s): autonomous run montage — edits, tests, progress, no human typing.
const LOG: { t: string; ok?: boolean; run?: boolean }[] = [
  { t: "edited   src/api/orders.ts", ok: true },
  { t: "edited   src/api/users.ts", ok: true },
  { t: "edited   src/db/pool.ts", ok: true },
  { t: "running  npm test …", run: true },
  { t: "tests    142 passed", ok: true },
  { t: "verify   success criteria", run: true },
  { t: "criteria 6 / 6 met", ok: true },
  { t: "commit   green, working tree clean", ok: true },
];
const SUBLINES = ["editing files…", "running tests…", "verifying criteria…"];

const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const prog = interpolate(f, [10, dur - 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const sub = SUBLINES[Math.min(SUBLINES.length - 1, Math.floor(f / 74))];
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — /goal (running)" w={1240}>
          <div style={{ height: 360 }}>
            {LOG.map((l, i) => {
              const at = 14 + i * 22;
              const a = spring({
                frame: f - at,
                fps,
                config: { damping: 200 },
                durationInFrames: 10,
              });
              if (f < at) return null;
              return (
                <div
                  key={l.t}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 16,
                    fontSize: 30,
                    lineHeight: "44px",
                    color: l.ok ? C.text : C.textDim,
                    opacity: a,
                    transform: `translateY(${interpolate(a, [0, 1], [10, 0])}px)`,
                  }}
                >
                  {l.ok ? (
                    <Check size={28} color={C.green2} />
                  ) : (
                    <span style={{ color: C.clay, width: 28, textAlign: "center" }}>
                      ·
                    </span>
                  )}
                  <span>{l.t}</span>
                </div>
              );
            })}
          </div>
          {/* clay progress bar */}
          <div style={{ marginTop: 8 }}>
            <div
              style={{
                height: 16,
                borderRadius: 99,
                background: "#1A1F27",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${prog * 100}%`,
                  height: "100%",
                  background: `linear-gradient(90deg, ${C.clay}, ${C.clayHi})`,
                }}
              />
            </div>
            <div
              style={{
                marginTop: 14,
                fontFamily: FONT_MONO,
                fontSize: 26,
                color: C.clay,
              }}
            >
              {sub}
            </div>
          </div>
        </Window>
      </AbsoluteFill>
      <Caption>It runs the whole job itself.</Caption>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 7 */
// (18-22s): MONEY SHOT — green GOAL COMPLETE pop.
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 6, fps, config: { damping: 9, mass: 0.9 } });
  const glow = interpolate(Math.sin(f / 9), [-1, 1], [0.35, 0.85]);
  const ticks = [0, 1, 2];
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 50 }}>
        <div style={{ display: "flex", gap: 26 }}>
          {ticks.map((i) => {
            const a = spring({
              frame: f - (i * 7),
              fps,
              config: { damping: 11 },
              durationInFrames: 12,
            });
            return (
              <div key={i} style={{ transform: `scale(${a})` }}>
                <Check size={64} color={C.green2} />
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
            boxShadow: `0 0 ${60 * glow}px ${18 * glow}px rgba(63,185,80,${0.45 * glow})`,
          }}
        >
          <Check size={84} color={C.green1} />
          <span
            style={{
              fontFamily: FONT_UI,
              fontWeight: 800,
              fontSize: 104,
              letterSpacing: -2,
              color: C.green1,
            }}
          >
            GOAL COMPLETE
          </span>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 8 */
// (22-25s): self-destruct — rm the goal file, strike-through dissolves.
const S8: React.FC = () => {
  const f = useCurrentFrame();
  const path = "rm ~/acme/.goal/cb-to-async.md";
  const strike = interpolate(f, [42, 64], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const dissolve = interpolate(f, [60, 80], [1, 0.12], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <Bg>
      <AbsoluteFill style={{ ...center }}>
        <Window title="claude code — done" w={1080} style={{ opacity: dissolve }}>
          <div style={{ fontSize: 34, color: C.text, position: "relative" }}>
            <span style={{ color: C.clay, marginRight: 14 }}>&gt;</span>
            <span style={{ position: "relative" }}>
              {typed(path, f, 2, 0.7)}
              <span
                style={{
                  position: "absolute",
                  left: 0,
                  top: "52%",
                  height: 3,
                  width: `${strike * 100}%`,
                  background: C.dotRed,
                }}
              />
            </span>
            {f < 40 && <Caret h={34} />}
          </div>
          <div
            style={{
              marginTop: 22,
              fontSize: 28,
              color: C.textDim,
              opacity: interpolate(f, [66, 78], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            file removed · nothing left behind
          </div>
        </Window>
      </AbsoluteFill>
      <Caption>Every criterion verified. The file deletes itself.</Caption>
    </Bg>
  );
};

/* ------------------------------------------------------------------- scene 9 */
// (25-26.5s): wordmark + clay underline.
const S9: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 200 }, durationInFrames: 16 });
  const underline = interpolate(f, [12, 34], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  return (
    <Bg flat>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 26 }}>
        <div
          style={{
            opacity: s,
            transform: `translateY(${interpolate(s, [0, 1], [18, 0])}px)`,
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: FONT_UI,
              fontWeight: 800,
              fontSize: 150,
              letterSpacing: -4,
              color: C.text,
            }}
          >
            goalify
          </div>
          <div
            style={{
              height: 8,
              width: 430,
              margin: "10px auto 0",
              borderRadius: 99,
              background: C.clay,
              transform: `scaleX(${underline})`,
              transformOrigin: "left center",
            }}
          />
        </div>
        <div
          style={{
            opacity: interpolate(f, [22, 38], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            fontFamily: FONT_MONO,
            fontSize: 40,
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

/* --------------------------------------------------------------- composition */
export const GoalifyTeaser: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: C.bg1 }}>
      <Sequence from={0} durationInFrames={60}>
        <Fade dur={60}>
          <S1 />
        </Fade>
      </Sequence>
      <Sequence from={60} durationInFrames={60}>
        <Fade dur={60}>
          <S2 />
        </Fade>
      </Sequence>
      <Sequence from={120} durationInFrames={90}>
        <Fade dur={90}>
          <S3 />
        </Fade>
      </Sequence>
      <Sequence from={210} durationInFrames={60}>
        <Fade dur={60}>
          <S4 />
        </Fade>
      </Sequence>
      <Sequence from={270} durationInFrames={30}>
        <Fade dur={30}>
          <S5 />
        </Fade>
      </Sequence>
      <Sequence from={300} durationInFrames={240}>
        <Fade dur={240}>
          <S6 dur={240} />
        </Fade>
      </Sequence>
      <Sequence from={540} durationInFrames={120}>
        <Fade dur={120}>
          <S7 />
        </Fade>
      </Sequence>
      <Sequence from={660} durationInFrames={90}>
        <Fade dur={90}>
          <S8 />
        </Fade>
      </Sequence>
      <Sequence from={750} durationInFrames={45}>
        <Fade dur={45}>
          <S9 />
        </Fade>
      </Sequence>
    </AbsoluteFill>
  );
};
