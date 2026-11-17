import { useEffect, useRef, type ReactNode } from "react";
import { highlightPy, escapeHtml } from "../lib/highlight";
import type { RunOutcome } from "../types";
import { Close } from "./Icons";

export function CodeView({ code }: { code: string }) {
  return <pre className="codeview"><code dangerouslySetInnerHTML={{ __html: highlightPy(code.replace(/\n$/, "")) }} /></pre>;
}

/** Shows text that might be several lines (expected/actual output) in a readable way. */
export const Out = ({ text }: { text: string | undefined }) =>
  <span className="out">{text === "" || text === undefined ? <em>(nothing)</em> : text}</span>;

export function TestResults({ r, stdout, hiddenNote }: { r: RunOutcome; stdout: boolean; hiddenNote?: string }) {
  return (
    <div className="results" aria-live="polite">
      {r.setupError && <div className="res-banner bad">{r.setupError}</div>}
      {r.rows && (
        <>
          <div className={`res-banner ${r.allPassed ? "good" : "bad"}`}>
            {r.allPassed ? `All ${r.total} ${hiddenNote ? "sample " : ""}tests passed` : `${r.passed} of ${r.total} ${hiddenNote ? "sample " : ""}tests passed`}
            {hiddenNote && <span className="res-note"> · {hiddenNote}</span>}
          </div>
          <div className="res-table-wrap">
            <table className="res-table">
              <thead><tr><th /><th>{stdout ? "Input" : "Call"}</th><th>Expected</th><th>{stdout ? "You printed" : "Got"}</th></tr></thead>
              <tbody>
                {r.rows.map((x, i) => (
                  <tr key={i} className={x.ok ? "ok" : "no"}>
                    <td className="res-mark">{x.ok ? "✓" : "✗"}</td>
                    <td><Out text={x.args} /></td>
                    <td><Out text={x.exp} /></td>
                    <td>{x.err ? <span className="res-err">{x.err}{x.got ? <><br /><br />Printed before the error:<br /><Out text={x.got} /></> : null}</span> : <Out text={x.got} />}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
      {r.error && <pre className="res-error">{r.error}</pre>}
      {r.output.trim() && <><div className="res-label">Your print output</div><pre className="res-console">{r.output}</pre></>}
    </div>
  );
}

export function Modal({ title, onClose, children, wide }: { title: string; onClose: () => void; children: ReactNode; wide?: boolean }) {
  const box = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    box.current?.focus();
    const key = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    addEventListener("keydown", key);
    return () => { removeEventListener("keydown", key); prev?.focus?.(); };
  }, [onClose]);
  return (
    <div className="modal-back" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className={`modal ${wide ? "wide" : ""}`} role="dialog" aria-modal="true" aria-label={title} tabIndex={-1} ref={box}>
        <div className="modal-head">
          <h2>{title}</h2>
          <button className="icon-btn" onClick={onClose} aria-label="Close"><Close /></button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}

export const Html = ({ html, className }: { html: string; className?: string }) =>
  <div className={className} dangerouslySetInnerHTML={{ __html: html }} />;

export const plain = (html: string) => { const d = document.createElement("div"); d.innerHTML = html; return d.textContent || ""; };
export { escapeHtml };
