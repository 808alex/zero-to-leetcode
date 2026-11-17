"""Stage 0 drills. Most are input/output programs (cmp="stdout"): tests are (input lines, expected printed output)."""
from drills import D


def S(id, module, title, prompt, starter, tests, solution, hint):
    D(id, module, title, "", prompt, starter, tests, solution, hint, cmp="stdout")


# ------------------------------------------------------------------ z1 variables, input, print
S("z-hello", "z1", "Say hello", "Read a name with <code>input()</code> and print <code>Hello, NAME!</code>",
  "# read the name, then print the greeting\n",
  r'[("Ada\n", "Hello, Ada!\n"), ("9\n", "Hello, 9!\n")]',
  'name = input()\nprint(f"Hello, {name}!")',
  'input() gives you a string. An f-string puts it in the sentence: f"Hello, {name}!"')

S("z-add", "z1", "Add two numbers", "Read two whole numbers (one per line) and print their sum.",
  "a = input()\nb = input()\n",
  r'[("3\n4\n", "7\n"), ("-2\n10\n", "8\n"), ("0\n0\n", "0\n")]',
  "a = int(input())\nb = int(input())\nprint(a + b)",
  'input() always returns text, so "3" + "4" is "34". Wrap it: int(input()).')

S("z-minutes", "z1", "Minutes to hours", "Read a number of minutes and print it as <code>H h M min</code>. For 125 that's <code>2 h 5 min</code>.",
  "minutes = int(input())\n",
  r'[("125\n", "2 h 5 min\n"), ("59\n", "0 h 59 min\n"), ("600\n", "10 h 0 min\n")]',
  'minutes = int(input())\nhours = minutes // 60\nleft = minutes % 60\nprint(f"{hours} h {left} min")',
  "// is whole-number division (125 // 60 is 2). % is the remainder (125 % 60 is 5).")

S("z-last-digit", "z1", "Chop off the last digit", "Read a whole number (0 or more). Print its last digit, then on the next line print the number with that digit removed. For 1234: <code>4</code> then <code>123</code>.",
  "n = int(input())\n",
  r'[("1234\n", "4\n123\n"), ("7\n", "7\n0\n"), ("90\n", "0\n9\n")]',
  "n = int(input())\nprint(n % 10)\nprint(n // 10)",
  "n % 10 is the last digit. n // 10 drops it. You'll use both constantly in the while-loop module.")

S("z-receipt", "z1", "Shop receipt", "Read a price (like <code>2.5</code>) and a quantity (a whole number). Print the total with exactly 2 decimal places.",
  "price = float(input())\n",
  r'[("2.5\n4\n", "10.00\n"), ("0.1\n3\n", "0.30\n"), ("19.99\n1\n", "19.99\n")]',
  'price = float(input())\nqty = int(input())\nprint(f"{price * qty:.2f}")',
  'float() for decimals. In an f-string, {x:.2f} shows x with 2 decimal places (0.1 * 3 is really 0.30000000000000004).')

# ------------------------------------------------------------------ z2 if / elif / else
S("z-even-odd", "z2", "Even or odd", "Read a whole number and print <code>even</code> or <code>odd</code>.",
  "n = int(input())\n",
  r'[("4\n", "even\n"), ("7\n", "odd\n"), ("0\n", "even\n"), ("-3\n", "odd\n")]',
  'n = int(input())\nif n % 2 == 0:\n    print("even")\nelse:\n    print("odd")',
  "A number is even when n % 2 == 0. Remember the colon after the condition and the indent under it.")

S("z-biggest", "z2", "Biggest of three", "Read three numbers (one per line) and print the biggest. Don't use <code>max()</code> for this one.",
  "a = int(input())\nb = int(input())\nc = int(input())\n",
  r'[("1\n5\n3\n", "5\n"), ("9\n9\n2\n", "9\n"), ("-1\n-5\n-3\n", "-1\n"), ("2\n3\n8\n", "8\n")]',
  "a = int(input())\nb = int(input())\nc = int(input())\nbiggest = a\nif b > biggest:\n    biggest = b\nif c > biggest:\n    biggest = c\nprint(biggest)",
  "Start with biggest = a. Then check b, then c, replacing biggest whenever you find something larger.")

