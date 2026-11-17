import type { Level } from "../types";
import { LEVELS } from "../content";
import { useProgress } from "../state";
import { Pip } from "../components/Mascot";
import { Heart } from "../components/Icons";
import { LeetCodeList } from "../components/LeetCodeList";

type Props = { level: Level | null; practice: boolean; boss: boolean; hearts: number; total: number; seconds: number; nextId?: string; onContinue: () => void };

const fmt = (s: number) => (s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, "0")}s`);

export function LevelComplete({ level, practice, boss, hearts, total, seconds, nextId, onContinue }: Props) {
  const { progress } = useProgress();
  const next = nextId ? LEVELS[nextId] : undefined;
  const title = practice ? "Practice done" : boss ? "Boss defeated!" : "Level complete!";
  return (
    <div className="center-screen complete">
      <Pip mood="cheer" size={140} say={boss ? "You beat it!" : practice ? "Good reps." : "Let's go!"} />
      <h1 className="pop-in">{title}</h1>
      {level && <p className="lede">{level.title}</p>}
      <div className="stat-row">
        {!practice && (
          <div className="stat-tile hearts-tile">
            <div className="stat-big">{Array.from({ length: 3 }, (_, i) => <Heart key={i} size={22} className={i < hearts ? "heart-on" : "heart-off"} />)}</div>
            <span>hearts left</span>
          </div>
        )}
        <div className="stat-tile"><div className="stat-big">{total}</div><span>{practice ? "answered" : "questions"}</span></div>
        <div className="stat-tile"><div className="stat-big">{fmt(seconds)}</div><span>time</span></div>
      </div>
      {level && level.lc.length > 0 && (
        <div className="complete-lc">
          <h3>Take it to LeetCode</h3>
          <p className="muted small">Try these on leetcode.com and tick off the ones you solve without looking at the answer.</p>
          <LeetCodeList problems={level.lc} />
        </div>
      )}
      {next && !progress.done[next.id] && <p className="muted">Next up: <strong>{next.title}</strong></p>}
      <button className="btn primary big" onClick={onContinue} autoFocus>Continue</button>
    </div>
  );
}
