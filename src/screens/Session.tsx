import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { LEVELS, QUESTIONS, ORDER, levelQuestions, skillOf } from "../content";
import type { CodeQuestion, Level, Question } from "../types";
import { useProgress, touchToday } from "../state";
import { startPython } from "../lib/python";
import { play } from "../lib/sound";
import { confetti } from "../lib/confetti";
import { CodeView2, FillView, MCView, type Result } from "../components/Questions";
import { Pip, type Mood } from "../components/Mascot";
import { Close, Heart, Crown } from "../components/Icons";
import { LessonCards } from "./LessonCards";
import { Helper } from "./Helper";
import { LevelComplete } from "./LevelComplete";

type Phase = "intro" | "lesson" | "questions" | "outOfHearts" | "review" | "complete" | "lost" | "empty";
type Feedback = { qid: string; correct: boolean; title: string; body: ReactNode; mood: Mood; again?: boolean };

const CHEERS = ["Nice one!", "Spot on!", "Correct!", "That's it!", "Clean!", "You got it!"];
const OOPS = ["Not quite.", "So close.", "Not this time.", "Nearly."];
const pick = (a: string[]) => a[Math.floor(Math.random() * a.length)];
const MAX_HEARTS = 3;

export type SessionProps =
  | { kind: "level"; levelId: string; start: "lesson" | "questions"; onExit: (completed?: string) => void }
  | { kind: "practice"; onExit: (completed?: string) => void };

function practiceQueue(done: Record<string, unknown>, missed: Record<string, number>): string[] {
  const doneLevels = Object.keys(done).map((id) => LEVELS[id]).filter((l) => l && l.kind === "lesson");
  const missedIds = Object.entries(missed).sort((a, b) => b[1] - a[1]).map(([id]) => id).filter((id) => QUESTIONS[id]).slice(0, 6);
  const pool = doneLevels.flatMap(levelQuestions).filter((id) => !missedIds.includes(id) && QUESTIONS[id].kind !== "code");
  for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
  return [...missedIds, ...pool].slice(0, 8);
}

