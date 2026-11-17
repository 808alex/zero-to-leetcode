"""All runnable drills. Each drill is verified by build.py: its solution must pass its tests."""

DRILLS = []


def D(id, module, title, fn, prompt, starter, tests, solution, hint, cmp="eq", prep=None, lc=None):
    DRILLS.append(dict(id=id, module=module, title=title, fn=fn, prompt=prompt,
                       starter=starter.strip("\n") + "\n", tests=tests.strip(),
                       solution=solution.strip("\n") + "\n", hint=hint, cmp=cmp,
                       prep=(prep or "").strip("\n"), lc=lc))


LL = "def _call(args):\n    return _from_ll(_fn(*[_to_ll(a) for a in args]))"
TREE_OUT = "def _call(args):\n    return _from_tree(_fn(_to_tree(args[0])))"
TREE_IN = "def _call(args):\n    return _fn(_to_tree(args[0]), *args[1:])"

# ------------------------------------------------------------------ m1 re-entry
D("first-upper", "m1", "First uppercase letter", "first_upper",
  "Return a tuple <code>(letter, index)</code> for the first uppercase letter in <code>s</code>, or <code>None</code> if there isn't one. Beginners often write this with a <code>while</code> loop and <code>i = len(s)</code> to escape. Use <code>enumerate</code> and an early <code>return</code> instead.",
  "def first_upper(s):\n    pass",
  '[(("helloWorld",), ("W", 5)), (("abc",), None), (("Abc",), ("A", 0)), (("",), None), (("a1 B2",), ("B", 3))]',
  """
def first_upper(s):
    for i, ch in enumerate(s):
        if ch.isupper():
            return ch, i
    return None
""",
  "enumerate(s) gives you (index, char) pairs. Returning inside the loop ends it immediately.")

D("palindrome", "m1", "Palindrome, two ways", "is_palindrome",
  "Return <code>True</code> if <code>s</code> reads the same backwards. Get it passing with slicing first, then rewrite it with two pointers (<code>l</code> from the left, <code>r</code> from the right) and no slicing. The two-pointer version is the one interviews want.",
  "def is_palindrome(s):\n    pass",
  '[(("racecar",), True), (("abba",), True), (("abc",), False), (("",), True), (("a",), True), (("ab",), False)]',
  """
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True
""",
  "Slicing version: s == s[::-1]. Two-pointer version: loop while l < r, compare s[l] and s[r], move both inward.")

D("split-words", "m1", "Split words by hand", "split_words",
  "Return the list of words in <code>s</code>, where words are separated by one or more spaces. Don't use <code>.split()</code>. The classic scan: <code>i</code> skips spaces, <code>j</code> walks to the end of the word, slice <code>s[i:j]</code>.",
  "def split_words(s):\n    pass",
  '[(("   Nobody   expects  the   Spanish Inquisition",), ["Nobody", "expects", "the", "Spanish", "Inquisition"]), (("",), []), (("one",), ["one"]), (("  a  ",), ["a"]), (("a b",), ["a", "b"])]',
  """
def split_words(s):
    words = []
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        j = i
        while j < n and s[j] != " ":
            j += 1
        if i < j:
            words.append(s[i:j])
        i = j
    return words
""",
  "Outer loop while i < n. Inside it: skip spaces, then set j = i and advance j until a space or the end. Only append if i < j, otherwise trailing spaces add empty strings.")

D("is-prime", "m1", "Prime check (properly)", "is_prime",
  "Return whether <code>n</code> is prime. Checking only 2 and 3 wrongly calls 25 prime. Test divisors up to the square root only, so it is O(√n). Large inputs are in the tests, so checking every number up to n is too slow.",
  "def is_prime(n):\n    pass",
  '[((1,), False), ((2,), True), ((3,), True), ((4,), False), ((25,), False), ((97,), True), ((0,), False), ((7919,), True), ((1000000007,), True), ((999999999,), False)]',
  """
def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
""",
  "If n = a * b with a <= b, then a <= √n. So if nothing up to √n divides n, nothing does. Loop while d * d <= n.")

D("most-frequent", "m1", "Most frequent character", "most_frequent",
  "Return the character that appears most often in <code>s</code> (non-empty). On a tie, return the one that appears first. Write it with a plain dict, then try <code>collections.Counter</code>.",
  "def most_frequent(s):\n    pass",
  '[(("hello",), "l"), (("aabb",), "a"), (("abcabcc",), "c"), (("z",), "z"), (("bbaa",), "b")]',
  """
from collections import Counter

def most_frequent(s):
    return Counter(s).most_common(1)[0][0]
""",
  "Dict version: counts[ch] = counts.get(ch, 0) + 1, then max(counts, key=counts.get). Dicts keep insertion order and max returns the first maximum, which handles ties.")

D("to-hex", "m1", "Decimal to hex", "to_hex",
  "Convert a non-negative integer to a lowercase hex string without <code>hex()</code> or <code>format()</code>. Loop until the number is used up (looping a fixed number of times, like <code>len(str(n))</code>, gives the wrong count), and remember 0.",
  "def to_hex(n):\n    pass",
  '[((0,), "0"), ((255,), "ff"), ((26,), "1a"), ((4096,), "1000"), ((15,), "f"), ((3735928559,), "deadbeef")]',
  """
def to_hex(n):
    if n == 0:
        return "0"
    digits = "0123456789abcdef"
    out = []
    while n > 0:
        out.append(digits[n % 16])
        n //= 16
    return "".join(reversed(out))
""",
  "A lookup string digits = '0123456789abcdef' replaces the whole if/elif chain: digits[n % 16]. Build a list and join at the end instead of prepending to a string.")

