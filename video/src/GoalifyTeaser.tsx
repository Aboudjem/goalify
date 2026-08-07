import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";

/* ===================== The goalify teaser — "Sunday Worktable" cut =====================
   The v2.5 re-script on the paper worktable system (see .goal/design-judgment-v25.md §3.5).
   One idea per screen, every frame a complete statement: no typing-on, no draw-ons, no
   terminal chrome. Beats cross-fade between complete compositions; inside a beat only
   emphasis moves (opacity 0.65→1). The /goal beat shows the full condition with all four
   teeth — the path, the quoted-evidence clause, the sentinel, the turn bound — visible
   simultaneously, each underlined and captioned in plain words. No frame anywhere shows
   the wrong form. */

// ---- worktable tokens (the SVG palette × the 2.1333 translation) ----
export const W = {
  paper: "#F6F1E8",
  sheet: "#FFFCF7",
  ink: "#263536",
  ink2: "#4C5654",
  briefInk: "#1B5A78",
  condInk: "#7A5200",
  condTint: "#F7E9C6",
  proofInk: "#265C43",
  rule: "#96896E",
  grain: "#EDE5D6",
};
export const FONT_SERIF = 'ui-serif, Georgia, "Times New Roman", serif';
export const FONT_SANS = 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
export const FONT_MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace';
const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

// the sunlit paper field: flat paper + white wash top-left + 13px grain
const Bg: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: W.paper }}>
    <AbsoluteFill style={{ background: `radial-gradient(60% 60% at 16% 4%, rgba(255,255,255,.55) 0%, transparent 70%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(circle at 1px 1px, ${W.grain} 1.3px, transparent 0)`, backgroundSize: "13px 13px", opacity: 0.5 }} />
    {children}
  </AbsoluteFill>
);

// scene-level cross-fade: 12-frame ramps; scenes overlap by the same 12 frames,
// so the screen always carries a complete composition
const XFADE = 12;
const Fade: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, XFADE, dur - XFADE, dur], [0, 1, 1, 0], clamp);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const Center: React.FC<{ children: React.ReactNode; gap?: number }> = ({ children, gap = 44 }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", gap }}>{children}</AbsoluteFill>
);
const Headline: React.FC<{ children: React.ReactNode; size?: number }> = ({ children, size = 136 }) => (
  <div style={{ fontFamily: FONT_SERIF, fontWeight: 700, fontSize: size, letterSpacing: -2, color: W.ink, textAlign: "center", lineHeight: 1.08, padding: "0 120px" }}>{children}</div>
);
const Caption: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = W.ink2 }) => (
  <div style={{ fontFamily: FONT_SANS, fontWeight: 500, fontSize: 60, color, textAlign: "center", lineHeight: 1.3, padding: "0 140px" }}>{children}</div>
);
// gentle breath for emphasis only — floor .94, 8s period
const breath = (f: number, period = 240) => 0.94 + 0.06 * Math.abs(Math.cos((Math.PI * f) / period));

// the BRIEF as an object: square sheet, folded corner, blue binding, ruled lines
const SheetCard: React.FC<{ w?: number }> = ({ w = 1100 }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ width: w, position: "relative", background: W.sheet, border: `3px solid ${W.rule}`, padding: "44px 56px 48px 78px", opacity: breath(f) }}>
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 21, background: W.briefInk }} />
      <div style={{ position: "absolute", right: 0, top: 0, borderStyle: "solid", borderWidth: "0 85px 85px 0", borderColor: `${W.paper} ${W.paper} ${W.grain} transparent` }} />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <span style={{ fontFamily: FONT_SANS, fontWeight: 800, fontSize: 72, color: W.briefInk }}>BRIEF</span>
        <span style={{ fontFamily: FONT_SANS, fontWeight: 700, fontSize: 60, letterSpacing: 3, color: W.briefInk, marginRight: 100 }}>A FILE</span>
      </div>
      <div style={{ fontFamily: FONT_MONO, fontSize: 60, color: W.ink, marginTop: 26 }}>~/acme/.goal/api-migration.md</div>
      <div style={{ height: 3, background: W.rule, opacity: 0.55, marginTop: 34, width: "92%" }} />
      <div style={{ height: 3, background: W.rule, opacity: 0.55, marginTop: 22, width: "78%" }} />
      <div style={{ height: 3, background: W.rule, opacity: 0.55, marginTop: 22, width: "86%" }} />
    </div>
  );
};

