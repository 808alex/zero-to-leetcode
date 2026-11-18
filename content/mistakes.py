"""Common mistakes library. build_content.py runs every `wrong` and `right` snippet and records what Python
actually prints or raises, so the messages shown in the app are real, not typed in by hand.
Set run=False for mistakes that are about speed (they don't produce a visible error)."""
from textwrap import dedent

MISTAKES = []
CATEGORIES = ["Syntax", "Types and numbers", "Loops", "Lists, strings and dicts", "Functions", "Speed", "LeetCode habits"]


def M(id, cat, level, title, wrong, right, why, stdin="", run=True):
    assert cat in CATEGORIES, cat
    MISTAKES.append({"id": id, "cat": cat, "level": level, "title": title, "wrong": dedent(wrong).strip("\n") + "\n",
                     "right": dedent(right).strip("\n") + "\n", "why": why, "stdin": stdin, "run": run})


# ---------------------------------------------------------------- syntax
M("colon", "Syntax", "z2", "Forgetting the colon", """
    x = 5
    if x > 3
        print("big")
""", """
    x = 5
    if x > 3:
        print("big")
""", "Every line that starts a block (if, elif, else, for, while, def, class) ends with a colon.")

M("assign-compare", "Syntax", "z2", "= instead of == in a condition", """
    x = 3
    if x = 3:
        print("three")
""", """
    x = 3
    if x == 3:
        print("three")
""", "One = stores a value. Two == compares. Conditions always compare.")

M("indent", "Syntax", "z2", "Indentation that doesn't line up", """
    for i in range(3):
        print(i)
          print("done")
""", """
    for i in range(3):
        print(i)
    print("done")
""", "Python uses indentation to know what's inside a block. Use exactly 4 spaces per level, and line them up.")

M("unclosed", "Syntax", "z1", "A bracket that's never closed", """
    print("total:", (3 + 4)
""", """
    print("total:", (3 + 4))
""", "Count your brackets. The error often points at the line after the real mistake.")

M("no-quotes", "Syntax", "z1", "Text without quotes", """
    print(hello)
""", """
    print("hello")
""", "Without quotes, Python thinks hello is a variable name, and there isn't one.")

# ---------------------------------------------------------------- types and numbers
M("input-text", "Types and numbers", "z1", "Treating input() as a number", """
    age = input()
    print(age + 1)
""", """
    age = int(input())
    print(age + 1)
""", "input() always returns a string. Convert with int() or float() before doing maths.", stdin="19\n")

M("str-plus-int", "Types and numbers", "z1", "Gluing text and a number with +", """
    score = 42
    print("Score: " + score)
""", """
    score = 42
    print(f"Score: {score}")
""", "+ joins two strings or adds two numbers, but not one of each. f-strings sidestep the problem.")

M("slash-float", "Types and numbers", "z1", "Expecting / to give a whole number", """
    print(7 / 2)
""", """
    print(7 // 2)
""", "/ always gives a float. // is whole-number division (it rounds down).")

M("floor-negative", "Types and numbers", "m2", "// with negative numbers", """
    print(-7 // 2)
""", """
    print(int(-7 / 2))
""", "// rounds down (towards minus infinity), so -3.5 becomes -4. To cut off the decimals towards zero, use int(a / b).")

M("float-eq", "Types and numbers", "z1", "Comparing floats with ==", """
    print(0.1 + 0.2 == 0.3)
""", """
    print(abs((0.1 + 0.2) - 0.3) < 1e-9)
""", "Floats are stored in binary, so 0.1 + 0.2 is 0.30000000000000004. Compare with a small tolerance.")

M("int-of-decimal", "Types and numbers", "z1", "int() on a decimal string", """
    print(int("3.5"))
""", """
    print(int(float("3.5")))
""", "int() only accepts whole-number text. Go through float() first (it cuts off the decimal part).")

# ---------------------------------------------------------------- loops
M("no-step", "Loops", "z3", "A while loop with no step", """
    i = 0
    while i < 3:
        print(i)
""", """
    i = 0
    while i < 3:
        print(i)
        i = i + 1
""", "If nothing in the body changes the condition, the loop never ends. Check that the loop variable moves every time round.", run=False)

M("range-stop", "Loops", "z4", "Off by one with range", """
    for i in range(1, 5):
        print(i)
""", """
    for i in range(1, 6):
        print(i)
""", "range stops before its stop value. To include n, write range(1, n + 1).")