# ------------------------------------------------------------------ m2 toolkit
D("group-length", "m2", "Group words by length", "group_by_length",
  "Return a dict mapping each word length to the list of words with that length, in their original order. Use <code>defaultdict(list)</code>.",
  "from collections import defaultdict\n\ndef group_by_length(words):\n    pass",
  '[((["hi", "yo", "cat", "a", "dog"],), {2: ["hi", "yo"], 3: ["cat", "dog"], 1: ["a"]}), (([],), {}), ((["same", "four"],), {4: ["same", "four"]})]',
  """
from collections import defaultdict

def group_by_length(words):
    groups = defaultdict(list)
    for w in words:
        groups[len(w)].append(w)
    return dict(groups)
""",
  "groups[len(w)].append(w) works without checking whether the key exists, because defaultdict(list) creates the empty list for you.")

D("first-unique", "m2", "First unique character", "first_uniq_char",
  "Return the index of the first character that appears exactly once in <code>s</code>, or -1. Two passes: count everything, then scan for a count of 1.",
  "def first_uniq_char(s):\n    pass",
  '[(("leetcode",), 0), (("loveleetcode",), 2), (("aabb",), -1), (("",), -1), (("z",), 0)]',
  """
from collections import Counter

def first_uniq_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
""",
  "Counter(s) in one pass, then enumerate(s) and return the first i where counts[ch] == 1.", lc="first-unique-character-in-a-string")

D("k-smallest", "m2", "k smallest with a heap", "k_smallest",
  "Return the <code>k</code> smallest numbers in ascending order. Do it with <code>heapq</code> (either <code>heapify</code> + <code>heappop</code> k times, or <code>heapq.nsmallest</code>).",
  "import heapq\n\ndef k_smallest(nums, k):\n    pass",
  '[(([5, 1, 4, 2, 3], 2), [1, 2]), (([7], 1), [7]), (([3, 3, 1], 3), [1, 3, 3]), (([9, 8, 7], 0), [])]',
  """
import heapq

def k_smallest(nums, k):
    heap = nums[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(k)]
""",
  "heapify is O(n) and each heappop is O(log n), so this is O(n + k log n). Copy nums first so you don't mutate the input.")

D("count-less", "m2", "Count below x with bisect", "count_less",
  "<code>nums</code> is sorted. Return how many elements are strictly less than <code>x</code>, in O(log n). Use <code>bisect</code>.",
  "from bisect import bisect_left\n\ndef count_less(nums, x):\n    pass",
  '[(([1, 2, 2, 3, 5], 2), 1), (([1, 2, 2, 3, 5], 4), 4), (([], 3), 0), (([1, 1, 1], 0), 0), (([1, 1, 1], 9), 3)]',
  """
from bisect import bisect_left

def count_less(nums, x):
    return bisect_left(nums, x)
""",
  "bisect_left(nums, x) returns the first index where x could be inserted while keeping nums sorted. Every element before that index is < x.")

D("sort-people", "m2", "Sort with a key", "sort_people",
  "<code>people</code> is a list of <code>(name, age)</code> tuples. Return them sorted by age, oldest first, and by name A→Z for equal ages. One <code>sorted</code> call with a tuple key.",
  "def sort_people(people):\n    pass",
  '[(([("bob", 20), ("al", 30), ("cy", 20)],), [("al", 30), ("bob", 20), ("cy", 20)]), (([],), []), (([("z", 1), ("a", 1)],), [("a", 1), ("z", 1)])]',
  """
def sort_people(people):
    return sorted(people, key=lambda p: (-p[1], p[0]))
""",
  "key=lambda p: (-p[1], p[0]). Negating the age flips that part to descending while the name stays ascending.")

# ------------------------------------------------------------------ m4 recursion
D("fast-power", "m4", "Fast power", "power",
  "Compute <code>x ** n</code> for integer <code>n >= 0</code> recursively in O(log n), without using <code>**</code> or <code>pow</code>. If n is even, x^n = (x^(n/2))²; if odd, multiply by x once more.",
  "def power(x, n):\n    pass",
  '[((2, 10), 1024), ((3, 0), 1), ((5, 1), 5), ((2, 31), 2147483648), ((-2, 3), -8)]',
  """
def power(x, n):
    if n == 0:
        return 1
    half = power(x, n // 2)
    if n % 2 == 0:
        return half * half
    return half * half * x
""",
  "Compute half = power(x, n // 2) once and reuse it. Calling power twice would make it O(n) again.")

D("flatten", "m4", "Flatten a nested list", "flatten",
  "Return a flat list of all the integers in an arbitrarily nested list. This is the same shape as walking a file system or a tree.",
  "def flatten(nested):\n    pass",
  '[(([1, [2, [3, 4]], 5],), [1, 2, 3, 4, 5]), (([],), []), (([[[]]],), []), (([[1], [], [2, [3]]],), [1, 2, 3])]',
  """
def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out
""",
  "For each item: if isinstance(item, list), extend with flatten(item); otherwise append it.")

D("sum-digits", "m4", "Sum of digits", "sum_digits",
  "Return the sum of the digits of a non-negative integer, recursively. No strings.",
  "def sum_digits(n):\n    pass",
  '[((0,), 0), ((7,), 7), ((1234,), 10), ((99999,), 45)]',
  """
def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)
""",
  "Last digit is n % 10, the rest is n // 10. Base case: a single digit.")

D("bsearch-rec", "m4", "Recursive binary search", "binary_search",
  "Return the index of <code>target</code> in sorted <code>nums</code>, or -1. Write it recursively with <code>lo</code> and <code>hi</code> parameters (default them so the caller only passes two arguments). Don't slice the list, because that copies it.",
  "def binary_search(nums, target, lo=0, hi=None):\n    pass",
  '[(([1, 3, 5, 7, 9], 7), 3), (([1, 3, 5, 7, 9], 1), 0), (([1, 3, 5, 7, 9], 4), -1), (([], 1), -1), (([2], 2), 0)]',
  """
def binary_search(nums, target, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return binary_search(nums, target, mid + 1, hi)
    return binary_search(nums, target, lo, mid - 1)
""",
  "hi=None as the default, then set it to len(nums) - 1 inside. Base case lo > hi means not found.")

