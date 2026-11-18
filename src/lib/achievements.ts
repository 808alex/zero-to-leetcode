import type { Progress } from "./storage";
import { streakOf } from "./storage";

export type Achievement = { id: string; name: string; desc: string; icon: string; test: (p: Progress) => boolean };

const done = (p: Progress, id: string) => !!p.done[id];
const lessons = (p: Progress) => Object.entries(p.done).filter(([id]) => !id.startsWith("b"));

export const ACHIEVEMENTS: Achievement[] = [
  { id: "first-steps", name: "First steps", desc: "Finish your first level.", icon: "foot", test: (p) => done(p, "z1") },
  { id: "loop-tamer", name: "Loop tamer", desc: "Finish While loops.", icon: "loop", test: (p) => done(p, "z3") },
  { id: "flawless", name: "Flawless", desc: "Finish a level without losing a heart.", icon: "heart", test: (p) => lessons(p).some(([, r]) => r.hearts === 3) },
  { id: "self-made", name: "Self-made", desc: "Finish a level without opening the helper.", icon: "star", test: (p) => lessons(p).some(([, r]) => !r.assisted) },
  { id: "comeback", name: "Comeback", desc: "Run out of hearts, review the lesson, and still finish the level.", icon: "rise", test: (p) => lessons(p).some(([, r]) => r.comeback) },
  { id: "bug-hunter", name: "Bug hunter", desc: "Fix 10 bugs.", icon: "bug", test: (p) => p.stats.fix >= 10 },
  { id: "code-reader", name: "Code reader", desc: "Get 25 \"what does this print\" questions right.", icon: "eye", test: (p) => p.stats.mc >= 25 },
  { id: "builder", name: "Builder", desc: "Pass 25 write-the-code challenges.", icon: "brick", test: (p) => p.stats.code >= 25 },
  { id: "practice-10", name: "Quick on the draw", desc: "Get 10 Quickfire questions right.", icon: "bolt", test: (p) => p.stats.practice >= 10 },
  { id: "streak-3", name: "On a roll", desc: "Keep a 3-day streak.", icon: "flame", test: (p) => streakOf(p.days).count >= 3 },
  { id: "streak-7", name: "Week strong", desc: "Keep a 7-day streak.", icon: "flame", test: (p) => streakOf(p.days).count >= 7 },
  { id: "quick-10", name: "Perfect round", desc: "Score 10 out of 10 in Quickfire.", icon: "bolt", test: (p) => p.stats.quickBest >= 10 },
  { id: "lc-10", name: "Into the wild", desc: "Tick off 10 real LeetCode problems.", icon: "flag", test: (p) => Object.keys(p.lc).length >= 10 },
  { id: "b0", name: "Gatekeeper down", desc: "Beat the Unit 0 boss.", icon: "crown", test: (p) => done(p, "b0") },
  { id: "b1", name: "Refactored", desc: "Beat the Unit 1 boss.", icon: "crown", test: (p) => done(p, "b1") },
  { id: "b2", name: "Pattern spotter", desc: "Beat the Unit 2 boss.", icon: "crown", test: (p) => done(p, "b2") },
  { id: "b3", name: "Linked up", desc: "Beat the Unit 3 boss.", icon: "crown", test: (p) => done(p, "b3") },
  { id: "b4", name: "Grand searcher", desc: "Beat the Unit 4 boss.", icon: "crown", test: (p) => done(p, "b4") },
  { id: "b5", name: "LeetCode ready", desc: "Beat the final boss.", icon: "trophy", test: (p) => done(p, "b5") },
];

/** Returns achievements that are newly earned in `p` (and not yet recorded). */
export const newlyEarned = (p: Progress) => ACHIEVEMENTS.filter((a) => !p.ach[a.id] && a.test(p));
