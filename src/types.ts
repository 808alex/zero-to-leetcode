export type Unit = { id: string; title: string; blurb: string; levels: string[]; boss: string };
export type Card = { title: string; html: string };
export type Skill = { name: string; questions: string[] };
export type LeetCodeProblem = { slug: string; title: string; diff: "Easy" | "Medium" | "Hard" };

export type Level = {
  id: string;
  unit: string;
  kind: "lesson" | "boss";
  title: string;
  short: string;
  cards: Card[];
  skills: Skill[];
  lc: LeetCodeProblem[];
};

export type TestSpec = { fn: string; tests: string; cmp: string; prep: string };

export type MCQuestion = {
  id: string;
  kind: "mc";
  prompt: string;
  code: string | null;
  stdin: string;
  options: string[];
  answer: number;
  explain: string;
  concept?: boolean;
};

export type FillQuestion = TestSpec & {
  id: string;
  kind: "fill";
  prompt: string;
  code: string;
  answer: string;
  hint: string;
  explain: string;
};

export type CodeQuestion = TestSpec & {
  id: string;
  kind: "code" | "fix";
  title: string;
  prompt: string;
  starter: string;
  hint: string;
  solution: string;
  explain?: string;
  lc?: string | null;
  boss?: boolean;
  testsVisible?: string;
  visibleCount?: number;
  hidden?: number;
};

export type Question = MCQuestion | FillQuestion | CodeQuestion;

export type Mistake = {
  id: string;
  cat: string;
  level: string;
  title: string;
  wrong: string;
  right: string;
  why: string;
  wrongOut?: string;
  wrongErr?: string | null;
  rightOut?: string;
};

export type Content = {
  mistakes: Mistake[];
  mistakeCategories: string[];
  units: Unit[];
  levels: Level[];
  questions: Record<string, Question>;
  harness: { prelude: string; functions: string; stdout: string };
};

export type TestRow = { args?: string; exp?: string; got?: string; ok?: boolean; err?: string };
export type RunOutcome = {
  rows: TestRow[] | null;
  passed: number;
  total: number;
  allPassed: boolean;
  setupError: string | null; // e.g. "Define a function called x" or a syntax error
  error: string | null; // crash outside the tests, timeout, Python not loading
  output: string; // anything the user printed
};
