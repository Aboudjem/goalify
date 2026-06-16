import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

/* ===== Deep Plum Neon palette (WCAG-checked: off-white body 16.96:1 on bg;
   neon1 4.8:1, neon2 10.51:1, success 13.58:1, danger 6.46:1 as LARGE text only.
   fill/glowDeep are for glow + fills ONLY, never readable words.) ===== */
export const P = {
  bg: "#150A28",
  bgDeep: "#0C0518",
  surface: "#1E0F38",
  line: "#33215C",
  textHi: "#F4F0FF",
  textDim: "#CFC4E8",
  neon1: "#A855F7", // violet
  neon2: "#22D3EE", // cyan
  success: "#34F5C5", // neon green — reserved for the verify/self-delete climax + CTA tag
  danger: "#FF5C8A",
  glow: "#DF00FF", // magenta — glow / large hero only
  fill: "#8A00FF", // glow / fill ONLY, never text
};

export const FONT_UI = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
export const FONT_MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace';

export const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
export const blink = (f: number, p = 32) => (f % p < p / 2 ? 1 : 0);
export const typed = (t: string, f: number, start: number, cpf = 0.55) =>
  t.slice(0, Math.max(0, Math.floor((f - start) * cpf)));
export const rise = (f: number, fps: number, delay: number, d = 18) =>
  spring({ frame: f - delay, fps, config: { damping: 200 }, durationInFrames: d });
export const center: React.CSSProperties = { alignItems: "center", justifyContent: "center" };

// deep-plum gradient + faint grid + up to one soft neon glow blob (never pure black)
export const Bg: React.FC<{ children?: React.ReactNode; glowColor?: string; glowAt?: string; glowSize?: number }> = ({
  children,
  glowColor = P.fill,
  glowAt = "20% 24%",
  glowSize = 42,
}) => (
  <AbsoluteFill style={{ background: `radial-gradient(135% 135% at 50% 10%, ${P.bg} 0%, ${P.bgDeep} 70%, #060312 100%)` }}>
    <AbsoluteFill style={{ background: `radial-gradient(${glowSize}% ${glowSize}% at ${glowAt}, ${glowColor}2E 0%, transparent 70%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(circle at 1px 1px, #2A1A47 1.1px, transparent 0)`, backgroundSize: "50px 50px", opacity: 0.22 }} />
    {children}
  </AbsoluteFill>
);

export const Fade: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 14, dur - 14, dur], [0, 1, 1, 0], clamp); // long ~0.47s cross-fades
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

export const Caret: React.FC<{ h?: number; color?: string }> = ({ h = 34, color = P.neon1 }) => {
  const f = useCurrentFrame();
  return (
    <span
      style={{
        display: "inline-block",
        width: h * 0.5,
        height: h,
        marginLeft: 6,
        marginBottom: -h * 0.1,
        background: color,
        boxShadow: `0 0 12px ${color}`,
        opacity: blink(f),
        borderRadius: 3,
      }}
    />
  );
};

export const Check: React.FC<{ size?: number; color?: string }> = ({ size = 28, color = P.success }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{ filter: `drop-shadow(0 0 7px ${color}cc)` }}>
    <path d="M5 13l4 4L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

// a small neon-glowing word inside a line
export const Neon: React.FC<{ children: React.ReactNode; color?: string; strength?: number }> = ({ children, color = P.neon1, strength = 22 }) => (
  <span style={{ color, textShadow: `0 0 ${strength}px ${color}99` }}>{children}</span>
);

// a real terminal window, plum-tinted with a faint neon edge
export const Win: React.FC<{ children: React.ReactNode; title?: string; w?: number; bright?: number; edge?: string }> = ({
  children,
  title = "claude code",
  w = 1160,
  bright = 1,
  edge = P.line,
}) => (
  <div
    style={{
      width: w,
      borderRadius: 18,
      background: P.surface,
      border: `1px solid ${edge}`,
      boxShadow: `0 50px 130px rgba(0,0,0,0.6), 0 0 0 1px ${P.line}`,
      overflow: "hidden",
      opacity: bright,
    }}
  >
    <div style={{ height: 50, display: "flex", alignItems: "center", gap: 9, padding: "0 22px", background: "#170B2E", borderBottom: `1px solid ${P.line}` }}>
      <span style={{ width: 13, height: 13, borderRadius: 99, background: P.danger }} />
      <span style={{ width: 13, height: 13, borderRadius: 99, background: "#F6C945" }} />
      <span style={{ width: 13, height: 13, borderRadius: 99, background: P.success }} />
      <span style={{ marginLeft: 16, fontFamily: FONT_MONO, fontSize: 20, color: P.textDim }}>{title}</span>
    </div>
    <div style={{ padding: "32px 40px", fontFamily: FONT_MONO, minHeight: 190 }}>{children}</div>
  </div>
);

export const Prompt: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span>
    <span style={{ color: P.neon1, marginRight: 14 }}>{">"}</span>
    {children}
  </span>
);

// shared CTA hold — one static, copy-pasteable install line; loops back to the plum hook
export const CtaNeon: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = rise(f, fps, 6, 18);
  const box = rise(f, fps, 18, 16);
  return (
    <Bg glowColor={P.fill} glowAt="50% 18%" glowSize={50}>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 34 }}>
        <div style={{ opacity: s, transform: `translateY(${interpolate(s, [0, 1], [14, 0])}px)`, textAlign: "center" }}>
          <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 104, letterSpacing: -3, color: P.textHi, textShadow: `0 0 40px ${P.glow}55` }}>goalify</div>
        </div>
        <div style={{ opacity: box, transform: `translateY(${interpolate(box, [0, 1], [14, 0])}px)`, borderRadius: 14, border: `1px solid ${P.neon1}66`, background: P.surface, padding: "24px 42px", fontFamily: FONT_MONO, fontSize: 40, color: P.textHi, boxShadow: `0 0 40px ${P.fill}30` }}>
          <span style={{ color: P.success }}>$</span> claude plugin install <Neon color={P.neon1} strength={20}>goalify@10x</Neon>
        </div>
        <div style={{ opacity: interpolate(f, [22, 36], [0, 1], clamp), fontFamily: FONT_MONO, fontSize: 30, color: P.success, letterSpacing: 2, textShadow: `0 0 18px ${P.success}66` }}>Free.</div>
      </AbsoluteFill>
    </Bg>
  );
};