# ------------------------------------------------------------------ p1 arrays & hashing
D("two-sum", "p1", "Two Sum", "two_sum",
  "Return indices <code>[i, j]</code> of the two numbers that add up to <code>target</code>. Exactly one answer exists. Do it in one pass, O(n).",
  "def two_sum(nums, target):\n    pass",
  '[(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2]), (([3, 3], 6), [0, 1]), (([-1, -2, -3, -4, -5], -8), [2, 4])]',
  """
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
""",
  "Keep a dict value → index of what you've seen. For each x, check whether target - x is already in it before adding x.", cmp="sorted", lc="two-sum")

D("group-anagrams", "p1", "Group Anagrams", "group_anagrams",
  "Group the strings that are anagrams of each other. Any order of groups and of words within a group is fine.",
  "def group_anagrams(strs):\n    pass",
  '[((["eat", "tea", "tan", "ate", "nat", "bat"],), [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]), (([""],), [[""]]), ((["a"],), [["a"]])]',
  """
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())
""",
  "Anagrams have the same sorted letters. Use tuple(sorted(s)) as a dict key (lists can't be keys).", cmp="sorted_inner", lc="group-anagrams")

D("subarray-sum", "p1", "Subarray Sum Equals K", "subarray_sum",
  "Count contiguous subarrays whose sum is <code>k</code>. Numbers can be negative, so a sliding window doesn't work. Use prefix sums and a hashmap.",
  "def subarray_sum(nums, k):\n    pass",
  '[(([1, 1, 1], 2), 2), (([1, 2, 3], 3), 2), (([1, -1, 0], 0), 3), (([], 0), 0), (([3], 3), 1)]',
  """
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1
    for x in nums:
        prefix += x
        count += seen[prefix - k]
        seen[prefix] += 1
    return count
""",
  "sum(i..j) = prefix[j] - prefix[i-1]. So at each position, count how many earlier prefixes equal prefix - k. Start with seen[0] = 1 for the empty prefix.", lc="subarray-sum-equals-k")

D("longest-consec", "p1", "Longest Consecutive Sequence", "longest_consecutive",
  "Return the length of the longest run of consecutive integers (in any order in the array). O(n): no sorting.",
  "def longest_consecutive(nums):\n    pass",
  '[(([100, 4, 200, 1, 3, 2],), 4), (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9), (([],), 0), (([1, 2, 0, 1],), 3)]',
  """
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            length = 1
            while x + length in s:
                length += 1
            best = max(best, length)
    return best
""",
  "Put everything in a set. Only start counting from x when x - 1 isn't in the set (x is the start of a run). Each number is then visited at most twice overall.", lc="longest-consecutive-sequence")

# ------------------------------------------------------------------ p2 two pointers
D("two-sum-sorted", "p2", "Two Sum II (sorted)", "two_sum_sorted",
  "<code>numbers</code> is sorted. Return the 1-indexed positions <code>[i, j]</code> of the pair that sums to <code>target</code>, using O(1) extra space.",
  "def two_sum_sorted(numbers, target):\n    pass",
  '[(([2, 7, 11, 15], 9), [1, 2]), (([2, 3, 4], 6), [1, 3]), (([-1, 0], -1), [1, 2]), (([1, 2, 3, 4, 4, 9], 8), [4, 5])]',
  """
def two_sum_sorted(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target:
            return [l + 1, r + 1]
        if s < target:
            l += 1
        else:
            r -= 1
""",
  "Start at both ends. Sum too small → move l right (only way to increase). Too big → move r left.", lc="two-sum-ii-input-array-is-sorted")

D("container", "p2", "Container With Most Water", "max_area",
  "Pick two lines that, with the x-axis, hold the most water. Return that area.",
  "def max_area(height):\n    pass",
  '[(([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49), (([1, 1],), 1), (([4, 3, 2, 1, 4],), 16), (([1, 2, 1],), 2)]',
  """
def max_area(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best
""",
  "Area = width × shorter line. Moving the taller line inward can never help (width shrinks, height capped by the shorter one), so always move the shorter one.", lc="container-with-most-water")

D("three-sum", "p2", "3Sum", "three_sum",
  "Return all unique triplets that sum to 0. Sort first, fix one number, two-pointer the rest, and skip duplicates.",
  "def three_sum(nums):\n    pass",
  '[(([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]), (([0, 1, 1],), []), (([0, 0, 0, 0],), [[0, 0, 0]]), (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]])]',
  """
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
    return res
""",
  "After sorting: skip i if nums[i] == nums[i-1]. After finding a triplet, move l forward past equal values.", cmp="sorted_inner", lc="3sum")

D("move-zeroes", "p2", "Move Zeroes", "move_zeroes",
  "Move all 0s to the end in place, keeping the order of the other numbers. Return the list (LeetCode's version returns nothing; here return it so it can be checked).",
  "def move_zeroes(nums):\n    pass",
  '[(([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]), (([0],), [0]), (([1, 2],), [1, 2]), (([0, 0, 1],), [1, 0, 0])]',
  """
def move_zeroes(nums):
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w], nums[r] = nums[r], nums[w]
            w += 1
    return nums
""",
  "Read pointer r scans everything, write pointer w marks where the next non-zero goes. Swap and advance w on each non-zero.", lc="move-zeroes")

