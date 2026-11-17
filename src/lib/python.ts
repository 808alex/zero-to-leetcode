/**
 * Runs Python in the browser with Pyodide, inside a Web Worker so an infinite loop can be killed.
 * Falls back to the main thread if workers can't load Pyodide (some sandboxes block it).
 */
import { CONTENT } from "../content";
import type { RunOutcome, TestRow, TestSpec } from "../types";

const params = new URLSearchParams(location.search);
export const PYODIDE_URL = params.get("pyodide") || "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
const TIMEOUT_MS = 10000;

export type PyState = "idle" | "loading" | "ready" | "failed";
type Raw = { ok: boolean; out: string; err?: string };

async function runOn(py: any, code: string, stdin: string): Promise<Raw> {
  const out: string[] = [];
  py.setStdout({ batched: (s: string) => out.push(s) });
  py.setStderr({ batched: (s: string) => out.push(s) });
  const lines = stdin ? stdin.split("\n") : [];
  let i = 0;
  py.setStdin({ stdin: () => (i < lines.length ? lines[i++] : undefined) });
  const g = py.globals.get("dict")();
  try {
    await py.runPythonAsync(code, { globals: g });
    return { ok: true, out: out.join("\n") };
  } catch (err: any) {
    return { ok: false, out: out.join("\n"), err: String((err && err.message) || err) };
  } finally {
    try { g.destroy(); } catch { /* already gone */ }
  }
}

const WORKER_SRC = `importScripts(${JSON.stringify(PYODIDE_URL + "pyodide.js")});
const runOn = ${runOn.toString()};
let py = null;
const ready = loadPyodide({ indexURL: ${JSON.stringify(PYODIDE_URL)} })
  .then((p) => { py = p; postMessage({ type: "ready" }); })
  .catch((e) => postMessage({ type: "fatal", err: String(e) }));
onmessage = async (e) => {
  const { id, code, stdin } = e.data;
  await ready;
  if (!py) { postMessage({ type: "result", id, ok: false, out: "", err: "Python failed to load." }); return; }
  const r = await runOn(py, code, stdin);
  postMessage({ type: "result", id, ...r });
};`;

const listeners = new Set<(s: PyState) => void>();
let state: PyState = "idle";
function setState(s: PyState) { state = s; listeners.forEach((f) => f(s)); }
export function onPyState(f: (s: PyState) => void) { listeners.add(f); f(state); return () => { listeners.delete(f); }; }
export const pyState = () => state;

let mode: "worker" | "main" = "worker";
let worker: Worker | null = null;
let mainPy: any = null;
let readyP: Promise<boolean> | null = null;
let seq = 0;
const pending = new Map<number, { resolve: (r: Raw) => void; timer: number }>();

function startMain(): Promise<boolean> {
  return new Promise((resolve) => {
    const go = async () => {
      try { mainPy = await (window as any).loadPyodide({ indexURL: PYODIDE_URL }); resolve(true); }
      catch { resolve(false); }
    };
    if ((window as any).loadPyodide) { go(); return; }
    const s = document.createElement("script");
    s.src = PYODIDE_URL + "pyodide.js";
    s.onload = go;
    s.onerror = () => resolve(false);
    document.head.appendChild(s);
  });
}

function startWorker(): Promise<boolean> {
  return new Promise((resolve) => {
    let settled = false;
    const fallback = () => { mode = "main"; resolve(startMain()); };
    let w: Worker;
    try { w = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: "text/javascript" }))); }
    catch { fallback(); return; }
    worker = w;
    w.onmessage = (e) => {
      const m = e.data;
      if (m.type === "ready") { settled = true; resolve(true); }
      else if (m.type === "fatal") { if (!settled) { settled = true; w.terminate(); worker = null; fallback(); } }
      else if (m.type === "result") {
        const p = pending.get(m.id);
        if (p) { pending.delete(m.id); clearTimeout(p.timer); p.resolve(m); }
      }
    };
    w.onerror = (e) => { if (!settled) { settled = true; e.preventDefault(); w.terminate(); worker = null; fallback(); } };
  });
}

