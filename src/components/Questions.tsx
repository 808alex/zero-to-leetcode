import { useEffect, useMemo, useRef, useState, type MutableRefObject, type ReactNode } from "react";
import type { CodeQuestion, FillQuestion, MCQuestion, RunOutcome } from "../types";
import { runTests } from "../lib/python";
import { highlightPy } from "../lib/highlight";
import { CodeEditor } from "./CodeEditor";
import { CodeView, Html, Out, TestResults } from "./Bits";
import { Bulb, Lifebuoy, Play, Skip } from "./Icons";
import { play } from "../lib/sound";

export type Result = { correct: boolean; detail?: ReactNode; syntax?: boolean };

type Common = {
  attempt: number;
  locked: boolean;
  onResult: (r: Result) => void;
  helpAvailable: boolean;
  helpReason: string;
  onHelp: () => void;
  codeRef: MutableRefObject<() => string>;
  lastRunRef: MutableRefObject<string>;
};

function shuffle<T>(arr: T[], seed: number): T[] {
  const a = [...arr];
  let s = seed * 9301 + 49297;
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
const hash = (s: string) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);

function ActionBar({ left, children }: { left?: ReactNode; children: ReactNode }) {
  return <div className="actionbar"><div className="actionbar-left">{left}</div><div className="actionbar-right">{children}</div></div>;
}

function HelpButton({ available, reason, onHelp }: { available: boolean; reason: string; onHelp: () => void }) {
  return (
    <button className={`btn ghost help-btn ${available ? "ready" : ""}`} onClick={onHelp} disabled={!available} title={available ? "Open the helper" : reason}>
      <Lifebuoy size={20} /> <span>{available ? "Help me" : reason}</span>
    </button>
  );
}

function HintToggle({ hint }: { hint: string }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button className="btn ghost" onClick={() => { setOpen(!open); play("click"); }} aria-expanded={open}><Bulb size={20} /> <span>Hint</span></button>
      {open && <div className="hint-pop" role="note"><Bulb size={18} /> {hint}</div>}
    </>
  );
}

// ------------------------------------------------------------------------------------- multiple choice
export function MCView({ q, attempt, locked, onResult, helpAvailable, helpReason, onHelp }: Common & { q: MCQuestion }) {
  const order = useMemo(() => shuffle(q.options.map((_, i) => i), hash(q.id) + attempt * 7), [q.id, attempt, q.options]);
  const [picked, setPicked] = useState<number | null>(null);
  useEffect(() => setPicked(null), [q.id, attempt]);

  const check = () => {
    if (picked === null || locked) return;
    const correct = picked === q.answer;
    onResult({
      correct,
      detail: correct ? <Html html={q.explain} /> : (
        <>
          <div className="fb-answer">Correct answer: <code className="fb-code">{q.options[q.answer]}</code></div>
          <Html html={q.explain} />
        </>
      ),
    });
  };

  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (locked || (e.target as HTMLElement)?.closest?.("input,textarea,.cm-editor")) return;
      const n = Number(e.key);
      if (n >= 1 && n <= order.length) { setPicked(order[n - 1]); play("click"); }
      if (e.key === "Enter" && picked !== null) check();
    };
    addEventListener("keydown", key);
    return () => removeEventListener("keydown", key);
  });

  const isCode = !q.concept;
  return (
    <>
      <div className="q-body">
        <Html className="q-prompt" html={q.prompt} />
        {q.code && <CodeView code={q.code} />}
        {q.stdin && <div className="stdin-note">Input typed in: <code>{q.stdin.trim().split("\n").join(" ⏎ ")}</code></div>}
        <div className={`options ${isCode ? "mono" : ""}`} role="radiogroup" aria-label="Answers">
          {order.map((idx, i) => (
            <button key={idx} role="radio" aria-checked={picked === idx} disabled={locked}
              className={`option ${picked === idx ? "picked" : ""} ${locked && idx === q.answer ? "is-answer" : ""}`}
              onClick={() => { setPicked(idx); play("click"); }}>
              <span className="option-key">{i + 1}</span>
              <span className="option-text">{isCode ? <Out text={q.options[idx]} /> : q.options[idx]}</span>
            </button>
          ))}
        </div>
      </div>
      <ActionBar left={<HelpButton available={helpAvailable} reason={helpReason} onHelp={onHelp} />}>
        <button className="btn primary big" disabled={picked === null || locked} onClick={check}>Check</button>
      </ActionBar>
    </>
  );
}