# ------------------------------------------------------------------ p3 sliding window
D("longest-substr", "p3", "Longest Substring Without Repeating", "length_of_longest_substring",
  "Return the length of the longest substring with no repeated characters.",
  "def length_of_longest_substring(s):\n    pass",
  '[(("abcabcbb",), 3), (("bbbbb",), 1), (("pwwkew",), 3), (("",), 0), (("abba",), 2), (("dvdf",), 3)]',
  """
def length_of_longest_substring(s):
    window = set()
    l = 0
    best = 0
    for r, ch in enumerate(s):
        while ch in window:
            window.remove(s[l])
            l += 1
        window.add(ch)
        best = max(best, r - l + 1)
    return best
""",
  "Expand r every step. While s[r] is already in the window, remove s[l] and move l. The window is always valid after the while loop.", lc="longest-substring-without-repeating-characters")

D("max-window", "p3", "Max sum of a window of size k", "max_window_sum",
  "Return the largest sum of any <code>k</code> consecutive numbers (1 ≤ k ≤ len(nums)). O(n): slide the window, don't re-sum it.",
  "def max_window_sum(nums, k):\n    pass",
  '[(([1, 12, -5, -6, 50, 3], 4), 51), (([5], 1), 5), (([1, 2, 3], 3), 6), (([-1, -2, -3], 2), -3)]',
  """
def max_window_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for r in range(k, len(nums)):
        window += nums[r] - nums[r - k]
        best = max(best, window)
    return best
""",
  "Sum the first k once. Then each step adds nums[r] and drops nums[r - k]. Start best at the first window, not 0 (sums can be negative).")

D("char-replace", "p3", "Longest Repeating Character Replacement", "character_replacement",
  "You may change up to <code>k</code> characters. Return the length of the longest substring of one repeated letter you can get.",
  "def character_replacement(s, k):\n    pass",
  '[(("ABAB", 2), 4), (("AABABBA", 1), 4), (("", 0), 0), (("AAAA", 0), 4), (("ABCD", 0), 1)]',
  """
from collections import defaultdict

def character_replacement(s, k):
    count = defaultdict(int)
    l = 0
    max_freq = 0
    best = 0
    for r, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (r - l + 1) - max_freq > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
""",
  "A window is valid if (window length - count of its most common letter) <= k. Shrink from the left while it isn't.", lc="longest-repeating-character-replacement")

# ------------------------------------------------------------------ p4 stack
D("valid-parens", "p4", "Valid Parentheses", "is_valid",
  "Return whether every bracket in <code>s</code> (<code>()[]{}</code>) is closed by the same type in the right order.",
  "def is_valid(s):\n    pass",
  '[(("()",), True), (("()[]{}",), True), (("(]",), False), (("([)]",), False), (("{[]}",), True), (("(",), False), ((")",), False), (("",), True)]',
  """
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
""",
  "Push openers. On a closer, the top of the stack must be its matching opener. At the end the stack must be empty.", lc="valid-parentheses")

D("daily-temps", "p4", "Daily Temperatures", "daily_temperatures",
  "For each day, how many days until a warmer one? 0 if never. O(n) with a monotonic stack.",
  "def daily_temperatures(temperatures):\n    pass",
  '[(([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]), (([30, 40, 50, 60],), [1, 1, 1, 0]), (([30, 60, 90],), [1, 1, 0]), (([50],), [0])]',
  """
def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []  # indices, temperatures decreasing from bottom to top
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
""",
  "Keep a stack of indices still waiting for a warmer day. When today is warmer than the top, pop it and record i - j. Push today.", lc="daily-temperatures")

D("rpn", "p4", "Evaluate Reverse Polish Notation", "eval_rpn",
  "Evaluate a list of tokens in RPN. Division truncates toward zero (careful: Python's <code>//</code> floors).",
  "def eval_rpn(tokens):\n    pass",
  '[((["2", "1", "+", "3", "*"],), 9), ((["4", "13", "5", "/", "+"],), 6), ((["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), 22), ((["7", "-2", "/"],), -3)]',
  """
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in "+-*/" and len(t) == 1:
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(t))
    return stack[0]
""",
  "Pop b first, then a (order matters for - and /). int(a / b) truncates toward zero; -7 // 2 is -4 but int(-7 / 2) is -3. Watch out for '-11': it's a number, not an operator.", lc="evaluate-reverse-polish-notation")

# ------------------------------------------------------------------ p5 binary search
D("bsearch", "p5", "Binary Search", "search",
  "Iterative binary search: return the index of <code>target</code> in sorted <code>nums</code>, or -1.",
  "def search(nums, target):\n    pass",
  '[(([-1, 0, 3, 5, 9, 12], 9), 4), (([-1, 0, 3, 5, 9, 12], 2), -1), (([5], 5), 0), (([], 1), -1), (([1, 2], 2), 1)]',
  """
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""",
  "lo <= hi with hi = len - 1 (inclusive bounds). Always move past mid: lo = mid + 1 or hi = mid - 1, or you'll loop forever.", lc="binary-search")

D("koko", "p5", "Koko Eating Bananas", "min_eating_speed",
  "Return the minimum eating speed <code>k</code> so Koko finishes all piles within <code>h</code> hours (one pile per hour max, ceil(pile/k) hours each). Binary search on the answer.",
  "def min_eating_speed(piles, h):\n    pass",
  '[(([3, 6, 7, 11], 8), 4), (([30, 11, 23, 4, 20], 5), 30), (([30, 11, 23, 4, 20], 6), 23), (([1], 1), 1), (([1000000000], 2), 500000000)]',
  """
def min_eating_speed(piles, h):
    def hours(k):
        return sum((p + k - 1) // k for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
""",
  "Speeds 1..max(piles). If speed k works, every faster speed works too, so the answers are False...False True...True. Binary search for the first True. Ceil division: (p + k - 1) // k.", lc="koko-eating-bananas")

