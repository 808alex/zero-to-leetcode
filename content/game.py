"""Game layer: quick questions (what does this print / fill in the blank / fix the bug), skills per level, and bosses.

Answers are never typed in by hand where they can be computed:
  - "what does this print" runs the code and uses the real output as the correct option
  - fill-in-the-blank and fix-the-bug compute expected results from the reference answer
  - boss tests compute expected values from the reference solution
build_content.py does all of that and fails the build if anything doesn't line up.
"""
from textwrap import dedent


def c(s):
    return dedent(s).strip("\n") + "\n"


def mc(code, wrong, explain, prompt="What does this print?", stdin=""):
    return {"kind": "mc", "prompt": prompt, "code": c(code), "wrong": wrong, "explain": explain, "stdin": stdin}


def mct(prompt, options, answer, explain, code=None):
    """Multiple choice with a stated answer (concept questions). options[answer] is correct."""
    return {"kind": "mct", "prompt": prompt, "options": options, "answer": answer, "explain": explain,
            "code": c(code) if code else None}


def fill(prompt, code, answer, explain, hint, stdins=None, fn=None, args=None, cmp="eq", prep=""):
    return {"kind": "fill", "prompt": prompt, "code": c(code), "answer": answer, "explain": explain, "hint": hint,
            "stdins": stdins, "fn": fn, "args": args, "cmp": cmp, "prep": prep}


def fix(prompt, buggy, fixed, explain, hint, stdins=None, fn=None, args=None, cmp="eq", prep=""):
    return {"kind": "fix", "prompt": prompt, "buggy": c(buggy), "fixed": c(fixed), "explain": explain, "hint": hint,
            "stdins": stdins, "fn": fn, "args": args, "cmp": cmp, "prep": prep}


def boss(title, fn, prompt, starter, solution, args, hint, cmp="eq", prep="", visible=2, stdins=None):
    return {"kind": "boss", "title": title, "fn": fn, "prompt": prompt, "starter": c(starter), "solution": c(solution),
            "args": args, "hint": hint, "cmp": cmp, "prep": prep, "visible": visible, "stdins": stdins}


LL_IN = "def _call(args):\n    return _fn(_to_ll(args[0]), *args[1:])"
LL_OUT = "def _call(args):\n    return _from_ll(_fn(*[_to_ll(a) for a in args]))"
TREE_IN = "def _call(args):\n    return _fn(_to_tree(args[0]), *args[1:])"

LEVELS = {}


def level(lid, skills):
    LEVELS[lid] = skills


# =================================================================== UNIT 0
level("z1", [
    ("Variables and printing", [
        mc("""
            x = 5
            y = x
            x = x + 2
            print(x, y)
        """, ["7 7", "5 7", "x y"],
           "y = x copies the value 5 into y. Changing x afterwards doesn't touch y."),
        mc('print(f"{2 + 3} apples")', ["{2 + 3} apples", "2 + 3 apples", "23 apples"],
           "Anything inside {} in an f-string is worked out first, so {2 + 3} becomes 5."),
        "z-hello",
    ]),
    ("input() gives you text", [
        mc("""
            a = input()
            b = input()
            print(a + b)
        """, ["7", "3 4", "Error"],
           "input() always returns a string. \"3\" + \"4\" glues the text together: \"34\". Use int(input()) for numbers.",
           stdin="3\n4\n"),
        fill("Print the product of the two numbers.", """
            a = int(input())
            b = int(input())
            print(___)
        """, "a * b", "* multiplies. a and b are already numbers thanks to int().", "Which operator multiplies?",
             stdins=["6\n7\n", "0\n5\n", "-2\n3\n"]),
        "z-add",
    ]),
    ("// and %", [
        mc("print(17 // 5, 17 % 5)", ["3.4 2", "3 3", "2 3"],
           "17 // 5 is how many whole 5s fit in 17 (3). 17 % 5 is what's left over (2)."),
        mc("print(7 / 2, 8 / 2)", ["3 4", "3.5 4", "3 4.0"],
           "/ always gives a float in Python 3, even when it divides evenly: 8 / 2 is 4.0."),
        fix("This should print how many whole hours are in the minutes, like <code>2 hours</code>. It prints <code>2.0 hours</code>. Fix it.", """
            minutes = int(input())
            hours = minutes / 60
            print(hours, "hours")
        """, """
            minutes = int(input())
            hours = minutes // 60
            print(hours, "hours")
        """, "/ gives a float. // gives a whole number (rounded down).", "Which division operator gives a whole number?",
            stdins=["120\n", "59\n", "600\n"]),
        "z-minutes", "z-last-digit", "z-receipt",
    ]),
])

level("z2", [
    ("if, elif, else", [
        mc("""
            score = 72
            if score >= 50:
                print("pass")
            elif score >= 70:
                print("merit")
            else:
                print("fail")
        """, ["merit", "pass\nmerit", "fail"],
           "Python runs only the first branch that's True. 72 >= 50 is True, so the elif is never checked. Put the stricter check first."),
        fill("Print <code>negative</code> for numbers below zero.", """
            n = int(input())
            if ___:
                print("negative")
            else:
                print("not negative")
        """, "n < 0", "The condition must be True exactly when n is below zero.", "Compare n with 0.",
             stdins=["-4\n", "0\n", "5\n"]),
        "z-even-odd", "z-weekend",
    ]),
    ("and, or, and the order of checks", [
        mc("""
            day = 3
            if day == 6 or 7:
                print("weekend")
            else:
                print("weekday")
        """, ["weekday", "Error", "(nothing)"],
           "This is a classic trap. `day == 6 or 7` means `(day == 6) or 7`, and 7 on its own counts as True. Write `day == 6 or day == 7`."),
        fix("FizzBuzz for one number, but 15 prints <code>fizz</code> instead of <code>fizz-buzz</code>. Fix it.", """
            n = int(input())
            if n % 3 == 0:
                print("fizz")
            elif n % 5 == 0:
                print("buzz")
            elif n % 3 == 0 and n % 5 == 0:
                print("fizz-buzz")
            else:
                print(n)
        """, """
            n = int(input())
            if n % 3 == 0 and n % 5 == 0:
                print("fizz-buzz")
            elif n % 3 == 0:
                print("fizz")
            elif n % 5 == 0:
                print("buzz")
            else:
                print(n)
        """, "The 'both' check must come first. Once n % 3 == 0 matches, the later elifs are skipped.",
            "Which branch does 15 hit first?", stdins=["15\n", "9\n", "10\n", "7\n"]),
        "z-fizzbuzz-one", "z-biggest", "z-grade", "z-leap",
    ]),
])

level("z3", [
    ("Start, condition, step", [
        mc("""
            i = 0
            while i < 3:
                print(i)
                i = i + 1
        """, ["1\n2\n3", "0\n1\n2\n3", "(nothing)"],
           "i starts at 0 and the loop stops as soon as i < 3 is False, so 3 itself is never printed."),
        mc("""
            i = 10
            count = 0
            while i > 0:
                i = i - 3
                count = count + 1
            print(count, i)
        """, ["3 1", "4 -1", "3 -2"],
           "Trace it: i goes 10 → 7 → 4 → 1 → -2. That's 4 rounds. The loop only checks i > 0 at the top, so i ends up negative."),
        fill("Print the numbers 1 to n.", """
            n = int(input())
            i = 1
            while ___:
                print(i)
                i = i + 1
        """, "i <= n", "Keep going while i hasn't passed n. With < you'd miss n itself.", "Should n itself be printed?",
             stdins=["3\n", "1\n", "0\n"]),
        "z-count-up", "z-countdown",
    ]),
    ("Running totals", [
        fix("This should add up 1 + 2 + ... + n, but it's always short. Fix it.", """
            n = int(input())
            total = 0
            i = 1
            while i < n:
                total = total + i
                i = i + 1
            print(total)
        """, """
            n = int(input())
            total = 0
            i = 1
            while i <= n:
                total = total + i
                i = i + 1
            print(total)
        """, "Off by one: with i < n the last number n never gets added.", "Trace the last time round the loop when n = 4.",
            stdins=["4\n", "1\n", "100\n"]),
        "z-sum-to-n", "z-multiples",
    ]),
    ("Loops with // and %", [
        mc("""
            n = 4096
            steps = 0
            while n > 1:
                n = n // 2
                steps = steps + 1
            print(steps)
        """, ["11", "13", "4096"],
           "4096 is 2 to the power 12, so it takes 12 halvings to reach 1. That's the idea behind O(log n)."),
        "z-count-digits", "z-collatz",
    ]),
    ("Loops that wait for something", [
        mc("""
            count = 0
            while True:
                word = input()
                if word == "stop":
                    break
                count = count + 1
            print(count)
        """, ["3", "4", "Error"],
           "break leaves the loop the moment it sees \"stop\". The \"c\" after it is never read.", stdin="a\nb\nstop\nc\n"),
        "z-until-end",
    ]),
])