// ------------------------------------------------------------------------------------- fill in the blank
export function FillView({ q, attempt, locked, onResult, helpAvailable, helpReason, onHelp, codeRef, lastRunRef }: Common & { q: FillQuestion }) {
  const [value, setValue] = useState("");
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => { setValue(""); setNote(null); input.current?.focus(); }, [q.id, attempt]);
  codeRef.current = () => q.code.replace("___", value || "___");

  const [before, after] = q.code.split("___");
  const check = async () => {
    if (!value.trim() || busy || locked) return;
    setBusy(true);
    setNote(null);
    const r: RunOutcome = await runTests(q.code.replace("___", value.trim()), q);
    setBusy(false);
    lastRunRef.current = summarise(r);
    if (r.setupError && /SyntaxError|IndentationError/.test(r.setupError)) { setNote("That isn't valid Python yet: " + r.setupError); return; }
    if (r.error && !r.rows) { setNote(r.error); return; }
    if (r.allPassed) { onResult({ correct: true, detail: <Html html={q.explain} /> }); return; }
    const bad = r.rows?.find((x) => !x.ok);
    onResult({
      correct: false,
      detail: bad ? (
        <div className="fb-compare">
          <div><span>{q.cmp === "stdout" ? "Input" : "Call"}</span><Out text={bad.args} /></div>
          <div><span>Expected</span><Out text={bad.exp} /></div>
          <div><span>Yours</span>{bad.err ? <span className="res-err">{bad.err}</span> : <Out text={bad.got} />}</div>
        </div>
      ) : r.setupError || "Not quite.",
    });
  };

  const width = Math.max(6, value.length + 2);
  return (
    <>
      <div className="q-body">
        <Html className="q-prompt" html={q.prompt} />
        <pre className="codeview fill">
          <code>
            <span dangerouslySetInnerHTML={{ __html: highlightPy(before) }} />
            <input ref={input} className="blank" value={value} onChange={(e) => setValue(e.target.value)} disabled={locked || busy}
              onKeyDown={(e) => { if (e.key === "Enter") check(); }} style={{ width: `${width}ch` }}
              aria-label="Fill in the blank" spellCheck={false} autoCapitalize="off" autoComplete="off" />
            <span dangerouslySetInnerHTML={{ __html: highlightPy(after.replace(/\n$/, "")) }} />
          </code>
        </pre>
        {note && <div className="res-banner bad">{note}</div>}
      </div>
      <ActionBar left={<><HintToggle hint={q.hint} /><HelpButton available={helpAvailable} reason={helpReason} onHelp={onHelp} /></>}>
        <button className="btn primary big" disabled={!value.trim() || locked || busy} onClick={check}>{busy ? "Checking…" : "Check"}</button>
      </ActionBar>
    </>
  );
}

// ------------------------------------------------------------------------------------- write / fix code (and bosses)
export function summarise(r: RunOutcome): string {
  if (r.setupError) return r.setupError;
  if (!r.rows) return r.error || "";
  return r.rows.map((x) => `${x.ok ? "PASS" : "FAIL"} | ${x.args} | expected ${x.exp} | got ${x.err || x.got}`).join("\n");
}

const draftKey = (id: string) => "z2l:draft:" + id;
const loadDraft = (q: CodeQuestion) => { try { return localStorage.getItem(draftKey(q.id)) ?? q.starter; } catch { return q.starter; } };

