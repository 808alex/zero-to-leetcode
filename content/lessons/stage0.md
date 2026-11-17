=== z1
A year away means the syntax has gone fuzzy, and your brain isn't in "think in steps" mode yet. That's normal, and it comes back faster than learning it the first time. This unit assumes nothing. Read slowly, and type the examples yourself rather than copy-pasting. The questions are small on purpose: the point is reps.

The coding questions in Unit 0 work like classic beginner programs: read with `input()`, print the answer, and the tests feed in the input and check what you printed.

## Variables

A variable is a name pointing at a value. `=` means "make this name point at this value", not "equals".

```python
age = 19
name = "Alex"
height = 1.82
is_student = True
age = age + 1      # read age (19), add 1, point age at 20
```

The four basic types: `int` (whole numbers), `float` (decimals), `str` (text, in quotes), `bool` (`True` / `False`). `type(x)` tells you which one you have.

## Printing

```python
print("hello")
print("age:", age)            # commas add a space between items
print(f"{name} is {age}")     # f-string: anything in {} gets filled in
print(f"{3.14159:.2f}")       # 3.14  (2 decimal places)
```

## Reading input

`input()` waits for a line of text and gives it back **as a string**, always. If you want a number, convert it:

```python
n = int(input())       # whole number
x = float(input())     # decimal
word = input()         # leave text as text
```

Forgetting `int()` is the most common Unit 0 bug: `"3" + "4"` is `"34"`.

## Arithmetic

```python
7 + 2    # 9
7 - 2    # 5
7 * 2    # 14
7 / 2    # 3.5   always gives a float
7 // 2   # 3     whole-number division (rounds down)
7 % 2    # 1     remainder
7 ** 2   # 49    power
```

`//` and `%` come up constantly: `n % 10` is the last digit of n, `n // 10` removes it, and `n % 2 == 0` checks for even.

```python
x = 10
x = x * 2
x = x // 3
print(x, x % 4)
```