// the CONDITION as an object: ochre capsule label strip
const Plate: React.FC<{ children: React.ReactNode; w?: number; label?: string }> = ({ children, w = 1100, label = "CONDITION" }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ width: w, background: W.condTint, border: `5px solid ${W.condInk}`, borderRadius: 94, padding: "40px 64px", opacity: breath(f) }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <span style={{ fontFamily: FONT_SANS, fontWeight: 800, fontSize: 72, color: W.condInk }}>{label}</span>
        <span style={{ fontFamily: FONT_SANS, fontWeight: 700, fontSize: 60, letterSpacing: 3, color: W.condInk }}>ONE STRING</span>
      </div>
      {children}
    </div>
  );
};

const Chip: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ background: W.ink, color: W.sheet, borderRadius: 24, padding: "12px 40px", fontFamily: FONT_MONO, fontWeight: 700, fontSize: 64 }}>{children}</span>
);

// 1 — HOOK: the locked story, and nothing else
const S1: React.FC = () => (
  <Bg>
    <Center gap={52}>
      <Headline>Hand Claude a huge task.</Headline>
      <Caption>Come back to proof it's done — not a promise that it is.</Caption>
    </Center>
  </Bg>
);

// 2 — THE BRIEF: a sheet of paper, the full instructions
const S2: React.FC = () => (
  <Bg>
    <Center gap={56}>
      <Headline size={96}>goalify writes the brief —</Headline>
      <SheetCard />
      <Caption>a file with everything the run needs: your decisions, the paths, the order of work</Caption>
    </Center>
  </Bg>
);

// 3 — THE CONDITION: a label strip, the finish line
const S3: React.FC = () => (
  <Bg>
    <Center gap={56}>
      <Headline size={96}>— and the condition.</Headline>
      <Plate>
        <div style={{ fontFamily: FONT_MONO, fontSize: 60, color: W.ink, marginTop: 26 }}>Do everything in … and prove it …</div>
      </Plate>
      <Caption>one line that says what done must look like</Caption>
    </Center>
  </Bg>
);

// 4 — THE /goal BEAT: the full condition, all four teeth visible at once.
// Mono geometry: at 54px the advance is 32.4px, so the underlines are char-addressed.
const CH = 32.4;
const COND_LINES = [
  "Do everything in",
  "~/acme/.goal/api-migration.md",
  "and prove it — done when the last turn",
  "quotes npm test passing and says ASYNC-OK.",
  "Stop after 40 turns.",
];
// [line index, start char, char count] per tooth, in caption order
const TEETH: { seg: [number, number, number]; cap: string }[] = [
  { seg: [1, 0, 29], cap: "the path — where the work is written down" },
  { seg: [3, 0, 23], cap: "the proof it has to show you" },
  { seg: [3, 33, 9], cap: "a made-up word it has to say" },
  { seg: [4, 0, 20], cap: "when it has to stop" },
];
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const active = Math.floor(f / 40) % 4; // emphasis cycles; nothing appears or vanishes
  const em = (i: number) => (i === active ? 1 : 0.65);
  return (
    <Bg>
      <Center gap={40}>
        <div style={{ display: "flex", alignItems: "center", gap: 32 }}>
          <Chip>/goal</Chip>
          <span style={{ fontFamily: FONT_SANS, fontSize: 60, color: W.ink2 }}>Claude Code's built-in stop-check — you paste the whole line</span>
        </div>
        <div style={{ width: 1560, background: W.condTint, border: `5px solid ${W.condInk}`, borderRadius: 94, padding: "44px 82px" }}>
          {COND_LINES.map((ln, li) => (
            <div key={li} style={{ position: "relative", fontFamily: FONT_MONO, fontSize: 54, lineHeight: "80px", color: W.ink, whiteSpace: "pre" }}>
              {ln}
              {TEETH.map((t, ti) =>
                t.seg[0] === li ? (
                  <div key={ti} style={{ position: "absolute", left: t.seg[1] * CH, top: 70, width: t.seg[2] * CH, height: 5, background: W.condInk, opacity: em(ti) }} />
                ) : null
              )}
            </div>
          ))}
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "18px 64px", width: 1560 }}>
          {TEETH.map((t, ti) => (
            <div key={ti} style={{ display: "flex", alignItems: "center", gap: 20, opacity: em(ti) }}>
              <span style={{ width: 44, height: 5, background: W.condInk, flex: "none" }} />
              <span style={{ fontFamily: FONT_SANS, fontSize: 44, color: W.ink2 }}>{t.cap}</span>
            </div>
          ))}
        </div>
      </Center>
    </Bg>
  );
};