D("rotated-min", "p5", "Find Minimum in Rotated Sorted Array", "find_min",
  "A sorted array of unique numbers was rotated. Return the minimum in O(log n).",
  "def find_min(nums):\n    pass",
  '[(([3, 4, 5, 1, 2],), 1), (([4, 5, 6, 7, 0, 1, 2],), 0), (([11, 13, 15, 17],), 11), (([1],), 1), (([2, 1],), 1)]',
  """
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
""",
  "Compare nums[mid] with nums[hi]. If mid is bigger, the drop (and the minimum) is to the right of mid. Otherwise the minimum is at mid or left of it.", lc="find-minimum-in-rotated-sorted-array")

# ------------------------------------------------------------------ p6 linked lists
D("reverse-ll", "p6", "Reverse Linked List", "reverse_list",
  "Reverse a singly linked list and return the new head. <code>ListNode</code> is predefined (<code>val</code>, <code>next</code>). The tests convert Python lists to linked lists for you.",
  "def reverse_list(head):\n    pass",
  '[(([1, 2, 3, 4, 5],), [5, 4, 3, 2, 1]), (([1, 2],), [2, 1]), (([],), [])]',
  """
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
""",
  "Three pointers: prev, cur, nxt. Save cur.next, point cur.next back at prev, then shift prev and cur forward.", prep=LL, lc="reverse-linked-list")

D("middle-ll", "p6", "Middle of the Linked List", "middle_node",
  "Return the middle node (the second middle if there are two). Fast and slow pointers, one pass.",
  "def middle_node(head):\n    pass",
  '[(([1, 2, 3, 4, 5],), [3, 4, 5]), (([1, 2, 3, 4, 5, 6],), [4, 5, 6]), (([1],), [1])]',
  """
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
""",
  "fast moves 2, slow moves 1. When fast falls off the end, slow is in the middle.", prep=LL, lc="middle-of-the-linked-list")

D("merge-ll", "p6", "Merge Two Sorted Lists", "merge_two_lists",
  "Merge two sorted linked lists into one sorted list and return its head.",
  "def merge_two_lists(list1, list2):\n    pass",
  '[(([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]), (([], []), []), (([], [0]), [0]), (([5], [1, 2]), [1, 2, 5])]',
  """
def merge_two_lists(list1, list2):
    dummy = tail = ListNode()
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
""",
  "Dummy node trick: dummy = tail = ListNode(). Attach the smaller head each step. At the end, attach whichever list is left. Return dummy.next.", prep=LL, lc="merge-two-sorted-lists")

D("cycle-ll", "p6", "Linked List Cycle", "has_cycle",
  "Return whether the list has a cycle. O(1) memory: Floyd's fast/slow pointers. (Tests build the cycle from <code>pos</code>, the index the tail links back to, or -1.)",
  "def has_cycle(head):\n    pass",
  '[(([3, 2, 0, -4], 1), True), (([1, 2], 0), True), (([1], -1), False), (([], -1), False), (([1, 2, 3], -1), False)]',
  """
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
""",
  "If there's a cycle, fast eventually laps slow and they meet. If fast reaches None, there's no cycle. Compare nodes with 'is'.",
  prep="""def _call(args):
    vals, pos = args
    head = _to_ll(vals)
    if pos >= 0:
        nodes = []
        n = head
        while n:
            nodes.append(n)
            n = n.next
        nodes[-1].next = nodes[pos]
    return _fn(head)""", lc="linked-list-cycle")

D("remove-nth", "p6", "Remove Nth Node From End", "remove_nth_from_end",
  "Remove the n-th node from the end and return the head. One pass: put a gap of n between two pointers.",
  "def remove_nth_from_end(head, n):\n    pass",
  '[(([1, 2, 3, 4, 5], 2), [1, 2, 3, 5]), (([1], 1), []), (([1, 2], 1), [1]), (([1, 2], 2), [2])]',
  """
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
""",
  "Start both at a dummy node before head (handles removing the head). Move fast n steps, then move both until fast is on the last node. slow is now just before the node to delete.",
  prep="def _call(args):\n    return _from_ll(_fn(_to_ll(args[0]), args[1]))", lc="remove-nth-node-from-end-of-list")