S("z-weekend", "z2", "Weekday or weekend", "Read a day number from 1 to 7 (1 is Monday) and print <code>weekday</code> or <code>weekend</code>. Careful: Saturday and Sunday are 6 and 7, and it's easy to get this backwards.",
  "day = int(input())\n",
  r'[("1\n", "weekday\n"), ("5\n", "weekday\n"), ("6\n", "weekend\n"), ("7\n", "weekend\n")]',
  'day = int(input())\nif day >= 6:\n    print("weekend")\nelse:\n    print("weekday")',
  "Which numbers are the weekend? Write the condition for those, and else handles the rest.")

S("z-fizzbuzz-one", "z2", "FizzBuzz for one number", "Read a number. Print <code>fizz-buzz</code> if it divides by 3 and 5, <code>fizz</code> if only by 3, <code>buzz</code> if only by 5, otherwise the number itself.",
  "number = int(input())\n",
  r'[("15\n", "fizz-buzz\n"), ("9\n", "fizz\n"), ("10\n", "buzz\n"), ("7\n", "7\n"), ("30\n", "fizz-buzz\n")]',
  'number = int(input())\nif number % 3 == 0 and number % 5 == 0:\n    print("fizz-buzz")\nelif number % 3 == 0:\n    print("fizz")\nelif number % 5 == 0:\n    print("buzz")\nelse:\n    print(number)',
  "Order matters: check 'both' first. If you check % 3 first, 15 prints fizz and never reaches the fizz-buzz line.")

S("z-grade", "z2", "Mark to grade", "Read a mark from 0 to 100. Print <code>A</code> for 70+, <code>B</code> for 55–69, <code>C</code> for 40–54, and <code>F</code> below 40.",
  "mark = int(input())\n",
  r'[("85\n", "A\n"), ("70\n", "A\n"), ("69\n", "B\n"), ("55\n", "B\n"), ("40\n", "C\n"), ("39\n", "F\n")]',
  'mark = int(input())\nif mark >= 70:\n    print("A")\nelif mark >= 55:\n    print("B")\nelif mark >= 40:\n    print("C")\nelse:\n    print("F")',
  "Go from the top band down with elif. By the time you reach elif mark >= 55, you already know it's under 70.")

S("z-leap", "z2", "Leap year", "Read a year and print <code>leap</code> or <code>not leap</code>. A year is a leap year if it divides by 4, except years that divide by 100, unless they also divide by 400.",
  "year = int(input())\n",
  r'[("2024\n", "leap\n"), ("2023\n", "not leap\n"), ("1900\n", "not leap\n"), ("2000\n", "leap\n")]',
  'year = int(input())\nif year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):\n    print("leap")\nelse:\n    print("not leap")',
  "One way: year % 400 == 0 or (year % 4 == 0 and year % 100 != 0). Test 1900 and 2000 in your head.")

# ------------------------------------------------------------------ z3 while loops
S("z-count-up", "z3", "Count to n", "Read <code>n</code> and print the numbers 1 to n, one per line, using a <code>while</code> loop. If n is 0, print nothing.",
  "n = int(input())\ni = 1\n",
  r'[("3\n", "1\n2\n3\n"), ("1\n", "1\n"), ("0\n", "")]',
  "n = int(input())\ni = 1\nwhile i <= n:\n    print(i)\n    i = i + 1",
  "Start i at 1, loop while i <= n, and don't forget i = i + 1 at the end of the body, or it never stops.")

S("z-countdown", "z3", "Countdown", "Read <code>n</code> and print n down to 1, then <code>Liftoff!</code>",
  "n = int(input())\n",
  r'[("3\n", "3\n2\n1\nLiftoff!\n"), ("1\n", "1\nLiftoff!\n"), ("0\n", "Liftoff!\n")]',
  'n = int(input())\nwhile n > 0:\n    print(n)\n    n = n - 1\nprint("Liftoff!")',
  "Count n itself down: while n > 0, print it, subtract 1. The Liftoff! print goes after the loop, not indented.")

