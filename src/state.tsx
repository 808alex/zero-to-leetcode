import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { ACHIEVEMENTS, newlyEarned, type Achievement } from "./lib/achievements";
import { play, setSoundEnabled } from "./lib/sound";
import { connectRemote, loadLocal, saveLocal, saveRemote, today, type Progress } from "./lib/storage";
import { ORDER } from "./content";

type Toast = { id: number; achievement: Achievement };

type Ctx = {
  progress: Progress;
  update: (mutate: (p: Progress) => void) => void;
  toasts: Toast[];
  dismissToast: (id: number) => void;
  isUnlocked: (levelId: string) => boolean;
  currentLevel: string | null;
};

const ProgressContext = createContext<Ctx | null>(null);

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [progress, setProgress] = useState<Progress>(() => loadLocal());
  const [toasts, setToasts] = useState<Toast[]>([]);
  const ref = useRef(progress);
  ref.current = progress;
  const toastId = useRef(0);

  useEffect(() => {
    connectRemote(ref.current).then((remote) => {
      if (remote) { setProgress(remote); saveLocal(remote); }
    });
  }, []);

  useEffect(() => {
    document.documentElement.dataset.skin = progress.settings.theme;
    setSoundEnabled(progress.settings.sound);
  }, [progress.settings.theme, progress.settings.sound]);

  const update = useCallback((mutate: (p: Progress) => void) => {
    const next: Progress = structuredClone(ref.current);
    mutate(next);
    const earned = newlyEarned(next);
    if (earned.length) {
      const now = Date.now();
      earned.forEach((a) => (next.ach[a.id] = now));
      setTimeout(() => {
        play("achievement");
        setToasts((t) => [...t, ...earned.map((a) => ({ id: ++toastId.current, achievement: a }))]);
      }, 600);
    }
    ref.current = next;
    setProgress(next);
    saveLocal(next);
    saveRemote(next);
  }, []);

  const dismissToast = useCallback((id: number) => setToasts((t) => t.filter((x) => x.id !== id)), []);

  const value = useMemo<Ctx>(() => {
    const isUnlocked = (id: string) => {
      if (progress.settings.unlockAll) return true;
      const i = ORDER.indexOf(id);
      return i === 0 || !!progress.done[ORDER[i - 1]];
    };
    const currentLevel = ORDER.find((id) => !progress.done[id] && isUnlocked(id)) ?? null;
    return { progress, update, toasts, dismissToast, isUnlocked, currentLevel };
  }, [progress, update, toasts, dismissToast]);

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
}

export function useProgress() {
  const c = useContext(ProgressContext);
  if (!c) throw new Error("useProgress outside provider");
  return c;
}

/** Mark today as active (for the streak). */
export function touchToday(p: Progress) {
  const d = today();
  if (!p.days.includes(d)) p.days = [...p.days.slice(-120), d];
}

export const achievementCount = (p: Progress) => ACHIEVEMENTS.filter((a) => p.ach[a.id]).length;