export function startPython(): Promise<boolean> {
  if (readyP) return readyP;
  setState("loading");
  readyP = (mode === "worker" ? startWorker() : startMain()).then((ok) => {
    setState(ok ? "ready" : "failed");
    if (!ok) readyP = null;
    return ok;
  });
  return readyP;
}

async function runRaw(code: string, stdin = ""): Promise<Raw> {
  const ok = await startPython();
  if (!ok) return { ok: false, out: "", err: "Python couldn't load. Check your connection, then try again." };
  if (mode === "worker" && worker) {
    const id = ++seq;
    return new Promise((resolve) => {
      const timer = window.setTimeout(() => {
        pending.delete(id);
        worker?.terminate();
        worker = null; readyP = null; setState("idle");
        resolve({ ok: false, out: "", err: "TIMEOUT" });
        startPython();
      }, TIMEOUT_MS);
      pending.set(id, { resolve, timer });
      worker!.postMessage({ id, code, stdin });
    });
  }
  return runOn(mainPy, code, stdin);
}

const PRELUDE_LINES = CONTENT.harness.prelude.split("\n").length - 1;

export function cleanError(msg: string): string {
  if (msg === "TIMEOUT") {
    return "Stopped after 10 seconds. That's usually an infinite loop: check that the loop variable actually changes each time round.";
  }
  const lines = msg.split("\n");
  const start = lines.findIndex((l) => l.includes('File "<exec>"'));
  const body = start >= 0 ? lines.slice(start) : lines.slice(-4);
  return body.map((l) => l.replace(/File "<exec>", line (\d+)/, (_, n) => "line " + Math.max(1, Number(n) - PRELUDE_LINES))).join("\n").trim();
}

export function buildProgram(code: string, spec: TestSpec, testsOverride?: string): string {
  const tests = testsOverride ?? spec.tests;
  if (spec.cmp === "stdout") {
    return CONTENT.harness.stdout.replace("__SRC__", () => JSON.stringify(code)).replace("__TESTS__", () => tests);
  }
  const prep = spec.prep ? spec.prep.split("\n").map((l) => "    " + l).join("\n") : "    pass";
  const h = CONTENT.harness.functions
    .replace(/__FN__/g, () => "'" + spec.fn + "'")
    .replace(/__CMP__/g, () => "'" + spec.cmp + "'")
    .replace(/__PREP__/g, () => prep)
    .replace(/__TESTS__/g, () => tests);
  return CONTENT.harness.prelude + code + "\n" + h;
}

/** Run user code against a test spec and return a structured outcome. */
export async function runTests(code: string, spec: TestSpec, testsOverride?: string): Promise<RunOutcome> {
  const r = await runRaw(buildProgram(code, spec, testsOverride));
  const lines = (r.out || "").split("\n");
  const idx = lines.findIndex((l) => l.startsWith("@@RESULTS@@"));
  let rows: TestRow[] | null = null;
  if (idx >= 0) {
    try { rows = JSON.parse(lines[idx].slice(11)); } catch { rows = null; }
    lines.splice(idx, 1);
  }
  const output = lines.join("\n");
  let setupError: string | null = null;
  if (rows && rows.length === 1 && rows[0].err && !("args" in rows[0])) { setupError = rows[0].err; rows = null; }
  const passed = rows ? rows.filter((x) => x.ok).length : 0;
  const total = rows ? rows.length : 0;
  return {
    rows, passed, total, allPassed: !!rows && total > 0 && passed === total,
    setupError, error: !r.ok && r.err ? cleanError(r.err) : null, output,
  };
}

/** Run a plain script (scratch use). */
export async function runScript(code: string, stdin = "") {
  const r = await runRaw(CONTENT.harness.prelude + code, stdin);
  return { output: r.out, error: !r.ok && r.err ? cleanError(r.err) : null };
}