level("z4", [
    ("range", [
        mc("""
            for i in range(2, 10, 3):
                print(i, end=" ")
        """, ["2 5 8 11", "3 6 9", "2 3 4 5 6 7 8 9"],
           "range(start, stop, step): start at 2, add 3 each time, stop before 10."),
        mc("""
            for i in range(5, 0, -2):
                print(i)
        """, ["5\n3\n1\n-1", "4\n2\n0", "5\n4\n3\n2\n1"],
           "A negative step counts down. It stops before reaching 0, so the last value is 1."),
        fill("Print 1 to n with a for loop.", """
            n = int(input())
            for i in range(___):
                print(i)
        """, "1, n + 1", "range stops before the stop value, so you need n + 1 to include n.", "Two numbers: where to start, and one past where to stop.",
             stdins=["3\n", "1\n", "5\n"]),
        "z-times-table", "z-evens", "z-squares",
    ]),
    ("Looping over things", [
        mc("""
            word = "loop"
            count = 0
            for ch in word:
                if ch == "o":
                    count = count + 1
            print(count)
        """, ["1", "4", "0"], "for ch in word visits each letter once. There are two o's."),
        "z-vowels", "z-stars",
    ]),
    ("break and continue", [
        mc("""
            for n in range(1, 10):
                if n % 4 == 0:
                    break
                print(n)
        """, ["1\n2\n3\n4", "4", "1\n2\n3\n5\n6\n7\n9"],
           "When n is 4, break ends the whole loop before the print, so 4 is never printed."),
        fix("Should print the index of the <strong>first</strong> digit (or -1). It prints the last one instead. Fix it.", """
            s = input()
            pos = -1
            for i in range(len(s)):
                if s[i].isdigit():
                    pos = i
            print(pos)
        """, """
            s = input()
            pos = -1
            for i in range(len(s)):
                if s[i].isdigit():
                    pos = i
                    break
            print(pos)
        """, "Without break, the loop keeps going and overwrites pos with every later digit.", "Stop the loop as soon as you find one.",
            stdins=["ab12\n", "x\n", "9a9\n"]),
        "z-first-digit",
    ]),
])

level("z5", [
    ("Indexing and slicing", [
        mc('''
            s = "keyboard"
            print(s[1], s[-2], s[2:5])
        ''', ["k r ybo", "e d ybo", "e r yboa"],
           "Indexes start at 0, so s[1] is \"e\". s[-2] is second from the end. s[2:5] takes positions 2, 3 and 4."),
        mc('print("python"[::2])', ["yhn", "nohtyp", "py"], "Step 2 takes every second character starting at index 0: p, t, o."),
        fill("Print the last 3 characters of the input.", """
            s = input()
            print(___)
        """, "s[-3:]", "Negative indexes count from the end; leaving the stop empty means \"to the end\".", "Start 3 from the end and go to the end.",
             stdins=["hello\n", "abc\n", "python\n"]),
        "z-reverse", "z-palindrome",
    ]),
    ("String methods", [
        mc('print("  Hi There ".strip().lower().split())', ["['Hi', 'There']", "hi there", "['  hi', 'there ']"],
           "Methods chain left to right: strip the outer spaces, lowercase, then split into a list of words."),
        mc('print("-".join("abc"))', ["abc-", "-a-b-c-", "Error"],
           "join puts the separator between items. A string is a sequence of characters, so it joins a, b and c."),
        "z-initials", "z-capitals", "z-count-char",
    ]),
    ("Building new strings", [
        fix("Should print the input with its first letter in capitals. It crashes. Fix it.", """
            s = input()
            s[0] = s[0].upper()
            print(s)
        """, """
            s = input()
            s = s[0].upper() + s[1:]
            print(s)
        """, "Strings can't be changed in place (TypeError). Build a new one: first letter upper, plus the rest.",
            "s[1:] is everything after the first character.", stdins=["hello\n", "a\n", "Zed\n"]),
        "z-hyphens",
    ]),
])

level("z6", [
    ("Making and changing lists", [
        mc("""
            nums = [3, 1, 4]
            nums.append(1)
            nums[0] = 9
            print(nums, len(nums))
        """, ["[3, 1, 4, 1, 9] 5", "[9, 1, 4] 3", "[9, 3, 1, 4, 1] 5"],
           "append adds to the end. nums[0] = 9 replaces the first item; it doesn't insert."),
        mc("""
            a = [1, 2]
            b = a[:]
            b.append(3)
            print(a, b)
        """, ["[1, 2, 3] [1, 2, 3]", "[1, 2] [1, 2]", "Error"],
           "a[:] makes a copy, so changing b leaves a alone. With b = a, both would change."),
        fill("Print the last number in the list.", """
            nums = [int(x) for x in input().split()]
            print(___)
        """, "nums[-1]", "Index -1 is the last item, whatever the length.", "Negative indexes count from the end.",
             stdins=["3 8 5\n", "7\n", "1 2\n"]),
        "z-reverse-list", "z-dedupe",
    ]),
    ("Looping to find things", [
        mc("""
            nums = [4, 7, 1, 7]
            total = 0
            for i in range(len(nums)):
                if nums[i] == 7:
                    total = total + i
            print(total)
        """, ["14", "2", "7"], "It adds the positions (1 and 3) where 7 appears, not the 7s themselves."),
        fix("Should print the biggest number. It's wrong when all the numbers are negative. Fix it.", """
            nums = [int(x) for x in input().split()]
            best = 0
            for x in nums:
                if x > best:
                    best = x
            print(best)
        """, """
            nums = [int(x) for x in input().split()]
            best = nums[0]
            for x in nums:
                if x > best:
                    best = x
            print(best)
        """, "Starting at 0 assumes something beats 0. Start with a real value from the list.", "What should best start as?",
            stdins=["3 9 2\n", "-5 -2 -8\n", "4\n"]),
        "z-max-min", "z-sum-evens", "z-above-avg",
    ]),
])

level("z7", [
    ("def and return", [
        mc("""
            def double(x):
                return x * 2

            print(double(3) + double(4))
        """, ["68", "7", "None"], "Each call returns a number (6 and 8), and then they're added."),
        mc("""
            def shout(word):
                print(word.upper())

            result = shout("hi")
            print(result)
        """, ["HI\nHI", "HI", "None"],
           "shout prints HI but returns nothing, so result is None. This is why LeetCode answers must return."),
        "z-square", "z-is-even", "z-sign-word",
    ]),
    ("Programs become functions", [
        fill("Finish the function so it returns the count.", """
            def count_evens(nums):
                count = 0
                for x in nums:
                    if x % 2 == 0:
                        count = count + 1
                ___
        """, "return count", "The function has to hand the answer back with return, after the loop.", "What keyword sends a value back?",
             fn="count_evens", args=[([1, 2, 4],), ([],), ([3, 5],), ([0, 0, 1],)]),
        fix("<code>total</code> should return the sum of the list. It's wrong for most inputs. Fix it.", """
            def total(nums):
                s = 0
                for x in nums:
                    s = s + x
                    return s
        """, """
            def total(nums):
                s = 0
                for x in nums:
                    s = s + x
                return s
        """, "The return was inside the loop, so the function stopped after the first number.", "Look at the indentation of return.",
            fn="total", args=[([1, 2, 3],), ([],), ([5],), ([-1, 1, 10],)]),
        "z-max3", "z-count-char-fn", "z-average",
    ]),
])