// 5 — THE RUN: live progress you can glance at
const ROWS = ["decisions locked before the start", "work ticked off step by step", "checks rerun after every change", "nothing lost if it stops"];
const S5: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Bg>
      <Center gap={48}>
        <Headline size={96}>The run works through it.</Headline>
        <div style={{ width: 1180, background: W.sheet, border: `3px solid ${W.rule}`, padding: "40px 64px", display: "flex", flexDirection: "column", gap: 26 }}>
          {ROWS.map((r, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 28, opacity: 0.75 + 0.25 * Math.abs(Math.cos((Math.PI * (f - i * 30)) / 240)) }}>
              <svg width="44" height="44" viewBox="0 0 26 26" fill="none"><path d="M4 14l6 6L22 6" stroke={W.briefInk} strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round" /></svg>
              <span style={{ fontFamily: FONT_SANS, fontSize: 56, color: W.ink }}>{r}</span>
            </div>
          ))}
        </div>
        <Caption>live progress you can glance at — no babysitting</Caption>
      </Center>
    </Bg>
  );
};

// 6 — PROOF: the closing turn, the one proof-colour moment
const S6: React.FC = () => (
  <Bg>
    <Center gap={48}>
      <div style={{ width: 1180, background: W.sheet, border: `4px solid ${W.proofInk}`, padding: "52px 72px", display: "flex", flexDirection: "column", gap: 30 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 32 }}>
          <svg width="64" height="64" viewBox="0 0 26 26" fill="none"><path d="M4 14l6 6L22 6" stroke={W.proofInk} strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round" /></svg>
          <span style={{ fontFamily: FONT_SANS, fontWeight: 800, fontSize: 80, color: W.proofInk }}>GOAL COMPLETE</span>
        </div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 60, color: W.ink2 }}>npm test ✓ · ASYNC-OK</div>
      </div>
      <Caption>the last turn quotes the checks passing and says the made-up word</Caption>
    </Center>
  </Bg>
);

// 7 — ARCHIVE: the brief comes to rest, in the brief's colour
const S7: React.FC = () => (
  <Bg>
    <Center gap={48}>
      <Headline size={96}>Then the brief files itself.</Headline>
      <div style={{ display: "flex", alignItems: "center", gap: 44 }}>
        <div style={{ width: 190, height: 190, background: W.sheet, border: `3px solid ${W.rule}`, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ width: 74, height: 74, background: W.briefInk }} />
        </div>
        <span style={{ fontFamily: FONT_MONO, fontSize: 60, color: W.ink2 }}>.goal/done/</span>
      </div>
      <Caption>a file move you can see in any file browser — proof, then filing</Caption>
    </Center>
  </Bg>
);

// 8 — CTA
const S8: React.FC = () => (
  <Bg>
    <Center gap={44}>
      <div style={{ fontFamily: FONT_SERIF, fontWeight: 700, fontSize: 150, letterSpacing: -3, color: W.ink }}>goalify</div>
      <Caption>Hand Claude a huge task. Come back to proof it's done — not a promise that it is.</Caption>
      <div style={{ background: W.sheet, border: `3px solid ${W.rule}`, borderRadius: 20, padding: "28px 52px", fontFamily: FONT_MONO, fontSize: 60, color: W.ink }}>
        claude plugin install goalify@10x
      </div>
      <div style={{ fontFamily: FONT_SANS, fontWeight: 700, fontSize: 56, color: W.ink2 }}>Free.</div>
    </Center>
  </Bg>
);

const SCENES: [React.FC, number][] = [
  [S1, 90],  // hook — the locked story
  [S2, 95],  // the brief: a sheet, the full instructions
  [S3, 95],  // the condition: a label, the finish line
  [S4, 170], // the /goal beat — all four teeth, underlined and captioned
  [S5, 120], // the run: live progress
  [S6, 120], // proof: GOAL COMPLETE quotes the checks
  [S7, 110], // archive: the brief comes to rest
  [S8, 120], // CTA
];

// Scenes overlap by XFADE frames so the cross-fade always sums to a full screen.
// Single source of truth for the composition length — Root.tsx imports this.
export const TEASER_FRAMES = SCENES.reduce((a, [, d]) => a + d, 0) - XFADE * (SCENES.length - 1);

export const GoalifyTeaser: React.FC = () => {
  let at = 0;
  return (
    <AbsoluteFill style={{ background: W.paper }}>
      <Audio src={staticFile("music.mp3")} volume={(fr) => interpolate(fr, [0, 16, TEASER_FRAMES - 32, TEASER_FRAMES], [0, 0.4, 0.4, 0], clamp)} />
      {SCENES.map(([Comp, dur], i) => {
        const from = at;
        at += dur - XFADE;
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
