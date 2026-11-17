import { useEffect, useState } from "react";
import type { Question } from "../types";
import { CodeView, Html, Modal, Out, plain } from "../components/Bits";
import { Pip } from "../components/Mascot";
import { askClaude, getSampler, miniMarkdown } from "../lib/claude";

type Props = { q: Question; boss: boolean; onClose: () => void; onReveal: () => void; getCode: () => string; lastRun: string };

/** Step-by-step helper: hint → explanation → the answer. Bosses only get the hint. */
export function Helper({ q, boss, onClose, onReveal, getCode, lastRun }: Props) {
  const [step, setStep] = useState(0);
  const [claudeOk, setClaudeOk] = useState(false);
  const [reply, setReply] = useState<string | null>(null);
  const [asking, setAsking] = useState(false);
  useEffect(() => { getSampler().then((s) => setClaudeOk(!!s)); }, []);

  const hint = "hint" in q ? q.hint : null;
  const explain = "explain" in q && q.explain ? q.explain : null;
  const maxStep = boss ? 0 : 2;

  const reveal = () => { setStep(2); onReveal(); };

  const ask = async () => {
    setAsking(true);
    setReply("");
    try {
      const problem = plain(q.prompt) + ("fn" in q && q.fn ? ` (function: ${q.fn})` : "");
      const text = await askClaude(problem, getCode(), lastRun, (t) => setReply(t));
      setReply(text);
    } catch { setReply("Couldn't reach Claude right now. Try the steps above instead."); }
    finally { setAsking(false); }
  };

  return (
    <Modal title="Helper" onClose={onClose} wide>
      <div className="helper">
        <div className="helper-pip"><Pip mood="think" size={72} say={boss ? "Boss rules: a hint, nothing more." : "Let's get you unstuck, one step at a time."} /></div>

        <section className="helper-step">
          <h3>1. A nudge</h3>
          <p>{hint || (q.kind === "mc" ? "Trace the code line by line on paper, writing down each variable's value as it changes." : "Re-read the question and test the smallest input in your head.")}</p>
        </section>

        {!boss && (
          step >= 1 ? (
            <section className="helper-step">
              <h3>2. Why it works</h3>
              {explain ? <Html html={explain} /> : <p>Compare your approach with the lesson's template for this skill. The pattern is usually exactly what's needed.</p>}
            </section>
          ) : <button className="btn secondary" onClick={() => setStep(1)}>Still stuck: explain it</button>
        )}

        {!boss && step >= 1 && (
          step >= 2 ? (
            <section className="helper-step">
              <h3>3. The answer</h3>
              {q.kind === "mc" && <p className="helper-answer"><Out text={q.options[q.answer]} /></p>}
              {q.kind === "fill" && <p className="helper-answer"><code>{q.answer}</code></p>}
              {(q.kind === "code" || q.kind === "fix") && (
                <>
                  <CodeView code={q.solution} />
                  <p className="muted small">Type it out yourself rather than copying. Typing it is how it sticks.</p>
                </>
              )}
              {(q.kind === "mc" || q.kind === "fill") && <p className="muted small">This question will come back once more later, so you'll have to get it on your own.</p>}
            </section>
          ) : <button className="btn secondary" onClick={reveal}>Show me the answer</button>
        )}

        {claudeOk && q.kind !== "mc" && (
          <section className="helper-step">
            <h3>Ask Claude about your attempt</h3>
            {reply === null ? (
              <button className="btn secondary" onClick={ask}>Ask Claude</button>
            ) : (
              <div className="claude-reply" aria-live="polite">
                {reply ? <div dangerouslySetInnerHTML={{ __html: miniMarkdown(reply) }} /> : <p className="muted">Thinking…</p>}
                {!asking && <button className="btn ghost small" onClick={ask}>Ask again</button>}
              </div>
            )}
          </section>
        )}
        {step < maxStep && <p className="muted small">Each step gives a bit more away. Try again after each one.</p>}
      </div>
    </Modal>
  );
}
