import "./index.css";
import { Composition } from "remotion";
import { GoalifyTeaser } from "./GoalifyTeaser";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="GoalifyTeaser"
      component={GoalifyTeaser}
      durationInFrames={795}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
