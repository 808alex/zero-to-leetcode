=== p1
The most common first step on LeetCode: trade O(n) memory for O(1) lookups and turn a nested loop into a single pass.

## Spot it

- "Find two numbers / a pair / a duplicate" in an **unsorted** array.
- Counting, frequency, "anagram", "appears more than once".
- Subarray sums, especially with negative numbers (prefix sums).

## Templates

**Seen-so-far lookup (one pass):**

```python
seen = {}                         # value -> index (or a set if you only need membership)
for i, x in enumerate(nums):
    if target - x in seen:        # the partner we need
        return [seen[target - x], i]
    seen[x] = i
```

**Group by a key:**

```python
groups = defaultdict(list)
for s in strs:
    groups[key_of(s)].append(s)   # key_of: tuple(sorted(s)), len(s), s[0], ...
```

**Prefix sums:**

```python
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)
# sum of nums[i:j] == prefix[j] - prefix[i]   (O(1) per query)
```

To count subarrays with sum k: walk once, and at each step ask how many earlier prefixes equal `current - k`, using a dict of prefix counts that starts with `{0: 1}`.

## Why it works

The brute force checks every pair, O(n²). The hashmap remembers everything you've passed, so "have I seen the partner?" is O(1), and one pass is enough.

## Traps

- Check for the partner **before** inserting the current element, or `[3, 2, 4]` with target 6 pairs the 3 with itself.
- Lists aren't hashable. Use a tuple, or a string such as `"#".join(...)`, as the key.
- `Counter(a) == Counter(b)` is the one-line anagram check.

=== p2
Two indexes moving through the array, usually from both ends inward, or one fast and one slow. Turns O(n²) pair-checking into O(n) on sorted data.

## Spot it

- Sorted array plus "pair / triplet that sums to...".
- Palindromes, reversing in place.
- "In place, O(1) extra space": remove duplicates, move zeroes, partition.

## Templates

**Opposite ends:**

```python
l, r = 0, len(a) - 1
while l < r:
    s = a[l] + a[r]
    if s == target:
        return [l, r]
    if s < target:
        l += 1        # need bigger: only l moving right can do that
    else:
        r -= 1        # need smaller
```

**Read / write (same direction):**

```python
w = 0                       # next position to write
for r in range(len(a)):     # r reads everything
    if keep(a[r]):
        a[w] = a[r]
        w += 1
# a[:w] is the result
```

**k-Sum:** sort, fix the first number with a loop, then run opposite-ends on the rest. 3Sum is O(n²).

## Why it works

On a sorted array, each comparison rules out a whole row of pairs. If `a[l] + a[r]` is too small, `a[l]` paired with anything left of `r` is also too small, so `l` can move on for good.

## Traps

- Skipping duplicates in 3Sum: skip equal `i` values, and after a match move `l` past equal values.
- `while l < r` vs `l <= r`: for pairs you need two distinct elements, so `<`.
- If the input isn't sorted and you sort it, you lose the original indexes (that's why Two Sum I uses a hashmap).

=== p3
A window `[l, r]` that grows on the right and shrinks on the left, each pointer moving forward only. Every element enters and leaves once, so it's O(n).

## Spot it

- **Contiguous** subarray or substring.
- "Longest / shortest / count of windows such that..." with a condition you can update incrementally (counts, sums, distinct characters).
- Fixed size k: "max sum of k consecutive", "every window of size k".

## Templates

**Variable window (longest valid):**

```python
l = 0
best = 0
for r in range(len(s)):
    add(s[r])                    # grow the window
    while not valid():           # shrink until valid again
        remove(s[l])
        l += 1
    best = max(best, r - l + 1)
```

For **shortest** valid: shrink *while it is* valid, updating the best inside the while loop.

**Fixed window of size k:**

```python
window = sum(a[:k])
best = window
for r in range(k, len(a)):
    window += a[r] - a[r - k]    # one in, one out
    best = max(best, window)
```

## Why it works

