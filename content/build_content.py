"""Builds src/content/content.json and verifies every answer by executing it.

Run: python3 content/build_content.py
Fails (non-zero exit) if any question, drill, fix or boss doesn't check out.
"""
import contextlib, copy, io, json, os, re, signal, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.setrecursionlimit(5000)

import markdown  # noqa: E402
from modules import MODULES, STAGES  # noqa: E402
from drills import DRILLS  # noqa: E402
import drills_z  # noqa: E402,F401
from harness import PRELUDE, HARNESS, STDOUT_HARNESS, build_program  # noqa: E402
from game import LEVELS, BOSSES  # noqa: E402
from mistakes import MISTAKES, CATEGORIES  # noqa: E402

OUT = HERE.parent / "src" / "content" / "content.json"
DRILL = {d["id"]: d for d in DRILLS}
MOD = {m["id"]: m for m in MODULES}
errors = []

UNITS = [
    {"id": "u0", "title": "Dip your toes in", "blurb": STAGES[0]["blurb"], "levels": ["z1", "z2", "z3", "z4", "z5", "z6", "z7"], "boss": "b0"},
    {"id": "u1", "title": "Get the rust off", "blurb": STAGES[1]["blurb"], "levels": ["m1", "m2", "m3", "m4"], "boss": "b1"},
    {"id": "u2", "title": "Core patterns", "blurb": "Hashing, two pointers, sliding window, stacks, binary search.", "levels": ["p1", "p2", "p3", "p4", "p5"], "boss": "b2"},
    {"id": "u3", "title": "Data structures", "blurb": "Linked lists, trees and heaps.", "levels": ["p6", "p7", "p8"], "boss": "b3"},
    {"id": "u4", "title": "Search & DP", "blurb": "Backtracking, graphs, dynamic programming, intervals and greedy.", "levels": ["p9", "p10", "p11", "p12"], "boss": "b4"},
    {"id": "u5", "title": "Interview mode", "blurb": STAGES[3]["blurb"], "levels": ["x1"], "boss": "b5"},
]


def norm_out(s):
    return "\n".join(l.rstrip() for l in s.rstrip().split("\n"))


def run_script(code, stdin=""):
    feed = io.StringIO(stdin)

    def _input(prompt=""):
        line = feed.readline()
        if line == "":
            raise EOFError("no more input")
        return line.rstrip("\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<mc>", "exec"), {"__name__": "__main__", "input": _input})
    return norm_out(buf.getvalue())


def expected_from_function(code, fn, args_list, prep):
    ns = {"__name__": "__main__"}
    exec(PRELUDE + code, ns)
    ns["_fn"] = ns[fn]
    if prep:
        exec(prep, ns)
    else:
        exec("def _call(args):\n    return _fn(*args)", ns)
    return [ns["_call"](copy.deepcopy(a)) for a in args_list]


def tests_literal(code, fn, args, stdins, prep):
    if stdins is not None:
        return repr([(s, run_script(code, s) + "\n") for s in stdins]), "stdout"
    exp = expected_from_function(code, fn, args, prep)
    return repr([(tuple(a), e) for a, e in zip(args, exp)]), None


class Timeout(BaseException):
    pass


TIMED_OUT = [False]


def _alarm(*_):
    TIMED_OUT[0] = True
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)


def check(code, fn, tests, cmp, prep, seconds=3):
    prog = build_program(code, fn or "", tests, cmp, prep)
    buf = io.StringIO()
    TIMED_OUT[0] = False
    signal.setitimer(signal.ITIMER_REAL, seconds, 0.05)  # keeps firing, so a harness that swallows it still finishes
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(prog, "<exec>", "exec"), {"__name__": "__main__"})
    except Timeout:
        return False, "timed out"
    except Exception as e:  # harness itself should never raise
        return False, repr(e)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
    if TIMED_OUT[0]:
        return False, "timed out"
    line = [l for l in buf.getvalue().splitlines() if l.startswith("@@RESULTS@@")]
    if not line:
        return False, "no results"
    res = json.loads(line[0][11:])
    return bool(res) and all(r.get("ok") for r in res), res


def cards_for(html, title):
    parts = re.split(r"(?=<h2>)", html)
    cards = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.match(r"<h2>(.*?)</h2>", p)
        cards.append({"title": m.group(1) if m else title, "html": p[m.end():].strip() if m else p})
    return cards


lessons = {}
for f in ("stage0.md", "stage1.md", "patterns.md"):
    for block in re.split(r"^=== ", (HERE / "lessons" / f).read_text(), flags=re.M)[1:]:
        mid, body = block.split("\n", 1)
        lessons[mid.strip()] = markdown.markdown(body, extensions=["fenced_code", "tables"])