# ------------------------------------------------------------------ p7 trees
D("max-depth", "p7", "Maximum Depth of Binary Tree", "max_depth",
  "Return the depth of the tree. <code>TreeNode</code> is predefined (<code>val</code>, <code>left</code>, <code>right</code>). Tests give trees in LeetCode's level-order format, e.g. <code>[3, 9, 20, None, None, 15, 7]</code>.",
  "def max_depth(root):\n    pass",
  '[(([3, 9, 20, None, None, 15, 7],), 3), (([1, None, 2],), 2), (([],), 0), (([1],), 1)]',
  """
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
  "Depth of an empty tree is 0. Otherwise 1 + the deeper of the two subtrees. Trust the recursion.", prep=TREE_IN, lc="maximum-depth-of-binary-tree")

D("invert-tree", "p7", "Invert Binary Tree", "invert_tree",
  "Mirror the tree (swap every left and right child) and return the root.",
  "def invert_tree(root):\n    pass",
  '[(([4, 2, 7, 1, 3, 6, 9],), [4, 7, 2, 9, 6, 3, 1]), (([2, 1, 3],), [2, 3, 1]), (([],), [])]',
  """
def invert_tree(root):
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
""",
  "Swap the children, recursing into each. Tuple assignment does it in one line.", prep=TREE_OUT, lc="invert-binary-tree")

D("level-order", "p7", "Binary Tree Level Order Traversal", "level_order",
  "Return the values level by level, as a list of lists. BFS with a <code>deque</code>.",
  "from collections import deque\n\ndef level_order(root):\n    pass",
  '[(([3, 9, 20, None, None, 15, 7],), [[3], [9, 20], [15, 7]]), (([1],), [[1]]), (([],), []), (([1, 2, 3, 4, None, None, 5],), [[1], [2, 3], [4, 5]])]',
  """
from collections import deque

def level_order(root):
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
""",
  "At the start of each round, len(q) is exactly the number of nodes on the current level. Pop that many, pushing their children.", prep=TREE_IN, lc="binary-tree-level-order-traversal")

D("valid-bst", "p7", "Validate Binary Search Tree", "is_valid_bst",
  "Return whether the tree is a valid BST (strictly less on the left, strictly greater on the right, for every subtree).",
  "def is_valid_bst(root):\n    pass",
  '[(([2, 1, 3],), True), (([5, 1, 4, None, None, 3, 6],), False), (([5, 4, 6, None, None, 3, 7],), False), (([],), True), (([1, 1],), False)]',
  """
def is_valid_bst(root):
    def ok(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)

    return ok(root, float("-inf"), float("inf"))
""",
  "Checking only parent vs child is the classic bug (third test). Pass down an allowed range (lo, hi): going left tightens hi, going right tightens lo.", prep=TREE_IN, lc="validate-binary-search-tree")

D("diameter", "p7", "Diameter of Binary Tree", "diameter_of_binary_tree",
  "Return the number of edges on the longest path between any two nodes. Compute heights, and update a running best on the way back up.",
  "def diameter_of_binary_tree(root):\n    pass",
  '[(([1, 2, 3, 4, 5],), 3), (([1, 2],), 1), (([1],), 0), (([1, 2, None, 3, 4, 5, None, None, 6],), 4)]',
  """
def diameter_of_binary_tree(root):
    best = 0

    def height(node):
        nonlocal best
        if not node:
            return 0
        l = height(node.left)
        r = height(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)

    height(root)
    return best
""",
  "The longest path through a node is height(left) + height(right). Return the height, but track the best path in an outer variable (nonlocal).", prep=TREE_IN, lc="diameter-of-binary-tree")

# ------------------------------------------------------------------ p8 heaps
D("kth-largest", "p8", "Kth Largest Element", "find_kth_largest",
  "Return the k-th largest element. Keep a min-heap of size k: O(n log k).",
  "import heapq\n\ndef find_kth_largest(nums, k):\n    pass",
  '[(([3, 2, 1, 5, 6, 4], 2), 5), (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4), (([1], 1), 1), (([2, 1], 2), 1)]',
  """
import heapq

def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
""",
  "Push every number; whenever the heap holds more than k, pop the smallest. What's left is the k largest, and the root heap[0] is the k-th largest.", lc="kth-largest-element-in-an-array")

D("top-k-freq", "p8", "Top K Frequent Elements", "top_k_frequent",
  "Return the <code>k</code> most frequent numbers, in any order.",
  "def top_k_frequent(nums, k):\n    pass",
  '[(([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1]), (([4, 4, 5, 5, 5, 6], 1), [5]), (([1, 2, 2, 3, 3, 3], 3), [1, 2, 3])]',
  """
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)
""",
  "Counter for frequencies, then heapq.nlargest(k, counts, key=counts.get). Bonus: bucket sort by frequency gets O(n).", cmp="sorted", lc="top-k-frequent-elements")

D("k-closest", "p8", "K Closest Points to Origin", "k_closest",
  "Return the <code>k</code> points closest to (0, 0), in any order. No need for square roots: compare x² + y².",
  "def k_closest(points, k):\n    pass",
  '[(([[1, 3], [-2, 2]], 1), [[-2, 2]]), (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]]), (([[0, 1]], 1), [[0, 1]])]',
  """
import heapq

def k_closest(points, k):
    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])
""",
  "heapq.nsmallest(k, points, key=...) with key = x*x + y*y. Doing it by hand: a max-heap of size k using negated distances.", cmp="sorted", lc="k-closest-points-to-origin")

D("last-stone", "p8", "Last Stone Weight", "last_stone_weight",
  "Repeatedly smash the two heaviest stones; if they differ, the difference goes back. Return the last stone's weight, or 0. Python only has a min-heap, so store negatives.",
  "import heapq\n\ndef last_stone_weight(stones):\n    pass",
  '[(([2, 7, 4, 1, 8, 1],), 1), (([1],), 1), (([2, 2],), 0), (([10, 4],), 6)]',
  """
import heapq

def last_stone_weight(stones):
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)
        b = -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))
    return -heap[0] if heap else 0
""",
  "heap = [-s for s in stones], heapify, then pop twice with a minus sign. Push back -(a - b) if they differ.", lc="last-stone-weight")

# ------------------------------------------------------------------ p9 backtracking
D("subsets", "p9", "Subsets", "subsets",
  "Return all subsets of a list of unique numbers, in any order.",
  "def subsets(nums):\n    pass",
  '[(([1, 2, 3],), [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]), (([0],), [[], [0]]), (([],), [[]])]',
  """