Once a window `[l, r]` is invalid, every bigger window starting at `l` is invalid too, so `l` never has to move back. That one-directional property is what you must check before using a window.

## Traps

- Negative numbers break "sum ≤ k" windows: growing doesn't always increase the sum. Use prefix sums instead.
- Window length is `r - l + 1`.
- Keep window state in a `Counter`/`defaultdict(int)` or a set, and update it in both `add` and `remove`.

=== p4
A stack remembers things "until something resolves them". A **monotonic** stack keeps its contents sorted, so each element waits on the stack until the first element that beats it arrives.

## Spot it

- Matching pairs: brackets, tags, undo.
- Evaluating expressions (RPN, calculators).
- "Next greater element", "days until warmer", "how far can I see": anything asking for the nearest bigger or smaller item to the left or right.
- Histogram and rectangle problems.

## Templates

A Python list is a stack: `append` to push, `pop()` to pop, `stack[-1]` to peek, `if stack:` to check it isn't empty.

**Next greater element (monotonic decreasing stack of indexes):**

```python
ans = [-1] * len(a)
stack = []                        # indexes still waiting for a bigger value
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        j = stack.pop()
        ans[j] = x                # or i - j for "how many steps until"
    stack.append(i)
```

Each index is pushed once and popped once, so the whole loop is O(n) despite the inner `while`.

## Traps

- Store **indexes** on the stack, not values, when you need distances or positions.
- Always check `if stack` before `stack[-1]` or `pop()`.
- Strictly greater (`<`) vs greater-or-equal (`<=`) in the while condition changes how equal values behave. Read the problem.
- Min Stack: push `(value, current_min)` pairs so the min is O(1).

=== p5
Halve the search space every step: O(log n). Works on sorted arrays, but also on any yes/no question whose answers flip once (False False False True True).

## Spot it

- Sorted (or rotated sorted) input and a target.
- O(log n) required, or n up to 10⁹.
- "Minimum speed / capacity / days such that it works" (binary search on the answer).

## Templates

**Find exact target:**

```python
lo, hi = 0, len(a) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if a[mid] == target:
        return mid
    if a[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
return -1          # lo is now where target would be inserted
```

**First position where `ok(x)` is True** (the most useful one):

```python
lo, hi = smallest_possible, largest_possible
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid          # mid might be the answer, keep it
    else:
        lo = mid + 1      # mid definitely isn't
return lo
```

Koko, ship capacity, split array: write `ok(speed)` as "can we finish in time at this speed?", then use the second template.

## Traps

- Infinite loops come from `lo = mid` with `mid = (lo + hi) // 2`. In the second template, only `hi = mid` is allowed; `lo` always moves to `mid + 1`.
- Decide inclusive vs exclusive bounds once and stick with it.
- Rotated arrays: compare `a[mid]` with `a[hi]` to see which half is sorted.
- For plain lists, `bisect_left`/`bisect_right` already do this.

=== p6
Linked list problems are pointer bookkeeping. A handful of tricks cover almost all of them: dummy head, fast/slow pointers, in-place reversal.

## Spot it

You're given `head` of a `ListNode`. That's it.

## Templates

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

**Dummy head:** use it whenever the head itself might change (deleting, merging, inserting at the front).

```python
dummy = tail = ListNode()
# ... tail.next = something; tail = tail.next
return dummy.next
```

**Reverse in place:**

```python
prev, cur = None, head
while cur:
    cur.next, prev, cur = prev, cur, cur.next
return prev
```