questions = {}


def add_drill(d, qid=None):
    qid = qid or d["id"]
    ok, res = check(d["solution"], d["fn"], d["tests"], d["cmp"], d["prep"])
    if not ok:
        errors.append(f"drill {qid}: solution fails {res}")
    questions[qid] = {"id": qid, "kind": "code", "title": d["title"], "prompt": d["prompt"], "starter": d["starter"], "fn": d["fn"],
                      "tests": d["tests"], "cmp": d["cmp"], "prep": d["prep"], "hint": d["hint"], "solution": d["solution"], "lc": d.get("lc")}
    return qid


def add_quick(item, qid):
    k = item["kind"]
    if k == "mc":
        try:
            out = run_script(item["code"], item["stdin"])
        except Exception as e:
            errors.append(f"{qid}: mc code raised {e!r}")
            return qid
        ans = out if out else "(nothing)"
        wrong = [w for w in item["wrong"]]
        if ans in [norm_out(w) for w in wrong]:
            errors.append(f"{qid}: a distractor equals the real output {ans!r}")
        if len(set(wrong)) != len(wrong):
            errors.append(f"{qid}: duplicate distractors")
        questions[qid] = {"id": qid, "kind": "mc", "prompt": item["prompt"], "code": item["code"], "stdin": item["stdin"],
                          "options": [ans] + wrong, "answer": 0, "explain": item["explain"]}
    elif k == "mct":
        questions[qid] = {"id": qid, "kind": "mc", "prompt": item["prompt"], "code": item["code"], "stdin": "",
                          "options": item["options"], "answer": item["answer"], "explain": item["explain"], "concept": True}
    elif k == "fill":
        if "___" not in item["code"]:
            errors.append(f"{qid}: fill has no blank")
        full = item["code"].replace("___", item["answer"])
        tests, mode = tests_literal(full, item["fn"], item["args"], item["stdins"], item["prep"])
        cmp = "stdout" if mode else item["cmp"]
        ok, res = check(full, item["fn"], tests, cmp, item["prep"])
        if not ok:
            errors.append(f"{qid}: fill reference fails {res}")
        for junk in ("None", "0", "True", "\"\""):
            ok2, _ = check(item["code"].replace("___", junk), item["fn"], tests, cmp, item["prep"])
            if ok2:
                errors.append(f"{qid}: fill passes with junk answer {junk}")
        questions[qid] = {"id": qid, "kind": "fill", "prompt": item["prompt"], "code": item["code"], "answer": item["answer"],
                          "fn": item["fn"] or "", "tests": tests, "cmp": cmp, "prep": item["prep"], "hint": item["hint"], "explain": item["explain"]}
    elif k == "fix":
        tests, mode = tests_literal(item["fixed"], item["fn"], item["args"], item["stdins"], item["prep"])
        cmp = "stdout" if mode else item["cmp"]
        ok, res = check(item["fixed"], item["fn"], tests, cmp, item["prep"])
        if not ok:
            errors.append(f"{qid}: fixed version fails {res}")
        bad, _ = check(item["buggy"], item["fn"], tests, cmp, item["prep"])
        if bad:
            errors.append(f"{qid}: buggy version passes, so there's nothing to fix")
        questions[qid] = {"id": qid, "kind": "fix", "title": "Fix the bug", "prompt": item["prompt"], "starter": item["buggy"],
                          "fn": item["fn"] or "", "tests": tests, "cmp": cmp, "prep": item["prep"], "hint": item["hint"],
                          "solution": item["fixed"], "explain": item["explain"]}
    return qid


