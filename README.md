# Zero to LeetCode

A game that takes you from your first line of Python (or from "I used to know this") to LeetCode-ready. You follow a winding level path with Pip the snake, read a short lesson, then answer questions in real Python that runs in your browser. Each unit ends with a boss fight.

![The level path](docs/path.png)

## What's in it

- **30 levels across 6 units.** Unit 0 starts from `print` and `input`. Unit 1 covers interview Python, the standard toolkit, Big-O and recursion. Units 2–4 cover the 12 core LeetCode patterns: hashing, two pointers, sliding window, stacks, binary search, linked lists, trees, heaps, backtracking, graphs, DP, intervals and greedy. Unit 5 is about how to practise.
- **237 questions in four types:**
  - **What does this print?** You read code and pick its output.
  - **Fill in the blank.** You type the missing expression, and it runs against tests.
  - **Fix the bug.** Broken code goes into a real editor, and you make the tests pass.
  - **Write the code.** A full exercise with tests. Several also link to the matching LeetCode problem.
- **Mastery, not luck.** Every skill has several questions, and a wrong answer goes back into the queue, so you have to get it right again later.
- **Hearts that send you back to learn.** You get 3 hearts per level, and only the quick-answer questions (what does this print, fill in the blank) cost them. Running your code is always free. Lose all 3 and you're sent back over the lesson. You return with full hearts and the helper unlocked, and your progress in the level is kept.
- **A helper that gives away a bit at a time.** It unlocks after 3 failed tries and goes hint, then explanation, then the answer. If the helper reveals the answer to a question, that question comes back once more so you still have to get it on your own.
- **Boss levels.** Three harder challenges with hidden tests, and a failed submit costs a heart. You get no lesson and no solutions.
- **Quickfire.** A scored round of random quick questions from every level you've reached, with your past mistakes mixed in and a streak counter.
- **Common mistakes.** 35 classic slips (missing colons, `x == 6 or 7`, `nums = nums.sort()`, `[[0] * n] * m`, mutable defaults, `x in list` in a loop...). Each shows the wrong code, the fix, and the message Python really prints, recorded by running it at build time.
- **Next stop: LeetCode.** A guide at the end of the path: setting up LeetCode, what a problem looks like in Python, the solving routine and practice habits from the levels, and where to go next.
- **Extras:** 19 achievements, a daily streak, four themes, synthesised sound effects (no audio files) and 137 real LeetCode problems to tick off.

| | |
|---|---|
| ![A question](docs/question.png) | ![Boss fight](docs/boss.png) |
| ![Level complete](docs/complete.png) | ![Midnight theme](docs/midnight.png) |

## Every answer is checked by running it

The content is written in Python (`content/`), and `content/build_content.py` turns it into `src/content/content.json`. Along the way it:

- runs the code in every "what does this print" question and uses the **real output** as the correct option. It fails if a wrong option happens to match.
- computes the expected results for fill-in and fix-the-bug questions from the reference answer. It checks that the buggy version really fails, and that junk answers like `0`, `None` or `True` don't pass.
- runs every coding solution and boss solution against its tests. Two bosses are also cross-checked against brute force.
- runs every snippet in the Common mistakes library and records the real error message or output.
- times out anything that loops forever.

The GitHub Action runs this on every push, so a wrong answer can't be deployed.

## How it runs

- **React + TypeScript + Vite**, with no UI framework. The mascot, icons and road are hand-drawn SVG, and the animations are CSS.
- **Pyodide** runs CPython (compiled to WebAssembly) inside a Web Worker. Infinite loops get killed after 10 seconds instead of freezing the tab. The worker builds a small test harness around your code and reports each test case back.
- **CodeMirror 6** is the editor, and **Prism** highlights the read-only code.
- Progress is stored in `localStorage`. Nothing you type leaves your browser.

## Run it locally

```bash
npm install
pip install markdown        # only needed to rebuild the content
npm run content             # verify every question and regenerate content.json
npm run dev
```

`npm run build` writes a static site to `dist/`. The site loads Pyodide from jsDelivr, or from another URL if you add `?pyodide=<url>`.

## Deploy

Push to `main`. The workflow in `.github/workflows/deploy.yml` verifies the content, builds the site and publishes it to GitHub Pages. In the repo's settings, go to Pages → Source and choose **GitHub Actions**.

## Project layout

```
content/            question bank (Python) + the build/verify script
  lessons/*.md      lesson text, split into cards at each "## " heading
  drills*.py        coding questions with tests
  game.py           quick questions, skills per level, bosses
  mistakes.py       the common mistakes library
  harness.py        the Python test harness that also runs in the browser
src/
  lib/python.ts     Pyodide worker, timeouts, test running
  screens/          path, lessons, question session, helper, mistakes, LeetCode guide
  components/       questions, editor, Pip, icons
  styles/app.css    four themes and all the animation
```

## Licence

MIT
