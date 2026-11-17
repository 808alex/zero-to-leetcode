/**
 * Progress lives in localStorage. When the app runs inside Claude (as an artifact), it also syncs to the
 * viewer's private database so progress follows them between devices. On GitHub Pages that part simply
 * never switches on.
 */
export type ThemeId = "jungle" | "midnight" | "sunset" | "ocean";

export type LevelRecord = { at: number; hearts: number; assisted: boolean; comeback: boolean; firstTry: number; total: number };

export type Progress = {
  v: 1;
  done: Record<string, LevelRecord>;
  partial: Record<string, string[]>;
  missed: Record<string, number>;
  lc: Record<string, number>;
  ach: Record<string, number>;
  days: string[];
  stats: { mc: number; fill: number; fix: number; code: number; practice: number };
  settings: { theme: ThemeId; sound: boolean; unlockAll: boolean };
};

const KEY = "z2l:progress";

export function freshProgress(): Progress {
  const dark = typeof matchMedia !== "undefined" && matchMedia("(prefers-color-scheme: dark)").matches;
  return {
    v: 1, done: {}, partial: {}, missed: {}, lc: {}, ach: {}, days: [],
    stats: { mc: 0, fill: 0, fix: 0, code: 0, practice: 0 },
    settings: { theme: dark ? "midnight" : "jungle", sound: true, unlockAll: false },
  };
}

function merge(base: Progress, p: Partial<Progress>): Progress {
  return {
    ...base, ...p,
    stats: { ...base.stats, ...(p.stats || {}) },
    settings: { ...base.settings, ...(p.settings || {}) },
  } as Progress;
}

export function loadLocal(): Progress {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return merge(freshProgress(), JSON.parse(raw));
  } catch { /* storage unavailable or corrupt */ }
  return freshProgress();
}

export function saveLocal(p: Progress) {
  try { localStorage.setItem(KEY, JSON.stringify(p)); } catch { /* ignore */ }
}

// ---------------------------------------------------------------- optional sync inside Claude
type DocRef = { get(): Promise<{ exists: boolean; data(): any }>; set(d: any): Promise<void> };
let remote: DocRef | null = null;
let timer: number | undefined;
let saving = false;
let queued: Progress | null = null;

const withTimeout = <T,>(p: Promise<T>, ms: number) =>
  Promise.race([p, new Promise<T>((_, rej) => setTimeout(() => rej(new Error("timeout")), ms))]);

export async function connectRemote(local: Progress): Promise<Progress | null> {
  try {
    const claude = (window as any).claude;
    if (!claude || typeof claude.use !== "function") return null;
    const [db, user] = await Promise.all([claude.use("db"), claude.use("user")]);
    if (!db || !user) return null;
    const uid = await user.id();
    if (!uid) return null;
    const ref: DocRef = db.doc("data/users/" + uid + "/game");
    const snap = await withTimeout(ref.get(), 10000);
    remote = ref;
    if (snap.exists) {
      const r = merge(freshProgress(), JSON.parse(snap.data()!.json || "{}"));
      // keep whichever has more finished levels; ties go to the remote copy
      if (Object.keys(r.done).length >= Object.keys(local.done).length) return r;
    }
    saveRemote(local);
    return null;
  } catch {
    remote = null;
    return null;
  }
}

export function saveRemote(p: Progress) {
  if (!remote) return;
  queued = p;
  clearTimeout(timer);
  timer = window.setTimeout(flush, 1200);
}

async function flush() {
  if (!remote || saving || !queued) return;
  saving = true;
  const p = queued;
  queued = null;
  try { await remote.set({ json: JSON.stringify(p) }); }
  catch { remote = null; }
  finally { saving = false; if (queued) flush(); }
}

// ---------------------------------------------------------------- streak
export const today = () => new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD in local time

export function streakOf(days: string[]): { count: number; activeToday: boolean } {
  const set = new Set(days);
  const d = new Date();
  const activeToday = set.has(today());
  if (!activeToday) d.setDate(d.getDate() - 1);
  let count = 0;
  while (set.has(d.toLocaleDateString("en-CA"))) { count++; d.setDate(d.getDate() - 1); }
  return { count, activeToday };
}
