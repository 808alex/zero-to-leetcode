import { useEffect, useLayoutEffect, useState } from "react";
import { LEVELS, UNITS, levelQuestions } from "../content";
import type { Level } from "../types";
import { useProgress, achievementCount } from "../state";
import { streakOf } from "../lib/storage";
import { play } from "../lib/sound";
import { Pip } from "../components/Mascot";
import { Check, Crown, Dumbbell, Flame, Gear, Lock, Star, Trophy, Book, Play } from "../components/Icons";
import { ACHIEVEMENTS } from "../lib/achievements";

type Props = {
  justDone?: string;
  onStart: (levelId: string, start: "lesson" | "questions") => void;
  onPractice: () => void;
  onAchievements: () => void;
  onSettings: () => void;
};

const OFFSETS = [0, 62, 96, 62, 0, -62, -96, -62];
const STEP = 112;
const TOP = 100;

export function PathScreen({ justDone, onStart, onPractice, onAchievements, onSettings }: Props) {
  const { progress, isUnlocked, currentLevel } = useProgress();
  const [open, setOpen] = useState<string | null>(null);
  const [shake, setShake] = useState<string | null>(null);
  const streak = streakOf(progress.days);
  const missed = Object.keys(progress.missed).length;
  const nextAfterDone = justDone ? currentLevel : null;

  useLayoutEffect(() => {
    const el = document.querySelector<HTMLElement>(".node.current");
    el?.scrollIntoView({ block: "center", behavior: justDone ? "smooth" : "auto" });
  }, [justDone]);

  useEffect(() => {
    if (nextAfterDone) { const t = setTimeout(() => play("unlock"), 500); return () => clearTimeout(t); }
  }, [nextAfterDone]);

  useEffect(() => {
    const close = (e: MouseEvent) => { if (!(e.target as HTMLElement).closest(".node-wrap")) setOpen(null); };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(null); };
    addEventListener("mousedown", close);
    addEventListener("keydown", esc);
    return () => { removeEventListener("mousedown", close); removeEventListener("keydown", esc); };
  }, []);

  const totalLevels = UNITS.reduce((n, u) => n + u.levels.length + 1, 0);
  const doneCount = Object.keys(progress.done).length;

  return (
    <div className="path-screen">
      <header className="topnav">
        <div className="brand">
          <Pip size={40} mood="happy" />
          <div>
            <div className="brand-name">Zero to LeetCode</div>
            <div className="brand-sub">{doneCount} of {totalLevels} levels</div>
          </div>
        </div>
        <div className="topnav-right">
          <div className={`streak ${streak.activeToday ? "lit" : ""}`} title={streak.activeToday ? "Streak: you've practised today" : "Answer a question today to keep your streak"}>
            <Flame size={22} /><span>{streak.count}</span>
          </div>
          <button className="icon-btn labelled" onClick={onPractice} title="Practice your mistakes">
            <Dumbbell /><span className="hide-sm">Practice</span>{missed > 0 && <span className="badge">{missed > 99 ? "99+" : missed}</span>}
          </button>
          <button className="icon-btn labelled" onClick={onAchievements} title="Achievements">
            <Trophy /><span className="hide-sm">{achievementCount(progress)}/{ACHIEVEMENTS.length}</span>
          </button>
          <button className="icon-btn" onClick={onSettings} aria-label="Settings" title="Settings"><Gear /></button>
        </div>
      </header>

      <main className="path">
        {UNITS.map((u, ui) => {
          const nodes: Level[] = [...u.levels.map((id) => LEVELS[id]), LEVELS[u.boss]];
          const unitDone = nodes.filter((n) => progress.done[n.id]).length;
          const pts = nodes.map((_, i) => ({ x: OFFSETS[i % OFFSETS.length], y: TOP + i * STEP }));
          const height = TOP + (nodes.length - 1) * STEP + 90;
          const reachIdx = nodes.reduce((acc, n, i) => (progress.done[n.id] ? i + 1 : acc), 0);
          const d = pts.map((p, i) => (i === 0 ? `M ${p.x} ${p.y}` : `C ${pts[i - 1].x} ${pts[i - 1].y + STEP / 2}, ${p.x} ${p.y - STEP / 2}, ${p.x} ${p.y}`)).join(" ");
          const dDone = pts.slice(0, Math.min(reachIdx + 1, pts.length)).map((p, i, arr) => (i === 0 ? `M ${p.x} ${p.y}` : `C ${arr[i - 1].x} ${arr[i - 1].y + STEP / 2}, ${p.x} ${p.y - STEP / 2}, ${p.x} ${p.y}`)).join(" ");
          return (
            <section className="unit" key={u.id} style={{ ["--unit" as any]: `var(--u${ui})` }}>
              <div className="unit-banner">
                <div>
                  <div className="unit-num">Unit {ui}</div>
                  <h2>{u.title}</h2>
                  <p>{u.blurb}</p>
                </div>
                <div className="unit-count" aria-label={`${unitDone} of ${nodes.length} done`}>
                  <svg viewBox="0 0 36 36" width="54" height="54">
                    <circle cx="18" cy="18" r="15" className="ring-bg" />
                    <circle cx="18" cy="18" r="15" className="ring-fg" strokeDasharray={`${(94.2 * unitDone) / nodes.length} 94.2`} />
                  </svg>
                  <span>{unitDone}/{nodes.length}</span>
                </div>
              </div>

              <div className="track" style={{ height }}>
                <svg className="road" viewBox={`-200 0 400 ${height}`} preserveAspectRatio="xMidYMin meet" style={{ height }} aria-hidden="true">
                  <path d={d} className="road-base" />
                  <path d={d} className="road-dash" />
                  {reachIdx > 0 && <path d={dDone} className="road-done" />}
                </svg>

                {nodes.map((n, i) => {
                  const done = !!progress.done[n.id];
                  const unlocked = isUnlocked(n.id);
                  const current = n.id === currentLevel;
                  const state = done ? "done" : current ? "current" : unlocked ? "open" : "locked";
                  const isBoss = n.kind === "boss";
                  const partial = (progress.partial[n.id] || []).length;
                  const qcount = levelQuestions(n).length;
                  const side = pts[i].x >= 0 ? "left" : "right";
                  const cls = ["node", state, isBoss ? "boss" : "", n.id === justDone ? "just-done" : "", n.id === nextAfterDone ? "just-unlocked" : "", shake === n.id ? "shake" : ""].join(" ");
                  return (
                    <div className="node-wrap" key={n.id} style={{ left: `calc(50% + ${pts[i].x}px)`, top: pts[i].y, animationDelay: `${Math.min(i, 8) * 45}ms` }}>
                      {current && <div className="start-bubble">{partial ? "CONTINUE" : isBoss ? "FIGHT" : "START"}</div>}
                      <button className={cls} aria-label={`${n.title}${done ? ", done" : state === "locked" ? ", locked" : ""}`}
                        onClick={() => {
                          play("click");
                          if (state === "locked") { setShake(n.id); setTimeout(() => setShake(null), 500); }
                          setOpen(open === n.id ? null : n.id);
                        }}>
                        {done ? (isBoss ? <Crown size={34} /> : <Check size={34} />) : state === "locked" ? (isBoss ? <Crown size={30} /> : <Lock size={28} />) : isBoss ? <Crown size={36} /> : <Star size={32} />}
                        {partial > 0 && !done && <svg className="node-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" strokeDasharray={`${(289 * partial) / qcount} 289`} /></svg>}
                      </button>
                      <div className={`node-label ${side}`}>{n.title}</div>
                      {current && !open && (
                        <div className={`path-pip ${side}`}><Pip mood={justDone ? "cheer" : "idle"} size={78} /></div>
                      )}
                      {open === n.id && (
                        <div className="node-pop" role="dialog" aria-label={n.title}>
                          <div className="pop-kicker">{isBoss ? "Boss" : `Level ${i + 1}`}{done && " · done"}</div>
                          <h3>{n.title}</h3>
                          <p>{n.short}</p>
                          {state === "locked" ? (
                            <p className="muted small">Finish the level before this one to unlock it.</p>
                          ) : (
                            <>
                              {!isBoss && <div className="pop-skills">{n.skills.map((s) => <span key={s.name} className="chip">{s.name}</span>)}</div>}
                              {partial > 0 && !done && <p className="muted small">{partial} of {qcount} questions done. You'll pick up where you left off.</p>}
                              <div className="pop-actions">
                                {isBoss ? (
                                  <button className="btn primary" onClick={() => onStart(n.id, "questions")}><Play size={16} /> {done ? "Fight again" : "Fight the boss"}</button>
                                ) : (
                                  <>
                                    <button className="btn primary" onClick={() => onStart(n.id, partial && !done ? "questions" : "lesson")}>
                                      <Play size={16} /> {done ? "Play again" : partial ? "Continue" : "Start"}
                                    </button>
                                    {(partial > 0 || done) && <button className="btn secondary" onClick={() => onStart(n.id, "lesson")}><Book size={16} /> Lesson</button>}
                                  </>
                                )}
                              </div>
                              {n.lc.length > 0 && <p className="muted small pop-lc">{n.lc.filter((p) => progress.lc[p.slug]).length}/{n.lc.length} LeetCode problems ticked off</p>}
                            </>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </section>
          );
        })}
        <footer className="path-end">
          <Pip mood={progress.done.b5 ? "cheer" : "think"} size={90} />
          <p>{progress.done.b5 ? "You're LeetCode ready. Keep the streak going with practice and real problems." : "At the end of the road: LeetCode ready."}</p>
        </footer>
      </main>
    </div>
  );
}
