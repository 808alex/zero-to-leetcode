import type { LeetCodeProblem } from "../types";
import { useProgress } from "../state";
import { play } from "../lib/sound";

export function LeetCodeList({ problems }: { problems: LeetCodeProblem[] }) {
  const { progress, update } = useProgress();
  return (
    <ul className="lc-list">
      {problems.map((p) => {
        const done = !!progress.lc[p.slug];
        return (
          <li key={p.slug} className={done ? "done" : ""}>
            <input type="checkbox" id={`lc-${p.slug}`} checked={done} aria-label={`Mark ${p.title} as solved`}
              onChange={(e) => { const on = e.target.checked; if (on) play("click"); update((pr) => { if (on) pr.lc[p.slug] = Date.now(); else delete pr.lc[p.slug]; }); }} />
            <a href={`https://leetcode.com/problems/${p.slug}/`} target="_blank" rel="noopener">{p.title}</a>
            <span className={`diff ${p.diff}`}>{p.diff}</span>
          </li>
        );
      })}
    </ul>
  );
}