# =================================================================== UNIT 1
level("m1", [
    ("Loops without manual indexes", [
        mc("""
            for i, ch in enumerate("hey"):
                print(i, ch)
        """, ["1 h\n2 e\n3 y", "h 0\ne 1\ny 2", "0\n1\n2"], "enumerate gives (index, item) pairs, starting at 0."),
        mc("""
            names = ["ann", "bo", "cy"]
            ages = [20, 31]
            for n, a in zip(names, ages):
                print(n, a)
        """, ["ann 20\nbo 31\ncy None", "Error", "ann bo cy 20 31"], "zip stops at the shorter list, so cy is never paired."),
        "first-upper", "palindrome", "split-words",
    ]),
    ("Comprehensions", [
        mc("print([x * x for x in range(6) if x % 2 == 1])", ["[0, 4, 16]", "[1, 4, 9, 16, 25]", "[1, 3, 5]"],
           "Keep only the odd x (1, 3, 5), then square each."),
        fill("Return only the even numbers, using a comprehension.", """
            def evens(nums):
                return ___
        """, "[x for x in nums if x % 2 == 0]", "Shape: [expression for item in list if condition].", "[x for x in nums if ...]",
             fn="evens", args=[([1, 2, 3, 4],), ([],), ([5, 7],), ([0, -2, 3],)]),
        "most-frequent",
    ]),
    ("Return the right thing", [
        fix("<code>average</code> is wrong whenever the average isn't a whole number. Fix it.", """
            def average(nums):
                return sum(nums) // len(nums)
        """, """
            def average(nums):
                return sum(nums) / len(nums)
        """, "// rounds down to a whole number. / gives the true average.", "Which division keeps the decimal part?",
            fn="average", args=[([1, 2],), ([2, 4],), ([1, 2, 2],)]),
        "is-prime", "to-hex",
    ]),
])

level("m2", [
    ("What things cost", [
        mct("You loop over n items and check <code>if x in seen</code> each time. <code>seen</code> is a <strong>list</strong> that grows to n items. Overall time?",
            ["O(n)", "O(n log n)", "O(n²)", "O(1)"], 2,
            "x in list scans the list, so each check is O(n), and doing it n times gives O(n²). Make seen a set and each check is O(1), so the whole loop is O(n)."),
        mct("Which of these removes from the front of a queue in O(1)?",
            ["list.pop(0)", "deque.popleft()", "list.remove(x)", "sorted(q)[1:]"], 1,
            "list.pop(0) shifts every remaining element, so it's O(n). deque is built for both ends."),
    ]),
    ("collections", [
        mc("""
            from collections import Counter
            c = Counter("mississippi")
            print(c["s"], c["z"], c.most_common(1))
        """, ["4 Error", "4 0 [('s', 4)]", "4 None [('i', 4)]"],
           "A Counter returns 0 for missing keys instead of raising an error. On a tie, most_common keeps first-seen order, and 'i' appears before 's'."),
        fill("Group words by their first letter.", """
            from collections import defaultdict

            def index_by_first(words):
                groups = ___
                for w in words:
                    groups[w[0]].append(w)
                return dict(groups)
        """, "defaultdict(list)", "defaultdict(list) creates an empty list the first time a key is used.", "A dict whose missing keys start as empty lists.",
             fn="index_by_first", args=[(["ant", "bee", "ape"],), ([],), (["x"],)]),
        "group-length", "first-unique",
    ]),
    ("heapq, bisect, sorting", [
        mc("""
            import heapq
            h = [5, 1, 8, 3]
            heapq.heapify(h)
            heapq.heappush(h, 0)
            print(heapq.heappop(h), heapq.heappop(h), h[0])
        """, ["5 1 8", "0 1 8", "8 5 3"], "A min-heap always pops the smallest. After popping 0 and 1, the smallest left is 3."),
        fix("<code>mark_corner</code> should make a grid of zeros and set only the top-left cell to 1. Fix it.", """
            def mark_corner(rows, cols):
                grid = [[0] * cols] * rows
                grid[0][0] = 1
                return grid
        """, """
            def mark_corner(rows, cols):
                grid = [[0] * cols for _ in range(rows)]
                grid[0][0] = 1
                return grid
        """, "[[0] * cols] * rows repeats the same row object, so changing one row changes them all.",
            "Build each row separately with a comprehension.", fn="mark_corner", args=[(2, 2), (3, 1), (1, 3)]),
        "k-smallest", "count-less", "sort-people",
    ]),
])

level("m3", [
    ("Read the constraints", [
        mct("A problem says n ≤ 10⁵. Which complexity should you aim for?", ["O(n³)", "O(n²)", "O(n log n)", "O(2ⁿ)"], 2,
            "10⁵ squared is 10¹⁰, far too slow. O(n log n) is about 2 million operations."),
        mct("n ≤ 20 and you must consider every subset. What does that suggest?",
            ["Sorting", "Backtracking / O(2ⁿ) is fine", "Binary search", "It's impossible"], 1,
            "2²⁰ is about a million, which is fine. Tiny limits like this are a hint that an exponential solution is expected."),
        mct("n can be up to 10⁹. What do you need?", ["O(n)", "O(n log n)", "O(log n) or O(1)", "O(n²)"], 2,
            "Even a single loop over 10⁹ is too slow in Python. Think binary search or maths."),
    ]),
    ("Complexity of code", [
        mct("What's the time complexity?", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], 1,
            "The outer loop runs n times. The inner loop doubles j each time, so it runs about log n times per outer loop. n × log n.",
            code="""
                for i in range(n):
                    j = 1
                    while j < n:
                        j = j * 2
            """),
        mct("What's the time complexity?", ["O(n)", "O(n²)", "O(2ⁿ)", "O(log n)"], 2,
            "Each call makes two calls, so the calls double at each level: 2ⁿ. Memoising would make it O(n).",
            code="""
                def f(n):
                    if n <= 1:
                        return 1
                    return f(n - 1) + f(n - 1)
            """),
    ]),
    ("Spot the pattern", [
        mct("\"Longest substring with at most 2 distinct characters.\" Which pattern?",
            ["Sliding window", "Binary search", "Heap", "Backtracking"], 0,
            "Contiguous substring + longest + a condition you can update as you go = sliding window."),
        mct("\"Minimum ship capacity so all packages ship within D days.\" Which pattern?",
            ["Two pointers", "Binary search on the answer", "DFS", "Prefix sums"], 1,
            "If capacity C works, every bigger capacity works too. That False…True shape is binary search on the answer."),
        mct("\"Given prerequisites, find an order to take all courses.\" Which pattern?",
            ["Topological sort", "Sliding window", "Monotonic stack", "Kadane"], 0, "Dependencies + an ordering = topological sort."),
    ]),
])

level("m4", [
    ("Base case and trust", [
        mc("""
            def f(n):
                if n == 0:
                    return 0
                return n + f(n - 1)

            print(f(4))
        """, ["4", "0", "RecursionError"], "f(4) = 4 + f(3) = 4 + 3 + f(2) ... = 4 + 3 + 2 + 1 + 0."),
        mc("""
            def g(s):
                if s == "":
                    return ""
                return g(s[1:]) + s[0]

            print(g("abc"))
        """, ["abc", "a", "bca"], "g reverses: it puts the first character after the reverse of the rest."),
        fix("<code>count_down(n)</code> should return <code>[n, n-1, ..., 1]</code>. It crashes. Fix it.", """
            def count_down(n):
                return [n] + count_down(n - 1)
        """, """
            def count_down(n):
                if n == 0:
                    return []
                return [n] + count_down(n - 1)
        """, "No base case: it keeps calling itself with smaller and smaller n until Python gives up.",
            "What should count_down(0) return?", fn="count_down", args=[(3,), (0,), (1,)]),
        "sum-digits", "flatten",
    ]),
    ("Divide and memoise", [
        mc("""
            from functools import cache
            calls = 0

            @cache
            def fib(n):
                global calls
                calls += 1
                return n if n < 2 else fib(n - 1) + fib(n - 2)

            fib(10)
            print(calls)
        """, ["177", "10", "55"], "With @cache each fib(k) is computed once, for k = 0 to 10: 11 calls. Without it, fib(10) makes 177."),
        "fast-power", "bsearch-rec",
    ]),
])