(The one-liner is fine in Python because the right side is evaluated first. Write the 4-line version until it's automatic.)

**Fast and slow:**

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is at the middle; if slow is fast at any point, there's a cycle
```

**Gap of n:** move `fast` n steps first, then move both. When fast hits the end, slow is n from the end.

## Traps

- Save `cur.next` before overwriting it.
- `while fast and fast.next`: check both, or `fast.next.next` crashes.
- Compare nodes with `is`, not `==`.
- Harder problems (Reorder List) are combos: find middle, reverse second half, merge.
- LRU Cache = dict + doubly linked list. It's a favourite interview question.

=== p7
Almost every tree problem is either DFS with recursion (answer built from children) or BFS with a queue (level by level).

## Spot it

You're given `root` of a `TreeNode`. Then decide:

- Answer depends on subtrees (depth, balanced, same tree, path sums): **DFS, return values**.
- "Level", "row", "right side view", "minimum depth": **BFS**.
- BST: **inorder traversal is sorted**. Use the ordering to skip half the tree.

## Templates

**DFS returning a value:**

```python
def dfs(node):
    if not node:
        return 0                       # value for an empty tree
    l, r = dfs(node.left), dfs(node.right)
    return combine(node.val, l, r)
```

**DFS where the answer isn't what you return** (diameter, max path sum): return height, but update an outer `best` with `nonlocal`.

**BFS by level:**

```python
q = deque([root])
while q:
    for _ in range(len(q)):            # exactly one level
        node = q.popleft()
        ...
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
```

**Inorder (BST in sorted order):**

```python
def inorder(node):
    if node:
        yield from inorder(node.left)
        yield node.val
        yield from inorder(node.right)
```

**Passing constraints down:** for Validate BST, pass `(lo, hi)` bounds into children.

## Traps

- Handle `root is None` first.
- Checking only parent-vs-child for BST validity is wrong; use bounds.
- LCA in a BST: if both values are smaller, go left; both bigger, go right; otherwise you're at the LCA.
- Inorder successor (the next node in sorted order) is the leftmost node of the right subtree, if there is one.

=== p8
A heap gives you the smallest item in O(1) and lets you insert or remove in O(log n). Whenever you need "the best few" out of many, or the best item while things keep changing, use a heap.

## Spot it

- "k-th largest / smallest", "top k", "k closest".
- Merge k sorted things.
- Always process the cheapest / earliest / largest next (schedulers, Dijkstra).
- Running median (two heaps).

## Templates

**Top k with a size-k min-heap** (O(n log k)):

```python
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)      # throw away the smallest
# heap holds the k largest; heap[0] is the k-th largest
```

**Max-heap:** push `-x`, negate again when popping.

**Heap of tuples:** `(priority, tie_breaker, item)`. Tuples compare left to right. If two priorities tie and the items aren't comparable (such as ListNodes), Python crashes, so add an index as the tie-breaker.

**Merge k sorted lists:**

```python
heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
heapq.heapify(heap)
while heap:
    val, i, node = heapq.heappop(heap)
    ... # attach node; if node.next, push (node.next.val, i, node.next)
```

**Median of a stream:** max-heap for the lower half, min-heap for the upper half, kept within one of each other in size.

## Traps

- Python's heapq is a **min**-heap only.
- `heapq.heapify` returns `None`; it works in place.
- For "top k" you don't need a full sort (O(n log n)), but in an interview `sorted(...)[:k]` is fine to mention as the brute force.

=== p9
Backtracking is DFS over choices: make a choice, recurse, then undo it. Use it when you must generate or search all combinations, and n is small (≤ 20 or so).

## Spot it

- "All subsets / permutations / combinations / partitions".
- "Place N queens", Sudoku, word search in a grid.
- Constraints are tiny, which hints at exponential time.

## Template

```python
res = []
path = []

def backtrack(start):
    if is_complete(path):
        res.append(path[:])          # copy!
        return
    for i in range(start, len(choices)):
        if not allowed(choices[i]):
            continue
        path.append(choices[i])      # choose
        backtrack(i + 1)             # explore (i to allow reuse, i + 1 to forbid)
        path.pop()                   # un-choose
