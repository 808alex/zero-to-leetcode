/** Tiny synthesised sound effects (no audio files). */
let ctx: AudioContext | null = null;
let enabled = true;
export const setSoundEnabled = (on: boolean) => { enabled = on; };

function ac(): AudioContext | null {
  if (!enabled) return null;
  try {
    if (!ctx) ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  } catch { return null; }
}

function tone(freq: number, start: number, dur: number, type: OscillatorType = "sine", vol = 0.18, slideTo?: number) {
  const a = ac();
  if (!a) return;
  const t = a.currentTime + start;
  const o = a.createOscillator();
  const g = a.createGain();
  o.type = type;
  o.frequency.setValueAtTime(freq, t);
  if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, t + dur);
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(vol, t + 0.015);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(g).connect(a.destination);
  o.start(t);
  o.stop(t + dur + 0.05);
}

export type Sfx = "correct" | "wrong" | "heart" | "complete" | "unlock" | "click" | "boss" | "achievement";

export function play(s: Sfx) {
  switch (s) {
    case "click": tone(660, 0, 0.06, "triangle", 0.08); break;
    case "correct": tone(784, 0, 0.12, "triangle"); tone(1175, 0.09, 0.2, "triangle"); break;
    case "wrong": tone(220, 0, 0.22, "square", 0.08, 160); break;
    case "heart": tone(440, 0, 0.12, "sawtooth", 0.08, 330); tone(330, 0.12, 0.25, "sawtooth", 0.07, 180); break;
    case "complete": [523, 659, 784, 1047].forEach((f, i) => tone(f, i * 0.11, 0.28, "triangle", 0.16)); break;
    case "unlock": tone(880, 0, 0.1, "sine", 0.12); tone(1320, 0.08, 0.18, "sine", 0.12); break;
    case "boss": [196, 247, 294, 392].forEach((f, i) => tone(f, i * 0.13, 0.35, "sawtooth", 0.07)); break;
    case "achievement": [988, 1319, 1568].forEach((f, i) => tone(f, i * 0.07, 0.2, "sine", 0.12)); break;
  }
}