S("z-sum-to-n", "z3", "Add up 1 to n", "Read <code>n</code> and print 1 + 2 + ... + n.",
  "n = int(input())\ntotal = 0\n",
  r'[("4\n", "10\n"), ("1\n", "1\n"), ("100\n", "5050\n"), ("0\n", "0\n")]',
  "n = int(input())\ntotal = 0\ni = 1\nwhile i <= n:\n    total = total + i\n    i = i + 1\nprint(total)",
  "Two variables: a counter i and a running total. Each time round, add i to total, then move i on. Print once, after the loop.")

S("z-multiples", "z3", "First n multiples", "Read <code>n</code> then <code>m</code>, and print the first n multiples of m, one per line.",
  "n = int(input())\nm = int(input())\n",
  r'[("3\n7\n", "7\n14\n21\n"), ("0\n5\n", ""), ("4\n1\n", "1\n2\n3\n4\n")]',
  "n = int(input())\nm = int(input())\ni = 1\nwhile i <= n:\n    print(i * m)\n    i = i + 1",
  "Loop i from 1 to n and print i * m.")

S("z-count-digits", "z3", "Count the digits", "Read a whole number (0 or more) and print how many digits it has. Do it with a loop and <code>// 10</code>, not <code>len(str(n))</code>. 0 has one digit.",
  "n = int(input())\n",
  r'[("0\n", "1\n"), ("7\n", "1\n"), ("12345\n", "5\n"), ("1000\n", "4\n")]',
  "n = int(input())\ncount = 1\nwhile n >= 10:\n    n = n // 10\n    count = count + 1\nprint(count)",
  "Each n // 10 removes one digit. Count how many times you can do it before n is a single digit. Starting count at 1 handles 0 for free.")

S("z-collatz", "z3", "Collatz sequence", "Read <code>n</code> (1 or more). Print it, then keep going: if it's even, halve it; if odd, do 3n + 1. Stop after printing 1.",
  "n = int(input())\n",
  r'[("6\n", "6\n3\n10\n5\n16\n8\n4\n2\n1\n"), ("1\n", "1\n"), ("3\n", "3\n10\n5\n16\n8\n4\n2\n1\n")]',
  "n = int(input())\nprint(n)\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n        n = 3 * n + 1\n    print(n)",
  "Print n before the loop, then loop while n != 1: update n, print it. Use // to halve so it stays a whole number.")

S("z-until-end", "z3", "Add until \"end\"", "Keep reading lines until one says <code>end</code>. Each other line is a whole number. Print their total. This \"read until a stop word\" loop comes up all the time.",
  "total = 0\nline = input()\n",
  r'[("3\n4\nend\n", "7\n"), ("end\n", "0\n"), ("10\n-2\n5\nend\n", "13\n")]',
  'total = 0\nline = input()\nwhile line != "end":\n    total = total + int(line)\n    line = input()\nprint(total)',
  'Read the first line before the loop. Inside: use it, then read the next line as the last step. The condition is line != "end".')

# ------------------------------------------------------------------ z4 for loops and range
S("z-times-table", "z4", "Times table", "Read <code>n</code> and print its times table from 1 to 10, like <code>3 x 1 = 3</code>. Use <code>for</code> and <code>range</code>.",
  "n = int(input())\n",
  r'[("3\n", "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n3 x 6 = 18\n3 x 7 = 21\n3 x 8 = 24\n3 x 9 = 27\n3 x 10 = 30\n"), ("12\n", "12 x 1 = 12\n12 x 2 = 24\n12 x 3 = 36\n12 x 4 = 48\n12 x 5 = 60\n12 x 6 = 72\n12 x 7 = 84\n12 x 8 = 96\n12 x 9 = 108\n12 x 10 = 120\n")]',
  'n = int(input())\nfor i in range(1, 11):\n    print(f"{n} x {i} = {n * i}")',
  "range(1, 11) gives 1 to 10. The stop number is never included.")