```

Variations come from three knobs:

| Problem | Start index | Reuse? | Record when |
|---|---|---|---|
| Subsets | `i + 1` | no | every node |
| Combinations / Combination Sum II | `i + 1` | no | target hit |
| Combination Sum | `i` | yes | target hit |
| Permutations | always 0, with a `used` array | no | `len(path) == n` |

**Duplicates in the input** (Subsets II, Combination Sum II): sort first, then `if i > start and nums[i] == nums[i - 1]: continue`.

## Traps

- `res.append(path)` without `[:]` stores the same list over and over, and it ends up empty.
- Prune early (`if remaining < 0: return`, or break the loop once sorted candidates get too big).
- Grid backtracking: mark the cell visited before recursing and restore it after.

=== p10
Graphs are nodes and edges. On LeetCode they usually arrive as a **grid**, an **edge list**, or an adjacency list. Three algorithms cover most problems: DFS/BFS traversal, topological sort, and union-find.

## Spot it

- Grid of cells, "islands", "regions", "spread": grid DFS/BFS.
- "Fewest steps", "shortest path" with equal-cost moves: BFS.
- "Prerequisites", "order of tasks", "is there a cycle in dependencies": topological sort.
- "Connected components", "are these linked", adding edges one at a time: union-find.
- Weighted shortest path: Dijkstra (heap + BFS).

## Templates

**Build an adjacency list:**

```python
graph = defaultdict(list)
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)    # only if undirected
```

**Grid neighbours:**

```python
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and ...:
```

**BFS shortest path:**

```python
q = deque([(start, 0)])
seen = {start}
while q:
    node, dist = q.popleft()
    if node == goal:
        return dist
    for nxt in graph[node]:
        if nxt not in seen:
            seen.add(nxt)          # mark when pushing, not when popping
            q.append((nxt, dist + 1))
```

**Topological sort (Kahn):** count indegrees, queue every node with indegree 0, pop and decrement neighbours. If you processed fewer than n nodes, there's a cycle.

**Union-find:**

```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False        # already connected: this edge makes a cycle
    parent[ra] = rb
    return True
```

**Dijkstra:** `heap = [(0, src)]`; pop the closest; skip it if you've already finalised that node; push neighbours with `d + w`.

## Traps

- Mark visited when you **enqueue**, or nodes get queued many times.
- Multi-source BFS (Rotting Oranges, Walls and Gates): put every source in the queue before starting.
- Recursion depth on a 300×300 grid can pass 1000. Use BFS or an explicit stack if it crashes.

=== p11
DP is recursion where the same sub-problems repeat, so you store their answers. Every DP problem is: **define the state, write the recurrence, set the base cases, choose an order.**

## Spot it

- "How many ways", "minimum cost", "maximum value", "is it possible".
- Choices at each step whose effects overlap (rob this house or skip it; take this coin or not).
- A greedy idea that almost works but you can find a counterexample.

## The recipe

1. **State:** what does `dp[i]` (or `dp[i][j]`) mean, in one sentence? ("Fewest coins to make amount i.")
2. **Recurrence:** how is `dp[i]` built from smaller states? Think about the *last* decision.
3. **Base cases:** `dp[0]`, empty strings, first row and column.
4. **Order:** fill so that every state you read is already computed. Return the cell that answers the question.

## Templates

**Top-down (easiest to write first):**

```python
from functools import cache

@cache
def best(i):
    if i >= len(nums):
        return 0
    return max(best(i + 1), nums[i] + best(i + 2))   # skip vs take
return best(0)
```

**Bottom-up 1D:**

```python
dp = [0] * (n + 1)
dp[0] = base
for i in range(1, n + 1):
    dp[i] = f(dp[i - 1], dp[i - 2], ...)
