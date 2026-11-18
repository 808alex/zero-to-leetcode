import { useMemo } from "react";
import { LEVELS, ORDER } from "../content";
import { useProgress } from "../state";
import { CodeView } from "../components/Bits";
import { Back, Flag } from "../components/Icons";
import { Pip } from "../components/Mascot";
import { LeetCodeList } from "../components/LeetCodeList";

const SECTIONS = [
  ["setup", "Set up"],
  ["anatomy", "Anatomy of a problem"],
  ["python", "Python on LeetCode"],
  ["routine", "How to solve one"],
  ["habits", "How to practise"],
  ["constraints", "Read the constraints"],
  ["patterns", "Spot the pattern"],
  ["where", "What to do next"],
] as const;

const Ext = ({ href, children }: { href: string; children: React.ReactNode }) => <a href={href} target="_blank" rel="noopener">{children} ↗</a>;

export function GuideScreen({ onBack, onMistakes }: { onBack: () => void; onMistakes: () => void }) {
  const { progress } = useProgress();
  // the next problems you haven't ticked off yet, in path order
  const next = useMemo(() => {
    const seen = new Set<string>();
    return ORDER.flatMap((id) => LEVELS[id].lc).filter((p) => {
      if (seen.has(p.slug) || progress.lc[p.slug] || p.diff === "Hard") return false;
      seen.add(p.slug);
      return true;
    }).slice(0, 8);
  }, [progress.lc]);

  return (
    <div className="page">
      <header className="page-top">
        <button className="btn ghost" onClick={onBack}><Back size={18} /> Path</button>
        <h1><Flag size={28} /> Next stop: LeetCode</h1>
      </header>
      <div className="page-body guide">
        <div className="page-intro">
          <Pip mood="cheer" size={86} />
          <p>Everything in this game was practice for one site. This page shows you how to set it up, what a LeetCode problem looks like in Python, and the habits from the levels that matter most once you're on your own.</p>
        </div>
        <div className="guide-cta">
          <a className="btn primary big" href="https://leetcode.com/" target="_blank" rel="noopener">Open leetcode.com ↗</a>
          <a className="btn secondary big" href="https://leetcode.com/problemset/" target="_blank" rel="noopener">Problem list ↗</a>
        </div>
        <nav className="toc" aria-label="On this page">
          {SECTIONS.map(([id, t], i) => <a key={id} href={`#g-${id}`} onClick={(e) => { e.preventDefault(); document.getElementById(`g-${id}`)?.scrollIntoView({ behavior: "smooth" }); }}><span>{i + 1}</span>{t}</a>)}
        </nav>

        <section id="g-setup" className="guide-sec">
          <h2>1. Set up (five minutes)</h2>
          <ol>
            <li>Make a free account at <Ext href="https://leetcode.com/">leetcode.com</Ext>. You don't need Premium. The free problems cover everything in this game, and problems with a lock icon can simply be skipped.</li>
            <li>Open any problem, then pick <strong>Python3</strong> in the language menu above the code editor. LeetCode remembers it.</li>
            <li>In the editor settings, set the tab size to <strong>4 spaces</strong> and pick a font size you can read comfortably for 45 minutes.</li>
            <li>Keep a notes file (a doc, Notion page, or a text file). After every problem you'll write one line in it. More on that below.</li>
          </ol>
        </section>

        <section id="g-anatomy" className="guide-sec">
          <h2>2. Anatomy of a problem</h2>
          <ul>
            <li><strong>Description</strong>: the task, a few examples, and the <strong>constraints</strong> at the bottom. Read the constraints first; they tell you how fast your solution needs to be.</li>
            <li><strong>Code editor</strong>: starts with a <code>class Solution</code> and an empty method. You fill in the method and <strong>return</strong> the answer.</li>
            <li><strong>Run</strong> checks your code on the examples, plus any extra test cases you add in the Testcase panel. It's free, like <em>Run samples</em> in a boss fight.</li>
            <li><strong>Submit</strong> runs every hidden test. That's the real check, exactly like <em>Submit</em> in a boss fight. Add your own edge cases with Run before you submit.</li>
            <li><strong>Editorial</strong> and <strong>Solutions</strong> tabs: the official write-up and other people's answers. Use them after you've solved it, or once your time is up (see How to practise).</li>
          </ul>
          <p>Here's Two Sum, which you solved in Arrays &amp; hashing, as LeetCode shows it:</p>
          <CodeView code={`class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i`} />
        </section>

        <section id="g-python" className="guide-sec">
          <h2>3. Python on LeetCode</h2>
          <ul>
            <li><code>self</code> is there because the function lives inside a class. Ignore it: write the body exactly as you did in the game.</li>
            <li>Type hints like <code>List[int]</code> and <code>Optional[ListNode]</code> are only labels. <code>Optional[TreeNode]</code> means "a node, or None".</li>
            <li><code>ListNode</code> and <code>TreeNode</code> are already defined for you, shown in a comment above the class. Same fields as in the game: <code>val</code>, <code>next</code>, <code>left</code>, <code>right</code>.</li>
            <li>When a problem says <em>"do not return anything, modify nums in-place"</em>, LeetCode checks the list it gave you. Change it with <code>nums.sort()</code> or <code>nums[:] = ...</code>; writing <code>nums = ...</code> changes nothing it can see.</li>
            <li>Need a helper with <code>@cache</code> or recursion? Define it <strong>inside</strong> the method, the same way you wrote <code>dfs</code> and <code>backtrack</code> in the game.</li>
            <li>Very deep recursion (big grids, long linked lists) can hit Python's limit. Switch to BFS or an explicit stack, or add <code>sys.setrecursionlimit(10**6)</code>.</li>
            <li>The usual imports (<code>collections</code>, <code>heapq</code>, <code>bisect</code>, <code>functools</code>) work as normal. Writing the import yourself is a good habit, because interviewers expect it.</li>
          </ul>
          <CodeView code={`# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        return prev`} />
          <p>Most failed submissions come from the same handful of slips. They're all collected in <button className="linklike" onClick={onMistakes}>Common mistakes</button>.</p>
        </section>

        <section id="g-routine" className="guide-sec">
          <h2>4. How to solve one (the routine from Big-O &amp; approach)</h2>
          <ol>
            <li><strong>Restate it</strong> in your own words and walk the examples by hand. Invent an edge case: empty input, one element, duplicates, negatives.</li>
            <li><strong>Say the brute force</strong> and its complexity before writing anything clever.</li>
            <li><strong>Find the waste</strong>: what does the brute force recompute or rescan?</li>
            <li><strong>Pick the pattern</strong> (table below) and write it.</li>
            <li><strong>Test by hand</strong> with your edge cases, then Run, then Submit.</li>
          </ol>
        </section>

        <section id="g-habits" className="guide-sec">
          <h2>5. How to practise (from Practice system &amp; beyond)</h2>
          <ul>
            <li><strong>Use a timer</strong>: about 20 minutes for an Easy, 35 for a Medium, 50 for a Hard.</li>
            <li><strong>Stuck when the timer ends?</strong> Read only the <em>approach</em> in the Editorial, close it, and write the code yourself.</li>
            <li><strong>Write one line</strong> in your notes after every problem: the trick in plain words. ("Sort by end time; keep the earliest finisher.")</li>
            <li><strong>Re-solve from scratch</strong> after about 3 days and again after about 2 weeks. If you can't, it goes back on the list. Recalling a solution after a gap is the part that makes it stick.</li>
            <li><strong>Mediums are where interviews live.</strong> Once a pattern's Easies feel routine, move up.</li>
            <li><strong>Talk out loud</strong> while you solve, even alone. In an interview, they're grading your reasoning as much as your code.</li>
            <li><strong>Keep the streak going here too</strong>: a round of Quickfire on days you don't do a full problem.</li>
          </ul>
        </section>

        <section id="g-constraints" className="guide-sec">
          <h2>6. Read the constraints</h2>
          <div className="table-wrap">
            <table>
              <thead><tr><th>n up to</th><th>Aim for</th><th>Usually means</th></tr></thead>
              <tbody>
                <tr><td>10–12</td><td>O(n!)</td><td>permutations, brute force</td></tr>
                <tr><td>20–25</td><td>O(2ⁿ)</td><td>subsets, backtracking</td></tr>
                <tr><td>100–500</td><td>O(n³)</td><td>triple loops, interval DP</td></tr>
                <tr><td>1,000–5,000</td><td>O(n²)</td><td>double loop, 2D DP</td></tr>
                <tr><td>10⁵–10⁶</td><td>O(n log n) or O(n)</td><td>sorting, heaps, hashing, two pointers, sliding window</td></tr>
                <tr><td>10⁹+</td><td>O(log n) or O(1)</td><td>binary search, maths</td></tr>
              </tbody>
            </table>
          </div>
          <p className="muted small">Python manages roughly 10⁷ simple operations a second. If your plan is above that for the largest n, it will time out.</p>
        </section>

        <section id="g-patterns" className="guide-sec">
          <h2>7. Spot the pattern</h2>
          <div className="table-wrap">
            <table>
              <thead><tr><th>The problem says…</th><th>Try</th></tr></thead>
              <tbody>
                <tr><td>pair / duplicate in an unsorted array</td><td>hashmap or set</td></tr>
                <tr><td>sorted array, pair or triplet</td><td>two pointers</td></tr>
                <tr><td>longest / shortest contiguous subarray or substring</td><td>sliding window</td></tr>
                <tr><td>subarray sum equals k (with negatives)</td><td>prefix sums + hashmap</td></tr>
                <tr><td>next greater / smaller, brackets</td><td>(monotonic) stack</td></tr>
                <tr><td>sorted, or "minimum value that works"</td><td>binary search</td></tr>
                <tr><td>top k, k-th largest, merge k lists</td><td>heap</td></tr>
                <tr><td>all subsets / permutations / combinations</td><td>backtracking</td></tr>
                <tr><td>grid, islands, regions</td><td>DFS / BFS on the grid</td></tr>
                <tr><td>fewest steps, unweighted</td><td>BFS</td></tr>
                <tr><td>prerequisites, ordering</td><td>topological sort</td></tr>
                <tr><td>how many ways, min cost, can you reach</td><td>dynamic programming</td></tr>
                <tr><td>intervals, meetings</td><td>sort, then greedy sweep</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section id="g-where" className="guide-sec">
          <h2>8. What to do next</h2>
          <p><strong>First, the problems from this game</strong> you haven't ticked off yet. Each level's set is in its menu on the path; these are the next ones in order (Hards left out for now):</p>
          {next.length ? <LeetCodeList problems={next} /> : <p className="muted">You've ticked off every Easy and Medium in the game. Nice.</p>}
          <p><strong>Then, a LeetCode study plan.</strong> Both are free, ordered by topic, and give you a badge when you finish:</p>
          <ul>
            <li><Ext href="https://leetcode.com/studyplan/leetcode-75/">LeetCode 75</Ext>: 75 essential problems, aimed at one to three months of prep. A good first plan.</li>
            <li><Ext href="https://leetcode.com/studyplan/top-interview-150/">Top Interview 150</Ext>: broader, aimed at three months or more.</li>
          </ul>
          <p>You can also filter the <Ext href="https://leetcode.com/problemset/">problem list</Ext> by topic tag (Array, Hash Table, Two Pointers, Sliding Window, Tree, Graph, Dynamic Programming…) to drill one pattern at a time, the same way the units here are laid out.</p>
        </section>
      </div>
    </div>
  );
}