def subsets(nums):
    res = []
    path = []

    def backtrack(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
        backtrack(i + 1)

    backtrack(0)
    return res
""",
  "At index i, two choices: include nums[i] or don't. Record path[:] (a copy!) when i reaches the end.", cmp="sorted_inner", lc="subsets")

D("permutations", "p9", "Permutations", "permute",
  "Return all permutations of a list of unique numbers, in any order.",
  "def permute(nums):\n    pass",
  '[(([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), (([0, 1],), [[0, 1], [1, 0]]), (([1],), [[1]])]',
  """
def permute(nums):
    res = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(x)
                backtrack()
                path.pop()
                used[i] = False

    backtrack()
    return res
""",
  "Choose any unused number, recurse, then undo the choice (pop and mark unused). The undo step is what makes it backtracking.", cmp="sorted", lc="permutations")

D("combo-sum", "p9", "Combination Sum", "combination_sum",
  "Return all unique combinations of <code>candidates</code> (unique, positive) that sum to <code>target</code>. A number may be reused any number of times.",
  "def combination_sum(candidates, target):\n    pass",
  '[(([2, 3, 6, 7], 7), [[2, 2, 3], [7]]), (([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), (([2], 1), [])]',
  """
def combination_sum(candidates, target):
    res = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c <= remaining:
                path.append(c)
                backtrack(i, remaining - c)
                path.pop()

    backtrack(0, target)
    return res
""",
  "Pass a start index so you never pick a candidate before the previous one (this avoids [2,3] and [3,2] both appearing). Recurse with i, not i + 1, to allow reuse.", cmp="sorted_inner", lc="combination-sum")

D("word-search", "p9", "Word Search", "exist",
  "Return whether <code>word</code> can be traced in the grid through adjacent (up/down/left/right) cells, using each cell at most once.",
  "def exist(board, word):\n    pass",
  '[(([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"), True), (([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"), True), (([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"), False), (([["a"]], "a"), True)]',
  """
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
            return False
        tmp = board[r][c]
        board[r][c] = "#"
        found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                 dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
        board[r][c] = tmp
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
""",
  "DFS from every cell. Mark the cell as used (overwrite with '#'), explore 4 neighbours, then restore it. Bounds check first.", lc="word-search")

# ------------------------------------------------------------------ p10 graphs
D("islands", "p10", "Number of Islands", "num_islands",
  "Count islands of <code>\"1\"</code>s in a grid (connected up/down/left/right).",
  "def num_islands(grid):\n    pass",
  '[(([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]],), 1), (([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]],), 3), (([["0"]],), 0)]',
  """
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
""",
  "Scan every cell. On a '1', count an island and flood-fill (DFS) it to '0' so it's never counted again.", lc="number-of-islands")

D("course-schedule", "p10", "Course Schedule", "can_finish",
  "<code>prerequisites[i] = [a, b]</code> means take b before a. Return whether all courses can be finished (no cycle). Use Kahn's algorithm (BFS topological sort).",
  "from collections import deque\n\ndef can_finish(num_courses, prerequisites):\n    pass",
  '[((2, [[1, 0]]), True), ((2, [[1, 0], [0, 1]]), False), ((3, []), True), ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False), ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), True)]',
  """
from collections import deque

def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1
    q = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0
    while q:
        c = q.popleft()
        taken += 1
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    return taken == num_courses
""",
  "Build an adjacency list b → a and count incoming edges. Start with all courses that have indegree 0. Each time you take one, decrement its neighbours. If you took every course, there's no cycle.", lc="course-schedule")

D("rotting", "p10", "Rotting Oranges", "oranges_rotting",
  "Every minute, rotten oranges (2) rot their fresh neighbours (1). Return minutes until none are fresh, or -1 if impossible. Multi-source BFS.",
  "from collections import deque\n\ndef oranges_rotting(grid):\n    pass",
  '[(([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4), (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1), (([[0, 2]],), 0), (([[0]],), 0)]',
  """
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1
""",
  "Put every rotten orange in the queue at once. Process level by level (one level = one minute). Count fresh oranges so you know whether any are left at the end.", lc="rotting-oranges")

D("components", "p10", "Connected Components (Union-Find)", "count_components",
  "Given <code>n</code> nodes and undirected <code>edges</code>, return the number of connected components. Implement union-find with path compression.",
  "def count_components(n, edges):\n    pass",
  '[((5, [[0, 1], [1, 2], [3, 4]]), 2), ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1), ((3, []), 3), ((4, [[0, 1], [2, 3], [1, 2], [0, 3]]), 1)]',
  """
def count_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1
    return components
""",
  "parent[i] = i to start. find follows parents to the root (and shortens the path as it goes). Each union of two different roots merges two components, so subtract 1.")

D("flood-fill", "p10", "Flood Fill", "flood_fill",
  "Starting from <code>(sr, sc)</code>, recolour every connected cell of the same original colour to <code>color</code>. Return the image.",
  "def flood_fill(image, sr, sc, color):\n    pass",
  '[(([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), [[2, 2, 2], [2, 2, 0], [2, 0, 1]]), (([[0, 0, 0], [0, 0, 0]], 0, 0, 0), [[0, 0, 0], [0, 0, 0]]), (([[0, 0, 0], [0, 1, 1]], 1, 1, 1), [[0, 0, 0], [0, 1, 1]])]',
  """
def flood_fill(image, sr, sc, color):
    start = image[sr][sc]
    if start == color:
        return image
    rows, cols = len(image), len(image[0])

    def dfs(r, c):
        if 0 <= r < rows and 0 <= c < cols and image[r][c] == start:
            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

    dfs(sr, sc)
    return image
""",
  "If the start already has the new colour, return immediately, or the DFS never stops (recolouring doesn't change anything, so cells keep matching).", lc="flood-fill")

# ------------------------------------------------------------------ p11 dynamic programming
D("climb", "p11", "Climbing Stairs", "climb_stairs",
  "You climb 1 or 2 steps at a time. How many distinct ways to reach step <code>n</code>?",
  "def climb_stairs(n):\n    pass",
  '[((1,), 1), ((2,), 2), ((3,), 3), ((5,), 8), ((45,), 1836311903)]',
  """
def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
""",
  "ways(n) = ways(n-1) + ways(n-2): your last move was either 1 step or 2. It's Fibonacci. n = 45 is in the tests, so plain recursion without memoisation will time out.", lc="climbing-stairs")

D("house-robber", "p11", "House Robber", "rob",
  "You can't rob two adjacent houses. Return the maximum total.",
  "def rob(nums):\n    pass",
  '[(([1, 2, 3, 1],), 4), (([2, 7, 9, 3, 1],), 12), (([],), 0), (([5],), 5), (([2, 1, 1, 2],), 4)]',
  """
def rob(nums):
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur
""",
  "best(i) = max(best(i-1), best(i-2) + nums[i]): skip this house, or rob it and add the best from two back. You only need the last two values.", lc="house-robber")

D("coin-change", "p11", "Coin Change", "coin_change",
  "Return the fewest coins that make <code>amount</code>, or -1. Unlimited coins of each type.",
  "def coin_change(coins, amount):\n    pass",
  '[(([1, 2, 5], 11), 3), (([2], 3), -1), (([1], 0), 0), (([186, 419, 83, 408], 6249), 20)]',
  """
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
""",
  "dp[a] = fewest coins for amount a. dp[0] = 0, everything else starts at infinity. dp[a] = min over coins c of dp[a - c] + 1. Greedy (biggest coin first) is wrong here.", lc="coin-change")

D("unique-paths", "p11", "Unique Paths", "unique_paths",
  "A robot in the top-left of an m×n grid moves only right or down. How many paths reach the bottom-right?",
  "def unique_paths(m, n):\n    pass",
  '[((3, 7), 28), ((3, 2), 3), ((1, 1), 1), ((10, 10), 48620)]',
  """
def unique_paths(m, n):
    row = [1] * n
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
""",
  "paths[r][c] = paths[r-1][c] + paths[r][c-1]. The first row and column are all 1. You can keep just one row and update it in place.", lc="unique-paths")

D("lis", "p11", "Longest Increasing Subsequence", "length_of_lis",
  "Return the length of the longest strictly increasing subsequence. O(n²) DP is fine; O(n log n) with <code>bisect</code> is the bonus.",
  "def length_of_lis(nums):\n    pass",
  '[(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([0, 1, 0, 3, 2, 3],), 4), (([7, 7, 7, 7],), 1), (([],), 0)]',
  """
from bisect import bisect_left

def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
""",
  "O(n²): dp[i] = 1 + max(dp[j] for j < i with nums[j] < nums[i]). O(n log n): tails[k] = smallest possible tail of an increasing subsequence of length k + 1; bisect_left to place each x.", lc="longest-increasing-subsequence")

D("lcs", "p11", "Longest Common Subsequence", "longest_common_subsequence",
  "Return the length of the longest subsequence common to both strings. Classic 2D DP.",
  "def longest_common_subsequence(text1, text2):\n    pass",
  '[(("abcde", "ace"), 3), (("abc", "abc"), 3), (("abc", "def"), 0), (("", "a"), 0), (("bsbininm", "jmjkbkjkv"), 1)]',
  """
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
""",
  "dp[i][j] = LCS of the first i chars of text1 and first j of text2. Equal last chars: 1 + dp[i-1][j-1]. Otherwise max of dropping one char from either. Build the grid with a comprehension, not [[0]*(n+1)]*(m+1).", lc="longest-common-subsequence")

D("word-break", "p11", "Word Break", "word_break",
  "Return whether <code>s</code> can be split into words from <code>word_dict</code> (words can be reused).",
  "def word_break(s, word_dict):\n    pass",
  '[(("leetcode", ["leet", "code"]), True), (("applepenapple", ["apple", "pen"]), True), (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False), (("", ["a"]), True)]',
  """
def word_break(s, word_dict):
    words = set(word_dict)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]
