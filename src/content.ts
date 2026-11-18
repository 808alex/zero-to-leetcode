import raw from "./content/content.json";
import type { Content, Level, Question, Unit } from "./types";

export const CONTENT = raw as unknown as Content;

export const UNITS: Unit[] = CONTENT.units;
export const LEVELS: Record<string, Level> = Object.fromEntries(CONTENT.levels.map((l) => [l.id, l]));
export const QUESTIONS: Record<string, Question> = CONTENT.questions;

/** Every node on the path, in order: each unit's levels, then its boss. */
export const ORDER: string[] = UNITS.flatMap((u) => [...u.levels, u.boss]);

export const levelQuestions = (l: Level): string[] => l.skills.flatMap((s) => s.questions);
export const skillOf = (l: Level, qid: string) => l.skills.find((s) => s.questions.includes(qid));
export const unitOf = (id: string) => UNITS.find((u) => u.levels.includes(id) || u.boss === id)!;
export const unitIndex = (id: string) => UNITS.findIndex((u) => u.id === id);

export const MISTAKES = CONTENT.mistakes;
export const MISTAKE_CATEGORIES = CONTENT.mistakeCategories;

export const TOTAL_QUESTIONS = Object.keys(QUESTIONS).length;
