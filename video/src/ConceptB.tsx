import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { P, FONT_UI, FONT_MONO, clamp, rise, center, Bg, Fade, Check, Neon, CtaNeon } from "./neon";

/* ===================== Concept B — Bold Kinetic Typography =====================
   Big bold words own the screen. One neon hero word per beat. Real commands
   appear as small mono chips inside the headline, not a full terminal. */

const Big: React.FC<{ children: React.ReactNode; size?: number }> = ({ children, size = 94 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = rise(f, fps, 4, 22);
  return (
    <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: size, letterSpacing: -2.5, color: P.textHi, textAlign: "center", lineHeight: 1.04, padding: "0 110px", transform: `scale(${interpolate(s, [0, 1], [0.93, 1])})`, opacity: s }}>
      {children}
    </div>
  );
};

const Chip: React.FC<{ children: React.ReactNode; color?: string; delay?: number }> = ({ children, color = P.neon1, delay = 0 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = rise(f, fps, delay, 16);
  return (
    <span
      style={{
        display: "inline-block",
        fontFamily: FONT_MONO,
        fontSize: 33,
        color: P.textHi,
        background: P.surface,
        border: `1px solid ${color}88`,
        borderRadius: 11,
        padding: "8px 18px",
        boxShadow: `0 0 22px ${color}33`,
        opacity: s,
        transform: `translateY(${interpolate(s, [0, 1], [10, 0])}px)`,
      }}
    >
      {children}
    </span>
  );
};

const Col: React.FC<{ children: React.ReactNode; gap?: number }> = ({ children, gap = 40 }) => (
  <AbsoluteFill style={{ ...center, flexDirection: "column", gap }}>{children}</AbsoluteFill>
);

const Sub: React.FC<{ children: React.ReactNode; delay?: number }> = ({ children, delay = 14 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [delay, delay + 14], [0, 1], clamp);
  return <div style={{ fontFamily: FONT_UI, fontWeight: 500, fontSize: 40, color: P.textDim, opacity: o, display: "flex", alignItems: "center", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>{children}</div>;
};

// 1 — pain
const B1: React.FC = () => (
  <Bg glowColor={P.danger} glowAt="78% 76%">
    <Col>
      <Big>Big tasks forget the plan.</Big>
      <Sub delay={16}>It dies the moment you <Chip color={P.neon1} delay={20}>/clear</Chip></Sub>
    </Col>
  </Bg>
);

// 2 — what it is
const B2: React.FC = () => (
  <Bg glowColor={P.fill} glowAt="24% 22%">
    <Col>
      <Big><Neon color={P.glow} strength={40}>goalify</Neon> writes the goal.</Big>
      <Sub delay={16}>so a fresh session can finish it</Sub>
    </Col>
  </Bg>
);

// 3 — write
const B3: React.FC = () => (
  <Bg glowColor={P.fill} glowAt="22% 26%">
    <Col gap={36}>
      <Big>One command writes the file.</Big>
      <Sub delay={16}><Chip color={P.neon1} delay={18}>/goalify &lt;task&gt;</Chip></Sub>
      <div style={{ fontFamily: FONT_MONO, fontSize: 30, color: P.neon2, opacity: 1, textShadow: `0 0 16px ${P.neon2}55` }}>↳ .goal/auth.md</div>
    </Col>
  </Bg>
);

// 4 — run
const B4: React.FC = () => {
  const f = useCurrentFrame();
  const sweep = interpolate(f, [40, 96], [0, 1], clamp);
  return (
    <Bg glowColor={P.fill} glowAt="78% 26%">
      <Col gap={36}>
        <Big>A clean session runs it.</Big>
        <Sub delay={16}>
          <Chip color={P.neon1} delay={18}>/clear</Chip>
          <Chip color={P.neon2} delay={26}>/goal .goal/auth.md</Chip>
        </Sub>
        <div style={{ width: 620, height: 5, borderRadius: 99, background: "#2A1A47", overflow: "hidden" }}>
          <div style={{ width: `${sweep * 100}%`, height: "100%", background: P.neon1, boxShadow: `0 0 16px ${P.neon1}` }} />
        </div>
      </Col>
    </Bg>
  );
};

// 5 — verify + self-delete
const B5: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Bg glowColor={P.success} glowAt="50% 78%" glowSize={55}>
      <Col gap={40}>
        <Big><Neon color={P.success} strength={34}>Every check passes.</Neon></Big>
        <div style={{ display: "flex", gap: 26 }}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{ transform: `scale(${rise(f, fps, 10 + i * 8, 14)})` }}>
              <Check size={56} color={P.success} />
            </div>
          ))}
        </div>
        <Sub delay={40}>the goal file deletes itself</Sub>
      </Col>
    </Bg>
  );
};

const SCENES: [React.FC, number][] = [
  [B1, 108],
  [B2, 108],
  [B3, 108],
  [B4, 114],
  [B5, 120],
  [CtaNeon, 102],
];

export const ConceptB: React.FC = () => {
  let at = 0;
  return (
    <AbsoluteFill style={{ background: P.bg }}>
      <Audio src={staticFile("music.mp3")} volume={(fr) => interpolate(fr, [0, 16, 628, 660], [0, 0.4, 0.4, 0], clamp)} />
      {SCENES.map(([Comp, dur], i) => {
        const from = at;
        at += dur;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Fade dur={dur}>
              <Comp />
            </Fade>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
