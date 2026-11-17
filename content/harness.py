"""Shared harness: the exact Python the browser runs. build.py exports PRELUDE and HARNESS into the page."""

PRELUDE = '''class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
    def __repr__(self): return "ListNode(" + repr(_from_ll(self)) + ")"
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val = val; self.left = left; self.right = right
    def __repr__(self): return "TreeNode(" + repr(_from_tree(self)) + ")"
def _to_ll(a):
    d = t = ListNode()
    for v in a: t.next = ListNode(v); t = t.next
    return d.next
def _from_ll(h):
    out, seen = [], 0
    while h is not None and seen < 10000: out.append(h.val); h = h.next; seen += 1
    return out
def _to_tree(a):
    if not a or a[0] is None: return None
    nodes = [None if v is None else TreeNode(v) for v in a]; kids = nodes[::-1]; root = kids.pop()
    for n in nodes:
        if n is not None:
            if kids: n.left = kids.pop()
            if kids: n.right = kids.pop()
    return root
def _from_tree(root):
    out, q, i = [], [root], 0
    while i < len(q):
        n = q[i]; i += 1
        if n is None: out.append(None); continue
        out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None: out.pop()
    return out
'''

HARNESS = '''
# ---- test harness ----
import copy as _cp, json as _js
def _norm(x, mode):
    try:
        if mode == "sorted": return sorted(x)
        if mode == "sorted_inner": return sorted(sorted(i) for i in x)
    except TypeError:
        return x
    return x
_fn = globals().get(__FN__)
_out = []
if not callable(_fn):
    _out.append({"err": "Define a function called " + __FN__ + "."})
else:
__PREP__
    if "_call" not in globals():
        def _call(args): return _fn(*args)
    for _args, _exp in __TESTS__:
        _row = {"args": repr(_args)[1:-1].rstrip(","), "exp": repr(_exp)}
        try:
            _got = _call(_cp.deepcopy(_args))
            _row["got"] = repr(_got)
            _row["ok"] = _norm(_got, __CMP__) == _norm(_exp, __CMP__)
        except RecursionError:
            _row["err"] = "RecursionError: too deep. Missing a base case?"
        except Exception as _e:
            _row["err"] = type(_e).__name__ + ": " + str(_e)
        _out.append(_row)
print("@@RESULTS@@" + _js.dumps(_out))
'''


STDOUT_HARNESS = '''import io as _io, sys as _sys, json as _js
_SRC = __SRC__
def _clean(s):
    return "\\n".join(l.rstrip() for l in s.rstrip().split("\\n"))
def _line_of(e):
    ln, t = None, e.__traceback__
    while t is not None:
        if t.tb_frame.f_code.co_filename == "<user>": ln = t.tb_lineno
        t = t.tb_next
    return ln
_out = []
try:
    _code = compile(_SRC, "<user>", "exec")
except SyntaxError as _e:
    _code = None
    _out.append({"err": "SyntaxError: " + str(_e.msg) + " (line " + str(_e.lineno) + ")"})
if _code is not None:
    for _inp, _exp in __TESTS__:
        _feed = _io.StringIO(_inp)
        def _input(prompt=""):
            line = _feed.readline()
            if line == "":
                raise EOFError("input() was called but there was no more input. Check how many times you call input().")
            return line.rstrip("\\n")
        _buf = _io.StringIO()
        _row = {"args": _inp.rstrip("\\n") if _inp else "(no input)", "exp": _exp.rstrip("\\n")}
        _real = _sys.stdout
        _sys.stdout = _buf
        try:
            exec(_code, {"__name__": "__main__", "input": _input})
            _row["ok"] = _clean(_buf.getvalue()) == _clean(_exp)
        except BaseException as _e:
            _ln = _line_of(_e)
            _row["err"] = type(_e).__name__ + ": " + str(_e) + (" (line " + str(_ln) + ")" if _ln else "")
        finally:
            _sys.stdout = _real
        _row["got"] = _buf.getvalue().rstrip("\\n")
        _out.append(_row)
print("@@RESULTS@@" + _js.dumps(_out))
'''


def build_program(user_code, fn, tests, cmp="eq", prep=""):
    if cmp == "stdout":
        import json
        return STDOUT_HARNESS.replace("__SRC__", json.dumps(user_code)).replace("__TESTS__", tests)
    prep_block = "\n".join("    " + line for line in prep.splitlines()) if prep else "    pass"
    h = (HARNESS.replace("__FN__", repr(fn)).replace("__TESTS__", tests)
         .replace("__CMP__", repr(cmp)).replace("__PREP__", prep_block))
    return PRELUDE + user_code + "\n" + h
