import { useEffect, useState } from "react";
import { ProgressProvider, useProgress } from "./state";
import { PathScreen } from "./screens/PathScreen";
import { Session } from "./screens/Session";
import { AchievementsPanel, SettingsPanel } from "./screens/Panels";
import { Badge } from "./components/Icons";

type Screen =
  | { name: "path"; justDone?: string }
  | { name: "level"; id: string; start: "lesson" | "questions"; key: number }
  | { name: "practice"; key: number };

function Toasts() {
  const { toasts, dismissToast } = useProgress();
  useEffect(() => {
    if (!toasts.length) return;
    const t = setTimeout(() => dismissToast(toasts[0].id), 4200);
    return () => clearTimeout(t);
  }, [toasts, dismissToast]);
  return (
    <div className="toasts" aria-live="polite">
      {toasts.slice(0, 3).map((t) => (
        <button key={t.id} className="toast" onClick={() => dismissToast(t.id)}>
          <span className="toast-icon"><Badge name={t.achievement.icon} size={26} /></span>
          <span><strong>Achievement unlocked</strong><br />{t.achievement.name}</span>
        </button>
      ))}
    </div>
  );
}

function Game() {
  const [screen, setScreen] = useState<Screen>({ name: "path" });
  const [panel, setPanel] = useState<"" | "settings" | "achievements">("");
  const back = (completed?: string) => setScreen({ name: "path", justDone: completed });

  return (
    <>
      {screen.name === "path" && (
        <PathScreen justDone={screen.justDone}
          onStart={(id, start) => setScreen({ name: "level", id, start, key: Date.now() })}
          onPractice={() => setScreen({ name: "practice", key: Date.now() })}
          onAchievements={() => setPanel("achievements")}
          onSettings={() => setPanel("settings")} />
      )}
      {screen.name === "level" && <Session key={screen.key} kind="level" levelId={screen.id} start={screen.start} onExit={back} />}
      {screen.name === "practice" && <Session key={screen.key} kind="practice" onExit={() => back()} />}
      {panel === "settings" && <SettingsPanel onClose={() => setPanel("")} />}
      {panel === "achievements" && <AchievementsPanel onClose={() => setPanel("")} />}
      <Toasts />
    </>
  );
}

export default function App() {
  return <ProgressProvider><Game /></ProgressProvider>;
}