```

When `dp[i]` only uses the last two values, keep two variables instead of the array (O(1) space).

**Bottom-up 2D (two strings / grid):**

```python
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
```

## The common shapes

| Shape | Examples |
|---|---|
| Fibonacci-like `dp[i-1], dp[i-2]` | Climbing Stairs, House Robber, Decode Ways |
| Unbounded choice over items | Coin Change, Word Break, Combination Sum IV |
| 0/1 knapsack | Partition Equal Subset Sum, Target Sum |
| Best ending at i | LIS, Maximum Subarray |
| Two sequences `dp[i][j]` | LCS, Edit Distance |
| Grid paths | Unique Paths, Minimum Path Sum |

## Traps

- Write the brute-force recursion first, then add `@cache`. Convert to bottom-up only if you need to.
- Off-by-one: with `dp` of size `n + 1`, `dp[i]` usually refers to the first i items, so the item itself is `a[i - 1]`.
- `[[0] * n] * m` again: always build 2D tables with a comprehension.

=== p12
Two related families. **Intervals**: almost always sort first, then sweep once. **Greedy**: make the locally best choice and prove (or convince yourself) it never hurts later.

## Spot it

- Pairs `[start, end]`: merge, insert, count overlaps, meeting rooms.
- "Minimum number of X to remove / arrows / rooms".
- Reachability with jumps; running sums that can reset (Kadane).

## Templates

**Merge intervals:**

```python
intervals.sort(key=lambda x: x[0])
res = []
for s, e in intervals:
    if res and s <= res[-1][1]:
        res[-1][1] = max(res[-1][1], e)
    else:
        res.append([s, e])
```

**Max non-overlapping set (activity selection):** sort by **end**, keep each interval that starts after the last kept end.

**Meeting rooms (how many overlap at once):** sort starts and ends separately, or push end times onto a min-heap and pop any that finished before the next start. The heap size is the answer.

**Kadane (max subarray):**

```python
best = cur = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)     # extend or restart
    best = max(best, cur)
```

**Furthest reach (Jump Game):** track `reach = max(reach, i + nums[i])`; fail if `i > reach`.

## How to trust a greedy

Try to break it with small examples. If you can't find a counterexample after a few attempts, and you can explain in a sentence why swapping in your choice never makes things worse (the exchange argument), go with it. If you *can* break it, it's probably DP.

## Traps

- Sort by start for merging, by end for maximising the number kept.
- Touching endpoints (`[1,2]` and `[2,3]`): read whether they count as overlapping.
- Kadane: initialise with `nums[0]`, not 0, or all-negative arrays break.

=== x1
You've got the patterns. This stage is about doing problems under realistic conditions and remembering them a month later.

## The practice loop

1. **Set a timer**: 20 minutes for Easy, 35 for Medium, 50 for Hard.
2. Use the routine from Big-O & approach: restate, brute force, find the waste, pick the pattern, code, test by hand.
3. **Stuck at the time limit?** Read *only the approach* (not the code) of a good solution, close it, and write it yourself.
4. **After solving**, write one line in your notes: the trick in plain words. ("Sort by end time; keep the earliest finisher.")
5. **Re-solve from scratch** after 3 days and again after 2 weeks. If you can't, it goes back in the queue. This is where most of the learning happens.

## Rules of thumb

- Struggling with a problem for an hour and then reading the answer teaches less than 25 minutes of focused effort followed by the solution.
- Mediums are where interviews live. Once a pattern's Easies feel routine, move on.
- Re-solving a problem you've seen before is not cheating. Being able to recall a solution under pressure is a skill interviews test.
- Talk out loud while you solve, even alone. Interviewers grade your reasoning, not only the final code.

## A mock interview (once a week)

Pick a random Medium from a pattern you've finished. 45 minutes total: 5 to clarify and give examples, 5 to state the brute force and its complexity, 25 to code the optimal solution, 10 to test with edge cases and state final time/space. Talk through it out loud as if someone were listening.

## Beyond the core

These come up less often but still appear. Learn them once the 12 patterns feel solid:

- **Tries** (prefix trees): autocomplete, word search with many words.
- **Bit manipulation**: XOR tricks (`a ^ a == 0`), counting set bits, `n & (n - 1)` clears the lowest set bit.
- **Matrix manipulation**: rotate, spiral, set zeroes. Mostly careful indexing.
- **Dijkstra** (weighted shortest path) and **Bellman-Ford** (negative edges, limited stops).
- **Monotonic deque** for sliding window maximum.
