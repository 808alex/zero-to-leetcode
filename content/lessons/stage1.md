=== m1
Unit 0 got the basics moving again. This level tightens them into the Python people actually write in interviews: shortcuts that replace the manual index loops and extra variables beginners tend to write. If a line below looks unfamiliar, that's the bit to practise.

## Loops without manual indexes

Beginner code is full of `i = 0; while i < len(s): ...; i = i + 1`. In Python you almost never need that.

```python
for ch in s:                      # just the items
for i in range(n):                # 0 .. n-1
for i in range(n - 1, -1, -1):    # n-1 down to 0
for i, ch in enumerate(s):        # index and item together
for a, b in zip(xs, ys):          # walk two lists in step
```

Keep `while` for when the step isn't fixed: two pointers, binary search, "keep going until". To leave a loop early, use `break`, or `return` inside a function. Setting `i = len(s)` to force an exit is a workaround from languages without `break`.

## Slicing

`s[start:stop:step]`, stop excluded. Works on lists, strings and tuples, and always makes a **copy**.

```python
s[::-1]     # reversed
a[1:]       # all but the first
a[:k]       # first k
a[-1]       # last item
b = a[:]    # shallow copy of a list
```

## Comprehensions

```python
squares = [x * x for x in nums]
evens   = [x for x in nums if x % 2 == 0]
index   = {v: i for i, v in enumerate(nums)}
unique  = {x % 10 for x in nums}
grid    = [[0] * cols for _ in range(rows)]
```

## Functions return, they don't print

LeetCode calls your function and checks the **return value**. Get out of the `input()`/`print()` habit from beginner exercises.

```python
def min_max(nums):
    return min(nums), max(nums)   # returns a tuple

lo, hi = min_max([3, 1, 4])       # unpacking
a, b = b, a                       # swap, no temp variable
```

## Things you'll use every day

```python
x if cond else y                  # ternary
any(x < 0 for x in nums)          # True if at least one
all(x > 0 for x in nums)
max(words, key=len)               # longest word
sorted(pairs, key=lambda p: p[1]) # sort by second item
ch.isdigit(), ch.isalpha(), ch.isupper(), ch.lower()
" ".join(words)                   # list of strings -> one string
s.split()                         # string -> words
ord("a"), chr(97)                 # char <-> code; ord(ch) - ord("a") gives 0..25
float("inf"), float("-inf")       # starting values for min/max searches
divmod(17, 5)                     # (3, 2)
```

Truthiness: empty list, empty string, `0`, `None` are all falsy. `if not stack:` is the normal way to check for empty.

> **Coming up:** classic beginner programs, rewritten the Python way.

=== m2
LeetCode in Python is mostly about picking the right built-in container. Know what each operation costs, because the cost is usually what makes a solution pass or fail.

## What things cost

| Operation | list | dict / set | deque |
|---|---|---|---|
| index `a[i]` | O(1) | — | O(n) |
| `x in ...` | **O(n)** | **O(1)** | O(n) |
| append / add at end | O(1) | O(1) | O(1) |
| pop from end | O(1) | — | O(1) |
| pop from front | **O(n)** | — | **O(1)** |
| insert at front | O(n) | — | O(1) |
| sort | O(n log n) | — | — |

The two rows that catch people: `x in list` inside a loop turns O(n) into O(n²), and `list.pop(0)` is O(n). If you need a queue, use a `deque`.

## collections

```python
from collections import Counter, defaultdict, deque

Counter("hello")              # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
Counter(nums).most_common(2)  # [(value, count), ...]

graph = defaultdict(list)     # missing keys start as []
graph[a].append(b)
count = defaultdict(int)      # missing keys start as 0
count[x] += 1

q = deque([start])
q.append(x); q.popleft()      # BFS queue, both O(1)
```

## heapq (min-heap on a plain list)

```python
import heapq
heapq.heapify(nums)            # O(n), in place
heapq.heappush(h, x)           # O(log n)
smallest = heapq.heappop(h)    # O(log n)
h[0]                           # peek at the smallest
heapq.heappush(h, -x)          # max-heap trick: store negatives
heapq.heappush(h, (dist, node))  # tuples compare by first item
heapq.nlargest(k, nums), heapq.nsmallest(k, nums, key=...)
```

## bisect (binary search on a sorted list)

```python
from bisect import bisect_left, bisect_right
bisect_left(a, x)    # first index i with a[i] >= x
bisect_right(a, x)   # first index i with a[i] > x
```

## Sorting

`a.sort()` sorts in place and returns `None`. `sorted(a)` returns a new list. For multiple criteria, use a tuple key: `key=lambda p: (-p.score, p.name)`.

## Traps