# =================================================================== UNIT 2
level("p1", [
    ("Seen-so-far", [
        mc("""
            seen = {}
            for i, x in enumerate([4, 1, 4, 2]):
                if x in seen:
                    print("dup", x, "first at", seen[x])
                seen[x] = i
        """, ["dup 4 first at 2", "dup 4 first at 0\ndup 2 first at 3", "(nothing)"],
           "The dict remembers where each value was first stored. Only 4 repeats."),
        fix("This Two Sum returns <code>[0, 0]</code> for <code>[3, 2, 4]</code>, target 6. Fix it.", """
            def two_sum(nums, target):
                seen = {}
                for i, x in enumerate(nums):
                    seen[x] = i
                    if target - x in seen:
                        return [seen[target - x], i]
        """, """
            def two_sum(nums, target):
                seen = {}
                for i, x in enumerate(nums):
                    if target - x in seen:
                        return [seen[target - x], i]
                    seen[x] = i
        """, "Storing x before checking lets x pair with itself. Check first, then store.", "Swap the order of two lines.",
            fn="two_sum", args=[([3, 2, 4], 6), ([2, 7, 11, 15], 9), ([3, 3], 6)], cmp="sorted"),
        fill("Return True if any value appears twice.", """
            def contains_duplicate(nums):
                return ___
        """, "len(set(nums)) != len(nums)", "A set drops duplicates, so if it's smaller than the list, something repeated.", "Compare the list with a set of it.",
             fn="contains_duplicate", args=[([1, 2, 3, 1],), ([1, 2, 3],), ([],), ([7, 7],)]),
        "two-sum", "group-anagrams",
    ]),
    ("Prefix sums", [
        mc("""
            nums = [3, 1, 4, 1, 5]
            prefix = [0]
            for x in nums:
                prefix.append(prefix[-1] + x)
            print(prefix[4] - prefix[1])
        """, ["5", "9", "10"], "prefix[j] - prefix[i] is the sum of nums[i:j], here nums[1:4] = 1 + 4 + 1."),
        "subarray-sum", "longest-consec",
    ]),
])

level("p2", [
    ("Opposite ends", [
        mc("""
            a = [1, 2, 4, 7, 11]
            l, r = 0, len(a) - 1
            steps = 0
            while l < r:
                s = a[l] + a[r]
                steps += 1
                if s == 9:
                    break
                if s < 9:
                    l += 1
                else:
                    r -= 1
            print(a[l], a[r], steps)
        """, ["2 7 2", "4 7 3", "1 7 2"], "12 is too big (r moves left), 8 is too small (l moves right), then 2 + 7 = 9."),
        fix("<code>is_pal</code> crashes on most inputs. Fix it.", """
            def is_pal(s):
                l, r = 0, len(s)
                while l < r:
                    if s[l] != s[r]:
                        return False
                    l += 1
                    r -= 1
                return True
        """, """
            def is_pal(s):
                l, r = 0, len(s) - 1
                while l < r:
                    if s[l] != s[r]:
                        return False
                    l += 1
                    r -= 1
                return True
        """, "The last index is len(s) - 1. s[len(s)] is out of range.", "What's the index of the last character?",
            fn="is_pal", args=[("abba",), ("abc",), ("",), ("racecar",)]),
        "two-sum-sorted", "container",
    ]),
    ("In place", [
        fill("Reverse the list in place with two pointers.", """
            def reverse_in_place(a):
                l, r = 0, len(a) - 1
                while l < r:
                    ___
                    l += 1
                    r -= 1
                return a
        """, "a[l], a[r] = a[r], a[l]", "Tuple assignment swaps without a temporary variable.", "Swap a[l] and a[r] in one line.",
             fn="reverse_in_place", args=[([1, 2, 3],), ([],), ([1, 2],), ([5, 6, 7, 8],)]),
        "move-zeroes",
    ]),
    ("k-Sum", [
        mct("3Sum: you sort, then fix one number and two-pointer the rest. Overall time?", ["O(n)", "O(n log n)", "O(n²)", "O(n³)"], 2,
            "Sorting is O(n log n), then n fixed numbers × an O(n) two-pointer scan = O(n²), which dominates."),
        "three-sum",
    ]),
])

level("p3", [
    ("Fixed windows", [
        mc("""
            nums = [2, 1, 5, 1, 3, 2]
            k = 3
            window = sum(nums[:k])
            best = window
            for r in range(k, len(nums)):
                window += nums[r] - nums[r - k]
                best = max(best, window)
            print(best)
        """, ["8", "11", "6"], "The windows sum to 8, 7, 9, 6. Each step adds one number and drops one."),
        "max-window",
    ]),
    ("Variable windows", [
        fill("Complete the shrinking step.", """
            def longest_unique(s):
                window = set()
                l = best = 0
                for r, ch in enumerate(s):
                    while ch in window:
                        ___
                        l += 1
                    window.add(ch)
                    best = max(best, r - l + 1)
                return best
        """, "window.remove(s[l])", "Before moving l forward, take the character at l out of the window.", "What leaves the window when l moves?",
             fn="longest_unique", args=[("abcabcbb",), ("bbbbb",), ("",), ("abba",)]),
        fix("Shortest subarray with sum ≥ target. The lengths come out one too small. Fix it.", """
            def min_sub_array_len(target, nums):
                l = total = 0
                best = float("inf")
                for r, x in enumerate(nums):
                    total += x
                    while total >= target:
                        best = min(best, r - l)
                        total -= nums[l]
                        l += 1
                return 0 if best == float("inf") else best
        """, """
            def min_sub_array_len(target, nums):
                l = total = 0
                best = float("inf")
                for r, x in enumerate(nums):
                    total += x
                    while total >= target:
                        best = min(best, r - l + 1)
                        total -= nums[l]
                        l += 1
                return 0 if best == float("inf") else best
        """, "A window from l to r inclusive has r - l + 1 elements.", "How long is the window [2, 2]?",
            fn="min_sub_array_len", args=[(7, [2, 3, 1, 2, 4, 3]), (4, [1, 4, 4]), (11, [1, 1, 1, 1])]),
        mct("Why does a sliding window fail for \"count subarrays with sum k\" when numbers can be negative?",
            ["Windows can't have negative numbers in them", "Growing the window doesn't always increase the sum, so you can't tell which pointer to move",
             "It's too slow", "It works fine"], 1,
            "A window relies on 'bigger window = bigger sum'. Negatives break that, so use prefix sums + a hashmap."),
        "longest-substr", "char-replace",
    ]),
])

level("p4", [
    ("Stacks", [
        mc("""
            stack = []
            for ch in "ab#c##d":
                if ch == "#":
                    stack.pop()
                else:
                    stack.append(ch)
            print("".join(stack))
        """, ["ad", "acd", "Error"], "Each # deletes the last kept letter: a, b, # leaves [a]; c, #, # empties it; then d is pushed."),
        fix("<code>is_valid</code> crashes on <code>\")\"</code> and says <code>\"((\"</code> is valid. Fix both bugs.", """
            def is_valid(s):
                pairs = {")": "(", "]": "[", "}": "{"}
                stack = []
                for ch in s:
                    if ch in pairs:
                        if stack.pop() != pairs[ch]:
                            return False
                    else:
                        stack.append(ch)
                return True
        """, """
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
        """, "Check the stack isn't empty before popping, and at the end every opener must have been closed.",
            "Two places: before the pop, and the final return.", fn="is_valid", args=[("()",), (")",), ("((",), ("([])",), ("(]",)]),
        "valid-parens", "rpn",
    ]),
    ("Monotonic stack", [
        mc("""
            a = [2, 7, 3, 5, 4, 6, 8]
            ans = [-1] * len(a)
            stack = []
            for i, x in enumerate(a):
                while stack and a[stack[-1]] < x:
                    ans[stack.pop()] = x
                stack.append(i)
            print(ans)
        """, ["[7, 8, 5, 6, 6, 8, 8]", "[7, 3, 5, 4, 6, 8, -1]", "[-1, 2, 7, 3, 5, 4, 6]"],
           "Each index waits on the stack until a bigger value arrives; that value is its next greater element. 8 has none."),
        fill("Complete the line that records how many days until a warmer one.", """
            def daily_temperatures(temps):
                ans = [0] * len(temps)
                stack = []
                for i, t in enumerate(temps):
                    while stack and temps[stack[-1]] < t:
                        j = stack.pop()
                        ans[j] = ___
                    stack.append(i)
                return ans
        """, "i - j", "Day i is the first warmer day after day j, so the wait is i - j.", "Distance between two indexes.",
             fn="daily_temperatures", args=[([73, 74, 75, 71, 69, 72, 76, 73],), ([30, 60, 90],), ([50],)]),
        "daily-temps",
    ]),
])

