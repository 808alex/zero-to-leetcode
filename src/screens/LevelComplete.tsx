import type { Level } from "../types";
import { LEVELS } from "../content";
import { useProgress } from "../state";
import { Pip } from "../components/Mascot";
import { Heart } from "../components/Icons";
import { LeetCodeList } from "../components/LeetCodeList";

type Quick = { score: number; total: number; bestCombo: number; best: number };
type Props = { level: Level | null; quick: Quick | null; boss: boolean; hearts: number; total: number; seconds: number; nextId?: string; onContinue: () => void };

const fmt = (s: number) => (s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, "0")}s`);

export function LevelComplete({ level, quick, boss, hearts, total, seconds, nextId, onContinue }: Props) {
  const practice = !!quick;
  const { progress } = useProgress();
  const next = nextId ? LEVELS[nextId] : undefined;
  const title = quick ? (quick.score === quick.total ? "Perfect round!" : "Quickfire done") : boss ? "Boss defeated!" : "Level complete!";
  return (
    <div className="center-screen complete">
      <Pip mood={quick && quick.score < quick.total / 2 ? "think" : "cheer"} size={140} say={boss ? "You beat it!" : quick ? (quick.score >= quick.best && quick.score > 0 ? "New best!" : "Good reps.") : "Let's go!"} />
      <h1 className="pop-in">{title}</h1>
      {level && <p className="lede">{level.title}</p>}
      <div className="stat-row">
        {!practice && (
          <div className="stat-tile hearts-tile">
            <div className="stat-big">{Array.from({ length: 3 }, (_, i) => <Heart key={i} size={22} className={i < hearts ? "heart-on" : "heart-off"} />)}</div>
            <span>hearts left</span>
          </div>
        )}
        {quick ? (
          <>
            <div className="stat-tile"><div className="stat-big">{quick.score}/{quick.total}</div><span>right</span></div>
            <div className="stat-tile"><div className="stat-big">{quick.bestCombo}</div><span>best streak</span></div>
            <div className="stat-tile"><div className="stat-big">{quick.best}</div><span>personal best</span></div>
          </>
        ) : <div className="stat-tile"><div className="stat-big">{total}</div><span>questions</span></div>}
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