M("or-trap", "Loops", "z2", "x == a or b", """
    day = 3
    if day == 6 or 7:
        print("weekend")
""", """
    day = 3
    if day == 6 or day == 7:
        print("weekend")
""", "`day == 6 or 7` means `(day == 6) or 7`, and 7 on its own counts as True. Repeat the comparison, or write `day in (6, 7)`.")

M("modify-while-looping", "Loops", "z6", "Removing items from a list while looping over it", """
    nums = [2, 4, 6, 7]
    for x in nums:
        if x % 2 == 0:
            nums.remove(x)
    print(nums)
""", """
    nums = [2, 4, 6, 7]
    nums = [x for x in nums if x % 2 != 0]
    print(nums)
""", "Removing shifts everything left, so the loop skips the next item. Build a new list instead.")

M("loop-var-after", "Loops", "z4", "Expecting a for loop to change the list", """
    nums = [1, 2, 3]
    for x in nums:
        x = x * 10
    print(nums)
""", """
    nums = [1, 2, 3]
    for i in range(len(nums)):
        nums[i] = nums[i] * 10
    print(nums)
""", "x is a copy of each value. Assigning to it doesn't touch the list. Write to nums[i] (or build a new list).")

# ---------------------------------------------------------------- lists, strings, dicts
M("index-range", "Lists, strings and dicts", "z5", "Indexing one past the end", """
    s = "hello"
    print(s[len(s)])
""", """
    s = "hello"
    print(s[len(s) - 1], s[-1])
""", "Indexes run from 0 to len(s) - 1. s[-1] is the neat way to get the last item.")

M("str-immutable", "Lists, strings and dicts", "z5", "Changing a character in a string", """
    s = "hello"
    s[0] = "H"
    print(s)
""", """
    s = "hello"
    s = "H" + s[1:]
    print(s)
""", "Strings can't be changed in place. Make a new string (or work on list(s) and join it back).")

M("alias", "Lists, strings and dicts", "z6", "b = a doesn't copy a list", """
    a = [1, 2]
    b = a
    b.append(3)
    print(a)
""", """
    a = [1, 2]
    b = a[:]
    b.append(3)
    print(a)
""", "Both names point at the same list. a[:] or list(a) makes a real copy.")

M("grid", "Lists, strings and dicts", "m2", "Building a grid with * ", """
    grid = [[0] * 3] * 2
    grid[0][0] = 1
    print(grid)
""", """
    grid = [[0] * 3 for _ in range(2)]
    grid[0][0] = 1
    print(grid)
""", "Multiplying the outer list repeats the same row object. Build each row separately.")

M("sort-none", "Lists, strings and dicts", "z6", "nums = nums.sort()", """
    nums = [3, 1, 2]
    nums = nums.sort()
    print(nums)
""", """
    nums = [3, 1, 2]
    nums.sort()
    print(nums)
""", ".sort() sorts in place and returns None. Use nums.sort() on its own, or new = sorted(nums).")

M("keyerror", "Lists, strings and dicts", "m2", "Counting into a dict without a default", """
    counts = {}
    for ch in "hello":
        counts[ch] += 1
    print(counts)
""", """
    counts = {}
    for ch in "hello":
        counts[ch] = counts.get(ch, 0) + 1
    print(counts)
""", "A missing key raises KeyError. Use .get(key, 0), defaultdict(int) or Counter.")

# ---------------------------------------------------------------- functions
M("print-not-return", "Functions", "z7", "Printing instead of returning", """
    def double(x):
        print(x * 2)

    result = double(4)
    print("result is", result)
""", """
    def double(x):
        return x * 2

    result = double(4)
    print("result is", result)
""", "A function without return gives back None. LeetCode checks what you return, never what you print.")

M("return-in-loop", "Functions", "z7", "return inside the loop", """
    def total(nums):
        s = 0
        for x in nums:
            s += x
            return s

    print(total([1, 2, 3]))
""", """
    def total(nums):
        s = 0
        for x in nums:
            s += x
        return s

    print(total([1, 2, 3]))
""", "return ends the function immediately. Dedent it so it runs after the loop finishes.")