S("z-squares", "z4", "Squares on one line", "Read <code>n</code> and print the squares of 1 to n on one line, separated by spaces. For 5: <code>1 4 9 16 25</code>",
  "n = int(input())\n",
  r'[("5\n", "1 4 9 16 25\n"), ("1\n", "1\n"), ("3\n", "1 4 9\n")]',
  'n = int(input())\nfor i in range(1, n + 1):\n    print(i * i, end=" ")\nprint()',
  'print(x, end=" ") prints a space instead of a new line. Another way: build a list and print(*squares).')

S("z-evens", "z4", "Even numbers up to n", "Read <code>n</code> and print every even number from 0 to n (including n if it's even), one per line. Use the third argument of <code>range</code>.",
  "n = int(input())\n",
  r'[("6\n", "0\n2\n4\n6\n"), ("5\n", "0\n2\n4\n"), ("0\n", "0\n")]',
  "n = int(input())\nfor i in range(0, n + 1, 2):\n    print(i)",
  "range(start, stop, step). range(0, n + 1, 2) counts 0, 2, 4, ... and the + 1 lets n itself be included.")

S("z-vowels", "z4", "Count vowels", "Read a line of text and print how many vowels (a, e, i, o, u, either case) it contains.",
  "text = input()\n",
  r'[("Hello World\n", "3\n"), ("rhythm\n", "0\n"), ("AEIOU aeiou\n", "10\n")]',
  'text = input()\ncount = 0\nfor ch in text:\n    if ch.lower() in "aeiou":\n        count = count + 1\nprint(count)',
  'for ch in text walks the string one character at a time. ch.lower() in "aeiou" checks for a vowel in either case.')

S("z-stars", "z4", "Star triangle", "Read <code>n</code> and print a triangle of stars: 1 star on the first line, up to n stars on the last.",
  "n = int(input())\n",
  r'[("3\n", "*\n**\n***\n"), ("1\n", "*\n"), ("5\n", "*\n**\n***\n****\n*****\n")]',
  'n = int(input())\nfor i in range(1, n + 1):\n    print("*" * i)',
  '"*" * 3 is "***". String times a number repeats it.')

S("z-first-digit", "z4", "Find the first digit", "Read a line. Print the first digit and its index like <code>3 at index 11</code>, or <code>no digit</code> if there isn't one. Stop the loop as soon as you find it.",
  "s = input()\n",
  r'[("There were 321 green bottles\n", "3 at index 11\n"), ("abc\n", "no digit\n"), ("7up\n", "7 at index 0\n")]',
  's = input()\nfound = False\nfor i in range(len(s)):\n    if s[i].isdigit():\n        print(s[i], "at index", i)\n        found = True\n        break\nif not found:\n    print("no digit")',
  "Loop over range(len(s)) so you have the index i. break leaves the loop straight away. Use a found flag to know whether to print 'no digit' afterwards.")

# ------------------------------------------------------------------ z5 strings
S("z-reverse", "z5", "Reverse it", "Read a line and print it backwards. One slice does it.",
  "s = input()\n",
  r'[("hello\n", "olleh\n"), ("a\n", "a\n"), ("ab c\n", "c ba\n")]',
  "s = input()\nprint(s[::-1])",
  "s[::-1] means: whole string, step -1 (backwards).")

S("z-capitals", "z5", "Pick out the capitals", "Read a line and print each uppercase letter on its own line.",
  "s = input()\n",
  r'[("Hello World\n", "H\nW\n"), ("abc\n", ""), ("NASA rocks\n", "N\nA\nS\nA\n")]',
  "s = input()\nfor ch in s:\n    if ch.isupper():\n        print(ch)",
  'ch.isupper() does the same job as checking "A" <= ch <= "Z", and reads better.')

S("z-initials", "z5", "Initials", "Read a full name (words separated by spaces) and print the initials in capitals with dots. <code>ada lovelace</code> → <code>A.L.</code>",
  "name = input()\n",
  r'[("ada lovelace\n", "A.L.\n"), ("grace brewster hopper\n", "G.B.H.\n"), ("x\n", "X.\n")]',
  'name = input()\nresult = ""\nfor word in name.split():\n    result = result + word[0].upper() + "."\nprint(result)',
  'name.split() gives a list of words. word[0] is a word\'s first letter. Build up a result string.')

