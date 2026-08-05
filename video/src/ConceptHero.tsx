import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { P, FONT_UI, FONT_MONO, clamp, typed, rise, center, Bg, Fade, Caret, Check, Neon, Win, Prompt, Big, Sub, Col, Stat } from "./neon";

/* ===================== The goalify teaser — "Sleep on it" cut =====================
   Outcome-first kinetic typography bookends a live-terminal core. One idea per screen.
   Leads with the feeling (approve once, sleep, wake to a finished verified job), shows
   the real CLI writing the brief, running it overnight, and the checks flipping green,
   then an honest sample KPI, the advantages, and the after-state.
   No context-reset framing anywhere. */

// ---- terminal helpers (the "show, don't tell" core) ----
const Cap: React.FC<{ main: React.ReactNode; sub?: string }> = ({ main, sub }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = rise(f, fps, 6, 18);
  return (
    <div style={{ position: "absolute", top: 146, left: 0, right: 0, textAlign: "center", padding: "0 120px", opacity: s, transform: `translateY(${interpolate(s, [0, 1], [-12, 0])}px)` }}>
      <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 58, letterSpacing: -1.5, color: P.textHi, lineHeight: 1.06 }}>{main}</div>
      {sub && <div style={{ fontFamily: FONT_MONO, fontSize: 26, color: P.textDim, marginTop: 14 }}>{sub}</div>}
    </div>
  );
};
const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ ...center, paddingTop: 168 }}>{children}</AbsoluteFill>
);
// a typed-in command with a live caret
const TermCmd: React.FC<{ cmd: string; start: number; cpf?: number; size?: number }> = ({ cmd, start, cpf = 0.7, size = 33 }) => {
  const f = useCurrentFrame();
  const t = typed(cmd, f, start, cpf);
  const typing = t.length < cmd.length;
  return (
    <div style={{ fontSize: size, color: P.textHi, lineHeight: "54px" }}>
      <Prompt><span style={{ whiteSpace: "pre" }}>{t}</span>{f >= start && typing && <Caret h={31} />}</Prompt>
    </div>
  );
};
// a terminal output line that reveals at frame d
const TLine: React.FC<{ d: number; color?: string; indent?: number; children: React.ReactNode }> = ({ d, color = P.textHi, indent = 0, children }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < d) return null;
  const s = rise(f, fps, d, 12);
  return <div style={{ fontFamily: FONT_MONO, fontSize: 31, color, lineHeight: "52px", paddingLeft: indent, display: "flex", alignItems: "center", gap: 12, opacity: s, transform: `translateY(${interpolate(s, [0, 1], [6, 0])}px)` }}>{children}</div>;
};
// a check line that pops in green
const TCheck: React.FC<{ d: number; label: React.ReactNode }> = ({ d, label }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < d) return null;
  const s = rise(f, fps, d, 13);
  return <div style={{ fontFamily: FONT_MONO, fontSize: 33, color: P.textHi, lineHeight: "58px", display: "flex", alignItems: "center", gap: 16, opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.9, 1])})` }}><Check size={30} color={P.success} /> {label}</div>;
};

// 1 — HOOK: lead with the feeling / outcome (kinetic)
const S1: React.FC = () => (
  <Bg glowColor={P.success} glowAt="50% 86%" glowSize={46}>
    <Col>
      <Big>Approve once. Go to sleep.</Big>
      <Sub delay={18}>wake up to a finished, verified job</Sub>
    </Col>
  </Bg>
);

// 2 — WHAT IT IS: orient the cold viewer (kinetic)
const S2: React.FC = () => (
  <Bg glowColor={P.fill} glowAt="24% 22%">
    <Col>
      <Big><Neon color={P.glow} strength={40}>goalify</Neon> preps your task to run without you.</Big>
      <Sub delay={18}>a free Claude Code plugin</Sub>
    </Col>
  </Bg>
);

// a labelled artifact row — the tag colour is the lane, shared with the README's SVGs
const Artifact: React.FC<{ d: number; tag: string; value: string; color: string }> = ({ d, tag, value, color }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < d) return null;
  const s = rise(f, fps, d, 13);
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 20, lineHeight: "58px", opacity: s, transform: `translateY(${interpolate(s, [0, 1], [8, 0])}px)` }}>
      <span style={{ fontFamily: FONT_MONO, fontSize: 23, fontWeight: 700, letterSpacing: 2, color, minWidth: 262 }}>{tag}</span>
      <span style={{ fontFamily: FONT_MONO, fontSize: 30, color: P.textHi }}>{value}</span>
    </div>
  );
};

// 3 — WHAT COMES BACK: two artifacts, visibly separate and differently coloured
const S3: React.FC = () => (
  <Bg glowColor={P.fill} glowAt="22% 22%">
    <Cap main="Two things come back, not one." sub="a brief file, and a condition string" />
    <Stage>
      <Win title="claude code" w={1180}>
        <TermCmd cmd="/goalify migrate our API to async/await" start={12} cpf={1.1} />
        <TLine d={52} color={P.textDim}>↳ researching the repo · locking the real decisions</TLine>
        <Artifact d={72} tag="BRIEF FILE" value="~/acme/.goal/api-migration.md" color={P.laneA} />
        <Artifact d={92} tag="CONDITION STRING" value="Read the brief at ~/acme/.goal/api-migration.md," color={P.laneB} />
        <Artifact d={104} tag="" value="then npm test must pass …" color={P.laneB} />
      </Win>
    </Stage>
  </Bg>
);

// 4 — RUNS ALL NIGHT: the /goal beat. What follows /goal is PROSE, never a path.
const S4: React.FC = () => (
  <Bg glowColor={P.fill} glowAt="78% 24%">
    <Cap main="Then it runs the whole job, all night." sub="you paste the condition — /goal never takes a file path" />
    <Stage>
      <Win title="claude code" w={1180}>
        <TermCmd cmd="/goal Read the brief at ~/acme/.goal/api-migration.md, then npm test must pass" start={12} cpf={1.8} size={23} />
        <TLine d={60} color={P.textDim}>[01:12]  building the feature…</TLine>
        <TLine d={84} color={P.textDim}>[03:40]  writing the tests…</TLine>
        <TLine d={108} color={P.neon2}>[05:28]  all checks passing</TLine>
      </Win>
    </Stage>
  </Bg>
);

// 5 — VERIFY: separate verifier agents check the work (terminal climax)
const S5: React.FC = () => (
  <Bg glowColor={P.success} glowAt="50% 80%" glowSize={54}>
    <Cap main="It has to show its work before it says done." sub="separate agents verify it, not itself" />
    <Stage>
      <Win title="claude code" w={1180}>
        <TLine d={14} color={P.textDim}>↳ verifier agents reviewing the work…</TLine>
        <TCheck d={34} label="builds" />
        <TCheck d={54} label="npm test · 37 passing" />
        <TCheck d={76} label="every criterion green" />
      </Win>
    </Stage>
  </Bg>
);

// 6 — KPI: honest, illustrative sample run + the gated archive step (kinetic stat)
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const gone = interpolate(f, [70, 88], [1, 0.18], clamp);
  return (
    <Bg glowColor={P.success} glowAt="50% 28%" glowSize={50}>
      <Col gap={20}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 28, color: P.textDim, opacity: interpolate(f, [4, 16], [0, 1], clamp), letterSpacing: 2 }}>EXAMPLE RUN · 0 check-ins</div>
        <Stat n="37" label="checks · all green" delay={8} />
        <div style={{ fontFamily: FONT_MONO, fontSize: 30, color: P.neon2, opacity: gone, transform: `translateX(${(1 - gone) * 22}px)`, textShadow: `0 0 14px ${P.neon2}44` }}>
          <span style={{ color: P.textDim }}>then the brief archives itself ·</span> ~/acme/.goal/api-migration.md
        </div>
      </Col>
    </Bg>
  );
};

// 7 — WHAT YOU GET: the advantages (kinetic list)
const ADV: React.ReactNode[] = [
  <>A self-contained brief, not a vague to-do</>,
  <>The key decisions, locked up front</>,
  <>Done only when the tests pass</>,
  <>Free and open source</>,
];
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const h = rise(f, fps, 4, 18);
  return (
    <Bg glowColor={P.fill} glowAt="50% 12%" glowSize={46}>
      <div style={{ position: "absolute", top: 150, left: 0, right: 0, textAlign: "center", opacity: h, transform: `translateY(${interpolate(h, [0, 1], [-12, 0])}px)` }}>
        <div style={{ fontFamily: FONT_UI, fontWeight: 800, fontSize: 76, letterSpacing: -2, color: P.textHi }}>What you get.</div>
      </div>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 18, paddingTop: 120 }}>
        {ADV.map((t, i) => {
          const a = rise(f, fps, 18 + i * 11, 16);
          return (
            <div key={i} style={{ width: 920, transform: `translateX(${interpolate(a, [0, 1], [-26, 0])}px)`, opacity: a, display: "flex", alignItems: "center", gap: 22, padding: "16px 32px", borderRadius: 14, background: P.surface, border: `1px solid ${P.line}` }}>
              <Check size={34} color={P.success} />
              <span style={{ fontFamily: FONT_UI, fontWeight: 600, fontSize: 40, color: P.textHi }}>{t}</span>
            </div>
          );
        })}
      </AbsoluteFill>
    </Bg>
  );
};

// 8 — CTA: after-state + one command (kinetic, terminal caret)
const S8: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const word = rise(f, fps, 4, 16);
  const tag = interpolate(f, [16, 30], [0, 1], clamp);
  const box = rise(f, fps, 24, 16);
  const free = interpolate(f, [40, 54], [0, 1], clamp);
  return (
    <Bg glowColor={P.fill} glowAt="50% 18%" glowSize={50}>
      <AbsoluteFill style={{ ...center, flexDirection: "column", gap: 28 }}>
        <div style={{ opacity: word, transform: `translateY(${interpolate(word, [0, 1], [14, 0])}px)`, fontFamily: FONT_UI, fontWeight: 800, fontSize: 104, letterSpacing: -3, color: P.textHi, textShadow: `0 0 40px ${P.glow}55` }}>goalify</div>
        <div style={{ opacity: tag, fontFamily: FONT_UI, fontWeight: 600, fontSize: 42, color: P.textDim }}>No babysitting. Evidence you can check.</div>
        <div style={{ opacity: box, transform: `translateY(${interpolate(box, [0, 1], [14, 0])}px)`, borderRadius: 14, border: `1px solid ${P.neon1}66`, background: P.surface, padding: "24px 42px", fontFamily: FONT_MONO, fontSize: 40, color: P.textHi, boxShadow: `0 0 40px ${P.fill}30`, display: "flex", alignItems: "center" }}>
          <span style={{ color: P.success }}>$</span>&nbsp;claude plugin install&nbsp;<Neon color={P.neon1} strength={20}>goalify@10x</Neon>{f >= 30 && <Caret h={34} />}
        </div>
        <div style={{ opacity: free, fontFamily: FONT_MONO, fontSize: 30, color: P.success, letterSpacing: 2, textShadow: `0 0 18px ${P.success}66` }}>Free.</div>
      </AbsoluteFill>
    </Bg>
  );
};

const SCENES: [React.FC, number][] = [
  [S1, 92],  // hook — approve once, go to sleep
  [S2, 90],  // what it is
  [S3, 150], // what comes back: the two artifacts, named and colour-coded
  [S4, 150], // runs all night (the /goal beat — prose after /goal, never a path)
  [S5, 120], // verify climax (terminal: checks flip green)
  [S6, 104], // sample KPI + the gated archive step
  [S7, 110], // what you get (advantages)
  [S8, 100], // CTA
];

// Single source of truth for the composition length — Root.tsx imports this.
export const TEASER_FRAMES = SCENES.reduce((a, [, d]) => a + d, 0);

export const ConceptHero: React.FC = () => {
  let at = 0;
  return (
    <AbsoluteFill style={{ background: P.bg }}>
      <Audio src={staticFile("music.mp3")} volume={(fr) => interpolate(fr, [0, 16, TEASER_FRAMES - 32, TEASER_FRAMES], [0, 0.4, 0.4, 0], clamp)} />
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