M("mutable-default", "Functions", "m2", "A list as a default argument", """
    def add(item, items=[]):
        items.append(item)
        return items

    add("a")
    print(add("b"))
""", """
    def add(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items

    add("a")
    print(add("b"))
""", "The default list is created once and shared by every call. Default to None and create the list inside.")

M("shadow", "Functions", "m1", "Naming a variable list, str, sum or max", """
    list = [1, 2, 3]
    print(list("abc"))
""", """
    nums = [1, 2, 3]
    print(list("abc"))
""", "Using a built-in's name as a variable hides the built-in for the rest of the program.")

M("no-base", "Functions", "m4", "Recursion with no base case", """
    def count(n):
        return 1 + count(n - 1)

    print(count(5))
""", """
    def count(n):
        if n == 0:
            return 0
        return 1 + count(n - 1)

    print(count(5))
""", "Every recursive function needs a case that returns without calling itself.")

M("path-copy", "Functions", "p9", "Saving the path without copying it (backtracking)", """
    res, path = [], []
    def bt(i):
        if i == 2:
            res.append(path)
            return
        path.append(i)
        bt(i + 1)
        path.pop()
    bt(0)
    print(res)
""", """
    res, path = [], []
    def bt(i):
        if i == 2:
            res.append(path[:])
            return
        path.append(i)
        bt(i + 1)
        path.pop()
    bt(0)
    print(res)
""", "res ends up holding the same list object, which is empty once every pop has run. Append path[:].")

# ---------------------------------------------------------------- speed
M("in-list", "Speed", "m2", "Checking `x in list` inside a loop", """
    seen = []
    for x in nums:
        if x in seen:      # scans the whole list every time
            return True
        seen.append(x)
""", """
    seen = set()
    for x in nums:
        if x in seen:      # O(1)
            return True
        seen.add(x)
""", "x in list is O(n), so doing it n times is O(n²). A set (or dict) lookup is O(1). This is the most common Time Limit Exceeded on LeetCode.", run=False)

M("pop-front", "Speed", "m2", "Using list.pop(0) as a queue", """
    queue = [start]
    while queue:
        node = queue.pop(0)   # shifts every element
""", """
    from collections import deque
    queue = deque([start])
    while queue:
        node = queue.popleft()   # O(1)
""", "Removing from the front of a list moves everything else along. deque is built for it. BFS needs this.", run=False)

M("str-concat", "Speed", "m2", "Building a big string with += in a loop", """
    out = ""
    for word in words:
        out += word + " "
""", """
    out = " ".join(words)
""", "Strings can't change, so each += can copy the whole string so far. Collect pieces in a list and join once.", run=False)

M("slice-recursion", "Speed", "m4", "Passing slices into recursion", """
    def total(nums):
        if not nums:
            return 0
        return nums[0] + total(nums[1:])   # copies the list every call
""", """
    def total(nums, i=0):
        if i == len(nums):
            return 0
        return nums[i] + total(nums, i + 1)
""", "nums[1:] copies the list, so the whole thing becomes O(n²). Pass an index instead.", run=False)

# ---------------------------------------------------------------- LeetCode habits
M("in-place", "LeetCode habits", "p2", "\"Modify nums in-place\" but you reassign it", """
    def sort_it(nums):
        nums = sorted(nums)     # makes a new list, caller never sees it

    data = [3, 1, 2]
    sort_it(data)
    print(data)
""", """
    def sort_it(nums):
        nums.sort()              # or: nums[:] = sorted(nums)

    data = [3, 1, 2]
    sort_it(data)
    print(data)
""", "When LeetCode says \"do not return anything\", it checks the list it passed you. Reassigning the name doesn't change that list; mutating it does.")

M("check-empty", "LeetCode habits", "p6", "Forgetting the empty input", """
    def first_val(head):
        return head.val

    print(first_val(None))
""", """
    def first_val(head):
        if head is None:
            return None
        return head.val

    print(first_val(None))
""", "Empty lists, empty strings, None heads and roots, n = 0: check them first. LeetCode's hidden tests always include them.")

M("max-init", "LeetCode habits", "z6", "Starting a max at 0", """
    nums = [-5, -2, -8]
    best = 0
    for x in nums:
        best = max(best, x)
    print(best)
""", """
    nums = [-5, -2, -8]
    best = float("-inf")
    for x in nums:
        best = max(best, x)
    print(best)
""", "If every value is negative, 0 wins wrongly. Start with nums[0] or float('-inf').")