S("z-hyphens", "z5", "Spaces to hyphens", "Read a line and print it with every space replaced by <code>-</code>. Build the new string with a loop; don't use <code>.replace()</code> (yet).",
  "s = input()\nresult = \"\"\n",
  r'[("a b c\n", "a-b-c\n"), ("nospace\n", "nospace\n"), ("two  spaces\n", "two--spaces\n")]',
  's = input()\nresult = ""\nfor ch in s:\n    if ch == " ":\n        result = result + "-"\n    else:\n        result = result + ch\nprint(result)',
  'Strings can\'t be changed in place, so make a new one. Once it works, compare with s.replace(" ", "-").')

S("z-count-char", "z5", "Count a character", "Read a line of text, then a single character on the next line. Print how many times the character appears.",
  "text = input()\nch = input()\n",
  r'[("banana\na\n", "3\n"), ("hello\nz\n", "0\n"), ("Mississippi\ns\n", "4\n")]',
  "text = input()\nch = input()\ncount = 0\nfor c in text:\n    if c == ch:\n        count = count + 1\nprint(count)",
  "Loop over the text and count the matches. (text.count(ch) does it in one go, but write the loop first.)")

S("z-palindrome", "z5", "Palindrome check", "Read a word and print <code>palindrome</code> or <code>not palindrome</code>.",
  "word = input()\n",
  r'[("racecar\n", "palindrome\n"), ("abba\n", "palindrome\n"), ("abc\n", "not palindrome\n"), ("a\n", "palindrome\n")]',
  'word = input()\nif word == word[::-1]:\n    print("palindrome")\nelse:\n    print("not palindrome")',
  "A palindrome equals its reverse. You already know how to reverse in one slice.")

# ------------------------------------------------------------------ z6 lists
S("z-max-min", "z6", "Biggest and smallest", "Read 5 numbers (one per line) into a list. Print the biggest, then the smallest, on separate lines. Use a loop, not <code>max()</code>/<code>min()</code>.",
  "nums = []\nfor i in range(5):\n    nums.append(int(input()))\n",
  r'[("3\n9\n-1\n4\n4\n", "9\n-1\n"), ("5\n5\n5\n5\n5\n", "5\n5\n"), ("-3\n-7\n-1\n-9\n-2\n", "-1\n-9\n")]',
  "nums = []\nfor i in range(5):\n    nums.append(int(input()))\nbig = nums[0]\nsmall = nums[0]\nfor x in nums:\n    if x > big:\n        big = x\n    if x < small:\n        small = x\nprint(big)\nprint(small)",
  "Start both big and small at nums[0] (not 0: all the numbers might be negative). Then loop and update.")

S("z-sum-evens", "z6", "Sum of the evens", "Read 10 numbers and print the sum of the even ones. Aim for about five lines.",
  "",
  r'[("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n", "30\n"), ("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n", "0\n"), ("-2\n0\n3\n5\n7\n9\n11\n4\n1\n1\n", "2\n")]',
  "total = 0\nfor i in range(10):\n    n = int(input())\n    if n % 2 == 0:\n        total = total + n\nprint(total)",
  "One loop of 10. Read a number, add it only if n % 2 == 0. No list needed.")

S("z-reverse-list", "z6", "Print in reverse", "Read <code>n</code>, then n numbers. Print them in reverse order, one per line.",
  "n = int(input())\nnums = []\n",
  r'[("3\n1\n2\n3\n", "3\n2\n1\n"), ("1\n5\n", "5\n"), ("0\n", "")]',
  "n = int(input())\nnums = []\nfor i in range(n):\n    nums.append(int(input()))\nfor x in nums[::-1]:\n    print(x)",
  "Collect them with append, then loop over nums[::-1] (slicing works on lists too).")

S("z-dedupe", "z6", "Remove duplicates", "Read a line of words separated by spaces. Print the words with duplicates removed, keeping the order they first appeared, separated by spaces.",
  "words = input().split()\n",
  r'[("a b a c b\n", "a b c\n"), ("x\n", "x\n"), ("the cat the hat\n", "the cat hat\n")]',
  'words = input().split()\nseen = []\nfor w in words:\n    if w not in seen:\n        seen.append(w)\nprint(" ".join(seen))',
  'Keep a new list. Only append a word if it\'s not in it yet. " ".join(list) glues a list of strings back together with spaces.')