<details class="predict"><summary>Predict it: what does this print? Decide, then click.</summary>
<p><code>6 2</code>. x goes 10 → 20 → 6 (20 // 3 is 6), and 6 % 4 is 2.</p>
</details>

=== z2
Programs make decisions with `if`. Python uses **indentation** (4 spaces) to show what's inside the `if`. There are no braces like in Java or C.

## if / elif / else

```python
mark = int(input())

if mark >= 70:
    print("A")
elif mark >= 55:        # only checked if the line above was False
    print("B")
else:                   # runs if nothing above matched
    print("F")
print("done")           # not indented: always runs
```

Python checks top to bottom and runs **only the first** branch that's True. That's why order matters.

## Comparisons and combining them

```python
a == b    # equal (one = assigns, two == compares)
a != b    # not equal
a < b, a <= b, a > b, a >= b

if age >= 18 and age < 65:
if day == 6 or day == 7:
if not finished:
if 18 <= age < 65:      # Python allows chained comparisons
```

## Common mistakes

- Forgetting the colon at the end of `if ...:` (SyntaxError).
- Using `=` instead of `==` in a condition.
- Writing separate `if`s when you meant `elif`. Several `if`s can **all** run; `elif` stops at the first match.
- Wrong boundary: is 70 an A or a B? Decide whether you need `>` or `>=`.

```python
n = 15
if n % 3 == 0:
    print("fizz")
if n % 5 == 0:
    print("buzz")
elif n % 3 == 0:
    print("three")
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>fizz</code> then <code>buzz</code>. The first <code>if</code> is separate, so it runs. The second <code>if</code> is also True, so its <code>elif</code> is skipped.</p>
</details>

=== z3
While loops are where rusty brains stall, so this level goes slowly.

## The shape of every while loop

A while loop needs three things. Get used to looking for all three:

```python
i = 1               # 1. START: set up the variable before the loop
while i <= 5:       # 2. CONDITION: keep going while this is True
    print(i)
    i = i + 1       # 3. STEP: change the variable so the condition eventually fails
print("after")
```

Python checks the condition, runs the indented body, goes back up, checks again. When the condition is False it skips to the first line after the loop.

## Trace it by hand

When a loop confuses you, make a table: one row per time round the loop. This is the single best habit for getting back into "programming mode".

```python
total = 0
i = 1
while i <= 4:
    total = total + i
    i = i + 1
print(total)
```

| check `i <= 4` | `total` after | `i` after |
|---|---|---|
| 1 ≤ 4 yes | 1 | 2 |
| 2 ≤ 4 yes | 3 | 3 |
| 3 ≤ 4 yes | 6 | 4 |
| 4 ≤ 4 yes | 10 | 5 |
| 5 ≤ 4 **no**, stop | | |

Prints `10`.

## The three ways a while loop goes wrong

1. **No step** (forgot `i = i + 1`): the condition never changes, and the loop runs forever. In this app it gets stopped after 10 seconds.
2. **Off by one**: `<` vs `<=`, or starting at 0 vs 1. Trace the first and last time round to check.
3. **Step in the wrong place**: `i = i + 1` indented under an `if` only runs sometimes.

## Loops that run "until something happens"

Not every loop counts. Sometimes you don't know how many times it'll go round:

```python
line = input()           # read the first one before the loop
while line != "end":
    print("got", line)
    line = input()       # read the next one as the LAST step
```

Now trace this one in your head before you click:

```python
n = 1
while n < 100:
    n = n * 3
print(n)
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>243</code>. n goes 1 → 3 → 9 → 27 → 81 → 243. The check happens before each round, so 81 &lt; 100 lets it go round once more.</p>
</details>

## break

`break` jumps out of the loop immediately. Setting `i = len(s)` to force a loop to end works, but `break` is the proper way.

```python
while True:          # loop "forever"...
    word = input()
    if word == "stop":
        break        # ...until this
    print(word)
```

=== z4
A `for` loop goes through things one at a time. Use it when you know what you're looping over: a range of numbers, the characters of a string, the items of a list. Python handles the start, the condition and the step for you, so you can't forget the step.

## for with range

```python
for i in range(5):          # 0, 1, 2, 3, 4   (5 numbers, stops BEFORE 5)
for i in range(1, 6):       # 1, 2, 3, 4, 5
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8   (third number is the step)
for i in range(5, 0, -1):   # 5, 4, 3, 2, 1   (counting down)
```

The stop number is never included. To go up to n, write `range(1, n + 1)`.

These two do exactly the same thing:

```python
i = 1
while i <= 5:
    print(i)
    i = i + 1

for i in range(1, 6):
    print(i)
```

## for over a string or a list

```python
for ch in "hey":
    print(ch)           # h, e, y on separate lines

for name in ["ann", "bob"]:
    print("hi", name)
```

When you need the position too, loop over `range(len(s))` and use `s[i]`. (In Unit 1 you'll learn `enumerate`, which is neater.)

## while or for?

- Know how many times, or looping over something? **for**.
- Looping until a condition changes (until "end", until n is 1, two pointers meeting)? **while**.

## break and continue

`break` leaves the loop. `continue` skips the rest of this round and goes on to the next.

```python
for i in range(1, 8):
    if i % 3 == 0:
        continue
    if i == 6:
        break
    print(i)
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>1 2 4 5 7</code>, one per line. 3 and 6 are skipped by <code>continue</code> before the <code>break</code> check, so the <code>break</code> never fires.</p>
</details>

## print on one line

`print(x, end=" ")` ends with a space instead of a new line. Call `print()` once at the end to finish the line.

=== z5
Strings are sequences of characters. Almost everything here works on lists too, so it pays off twice.

## Indexing

```python
s = "python"
#    012345      positions start at 0
s[0]       # "p"
s[5]       # "n"
s[-1]      # "n"   negative counts from the end
len(s)     # 6     so the last index is len(s) - 1
s[6]       # IndexError: there is no position 6
```

## Slicing

`s[start:stop]` takes from start up to, **but not including**, stop. Leave a side empty to mean "from the beginning" or "to the end".

```python
s[0:3]     # "pyt"
s[2:]      # "thon"
s[:2]      # "py"
s[::-1]    # "nohtyp"   (step -1 = backwards)
```

## Useful string methods

```python
"Hi There".lower()          # "hi there"
"hi".upper()                # "HI"
"  x  ".strip()             # "x"
"a b  c".split()            # ["a", "b", "c"]   (splits on any spaces)
"-".join(["a", "b", "c"])   # "a-b-c"
"banana".count("a")         # 3
"banana".replace("a", "o")  # "bonono"
"7".isdigit(), "x".isalpha(), "Q".isupper()
"an" in "banana"            # True
```

## Strings can't be changed

`s[0] = "P"` is an error. Strings are **immutable**. Build a new string instead:

```python
result = ""
for ch in s:
    result = result + ch.upper()
```

Check yourself:

```python
s = "Hello, World"
print(s[7:], s[-5:-2], len(s.split()))
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>World Wor 2</code>. Index 7 is "W". <code>s[-5:-2]</code> is positions 7, 8, 9. Splitting on spaces gives two words.</p>
</details>

=== z6
A list holds many values in order. It's the thing you'll use most on LeetCode.

## Making and using lists

```python
nums = [4, 8, 15]
nums[0]          # 4      same indexing as strings
nums[-1]         # 15
len(nums)        # 3
nums.append(16)  # add to the end: [4, 8, 15, 16]
nums[1] = 99     # lists CAN be changed: [4, 99, 15, 16]
nums.pop()       # removes and returns the last item (16)
8 in nums        # False now
```

## Building a list from input

```python
nums = []                        # start empty
for i in range(5):
    nums.append(int(input()))    # read 5 numbers into it
```

Or from one line of space-separated numbers:

```python
nums = [int(x) for x in input().split()]
```

(That bracket syntax is a list comprehension. Unit 1 covers it properly.)

## Looping over a list

```python
total = 0
for x in nums:
    total = total + x

for i in range(len(nums)):    # when you need the index
    print(i, nums[i])
```

## Built-ins worth knowing

```python
sum(nums), max(nums), min(nums)
sorted(nums)          # new sorted list
nums.sort()           # sorts nums itself
nums[::-1]            # reversed copy
```

Some questions ask you to do these by hand first. That's deliberate: on LeetCode you constantly write "keep track of the best so far" loops that `max` can't do for you.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>[1, 2, 3, 4]</code>. <code>b = a</code> doesn't copy the list; both names point at the same list. Use <code>b = a[:]</code> for a copy. This catches everyone at least once.</p>
</details>

=== z7
Last level of Unit 0, and the bridge to everything after it. **On LeetCode you never use input() or print().** You write a function, LeetCode calls it with the input, and it checks what you **return**.

## def and return

```python
def add(a, b):        # a and b are parameters
    return a + b      # send the answer back to whoever called it

result = add(3, 4)    # 7
print(add(10, 5))     # 15
```

`return` ends the function immediately. Anything after it in that function doesn't run.

## print is not return

```python
def bad_add(a, b):
    print(a + b)      # shows 7 on screen...

x = bad_add(3, 4)     # ...but x is None, because nothing was returned
```

If a test says it expected `7` but got `None`, you printed instead of returning, or forgot the `return`.

## From script style to function style

```python
# script style
n = int(input())
total = 0
for i in range(1, n + 1):
    total = total + i
print(total)

# from now on
def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total = total + i
    return total
```

Same logic. The input becomes a parameter and the print becomes a return.

## Returning early

```python
def first_negative(nums):
    for x in nums:
        if x < 0:
            return x      # found it, stop the whole function
    return None           # only reached if the loop finished without finding one
```

This "return inside the loop, fallback after it" shape shows up in loads of LeetCode problems.

One last check:

```python
def f(n):
    if n > 10:
        return "big"
    return "small"
    print("hello")

print(f(3), f(30))
```

<details class="predict"><summary>Predict it: what does this print?</summary>
<p><code>small big</code>. <code>print("hello")</code> never runs, because <code>return</code> always happens first.</p>
</details>

> **From here on, every coding question is a function with tests,** the same as LeetCode. After this unit's boss, Unit 1 sharpens all of this into the Python interviews use.