export function CodeView2({ q, locked, onResult, helpAvailable, helpReason, onHelp, codeRef, lastRunRef, onFailedRun, onSkip, boss }: Common & {
  q: CodeQuestion; onFailedRun: () => void; onSkip?: () => void; boss: boolean;
}) {
  const [code, setCode] = useState(() => loadDraft(q));
  const [busy, setBusy] = useState<"" | "run" | "submit">("");
  const [result, setResult] = useState<{ r: RunOutcome; kind: "run" | "submit" } | null>(null);
  useEffect(() => { setCode(loadDraft(q)); setResult(null); }, [q.id]);
  codeRef.current = () => code;
  const change = (v: string) => { setCode(v); try { localStorage.setItem(draftKey(q.id), v); } catch { /* ignore */ } };

  const run = async (kind: "run" | "submit") => {
    if (busy || locked) return;
    setBusy(kind);
    const r = await runTests(code, q, boss && kind === "run" ? q.testsVisible : undefined);
    setBusy("");
    setResult({ r, kind });
    lastRunRef.current = summarise(r);
    if (!boss) {
      if (r.allPassed) onResult({ correct: true, detail: q.explain ? <Html html={q.explain} /> : "Every test passed." });
      else onFailedRun();
      return;
    }
    if (kind === "submit") {
      if (r.allPassed) onResult({ correct: true, detail: "Every test passed, hidden ones included." });
      else onResult({ correct: false, detail: r.rows ? `${r.passed} of ${r.total} tests passed. Look for an edge case you haven't handled.` : r.setupError || r.error || "It didn't run." });
    }
  };

  // in boss mode, a submit only shows the visible rows (hidden tests stay hidden)
  const visibleRows = result && boss && result.kind === "submit" && result.r.rows ? result.r.rows.slice(0, q.visibleCount ?? 2) : null;
  const shown = visibleRows && result
    ? { ...result.r, rows: visibleRows, passed: visibleRows.filter((x) => x.ok).length, total: visibleRows.length, allPassed: visibleRows.every((x) => x.ok) }
    : result?.r;
  const hiddenNote = result && boss && result.kind === "submit" && result.r.rows
    ? `${result.r.passed} of ${result.r.total} including hidden tests` : undefined;

  const label = q.kind === "fix" ? "Fix the bug" : boss ? "Boss challenge" : "Write the code";
  return (
    <>
      <div className="q-body">
        <div className="q-title">{q.title !== label && <span>{q.title}</span>}</div>
        <Html className="q-prompt" html={q.prompt} />
        {q.lc && <a className="lc-link" href={`https://leetcode.com/problems/${q.lc}/`} target="_blank" rel="noopener">Also on LeetCode ↗</a>}
        <CodeEditor value={code} onChange={change} onRun={() => run("run")} ariaLabel={`Code for ${q.title}`} />
        <div className="code-tools">
          <button className="btn ghost small" onClick={() => change(q.starter)}>Reset code</button>
          <span className="kbd">Ctrl/⌘ + Enter runs</span>
        </div>
        {busy && <div className="res-banner neutral">Running…</div>}
        {shown && !busy && <TestResults r={shown} stdout={q.cmp === "stdout"} hiddenNote={hiddenNote} />}
      </div>
      <ActionBar left={<>
        {!boss && <HintToggle hint={q.hint} />}
        <HelpButton available={helpAvailable} reason={helpReason} onHelp={onHelp} />
        {onSkip && <button className="btn ghost" onClick={onSkip} title="Move this one to the end"><Skip size={18} /> <span>Later</span></button>}
      </>}>
        {boss ? (
          <>
            <button className="btn secondary big" disabled={!!busy || locked} onClick={() => run("run")}><Play size={16} /> Run samples</button>
            <button className="btn primary big" disabled={!!busy || locked} onClick={() => run("submit")}>Submit</button>
          </>
        ) : (
          <button className="btn primary big" disabled={!!busy || locked} onClick={() => run("run")}><Play size={16} /> {busy ? "Running…" : "Run tests"}</button>
        )}
      </ActionBar>
    </>
  );
}