level("p5", [
    ("Classic binary search", [
        mc("""
            a = list(range(0, 100, 3))
            lo, hi, steps = 0, len(a) - 1, 0
            while lo <= hi:
                steps += 1
                mid = (lo + hi) // 2
                if a[mid] == 42:
                    break
                if a[mid] < 42:
                    lo = mid + 1
                else:
                    hi = mid - 1
            print(a[mid], steps)
        """, ["42 4", "42 6", "42 14"], "34 items, found in 5 halvings. A linear scan would take 15 steps."),
        fix("<code>search</code> crashes when the target is bigger than everything. Fix it.", """
            def search(nums, target):
                lo, hi = 0, len(nums)
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if nums[mid] == target:
                        return mid
                    if nums[mid] < target:
                        lo = mid + 1
                    else:
                        hi = mid - 1
                return -1
        """, """
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
        """, "With lo <= hi the bounds are inclusive, so hi must start at the last valid index.", "What's the largest valid index?",
            fn="search", args=[([1, 3, 5], 5), ([1, 3, 5], 9), ([1, 3, 5], 0), ([], 1)]),
        "bsearch", "rotated-min",
    ]),
    ("Search on the answer", [
        mct("Binary search on the answer works when...",
            ["the input array is sorted", "if a value works, every larger value also works", "the answer is an integer", "n is small"], 1,
            "You need a yes/no test whose answers go False … False True … True. Then you search for the first True."),
        fill("Return the first index i with nums[i] >= x (or len(nums) if none).", """
            def first_at_least(nums, x):
                lo, hi = 0, len(nums)
                while lo < hi:
                    mid = (lo + hi) // 2
                    if nums[mid] >= x:
                        ___
                    else:
                        lo = mid + 1
                return lo
        """, "hi = mid", "mid might be the answer, so keep it in range: hi = mid (not mid - 1).", "Don't throw mid away.",
             fn="first_at_least", args=[([1, 3, 5, 7], 4), ([1, 3, 5, 7], 9), ([1, 3, 5, 7], 0), ([], 2), ([2, 2, 2], 2)]),
        "koko",
    ]),
])

# =================================================================== UNIT 3
level("p6", [
    ("Pointer surgery", [
        mc("""
            class Node:
                def __init__(self, val, next=None):
                    self.val, self.next = val, next

            head = Node(1, Node(2, Node(3)))
            head.next = head.next.next
            out = []
            cur = head
            while cur:
                out.append(cur.val)
                cur = cur.next
            print(out)
        """, ["[1, 2, 3]", "[2, 3]", "[3]"], "Pointing 1's next at 3 skips node 2. That's how you delete a node."),
        fix("<code>reverse_list</code> only returns the first node. Fix it.", """
            def reverse_list(head):
                prev, cur = None, head
                while cur:
                    cur.next = prev
                    prev = cur
                    cur = cur.next
                return prev
        """, """
            def reverse_list(head):
                prev, cur = None, head
                while cur:
                    nxt = cur.next
                    cur.next = prev
                    prev = cur
                    cur = nxt
                return prev
        """, "Once cur.next is overwritten, the rest of the list is lost. Save it first.", "Store cur.next in a variable before changing it.",
            fn="reverse_list", args=[([1, 2, 3],), ([],), ([1],)], prep=LL_OUT),
        "reverse-ll", "merge-ll",
    ]),
    ("Fast and slow", [
        fill("Complete the loop condition.", """
            def middle_node(head):
                slow = fast = head
                while ___:
                    slow = slow.next
                    fast = fast.next.next
                return slow
        """, "fast and fast.next", "fast jumps two nodes, so both fast and fast.next must exist.", "What would crash fast.next.next?",
             fn="middle_node", args=[([1, 2, 3, 4, 5],), ([1, 2, 3, 4],), ([1],)], prep=LL_OUT),
        "middle-ll", "cycle-ll", "remove-nth",
    ]),
])

level("p7", [
    ("DFS that returns", [
        mc("""
            class T:
                def __init__(self, v, l=None, r=None):
                    self.v, self.l, self.r = v, l, r

            root = T(1, T(2, T(4), T(5)), T(3))

            def pre(n):
                return [] if n is None else [n.v] + pre(n.l) + pre(n.r)

            def ino(n):
                return [] if n is None else ino(n.l) + [n.v] + ino(n.r)

            print(pre(root), ino(root))
        """, ["[4, 2, 5, 1, 3] [1, 2, 4, 5, 3]", "[1, 2, 3, 4, 5] [4, 5, 2, 3, 1]", "[1, 2, 4, 5, 3] [1, 2, 3, 4, 5]"],
           "Preorder visits the node first, then left, then right. Inorder visits left, then the node, then right."),
        fill("Count the nodes in the tree.", """
            def count_nodes(root):
                if not root:
                    return 0
                return ___
        """, "1 + count_nodes(root.left) + count_nodes(root.right)", "This node, plus everything on each side.", "1 + (left count) + (right count).",
             fn="count_nodes", args=[([1, 2, 3, 4],), ([],), ([1, None, 2, None, 3],)], prep=TREE_IN),
        fix("<code>min_depth</code> is wrong for trees where a node has only one child. Fix it.", """
            def min_depth(root):
                if not root:
                    return 0
                return 1 + min(min_depth(root.left), min_depth(root.right))
        """, """
            def min_depth(root):
                if not root:
                    return 0
                if not root.left:
                    return 1 + min_depth(root.right)
                if not root.right:
                    return 1 + min_depth(root.left)
                return 1 + min(min_depth(root.left), min_depth(root.right))
        """, "A missing child isn't a leaf. Depth counts down to a real leaf, so skip the empty side.",
            "What should happen when only one child exists?", fn="min_depth",
            args=[([3, 9, 20, None, None, 15, 7],), ([2, None, 3, None, 4],), ([],), ([1],)], prep=TREE_IN),
        "max-depth", "invert-tree", "diameter",
    ]),
    ("BFS and BSTs", [
        mct("What does an inorder traversal of a binary search tree give you?",
            ["The values in sorted order", "The root first", "Level by level", "Leaves only"], 0,
            "Left subtree (smaller), node, right subtree (bigger), recursively: ascending order."),
        "level-order", "valid-bst",
    ]),
])

level("p8", [
    ("Heap basics", [
        mc("""
            import heapq
            h = []
            for x in [5, 2, 9, 1, 7]:
                heapq.heappush(h, x)
                if len(h) > 3:
                    heapq.heappop(h)
            print(sorted(h), h[0])
        """, ["[1, 2, 5] 1", "[5, 7, 9] 9", "[7, 9] 7"], "Popping the smallest whenever size > 3 leaves the 3 largest. h[0] is the smallest of those."),
        mc("""
            import heapq
            h = [-x for x in [3, 8, 1]]
            heapq.heapify(h)
            print(-heapq.heappop(h))
        """, ["1", "-8", "3"], "Negate to fake a max-heap: the smallest negative is the largest original."),
        "last-stone", "kth-largest",
    ]),
    ("Top k", [
        fix("<code>find_kth_largest</code> returns the wrong element. Fix it.", """
            import heapq

            def find_kth_largest(nums, k):
                heap = []
                for x in nums:
                    heapq.heappush(heap, x)
                    if len(heap) > k:
                        heapq.heappop(heap)
                return heap[-1]
        """, """
            import heapq

            def find_kth_largest(nums, k):
                heap = []
                for x in nums:
                    heapq.heappush(heap, x)
                    if len(heap) > k:
                        heapq.heappop(heap)
                return heap[0]
        """, "Only heap[0] is guaranteed (the smallest). The last element of a heap isn't the largest or anything in particular.",
            "Which index of a heap means something?", fn="find_kth_largest", args=[([3, 2, 1, 5, 6, 4], 2), ([1], 1), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)]),
        "top-k-freq", "k-closest",
    ]),
])

