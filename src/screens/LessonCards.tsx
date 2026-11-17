import { useEffect, useLayoutEffect, useRef, useState } from "react";
import type { Level } from "../types";
import { highlightWithin } from "../lib/highlight";
import { play } from "../lib/sound";
import { Pip } from "../components/Mascot";
import { Back, Close } from "../components/Icons";

type Props = { level: Level; mode: "learn" | "review"; onDone: () => void; onExit: () => void };

export function LessonCards({ level, mode, onDone, onExit }: Props) {
  const [i, setI] = useState(0);
  const [dir, setDir] = useState<"next" | "prev">("next");
  const body = useRef<HTMLDivElement>(null);
  const cards = level.cards;
  const card = cards[i];
  const last = i === cards.length - 1;

  useLayoutEffect(() => { if (body.current) highlightWithin(body.current); }, [i]);
  useEffect(() => { body.current?.scrollTo({ top: 0 }); }, [i]);

  const go = (d: number) => {
    const n = i + d;
    if (n < 0) return;
    if (n >= cards.length) { play("click"); onDone(); return; }
    setDir(d > 0 ? "next" : "prev");
    setI(n);
    play("click");
  };

  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.closest?.("input,textarea,summary,.cm-editor")) return;
      if (e.key === "ArrowRight") go(1);
      if (e.key === "ArrowLeft") go(-1);
    };
    addEventListener("keydown", key);
    return () => removeEventListener("keydown", key);
  });

  return (
    <div className="lesson-screen">
      <div className="session-top">
        <button className="icon-btn" onClick={onExit} aria-label="Leave the lesson"><Close /></button>
        <div className="dots" aria-label={`Card ${i + 1} of ${cards.length}`}>
          {cards.map((_, k) => <span key={k} className={`dot ${k < i ? "seen" : ""} ${k === i ? "on" : ""}`} />)}
        </div>
        <span className="lesson-tag">{mode === "review" ? "Review" : "Lesson"}</span>
      </div>

      <div className="lesson-scroll" ref={body}>
        <article className={`lesson-card slide-${dir}`} key={i}>
          {i === 0 && (
            <div className="lesson-hello">
              <Pip mood={mode === "review" ? "think" : "happy"} size={84} />
              <div>
                <div className="eyebrow">{mode === "review" ? "Let's look at this again" : "New level"}</div>
                <h1>{level.title}</h1>
              </div>
            </div>
          )}
          {i > 0 && <h2 className="card-title">{card.title}</h2>}
          <div className="lesson-html" dangerouslySetInnerHTML={{ __html: card.html }} />
        </article>
      </div>

      <div className="actionbar">
        <div className="actionbar-left">
          {i > 0 && <button className="btn ghost" onClick={() => go(-1)}><Back size={18} /> Back</button>}
        </div>
        <div className="actionbar-right">
          <button className="btn primary big" onClick={() => go(1)}>
            {last ? (mode === "review" ? "Back to the questions" : "Start the questions") : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}