""",
  "dp[i] = can the first i characters be split? dp[0] = True. dp[i] is True if some j < i has dp[j] True and s[j:i] is a word.", lc="word-break")

# ------------------------------------------------------------------ p12 intervals & greedy
D("merge-intervals", "p12", "Merge Intervals", "merge",
  "Merge all overlapping intervals.",
  "def merge(intervals):\n    pass",
  '[(([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]), (([[1, 4], [4, 5]],), [[1, 5]]), (([[4, 7], [1, 4]],), [[1, 7]]), (([[1, 4], [2, 3]],), [[1, 4]])]',
  """
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for start, end in intervals:
        if res and start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res
""",
  "Sort by start. If the next interval starts before the last merged one ends, extend the end with max (the last test is why it's max and not just end).", lc="merge-intervals")

D("jump-game", "p12", "Jump Game", "can_jump",
  "<code>nums[i]</code> is your max jump from i. Can you reach the last index? Greedy, O(n).",
  "def can_jump(nums):\n    pass",
  '[(([2, 3, 1, 1, 4],), True), (([3, 2, 1, 0, 4],), False), (([0],), True), (([2, 0, 0],), True), (([1, 0, 1],), False)]',
  """
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
""",
  "Track the furthest index you can reach so far. If you ever stand on an index beyond it, you're stuck.", lc="jump-game")

D("kadane", "p12", "Maximum Subarray", "max_sub_array",
  "Return the largest sum of a non-empty contiguous subarray. Kadane's algorithm.",
  "def max_sub_array(nums):\n    pass",
  '[(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([1],), 1), (([5, 4, -1, 7, 8],), 23), (([-3, -1, -2],), -1)]',
  """
def max_sub_array(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
""",
  "At each x: either extend the current run (cur + x) or start fresh at x, whichever is bigger. Start best at nums[0], not 0, for all-negative inputs.", lc="maximum-subarray")

D("non-overlap", "p12", "Non-overlapping Intervals", "erase_overlap_intervals",
  "Return the minimum number of intervals to remove so the rest don't overlap (touching at an endpoint is fine).",
  "def erase_overlap_intervals(intervals):\n    pass",
  '[(([[1, 2], [2, 3], [3, 4], [1, 3]],), 1), (([[1, 2], [1, 2], [1, 2]],), 2), (([[1, 2], [2, 3]],), 0), (([[1, 100], [11, 22], [1, 11], [2, 12]],), 2)]',
  """
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    removed = 0
    end = float("-inf")
    for s, e in intervals:
        if s >= end:
            end = e
        else:
            removed += 1
    return removed
""",
  "Sort by end time. Keep an interval if it starts at or after the last kept end; otherwise remove it. Keeping the earliest-ending interval leaves the most room for the rest.", lc="non-overlapping-intervals")
