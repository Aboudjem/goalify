import "./index.css";
import { Composition } from "remotion";
import { GoalifyTeaser, TEASER_FRAMES } from "./GoalifyTeaser";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="GoalifyTeaser" component={GoalifyTeaser} durationInFrames={TEASER_FRAMES} fps={30} width={1920} height={1080} />
    </>
  );
};