S("z-above-avg", "z6", "Above average", "Read <code>n</code> (at least 1), then n numbers. Print how many of them are strictly above the average.",
  "n = int(input())\n",
  r'[("4\n1\n2\n3\n10\n", "1\n"), ("3\n5\n5\n5\n", "0\n"), ("5\n1\n2\n3\n4\n5\n", "2\n")]',
  "n = int(input())\nnums = []\nfor i in range(n):\n    nums.append(int(input()))\navg = sum(nums) / len(nums)\ncount = 0\nfor x in nums:\n    if x > avg:\n        count = count + 1\nprint(count)",
  "You need every number twice (once for the average, once to compare), which is why you store them in a list first.")

# ------------------------------------------------------------------ z7 functions (normal function drills)
D("z-square", "z7", "Your first function", "square",
  "Write <code>square(n)</code> that <strong>returns</strong> n × n. Don't print, return. The tests call your function and check what comes back.",
  "def square(n):\n    pass",
  '[((3,), 9), ((0,), 0), ((-4,), 16), ((12,), 144)]',
  "def square(n):\n    return n * n",
  "Replace pass with return n * n.")

D("z-is-even", "z7", "Return True or False", "is_even",
  "Write <code>is_even(n)</code> that returns <code>True</code> if n is even, otherwise <code>False</code>. It can be one line.",
  "def is_even(n):\n    pass",
  '[((4,), True), ((7,), False), ((0,), True), ((-3,), False)]',
  "def is_even(n):\n    return n % 2 == 0",
  "n % 2 == 0 already is True or False, so you can return it directly. No if needed.")

D("z-max3", "z7", "Biggest of three, as a function", "max_of_three",
  "Write <code>max_of_three(a, b, c)</code> that returns the biggest, without <code>max()</code>. Same logic as the Biggest of three question in Making decisions, but returned instead of printed.",
  "def max_of_three(a, b, c):\n    pass",
  '[((1, 5, 3), 5), ((9, 9, 2), 9), ((-1, -5, -3), -1), ((2, 3, 8), 8)]',
  "def max_of_three(a, b, c):\n    biggest = a\n    if b > biggest:\n        biggest = b\n    if c > biggest:\n        biggest = c\n    return biggest",
  "Copy your earlier logic, change the inputs into parameters and the print into return.")

D("z-sign-word", "z7", "Return a word", "sign_word",
  "Write <code>sign_word(n)</code> that returns <code>\"positive\"</code>, <code>\"negative\"</code> or <code>\"zero\"</code>.",
  "def sign_word(n):\n    pass",
  '[((5,), "positive"), ((-2,), "negative"), ((0,), "zero")]',
  'def sign_word(n):\n    if n > 0:\n        return "positive"\n    if n < 0:\n        return "negative"\n    return "zero"',
  "return ends the function immediately, so after an if that returns you don't even need else.")

D("z-count-char-fn", "z7", "Count with a loop, in a function", "count_char",
  "Write <code>count_char(s, ch)</code> that returns how many times <code>ch</code> appears in <code>s</code>. Use a loop.",
  "def count_char(s, ch):\n    pass",
  '[(("banana", "a"), 3), (("hello", "z"), 0), (("", "a"), 0), (("aaa", "a"), 3)]',
  "def count_char(s, ch):\n    count = 0\n    for c in s:\n        if c == ch:\n            count += 1\n    return count",
  "count = 0 at the start, add 1 for each match, return count after the loop (not inside it).")

D("z-average", "z7", "Average of a list", "average",
  "Write <code>average(nums)</code> that returns the average of a list of numbers, or <code>0</code> if the list is empty.",
  "def average(nums):\n    pass",
  '[(([1, 2, 3],), 2.0), (([1, 2],), 1.5), (([],), 0), (([10],), 10.0)]',
  "def average(nums):\n    if not nums:\n        return 0\n    return sum(nums) / len(nums)",
  "Check for the empty list first (dividing by len([]) = 0 crashes). if not nums: is True when the list is empty.")