levels = []
for u in UNITS:
    for lid in u["levels"]:
        m = MOD[lid]
        skills = []
        n = 0
        for name, items in LEVELS[lid]:
            ids = []
            for it in items:
                if isinstance(it, str):
                    if it not in DRILL:
                        errors.append(f"{lid}: unknown drill {it}")
                        continue
                    ids.append(add_drill(DRILL[it]))
                else:
                    n += 1
                    ids.append(add_quick(it, f"{lid}-q{n}"))
            if len(ids) < 2:
                errors.append(f"{lid}/{name}: a skill needs at least 2 questions")
            skills.append({"name": name, "questions": ids})
        used = {q for s in skills for q in s["questions"]}
        for d in DRILLS:
            if d["module"] == lid and d["id"] not in used:
                errors.append(f"{lid}: drill {d['id']} not placed in any skill")
        levels.append({"id": lid, "unit": u["id"], "kind": "lesson", "title": m["title"], "short": m["short"],
                       "cards": cards_for(lessons[lid], m["title"]), "skills": skills,
                       "lc": [{"slug": s, "title": t, "diff": dd} for s, t, dd in m["lc"]]})
    b = BOSSES[u["boss"]]
    ids = []
    for i, ch in enumerate(b["challenges"], 1):
        qid = f"{u['boss']}-{i}"
        tests, mode = tests_literal(ch["solution"], ch["fn"], ch["args"], ch["stdins"], ch["prep"])
        cmp = "stdout" if mode else ch["cmp"]
        allt = eval(tests)
        visible = repr(allt[:ch["visible"]])
        ok, res = check(ch["solution"], ch["fn"], tests, cmp, ch["prep"])
        if not ok:
            errors.append(f"{qid}: boss solution fails {res}")
        bad, _ = check(ch["starter"], ch["fn"], tests, cmp, ch["prep"])
        if bad:
            errors.append(f"{qid}: boss starter passes")
        questions[qid] = {"id": qid, "kind": "code", "boss": True, "title": ch["title"], "prompt": ch["prompt"], "starter": ch["starter"],
                          "fn": ch["fn"] or "", "tests": tests, "testsVisible": visible, "visibleCount": ch["visible"], "hidden": len(allt) - ch["visible"],
                          "cmp": cmp, "prep": ch["prep"], "hint": ch["hint"], "solution": ch["solution"]}
        ids.append(qid)
    levels.append({"id": u["boss"], "unit": u["id"], "kind": "boss", "title": b["title"], "short": b["blurb"], "cards": [],
                   "skills": [{"name": "Boss", "questions": ids}], "lc": []})

# sanity: brute-force cross-checks for a few boss solutions
def brute_k_diff(nums, k):
    return len({(a, b) for i, a in enumerate(nums) for j, b in enumerate(nums) if i != j and b - a == k})
for a in BOSSES["b2"]["challenges"][0]["args"]:
    got = expected_from_function(BOSSES["b2"]["challenges"][0]["solution"], "find_pairs", [a], "")[0]
    if got != brute_k_diff(*a):
        errors.append(f"b2-1 cross-check failed for {a}")
def brute_pal(s):
    return max([0] + [j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]])
for a in BOSSES["b5"]["challenges"][2]["args"]:
    if expected_from_function(BOSSES["b5"]["challenges"][2]["solution"], "longest_palindrome_len", [a], "")[0] != brute_pal(*a):
        errors.append(f"b5-3 cross-check failed for {a}")

# ---------------------------------------------------------------- common mistakes: record what Python really says
def run_capture(code, stdin=""):
    feed = io.StringIO(stdin)

    def _input(prompt=""):
        line = feed.readline()
        if line == "":
            raise EOFError("EOF when reading a line")
        return line.rstrip("\n")
    buf = io.StringIO()
    err = None
    signal.setitimer(signal.ITIMER_REAL, 3, 0.05)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<snippet>", "exec"), {"__name__": "__main__", "input": _input})
    except Timeout:
        err = "(never finishes)"
    except SyntaxError as e:
        err = f"{type(e).__name__}: {e.msg}"
    except RecursionError:
        err = "RecursionError: maximum recursion depth exceeded"
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
    return norm_out(buf.getvalue()), err


mistakes = []
for m in MISTAKES:
    if m["level"] not in LEVELS and m["level"] not in MOD:
        errors.append(f"mistake {m['id']}: unknown level {m['level']}")
    item = {k: m[k] for k in ("id", "cat", "level", "title", "wrong", "right", "why")}
    if m["run"]:
        wout, werr = run_capture(m["wrong"], m["stdin"])
        rout, rerr = run_capture(m["right"], m["stdin"])
        if rerr:
            errors.append(f"mistake {m['id']}: the right version raises {rerr}")
        if (wout, werr) == (rout, rerr):
            errors.append(f"mistake {m['id']}: wrong and right versions behave the same")
        item.update({"wrongOut": wout, "wrongErr": werr, "rightOut": rout})
    mistakes.append(item)

if errors:
    print("\n".join(errors))
    sys.exit(1)

data = {"units": UNITS, "levels": levels, "questions": questions, "mistakes": mistakes, "mistakeCategories": CATEGORIES,
        "harness": {"prelude": PRELUDE, "functions": HARNESS, "stdout": STDOUT_HARNESS}}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False))
kinds = {}
for q in questions.values():
    kinds[q["kind"] + ("-boss" if q.get("boss") else "")] = kinds.get(q["kind"] + ("-boss" if q.get("boss") else ""), 0) + 1
print(f"OK: {len(levels)} levels, {len(questions)} questions {kinds}, {OUT.stat().st_size // 1024} KB")