- `grid = [[0] * n] * m` makes m references to **the same row**. Use `[[0] * n for _ in range(m)]`.
- `def f(x, seen=[])`: the default list is shared between calls. Use `seen=None`.
- `s += ch` in a loop can be O(n²). Collect pieces in a list and `"".join(parts)`.
- `-7 // 2 == -4` (floors). For truncation toward zero, use `int(-7 / 2)`.
- Recursion limit is about 1000 deep. Deep DFS on big inputs might need `sys.setrecursionlimit(10**6)` or an explicit stack.
- Strings are immutable. To edit characters, `chars = list(s)`, edit, then `"".join(chars)`.

=== m3
Every LeetCode problem gives you constraints. They tell you which complexity the intended solution has before you've thought about the problem.

## Read the constraints first

| n up to | Target complexity | Usually means |
|---|---|---|
| 10–12 | O(n!) | permutations, brute force |
| 20–25 | O(2ⁿ) | subsets, backtracking, bitmasks |
| 100–500 | O(n³) | triple loop, interval DP |
| 1,000–5,000 | O(n²) | double loop, 2D DP |
| 10⁵–10⁶ | O(n log n) or O(n) | sorting, heap, hashing, two pointers, sliding window |
| 10⁹ or more | O(log n) or O(1) | binary search, maths |

Rule of thumb: Python handles about 10⁷ simple operations per second. If n = 10⁵, O(n²) = 10¹⁰, which will time out.

## Complexity, quickly

- One loop over n: O(n). Nested loops over n: O(n²).
- Halving each step (binary search): O(log n).
- Sorting: O(n log n). If you sort first, the whole solution is at least that.
- Recursion: (number of calls) × (work per call). Fibonacci without memo is O(2ⁿ); with memo, O(n).
- Hidden costs: `x in list`, slicing, `list.pop(0)`, `s + t` on strings. Each is O(n).
- Space counts too: a set of everything seen is O(n) extra.

## The routine (use it on every problem)

1. **Restate it** and walk through the given examples by hand. Invent an edge case: empty input, one element, all duplicates, negatives.
2. **Say the brute force** and its complexity. In interviews, saying it out loud is worth points.
3. **Find the waste.** What does the brute force recompute or rescan? That is usually where the pattern comes in.
4. **Pick the pattern** (table below), then write the code.
5. **Test by hand** with your edge cases before you hit submit.

## Spotting the pattern

| The problem says... | Try |
|---|---|
| "pair / two numbers that...", unsorted | hashmap |
| sorted array, pair or triplet | two pointers |
| contiguous subarray or substring, "longest/shortest with..." | sliding window |
| subarray sum equals k, with negatives | prefix sums + hashmap |
| "next greater/smaller", matching brackets | stack (monotonic) |
| sorted, or "minimum value such that it works" | binary search |
| top k, k-th largest, streaming median, merge k lists | heap |
| all combinations / subsets / permutations | backtracking |
| grid, islands, connected regions | DFS/BFS on the grid |
| shortest path, fewest steps (unweighted) | BFS |
| dependencies, ordering, "prerequisites" | topological sort |
| "how many ways", "min cost", "can you reach", choices that overlap | dynamic programming |
| intervals, meetings, ranges | sort by start or end, then greedy |

> **Self-check:** n = 2 × 10⁵ and your plan has a nested loop. Will it pass? (No: 4 × 10¹⁰ operations. Look for O(n log n).)

=== m4
Trees, backtracking, DFS and DP are all recursion. If recursion feels shaky, those four topics will too, so fix it here.

## The three questions

1. **Base case:** what's the smallest input whose answer you know immediately? (Empty list, `None` node, n == 0.)
2. **Smaller problem:** how does the input shrink? (`n - 1`, `node.left`, `nums[1:]`, index `i + 1`.)
3. **Combine:** assuming the recursive call returns the right answer for the smaller problem, how do you build this answer from it?

Step 3 is the hard part to accept. Don't trace the whole call stack in your head. Assume the recursive call is correct and only check that one level is.

```python
def depth(node):
    if node is None:               # 1. base case
        return 0
    left = depth(node.left)        # 2. smaller problems
    right = depth(node.right)
    return 1 + max(left, right)    # 3. combine
```

## Two styles

**Return the answer** (like `depth` above). This is cleanest when the answer for a node depends only on its children.

**Accumulate into an outer variable** when you need something global, such as a best-so-far or a list of results:

```python
def all_paths(root):
    res = []
    def dfs(node, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right:
            res.append(path[:])      # copy: path keeps changing
        dfs(node.left, path)
        dfs(node.right, path)
        path.pop()                   # undo before returning
    dfs(root, [])
    return res
```

To rebind an outer variable such as a number (`best = max(best, x)`), declare `nonlocal best` inside the inner function. Mutating an outer list (`res.append`) doesn't need it.

## Memoisation: recursion becomes DP

```python
from functools import cache

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)   # O(n) instead of O(2^n)
```

Arguments must be hashable (ints, strings, tuples; not lists).

## Traps

- Passing `nums[1:]` copies the list on every call, so O(n²) overall. Pass an index instead.
- Forgetting to `return` the recursive result: `return helper(...)`, not just `helper(...)`.
- No base case, or a base case that's never reached, gives a RecursionError.