export function Session(props: SessionProps) {
  const { progress, update } = useProgress();
  const level: Level | null = props.kind === "level" ? LEVELS[props.levelId] : null;
  const isBoss = level?.kind === "boss";
  const isPractice = props.kind === "practice";
  const usesHearts = !isPractice;

  const initial = useMemo(() => {
    if (isPractice) return { queue: practiceQueue(progress.done, progress.missed), passed: [] as string[] };
    const all = levelQuestions(level!);
    const partial = !isBoss && !progress.done[level!.id] ? (progress.partial[level!.id] || []).filter((q) => all.includes(q)) : [];
    return { queue: all.filter((q) => !partial.includes(q)), passed: partial };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const [phase, setPhase] = useState<Phase>(() => {
    if (isPractice) return initial.queue.length ? "questions" : "empty";
    if (isBoss) return "intro";
    return props.kind === "level" && props.start === "lesson" ? "lesson" : "questions";
  });
  const [queue, setQueue] = useState<string[]>(initial.queue);
  const [passed, setPassed] = useState<string[]>(initial.passed);
  const [hearts, setHearts] = useState(MAX_HEARTS);
  const [fails, setFails] = useState<Record<string, number>>({});
  const [helperAll, setHelperAll] = useState(false);
  const [revealed, setRevealed] = useState<Set<string>>(new Set());
  const [assisted, setAssisted] = useState(false);
  const [comeback, setComeback] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [helperOpen, setHelperOpen] = useState(false);
  const [heartAnim, setHeartAnim] = useState(-1);
  const [wrongFirst, setWrongFirst] = useState<Set<string>>(new Set());
  const [answered, setAnswered] = useState(0);
  const startedAt = useRef(Date.now());
  const codeRef = useRef<() => string>(() => "");
  const lastRunRef = useRef<string>("");
  const total = initial.queue.length + initial.passed.length;

  useEffect(() => { startPython(); }, []);

  // while the feedback sheet is up, keep showing the question it belongs to (the queue has already moved on)
  const qid = feedback?.qid ?? queue[0];
  const q: Question | undefined = qid ? QUESTIONS[qid] : undefined;
  const skill = level && qid ? skillOf(level, qid) : undefined;
  const failCount = qid ? fails[qid] || 0 : 0;
  const helpAvailable = isBoss ? failCount >= 1 : helperAll || failCount >= 3 || isPractice;
  const helpReason = isBoss ? "Help unlocks after a failed submit" : `Help unlocks after ${3 - failCount} more ${3 - failCount === 1 ? "try" : "tries"}`;

  const exit = (completed?: string) => props.onExit(completed);

  function savePartial(nextPassed: string[]) {
    if (props.kind !== "level" || isBoss || progress.done[props.levelId]) return;
    update((p) => { p.partial[props.levelId] = nextPassed; });
  }

  function onResult(r: Result) {
    if (!q || feedback) return;
    const id = q.id;
    setAnswered((n) => n + 1);
    if (r.correct) {
      play("correct");
      if (revealed.has(id)) {
        const nr = new Set(revealed); nr.delete(id); setRevealed(nr);
        setQueue((qq) => [...qq.slice(1), id]);
        setFeedback({ qid: id, correct: true, title: "Got it", mood: "happy", body: <>{r.detail}<p className="fb-again">You'll see this one again in a bit, without the answer showing.</p></>, again: true });
        return;
      }
      const nextPassed = passed.includes(id) ? passed : [...passed, id];
      setPassed(nextPassed);
      setQueue((qq) => qq.slice(1));
      savePartial(nextPassed);
      update((p) => {
        touchToday(p);
        const k = q.kind === "mc" ? "mc" : q.kind === "fill" ? "fill" : q.kind === "fix" ? "fix" : "code";
        p.stats[k] += 1;
        if (isPractice) { p.stats.practice += 1; delete p.missed[id]; }
      });
      setFeedback({ qid: id, correct: true, title: pick(CHEERS), mood: "cheer", body: r.detail });
      return;
    }
    // wrong answer: quick questions, and boss submits
    const nf = { ...fails, [id]: (fails[id] || 0) + 1 };
    setFails(nf);
    setWrongFirst((s) => new Set(s).add(id));
    if (!isPractice) update((p) => { p.missed[id] = Date.now(); });
    if (usesHearts) {
      setHeartAnim(hearts - 1);
      setHearts((h) => h - 1);
      play("heart");
      setTimeout(() => setHeartAnim(-1), 700);
    } else play("wrong");
    if (!isBoss) { setQueue((qq) => [...qq.slice(1), id]); }
    const left = hearts - 1;
    const tail = usesHearts && left > 0 ? `${left} ${left === 1 ? "heart" : "hearts"} left.` : "";
    setFeedback({
      qid: id, correct: false, title: pick(OOPS), mood: "sad",
      body: <>{r.detail}{!isBoss && <p className="fb-again">This question comes back at the end. {tail}</p>}{isBoss && tail && <p className="fb-again">{tail}</p>}</>,
    });
  }

  function onFailedRun() {
    if (!q) return;
    setFails((f) => ({ ...f, [q.id]: (f[q.id] || 0) + 1 }));
    play("wrong");
  }

  function finish() {
    if (isPractice) { setPhase("complete"); play("complete"); return; }
    const lv = level!;
    update((p) => {
      p.done[lv.id] = { at: Date.now(), hearts, assisted, comeback, firstTry: total - wrongFirst.size, total };
      delete p.partial[lv.id];
      touchToday(p);
    });
    play("complete");
    const css = getComputedStyle(document.documentElement);
    confetti(["--primary", "--gold", "--pink", "--sky", "--u2"].map((v) => css.getPropertyValue(v).trim() || "#58cc02"));
    setPhase("complete");
  }

  function continueOn() {
    const fb = feedback;
    setFeedback(null);
    setAttempt((a) => a + 1);
    if (usesHearts && hearts <= 0) {
      if (isBoss) { setPhase("lost"); play("wrong"); }
      else setPhase("outOfHearts");
      return;
    }
    if (fb?.correct && queue.length === 0) finish();
  }

  // Enter continues from the feedback sheet
  useEffect(() => {
    if (!feedback) return;
    const key = (e: KeyboardEvent) => { if (e.key === "Enter") { e.preventDefault(); continueOn(); } };
    const t = setTimeout(() => addEventListener("keydown", key), 150);
    return () => { clearTimeout(t); removeEventListener("keydown", key); };
  });

  function skip() {
    if (queue.length < 2) return;
    setQueue((qq) => [...qq.slice(1), qq[0]]);
    setAttempt((a) => a + 1);
  }

  function openHelper() {
    setHelperOpen(true);
  }

  function onReveal() {
    if (!q) return;
    setAssisted(true);
    if (q.kind === "mc" || q.kind === "fill") setRevealed((s) => new Set(s).add(q.id));
  }

  function restartBoss() {
    setQueue(levelQuestions(level!));
    setPassed([]);
    setHearts(MAX_HEARTS);
    setFails({});
    setFeedback(null);
    setAttempt((a) => a + 1);
    setPhase("questions");
    play("boss");
  }

  // ---------------------------------------------------------------- render phases
  if (phase === "empty") {
    return (
      <div className="center-screen">
        <Pip mood="think" size={120} />
        <h1>Nothing to practise yet</h1>
        <p className="muted">Practice mode mixes questions you got wrong with ones from levels you've finished. Finish your first level and come back.</p>
        <button className="btn primary big" onClick={() => exit()}>Back to the path</button>
      </div>
    );
  }

  if (phase === "lesson" || phase === "review") {
    return (
      <LessonCards level={level!} mode={phase === "review" ? "review" : "learn"} onExit={() => exit()}
        onDone={() => {
          if (phase === "review") { setHearts(MAX_HEARTS); setHelperAll(true); setComeback(true); play("unlock"); }
          setPhase("questions");
        }} />
    );
  }

  if (phase === "intro") {
    return (
      <div className="center-screen boss-intro">
        <div className="boss-crest"><Crown size={64} /></div>
        <div className="eyebrow">Boss level</div>
        <h1>{level!.title}</h1>
        <p className="lede">{level!.short}</p>
        <ul className="boss-rules">
          <li><Heart size={20} className="heart-on" /><span>3 hearts for the whole fight. A failed <strong>Submit</strong> costs one.</span></li>
          <li><span className="rule-dot" /><span><strong>Run samples</strong> is free, but Submit also runs hidden tests.</span></li>
          <li><span className="rule-dot" /><span>No lesson and no solutions. The hint unlocks after a failed submit.</span></li>
        </ul>
        <div className="row">
          <button className="btn ghost big" onClick={() => exit()}>Not yet</button>
          <button className="btn primary big" onClick={() => { play("boss"); setPhase("questions"); }}>Start the fight</button>
        </div>
      </div>
    );
  }

  if (phase === "outOfHearts") {
    return (
      <div className="center-screen">
        <Pip mood="sad" size={130} />
        <h1>Out of hearts</h1>
        <p className="lede">Three wrong answers means it's time to look at the lesson again rather than guess. Your progress in this level is saved, and you'll come back with full hearts and the helper unlocked.</p>
        <div className="row">
          <button className="btn ghost big" onClick={() => exit()}>Leave for now</button>
          <button className="btn primary big" onClick={() => setPhase("review")}>Review the lesson</button>
        </div>
      </div>
    );
  }

  if (phase === "lost") {
    return (
      <div className="center-screen">
        <Pip mood="sad" size={130} />
        <h1>{level!.title} wins this round</h1>
        <p className="lede">Bosses are meant to be hard. Go over the unit's levels if something felt shaky, then come back. You restart the fight with full hearts.</p>
        <div className="row">
          <button className="btn ghost big" onClick={() => exit()}>Back to the path</button>
          <button className="btn primary big" onClick={restartBoss}>Try again</button>
        </div>
      </div>
    );
  }

  if (phase === "complete") {
    return <LevelComplete level={level} practice={isPractice} hearts={hearts} total={isPractice ? answered : total}
      seconds={Math.round((Date.now() - startedAt.current) / 1000)} boss={isBoss}
      nextId={level ? ORDER[ORDER.indexOf(level.id) + 1] : undefined} onContinue={() => exit(level?.id)} />;
  }

  // ---------------------------------------------------------------- questions
  if (!q) return null;
  const pct = Math.round((100 * passed.length) / Math.max(1, isPractice ? initial.queue.length : total));
  const common = {
    attempt, locked: !!feedback, onResult, helpAvailable, helpReason, onHelp: openHelper, codeRef, lastRunRef,
  };
  const typeLabel = q.kind === "mc" ? (q.concept ? "Pick the answer" : "What does this print?") : q.kind === "fill" ? "Fill in the blank" : q.kind === "fix" ? "Fix the bug" : isBoss ? "Boss challenge" : "Write the code";
  const skillDone = skill ? skill.questions.filter((x) => passed.includes(x)).length : 0;

  return (
    <div className={`session ${isBoss ? "is-boss" : ""}`}>
      <div className="session-top">
        <button className="icon-btn" onClick={() => exit()} aria-label="Leave (progress is saved)" title="Leave (progress is saved)"><Close /></button>
        <div className="bar" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label="Level progress">
          <i style={{ width: `${pct}%` }} />
        </div>
        {usesHearts ? (
          <div className="hearts" aria-label={`${hearts} hearts left`}>
            {Array.from({ length: MAX_HEARTS }, (_, i) => (
              <Heart key={i} className={`${i < hearts ? "heart-on" : "heart-off"} ${i === heartAnim ? "heart-break" : ""}`} />
            ))}
          </div>
        ) : <span className="lesson-tag">Practice</span>}
      </div>

      <div className="session-scroll">
        <div className="q-head">
          <span className={`q-type type-${q.kind}`}>{typeLabel}</span>
          {skill && !isBoss && <span className="q-skill">{skill.name} · {skillDone}/{skill.questions.length}</span>}
          {isBoss && <span className="q-skill">Challenge {passed.length + 1} of {total}</span>}
        </div>
        <div className="q-anim" key={q.id + ":" + attempt}>
          {q.kind === "mc" && <MCView q={q} {...common} />}
          {q.kind === "fill" && <FillView q={q} {...common} />}
          {(q.kind === "code" || q.kind === "fix") && (
            <CodeView2 q={q as CodeQuestion} {...common} boss={isBoss} onFailedRun={onFailedRun}
              onSkip={!isBoss && queue.length > 1 ? skip : undefined} />
          )}
        </div>
      </div>

      {feedback && (
        <div className={`feedback ${feedback.correct ? "good" : "bad"}`} role="alert">
          <div className="feedback-inner">
            <Pip mood={feedback.mood} size={74} />
            <div className="feedback-text">
              <h3>{feedback.title}</h3>
              <div className="feedback-body">{feedback.body}</div>
            </div>
            <button className={`btn big ${feedback.correct ? "primary" : "danger"}`} onClick={continueOn} autoFocus>Continue</button>
          </div>
        </div>
      )}

      {helperOpen && (
        <Helper q={q} boss={isBoss} onClose={() => setHelperOpen(false)} onReveal={onReveal}
          getCode={() => codeRef.current()} lastRun={lastRunRef.current} />
      )}
    </div>
  );
}