# =================================================================== UNIT 4
level("p9", [
    ("Choose, explore, un-choose", [
        mc("""
            res = []
            def bt(path):
                if len(path) == 2:
                    res.append(path[:])
                    return
                for x in [1, 2, 3]:
                    if x not in path:
                        path.append(x)
                        bt(path)
                        path.pop()
            bt([])
            print(len(res), res[0], res[-1])
        """, ["9 [1, 1] [3, 3]", "3 [1, 2] [2, 3]", "6 [1, 2] [2, 3]"],
           "Ordered pairs of different numbers from 3: 3 × 2 = 6, generated in order from [1, 2] to [3, 2]."),
        fix("<code>subsets</code> returns a list of empty lists. Fix it.", """
            def subsets(nums):
                res, path = [], []
                def bt(i):
                    if i == len(nums):
                        res.append(path)
                        return
                    path.append(nums[i])
                    bt(i + 1)
                    path.pop()
                    bt(i + 1)
                bt(0)
                return res
        """, """
            def subsets(nums):
                res, path = [], []
                def bt(i):
                    if i == len(nums):
                        res.append(path[:])
                        return
                    path.append(nums[i])
                    bt(i + 1)
                    path.pop()
                    bt(i + 1)
                bt(0)
                return res
        """, "res kept getting the same list object, which ends up empty after all the pops. Append a copy.",
            "path[:]", fn="subsets", args=[([1, 2],), ([],), ([1, 2, 3],)], cmp="sorted_inner"),
        "subsets", "permutations",
    ]),
    ("Controlling the choices", [
        fill("Combination Sum: numbers may be reused. Fill in the recursive call's start index.", """
            def combination_sum(candidates, target):
                res, path = [], []
                def backtrack(start, remaining):
                    if remaining == 0:
                        res.append(path[:])
                        return
                    for i in range(start, len(candidates)):
                        c = candidates[i]
                        if c <= remaining:
                            path.append(c)
                            backtrack(___, remaining - c)
                            path.pop()
                backtrack(0, target)
                return res
        """, "i", "Passing i (not i + 1) allows the same number again; never going below i avoids duplicate orderings.",
             "Reuse allowed, but no going backwards.", fn="combination_sum", args=[([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([2], 1)], cmp="sorted_inner"),
        "combo-sum", "word-search",
    ]),
])

level("p10", [
    ("Grids", [
        fix("<code>max_area</code> should return the biggest island's size. It crashes with RecursionError. Fix it.", """
            def max_area(grid):
                rows, cols = len(grid), len(grid[0])
                def dfs(r, c):
                    if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
                        return 0
                    return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
                return max(dfs(r, c) for r in range(rows) for c in range(cols))
        """, """
            def max_area(grid):
                rows, cols = len(grid), len(grid[0])
                def dfs(r, c):
                    if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
                        return 0
                    grid[r][c] = 0
                    return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
                return max(dfs(r, c) for r in range(rows) for c in range(cols))
        """, "Without marking cells as visited, two neighbours keep calling each other forever.",
            "Mark the cell before recursing.", fn="max_area", args=[([[1, 1], [0, 1]],), ([[0]],), ([[1, 0], [0, 1]],), ([[1, 1, 0], [0, 0, 0], [0, 1, 1]],)]),
        "islands", "flood-fill", "rotting",
    ]),
    ("Graphs and ordering", [
        mc("""
            from collections import deque
            graph = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}
            dist = {0: 0}
            q = deque([0])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
            print(dist[4], len(dist))
        """, ["4 5", "3 4", "2 5"], "BFS finds the fewest edges: 0 → 1 → 3 → 4 is 3 steps, and all 5 nodes are reached."),
        mct("In Kahn's algorithm, what tells you the prerequisites contain a cycle?",
            ["The queue is empty at the start", "Fewer than n courses ever reach indegree 0 and get processed", "A node has two parents", "It never terminates"], 1,
            "Courses in a cycle wait on each other, so their indegree never hits 0 and they're never processed."),
        fill("Complete path compression in union-find.", """
            def count_components(n, edges):
                parent = list(range(n))
                def find(x):
                    while parent[x] != x:
                        parent[x] = ___
                        x = parent[x]
                    return x
                comps = n
                for a, b in edges:
                    ra, rb = find(a), find(b)
                    if ra != rb:
                        parent[ra] = rb
                        comps -= 1
                return comps
        """, "parent[parent[x]]", "Point x at its grandparent, halving the path each time.", "Skip one level up.",
             fn="count_components", args=[(5, [[0, 1], [1, 2], [3, 4]]), (3, []), (4, [[0, 1], [2, 3], [1, 2]]), (3, [[0, 1], [1, 2], [0, 2]])]),
        "course-schedule", "components",
    ]),
])

level("p11", [
    ("1D DP", [
        mc("""
            dp = [0] * 6
            dp[0], dp[1] = 1, 1
            for i in range(2, 6):
                dp[i] = dp[i - 1] + dp[i - 2]
            print(dp)
        """, ["[0, 1, 1, 2, 3, 5]", "[1, 1, 2, 3, 5, 8, 13]", "[1, 2, 3, 5, 8, 13]"],
           "Each cell is built from the two before it. That's Climbing Stairs."),
        fill("House Robber with two variables. Complete the update.", """
            def rob(nums):
                prev, cur = 0, 0
                for x in nums:
                    prev, cur = cur, ___
                return cur
        """, "max(cur, prev + x)", "Either skip this house (cur) or rob it and add the best from two back (prev + x).", "max of skip vs take.",
             fn="rob", args=[([1, 2, 3, 1],), ([2, 7, 9, 3, 1],), ([],), ([2, 1, 1, 2],)]),
        "climb", "house-robber",
    ]),
    ("Choices that repeat", [
        fix("This greedy coin change takes the biggest coin first. It's wrong for coins [1, 3, 4] and amount 6. Rewrite it as DP.", """
            def coin_change(coins, amount):
                count = 0
                for c in sorted(coins, reverse=True):
                    count += amount // c
                    amount %= c
                return count if amount == 0 else -1
        """, """
            def coin_change(coins, amount):
                INF = float("inf")
                dp = [0] + [INF] * amount
                for a in range(1, amount + 1):
                    for c in coins:
                        if c <= a:
                            dp[a] = min(dp[a], dp[a - c] + 1)
                return dp[amount] if dp[amount] != INF else -1
        """, "Greedy picks 4 + 1 + 1 (3 coins) but 3 + 3 is 2. dp[a] = min over coins of dp[a - c] + 1 checks every option.",
            "dp[a] = fewest coins for amount a.", fn="coin_change", args=[([1, 2, 5], 11), ([1, 3, 4], 6), ([2], 3), ([1], 0)]),
        "coin-change", "word-break", "lis",
    ]),
    ("2D DP", [
        mc("""
            row = [1, 1, 1]
            for _ in range(2):
                for c in range(1, 3):
                    row[c] += row[c - 1]
            print(row)
        """, ["[1, 2, 3]", "[1, 3, 4]", "[3, 3, 3]"],
           "This is Unique Paths on a 3×3 grid, keeping one row: each cell = from above (itself) + from the left."),
        mct("In a two-string DP like LCS, what does dp[i][j] usually mean?",
            ["The answer for the first i chars of one string and the first j of the other", "Whether char i equals char j",
             "The number of times i appears in j", "The distance between positions i and j"], 0,
            "Prefixes. Then the recurrence looks at the last characters of those prefixes."),
        "unique-paths", "lcs",
    ]),
])

level("p12", [
    ("Intervals", [
        mc("""
            intervals = [[6, 8], [1, 4], [7, 9], [2, 3]]
            intervals.sort()
            res = []
            for s, e in intervals:
                if res and s <= res[-1][1]:
                    res[-1][1] = max(res[-1][1], e)
                else:
                    res.append([s, e])
            print(res)
        """, ["[[1, 3], [6, 9]]", "[[1, 4], [2, 3], [6, 9]]", "[[1, 9]]"],
           "After sorting by start, [2, 3] sits inside [1, 4], and [7, 9] overlaps [6, 8]."),
        fix("Merging <code>[[1, 4], [2, 3]]</code> gives <code>[[1, 3]]</code>. Fix it.", """
            def merge(intervals):
                intervals.sort()
                res = []
                for s, e in intervals:
                    if res and s <= res[-1][1]:
                        res[-1][1] = e
                    else:
                        res.append([s, e])
                return res
        """, """
            def merge(intervals):
                intervals.sort()
                res = []
                for s, e in intervals:
                    if res and s <= res[-1][1]:
                        res[-1][1] = max(res[-1][1], e)
                    else:
                        res.append([s, e])
                return res
        """, "An interval fully inside the previous one must not shrink it. Keep the larger end.", "max(...)",
            fn="merge", args=[([[1, 4], [2, 3]],), ([[1, 3], [2, 6], [8, 10]],), ([[1, 4], [4, 5]],)]),
        mct("To keep the maximum number of non-overlapping intervals, sort them by...", ["start", "end", "length", "it doesn't matter"], 1,
            "Always keep the one that finishes earliest; it leaves the most room for everything after it."),
        "merge-intervals", "non-overlap",
    ]),
    ("Greedy runs", [
        fill("Kadane: complete the update for the best run ending here.", """
            def max_sub_array(nums):
                best = cur = nums[0]
                for x in nums[1:]:
                    cur = ___
                    best = max(best, cur)
                return best
        """, "max(x, cur + x)", "Extend the current run, or start fresh at x if the run so far is dragging you down.", "Extend or restart.",
             fn="max_sub_array", args=[([-2, 1, -3, 4, -1, 2, 1, -5, 4],), ([1],), ([-3, -1, -2],), ([5, 4, -1, 7, 8],)]),
        "kadane", "jump-game",
    ]),
])

# =================================================================== UNIT 5
level("x1", [
    ("The practice loop", [
        mct("You've been stuck on a Medium for 35 minutes. Best move?",
            ["Keep going until you get it, however long", "Read only the approach of a good solution, then write the code yourself",
             "Copy a solution and submit it", "Skip it forever"], 1,
            "Past the time limit you learn more by seeing the idea and doing the work yourself. Then re-solve it later."),
        mct("When should you re-solve a problem from scratch?",
            ["Never, once is enough", "Right away, 5 times in a row", "After about 3 days, then again after about 2 weeks", "Only before the interview"], 2,
            "Spaced repetition: recalling it after a gap is what makes it stick."),
        mct("In a mock interview, what should you say right after clarifying the problem?",
            ["The optimal solution's code", "The brute force and its complexity", "Nothing, start typing", "Which pattern it is from memory"], 1,
            "It shows you can solve it at all, and gives you something to optimise from."),
    ]),
    ("Beyond the core", [
        mc("print(5 ^ 3 ^ 5)", ["5", "7", "0"], "XOR cancels pairs: 5 ^ 5 = 0, leaving 3. That's the trick behind Single Number."),
        mc("print(12 & 11, bin(12), bin(12 & 11))", ["11 0b1100 0b1011", "4 0b1100 0b100", "0 0b1100 0b0"],
           "n & (n - 1) clears the lowest set bit: 1100 becomes 1000."),
    ]),
])

# =================================================================== BOSSES
BOSSES = {
    "b0": {"unit": "u0", "title": "The Gatekeeper", "blurb": "Everything from Unit 0 at once: loops, decisions, strings and functions.", "challenges": [
        boss("Count, sum and max", None,
             "Read whole numbers, one per line, until a line is <code>0</code>. Print three lines: how many numbers came before the 0, their sum, and the largest. If the very first line is 0, print <code>0</code>, <code>0</code> and <code>none</code>.",
             "# read until 0\n", """
                count = 0
                total = 0
                largest = None
                n = int(input())
                while n != 0:
                    count += 1
                    total += n
                    if largest is None or n > largest:
                        largest = n
                    n = int(input())
                print(count)
                print(total)
                print(largest if largest is not None else "none")
             """, None, "Read before the loop, read again at the end of the body. Track largest starting from None.",
             stdins=["4\n9\n2\n0\n", "0\n", "-3\n-1\n0\n", "7\n0\n5\n0\n", "5\n5\n5\n0\n"]),
        boss("Digital root", "digital_root",
             "Write <code>digital_root(n)</code>: keep adding up the digits of n until a single digit is left, and return it. 38 → 3 + 8 = 11 → 1 + 1 = 2.",
             "def digital_root(n):\n    pass\n", """
                def digital_root(n):
                    while n >= 10:
                        s = 0
                        while n > 0:
                            s += n % 10
                            n //= 10
                        n = s
                    return n
             """, [(38,), (0,), (9,), (99999,), (123456789,), (10,)], "A loop inside a loop: the inner one sums digits, the outer repeats until n < 10."),
        boss("Longest word", "longest_word",
             "Write <code>longest_word(sentence)</code> that returns the longest word (the first one if there's a tie), or <code>\"\"</code> if there are no words.",
             "def longest_word(sentence):\n    pass\n", """
                def longest_word(sentence):
                    best = ""
                    for w in sentence.split():
                        if len(w) > len(best):
                            best = w
                    return best
             """, [("the quick brown fox",), ("",), ("a bb cc",), ("   spaces   everywhere  ",), ("one",)],
             "Start with best = \"\". Only replace it when a word is strictly longer, which keeps the first on a tie."),
    ]},
    "b1": {"unit": "u1", "title": "The Refactorer", "blurb": "Interview Python, recursion and the toolkit, with no hand-holding.", "challenges": [
        boss("Run-length encoding", "compress",
             "Write <code>compress(s)</code>: replace each run of a repeated character with the character and the run length. <code>\"aaabccdddd\"</code> → <code>\"a3b1c2d4\"</code>.",
             "def compress(s):\n    pass\n", """
                def compress(s):
                    out = []
                    i = 0
                    while i < len(s):
                        j = i
                        while j < len(s) and s[j] == s[i]:
                            j += 1
                        out.append(s[i] + str(j - i))
                        i = j
                    return "".join(out)
             """, [("aaabccdddd",), ("",), ("z",), ("abc",), ("aaaaaaaaaaaa",), ("aabbaa",)],
             "Two pointers again: i marks the start of a run, j walks to its end. Collect pieces in a list and join."),
        boss("Binary strings", "binary_strings",
             "Write <code>binary_strings(n)</code> that returns every string of length n made of 0s and 1s, in sorted order. Use recursion.",
             "def binary_strings(n):\n    pass\n", """
                def binary_strings(n):
                    if n == 0:
                        return [""]
                    shorter = binary_strings(n - 1)
                    return ["0" + s for s in shorter] + ["1" + s for s in shorter]
             """, [(2,), (0,), (1,), (3,), (4,)],
             "binary_strings(0) is [\"\"]. Every longer string is \"0\" or \"1\" in front of a shorter one."),
        boss("Top words", "top_words",
             "Write <code>top_words(text, k)</code>: return the k most frequent words (lowercased), most frequent first; ties go alphabetically.",
             "def top_words(text, k):\n    pass\n", """
                from collections import Counter

                def top_words(text, k):
                    counts = Counter(text.lower().split())
                    ranked = sorted(counts.items(), key=lambda p: (-p[1], p[0]))
                    return [w for w, _ in ranked[:k]]
             """, [("the cat and the hat", 2), ("b a c", 3), ("Go go GO stop", 1), ("x y x y z", 2), ("", 3)],
             "Counter for the counts, then one sorted() with key (-count, word)."),
    ]},
    "b2": {"unit": "u2", "title": "The Pattern Warden", "blurb": "Hashing, two pointers, sliding windows, stacks and binary search. Pick the right one.", "challenges": [
        boss("k-diff pairs", "find_pairs",
             "Return how many <strong>unique</strong> pairs of values (a, b) in <code>nums</code> have b - a = k, for k ≥ 0. With k = 0, a value must appear at least twice.",
             "def find_pairs(nums, k):\n    pass\n", """
                from collections import Counter

                def find_pairs(nums, k):
                    counts = Counter(nums)
                    if k == 0:
                        return sum(1 for v in counts.values() if v > 1)
                    return sum(1 for x in counts if x + k in counts)
             """, [([3, 1, 4, 1, 5], 2), ([1, 2, 3, 4, 5], 1), ([1, 3, 1, 5, 4], 0), ([1, 1, 1], 0), ([], 3), ([1, 2, 4, 4, 3, 3, 0, 9, 2, 3], 3)],
             "Count the values. For k > 0, check x + k for each distinct x. k = 0 is its own case."),
        boss("Longest window under a budget", "longest_at_most",
             "<code>nums</code> are all ≥ 0. Return the length of the longest contiguous subarray whose sum is at most <code>k</code>.",
             "def longest_at_most(nums, k):\n    pass\n", """
                def longest_at_most(nums, k):
                    l = total = best = 0
                    for r, x in enumerate(nums):
                        total += x
                        while total > k:
                            total -= nums[l]
                            l += 1
                        best = max(best, r - l + 1)
                    return best
             """, [([1, 2, 1, 0, 1, 1, 0], 4), ([5, 5, 5], 4), ([], 3), ([0, 0, 0], 0), ([3, 1, 2, 1], 3), ([2, 2, 2, 2], 100)],
             "Non-negative numbers: a sliding window works. Shrink while the sum is over k."),
        boss("Search a rotated array", "search_rotated",
             "A sorted array of unique numbers was rotated. Return the index of <code>target</code> or -1, in O(log n).",
             "def search_rotated(nums, target):\n    pass\n", """
                def search_rotated(nums, target):
                    lo, hi = 0, len(nums) - 1
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        if nums[mid] == target:
                            return mid
                        if nums[lo] <= nums[mid]:
                            if nums[lo] <= target < nums[mid]:
                                hi = mid - 1
                            else:
                                lo = mid + 1
                        else:
                            if nums[mid] < target <= nums[hi]:
                                lo = mid + 1
                            else:
                                hi = mid - 1
                    return -1
             """, [([4, 5, 6, 7, 0, 1, 2], 0), ([4, 5, 6, 7, 0, 1, 2], 3), ([1], 0), ([1], 1), ([5, 1, 3], 5), ([3, 1], 1), ([6, 7, 1, 2, 3, 4, 5], 7)],
             "One half around mid is always sorted. Check whether the target lies inside that sorted half."),
    ]},
    "b3": {"unit": "u3", "title": "The Linker", "blurb": "Linked lists, trees and heaps, with hidden tests.", "challenges": [
        boss("Palindrome linked list", "is_palindrome_ll",
             "Return whether the linked list reads the same both ways. (Bonus: O(1) extra space by reversing the second half.)",
             "def is_palindrome_ll(head):\n    pass\n", """
                def is_palindrome_ll(head):
                    slow = fast = head
                    while fast and fast.next:
                        slow = slow.next
                        fast = fast.next.next
                    prev = None
                    while slow:
                        slow.next, prev, slow = prev, slow, slow.next
                    left, right = head, prev
                    while right:
                        if left.val != right.val:
                            return False
                        left, right = left.next, right.next
                    return True
             """, [([1, 2, 2, 1],), ([1, 2],), ([],), ([1],), ([1, 2, 3, 2, 1],), ([1, 2, 3, 1],)],
             "Find the middle with fast and slow, reverse from there, then walk both halves.", prep=LL_IN),
        boss("Symmetric tree", "is_symmetric",
             "Return whether the binary tree is a mirror of itself.",
             "def is_symmetric(root):\n    pass\n", """
                def is_symmetric(root):
                    def mirror(a, b):
                        if not a and not b:
                            return True
                        if not a or not b or a.val != b.val:
                            return False
                        return mirror(a.left, b.right) and mirror(a.right, b.left)
                    return mirror(root, root)
             """, [([1, 2, 2, 3, 4, 4, 3],), ([1, 2, 2, None, 3, None, 3],), ([],), ([1],), ([1, 2, 2, 2, None, 2],)],
             "Compare two trees at once: left of one against right of the other.", prep=TREE_IN),
        boss("Merge k sorted lists", "merge_k_sorted",
             "<code>lists</code> is a list of sorted Python lists. Return one sorted list with everything, using a heap (don't just sort it all).",
             "import heapq\n\ndef merge_k_sorted(lists):\n    pass\n", """
                import heapq

                def merge_k_sorted(lists):
                    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
                    heapq.heapify(heap)
                    out = []
                    while heap:
                        val, i, j = heapq.heappop(heap)
                        out.append(val)
                        if j + 1 < len(lists[i]):
                            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
                    return out
             """, [([[1, 4, 5], [1, 3, 4], [2, 6]],), ([],), ([[]],), ([[2], [1]],), ([[1, 1], [1], [0, 5]],)],
             "Heap of (value, which list, index in it). Pop the smallest, push the next one from the same list."),
    ]},
    "b4": {"unit": "u4", "title": "The Grand Search", "blurb": "Backtracking, graphs, DP and greedy: the hard end of the patterns.", "challenges": [
        boss("Phone keypad", "letter_combinations",
             "Return every letter combination the digits 2–9 could spell on a phone keypad (2 = abc, ..., 9 = wxyz), in any order. Empty input gives an empty list.",
             "def letter_combinations(digits):\n    pass\n", """
                def letter_combinations(digits):
                    if not digits:
                        return []
                    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
                    res = []
                    def bt(i, path):
                        if i == len(digits):
                            res.append(path)
                            return
                        for ch in keys[digits[i]]:
                            bt(i + 1, path + ch)
                    bt(0, "")
                    return res
             """, [("23",), ("",), ("2",), ("79",), ("234",)], "Backtrack over positions; each digit offers 3 or 4 choices.", cmp="sorted"),
        boss("Biggest island", "max_area_of_island",
             "Return the area of the largest island of 1s (connected up/down/left/right), or 0.",
             "def max_area_of_island(grid):\n    pass\n", """
                def max_area_of_island(grid):
                    rows, cols = len(grid), len(grid[0])
                    def dfs(r, c):
                        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != 1:
                            return 0
                        grid[r][c] = 0
                        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
                    return max(dfs(r, c) for r in range(rows) for c in range(cols))
             """, [([[0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 1, 1]],), ([[0, 0, 0]],), ([[1]],), ([[1, 0, 1], [0, 1, 0], [1, 0, 1]],), ([[1, 1], [1, 1]],)],
             "Flood fill each island, counting cells as you sink them."),
        boss("Minimum path sum", "min_path_sum",
             "Move only right or down from the top-left to the bottom-right of a grid of non-negative numbers. Return the smallest possible sum of the cells you pass through.",
             "def min_path_sum(grid):\n    pass\n", """
                def min_path_sum(grid):
                    rows, cols = len(grid), len(grid[0])
                    dp = [[0] * cols for _ in range(rows)]
                    for r in range(rows):
                        for c in range(cols):
                            if r == 0 and c == 0:
                                dp[r][c] = grid[0][0]
                            elif r == 0:
                                dp[r][c] = dp[r][c - 1] + grid[r][c]
                            elif c == 0:
                                dp[r][c] = dp[r - 1][c] + grid[r][c]
                            else:
                                dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]
                    return dp[-1][-1]
             """, [([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), ([[1, 2, 3], [4, 5, 6]],), ([[7]],), ([[1, 9, 9], [1, 1, 9], [9, 1, 1]],)],
             "dp[r][c] = grid[r][c] + min(from above, from the left). The first row and column have only one way in."),
    ]},
    "b5": {"unit": "u5", "title": "LeetCode Ready", "blurb": "The final exam: three real Mediums, hidden tests, three hearts.", "challenges": [
        boss("Product except self", "product_except_self",
             "Return a list where each position holds the product of every <em>other</em> number. No division, O(n).",
             "def product_except_self(nums):\n    pass\n", """
                def product_except_self(nums):
                    n = len(nums)
                    out = [1] * n
                    left = 1
                    for i in range(n):
                        out[i] = left
                        left *= nums[i]
                    right = 1
                    for i in range(n - 1, -1, -1):
                        out[i] *= right
                        right *= nums[i]
                    return out
             """, [([1, 2, 3, 4],), ([-1, 1, 0, -3, 3],), ([2, 3],), ([0, 0],), ([5, 1, 1, 1],)],
             "Two passes: products of everything to the left, then multiply in everything to the right."),
        boss("Decode ways", "num_decodings",
             "Letters map to numbers (A = 1 ... Z = 26). Return how many ways the digit string can be decoded. \"226\" → 3 (BZ, VF, BBF).",
             "def num_decodings(s):\n    pass\n", """
                def num_decodings(s):
                    if not s:
                        return 0
                    prev, cur = 1, 1 if s[0] != "0" else 0
                    for i in range(1, len(s)):
                        nxt = 0
                        if s[i] != "0":
                            nxt += cur
                        if 10 <= int(s[i - 1:i + 1]) <= 26:
                            nxt += prev
                        prev, cur = cur, nxt
                    return cur
             """, [("12",), ("226",), ("06",), ("0",), ("10",), ("11106",), ("2611055971756562",)],
             "Like Climbing Stairs: take one digit (if it isn't 0) or two (if they form 10–26)."),
        boss("Longest palindromic substring", "longest_palindrome_len",
             "Return the <strong>length</strong> of the longest palindromic substring.",
             "def longest_palindrome_len(s):\n    pass\n", """
                def longest_palindrome_len(s):
                    best = 0
                    for center in range(len(s)):
                        for l, r in ((center, center), (center, center + 1)):
                            while l >= 0 and r < len(s) and s[l] == s[r]:
                                l -= 1
                                r += 1
                            best = max(best, r - l - 1)
                    return best
             """, [("babad",), ("cbbd",), ("",), ("a",), ("forgeeksskeegfor",), ("abcde",)],
             "Expand around every centre (one character, or the gap between two). O(n²) is fine."),
    ]},
}
