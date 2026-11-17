import { useState } from "react";
import { Modal } from "../components/Bits";
import { Badge, Speaker } from "../components/Icons";
import { ACHIEVEMENTS } from "../lib/achievements";
import { freshProgress, type ThemeId } from "../lib/storage";
import { useProgress } from "../state";
import { play } from "../lib/sound";

const THEMES: { id: ThemeId; name: string; swatch: string[] }[] = [
  { id: "jungle", name: "Jungle", swatch: ["#58cc02", "#ffc800", "#1cb0f6", "#f7fff0"] },
  { id: "midnight", name: "Midnight", swatch: ["#8b5cff", "#2de2e6", "#ffd166", "#14112a"] },
  { id: "sunset", name: "Sunset", swatch: ["#ff7a45", "#ff4d8d", "#ffc23d", "#fff4ea"] },
  { id: "ocean", name: "Ocean", swatch: ["#1fb6ff", "#2ee6a6", "#ffd23f", "#0b1b2c"] },
];

export function SettingsPanel({ onClose }: { onClose: () => void }) {
  const { progress, update } = useProgress();
  const [confirm, setConfirm] = useState(false);
  const s = progress.settings;
  return (
    <Modal title="Settings" onClose={onClose}>
      <div className="settings">
        <section>
          <h3>Theme</h3>
          <div className="themes">
            {THEMES.map((t) => (
              <button key={t.id} className={`theme ${s.theme === t.id ? "on" : ""}`} aria-pressed={s.theme === t.id}
                onClick={() => { update((p) => { p.settings.theme = t.id; }); play("click"); }}>
                <span className="swatch">{t.swatch.map((c) => <i key={c} style={{ background: c }} />)}</span>
                {t.name}
              </button>
            ))}
          </div>
        </section>
        <section className="setting-row">
          <div><h3>Sound effects</h3><p className="muted small">Little sounds for right, wrong and level-ups.</p></div>
          <button className={`toggle ${s.sound ? "on" : ""}`} role="switch" aria-checked={s.sound} aria-label="Sound effects"
            onClick={() => { update((p) => { p.settings.sound = !p.settings.sound; }); if (!s.sound) setTimeout(() => play("correct"), 50); }}>
            <Speaker on={s.sound} size={18} /><span className="knob" />
          </button>
        </section>
        <section className="setting-row">
          <div><h3>Explore mode</h3><p className="muted small">Unlock every level so you can jump around. Your progress still counts.</p></div>
          <button className={`toggle ${s.unlockAll ? "on" : ""}`} role="switch" aria-checked={s.unlockAll} aria-label="Explore mode"
            onClick={() => update((p) => { p.settings.unlockAll = !p.settings.unlockAll; })}><span className="knob" /></button>
        </section>
        <section className="setting-row danger-zone">
          <div><h3>Reset progress</h3><p className="muted small">Wipes levels, achievements and streak. Your theme stays.</p></div>
          {confirm ? (
            <div className="row">
              <button className="btn ghost small" onClick={() => setConfirm(false)}>Cancel</button>
              <button className="btn danger small" onClick={() => { update((p) => { const f = freshProgress(); Object.assign(p, f, { settings: p.settings }); }); setConfirm(false); onClose(); }}>Yes, reset</button>
            </div>
          ) : <button className="btn ghost small" onClick={() => setConfirm(true)}>Reset…</button>}
        </section>
        <p className="muted small about">Every question in this game is checked by actually running it. Python runs in your browser with Pyodide; nothing you type leaves your device.</p>
      </div>
    </Modal>
  );
}

export function AchievementsPanel({ onClose }: { onClose: () => void }) {
  const { progress } = useProgress();
  return (
    <Modal title="Achievements" onClose={onClose} wide>
      <div className="ach-grid">
        {ACHIEVEMENTS.map((a) => {
          const got = !!progress.ach[a.id];
          return (
            <div key={a.id} className={`ach ${got ? "got" : ""}`}>
              <div className="ach-icon"><Badge name={a.icon} size={30} /></div>
              <div>
                <div className="ach-name">{a.name}</div>
                <div className="ach-desc">{a.desc}</div>
                {got && <div className="ach-date">{new Date(progress.ach[a.id]).toLocaleDateString()}</div>}
              </div>
            </div>
          );
        })}
      </div>
    </Modal>
  );
}
