"""lint: the static half. One file. Imports nothing from the build.

A static pass is SINGLE-FRAME by construction: it reads a tree and reports. There is no
promotion, no import, no second scale to cross to -- so the cross-scale half of the loop
has no expression here and pretending otherwise would be the decoration this exists to
catch. What it can see is shape: boundaries, comments, and the reference graph.

Four rules, and they are only the ones ruff cannot express. The layer boundary lives in
pyproject as TID251 bans, because ruff does that natively and reimplementing it would be
the reinvention no grep can see.

The discipline is the one that matters, carried over from kernel.py:

  EVERY RULE CARRIES A WITNESS.  Source it MUST flag and source it MUST NOT. `selftest`
  runs both, and a rule failing either is SUPPRESSED rather than trusted. A rule that
  cannot fire is not a rule.

  IT SAYS WHAT IT CANNOT SEE.  Twenty-one properties are named below with the seat that
  covers them, or the reason none does. A linter reporting only what it found reads as a
  complete account of something it accounts for a fifth of.

    python lint.py              check this repo
    python lint.py --selftest   witnesses only
    python lint.py --blind      what a static pass cannot see, and who can
"""

from __future__ import annotations

import ast
import io
import sys
import tokenize
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

PASS, FAIL, VACUOUS, SUPPRESSED = "PASS", "FAIL", "VACUOUS", "SUPPRESSED"


@dataclass
class Rule:
    rid: str
    cite: str
    fn: Callable[..., tuple[list[str], int]]
    bad: str
    ok: str
    n_bad: int
    n_ok: int
    crossfile: bool = False


RULES: list[Rule] = []


def rule(rid, cite, bad, ok, *, n_bad, n_ok, crossfile=False):
    def deco(fn):
        RULES.append(Rule(rid, cite, fn, bad, ok, n_bad, n_ok, crossfile))
        return fn
    return deco


# ---------------------------------------------------------------------------------------


@rule("ANCHOR",
      "DECLARING THE MODE: 'an unmeasured number is a specification of what to measure "
      "and can be worth a great deal' -- labelled as such, which is the whole condition",
      "ONE = 1\nEPS = 0.02\n",
      "ONE = 1\n"
      "EPS = 0.02  # anchor: human play completes a level in <500 actions; this is 2x\n",
      n_bad=1, n_ok=1)
def _anchor(src: str, *_: Any) -> tuple[list[str], int]:
    """A module-level constant with no stated basis is an invented metric. Comments are
    invisible to the AST, so this is one of the few things only a token pass can see."""
    anchored = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT and "anchor:" in tok.string:
                anchored.add(tok.start[0])
    except (tokenize.TokenError, IndentationError):
        pass
    out, seen = [], 0
    for node in ast.parse(src).body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
            continue
        t = node.targets[0]
        if not (isinstance(t, ast.Name) and t.id.isupper()):
            continue
        v = node.value
        if not (isinstance(v, ast.Constant) and isinstance(v.value, (int, float))
                and not isinstance(v.value, bool)):
            continue
        if v.value in (0, 1, -1):          # not a magic number in any code
            continue
        seen += 1
        if node.lineno not in anchored:
            out.append(f"{t.id} = {v.value} with no `# anchor:`")
    return out, seen


@rule("SINGLETON",
      "Step 2 generalised: 'the sorter must not be the composer' -- a module-level "
      "mutable lets a reference drift with the thing it is checking",
      "_C = None\ndef get():\n    global _C\n    _C = build()\n    return _C\n",
      "_C = None\ndef get():\n    return build(_C)\n",
      n_bad=1, n_ok=1)
def _singleton(src: str, *_: Any) -> tuple[list[str], int]:
    """The subject is every module-level binding that COULD be rebound from inside a
    function -- not the rebindings themselves. Counting only violations makes subject
    and violation the same set, so the rule can never report PASS and a clean file is
    indistinguishable from one with nothing to check. That is the guaranteed number in
    a rule's own denominator."""
    tree = ast.parse(src)
    seen = sum(1 for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign)))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            out.extend(f"`{n}`: module-level state rebound inside a function"
                       for n in node.names)
    return out, seen


@rule("NOFAIL",
      "Step 2: 'a bin without its discriminator is a label, not a diagnosis' -- a check "
      "with no failing path is a label",
      "def helper(x):\n    return True\n"
      "def check_x(rows):\n    return True\n",
      "def helper(x):\n    return True\n"
      "def check_x(rows):\n    for r in rows:\n        if r:\n            return False\n"
      "    return True\n",
      n_bad=1, n_ok=1)
def _nofail(src: str, *_: Any) -> tuple[list[str], int]:
    """A function named like a check whose returns are all truthy constants cannot ever
    report a defect, and reports PASS for work it did not do."""
    out, seen = [], 0
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not (fn.name.startswith("check") or fn.name.startswith("_check")
                or fn.name.endswith("_check")):
            continue
        rets = [r.value for r in ast.walk(fn) if isinstance(r, ast.Return)]
        if not rets:
            continue
        seen += 1
        consts = [r for r in rets if isinstance(r, ast.Constant)]
        if len(consts) == len(rets) and all(bool(c.value) for c in consts):
            out.append(f"`{fn.name}`: every return is a truthy constant; it cannot fail")
    return out, seen


@rule("ISOLATED",
      "'No isolated code. No silent code. No code without reason.'",
      # BOTH directions of the exemption. `sniff` uses startswith on something that is
      # NOT a namespace listing, so `head_` must not become a convention and head_dead
      # must still be flagged -- which is the poisoning this rule inflicted on itself,
      # now a fixture rather than a memory. And the control holds a REAL registry, so a
      # scope tightened until it exempts nothing would fail the control instead.
      "def used():\n    return 1\n"
      "def never():\n    return 2\n"
      "def sniff(n):\n    return n.startswith('head_')\n"
      "def head_dead():\n    return 3\n"
      "@reg\ndef decorated_dead():\n    return 4\n"
      "print(used(), sniff)\n",
      "def used():\n    return 1\n"
      "def test_a():\n    return 2\n"
      "fns = [v for k, v in globals().items() if k.startswith('test_')]\n"
      "print(used(), fns)\n",
      n_bad=4, n_ok=1, crossfile=True)
def _isolated(src: str, others: tuple[str, ...] = ()) -> tuple[list[str], int]:
    """Defined and referenced nowhere in the package. Cross-file by nature, which is why
    it cannot be a per-file ruff rule."""
    tree = ast.parse(src)
    # a DECORATED definition is registered by its decorator -- that is what a decorator
    # is for -- so its name need never appear again. Flagging it would report the
    # registry pattern as dead code, which is a rule firing on correct code: worse than
    # no rule, because it trains you to ignore the output.
    defined = {n.name: n.lineno for n in tree.body
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and not n.name.startswith("__") and not n.decorator_list}
    used: set[str] = set()
    conventions: set[str] = set()          # prefixes a registry collects by name
    for text in (src, *others):
        # `[v for k, v in globals().items() if k.startswith("test_")]` registers by
        # convention rather than by reference, the way a decorator registers by call.
        # Both are real uses. But a prefix only counts as a registry if it is applied to
        # a NAMESPACE listing -- otherwise this rule's own `startswith("check")` would
        # exempt every name ending in check, including the dead one it should catch.
        for stmt in ast.walk(ast.parse(text)):
            if not isinstance(stmt, ast.stmt):
                continue
            sub = list(ast.walk(stmt))
            listing = any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                          and c.func.id in ("globals", "vars", "dir") for c in sub)
            if not listing:
                continue
            for c in sub:
                if (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)
                        and c.func.attr in ("startswith", "endswith")):
                    conventions.update(a.value for a in c.args
                                       if isinstance(a, ast.Constant)
                                       and isinstance(a.value, str))
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, ast.Name):
                used.add(n.id)
            elif isinstance(n, ast.Attribute):
                used.add(n.attr)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str):
                used.update(n.value.split())        # registries, __all__
    out, seen = [], 0
    for name in defined:
        if any(name.startswith(c) or name.endswith(c) for c in conventions if c):
            continue                       # collected by convention
        seen += 1
        refs = sum(text.count(name) for text in (src, *others))
        if name not in used or refs <= 1:
            out.append(f"`{name}`: defined and referenced nowhere in the package")
    return out, seen


# ---------------------------------------------------------------------------------------
# WHAT A STATIC PASS CANNOT SEE. Named with the seat that covers it, or why none does.
# ---------------------------------------------------------------------------------------

BLIND: dict[str, tuple[str, str]] = {
    "B10": ("ELSEWHERE", "the layer boundary -- ruff TID251 bans in pyproject, natively"),
    "A2": ("ELSEWHERE", "the bargain pays -- kernel.Linter, over the record"),
    "A3": ("ELSEWHERE", "pays is not closes -- kernel.Linter"),
    "A4": ("ELSEWHERE", "the three causes of a low reading -- kernel.Linter"),
    "A5": ("ELSEWHERE", "a candidate is held, not cited -- kernel.Linter"),
    "A6": ("ELSEWHERE", "a label partitions its sites -- kernel.Linter"),
    "A7": ("ELSEWHERE", "R is never aggregated -- kernel.Linter, via `of` on each row"),
    "A8": ("ELSEWHERE", "origin and time on the stamp -- kernel.Linter"),
    "B1": ("ELSEWHERE", "unreached is not unreachable -- kernel.Linter and gate check 9"),
    "B2": ("ELSEWHERE", "a gate passing is not the ground -- kernel.Linter"),
    "B3": ("ELSEWHERE", "the bet is on b, not o' -- kernel.Linter"),
    "B4": ("ELSEWHERE", "the guards are a product -- kernel.Linter and gate check 5"),
    "B5": ("ELSEWHERE", "support at zero is an instruction -- kernel.Linter"),
    "B6": ("ELSEWHERE", "the surprise integral is monotone -- kernel.Linter"),
    "B15": ("ELSEWHERE", "the mode is declared on every row -- gate check 6"),
    "B7": ("NO-BEHAVIOUR", "F requires a pose -- step 6 is not built"),
    "B8": ("NO-BEHAVIOUR", "shadow then echo -- step 6 is not built"),
    "B9": ("NO-BEHAVIOUR", "generators cross, playback never -- step 6 is not built"),
    "B11": ("NO-BEHAVIOUR", "the library is restructured -- no refactor operator exists"),
    "B12": ("NO-BEHAVIOUR", "the habitat is enumerated -- no habitat type exists"),
    "A1": ("NOT-EXPRESSIBLE", "closure generated not stored -- keying on the identifier "
                              "`closure` goes blind on a rename, silently"),
    "A9": ("NOT-EXPRESSIBLE", "the reference is not the subject -- SINGLETON catches the "
                              "commonest shape; the general property is not static"),
    "A6i": ("NOT-EXPRESSIBLE", "one label covering two mechanisms -- a property of the "
                               "code, invisible to a record AND to a shape pass"),
    "B13": ("NOT-EXPRESSIBLE", "the ground is not a frame -- injection is visible, "
                               "nature is not"),
    "B14": ("NOT-CHECKABLE", "a seat is not a person -- a reading discipline"),
    "B16": ("NOT-CHECKABLE", "R is always a slice -- a reading discipline"),
}


# ---------------------------------------------------------------------------------------


def selftest() -> dict[str, str]:
    out = {}
    for r in RULES:
        try:
            bad, nb = r.fn(r.bad)
            ok, no = r.fn(r.ok)
        except Exception as e:                                   # noqa: BLE001
            out[r.rid] = f"UNWITNESSED ({type(e).__name__}: {e})"
            continue
        if not bad:
            out[r.rid] = "UNWITNESSED (the witness produced no finding)"
        elif ok:
            out[r.rid] = f"UNWITNESSED (the control produced {len(ok)})"
        elif r.n_ok == 0:
            # a control that examines NOTHING cannot demonstrate a clean state: subject
            # and violation are the same set, PASS is unreachable, and VACUOUS quietly
            # does its work. This is the check on the checkers, read off the fixture.
            out[r.rid] = "UNWITNESSED (the control examines nothing; PASS unreachable)"
        elif (nb, no) != (r.n_bad, r.n_ok):
            out[r.rid] = f"UNWITNESSED (counted {nb}/{no}, the fixtures hold {r.n_bad}/{r.n_ok})"
        else:
            out[r.rid] = "ok"
    return out


def run(paths: list[Path]) -> dict[str, dict]:
    trusted = {k for k, v in selftest().items() if v == "ok"}
    srcs = {p: p.read_text(encoding="utf-8") for p in paths}
    res: dict[str, dict] = {}
    for r in RULES:
        if r.rid not in trusted:
            res[r.rid] = {"status": SUPPRESSED, "why": ["its witness did not fire"]}
            continue
        found, seen = [], 0
        for p, src in srcs.items():
            others = tuple(v for q, v in srcs.items() if q != p) if r.crossfile else ()
            try:
                f, n = r.fn(src, others)
            except SyntaxError as e:
                found.append(f"{p.name}: unparseable -- {e}")
                continue
            found += [f"{p.name}: {x}" for x in f]
            seen += n
        if found:
            res[r.rid] = {"status": FAIL, "why": found}
        elif seen == 0:
            res[r.rid] = {"status": VACUOUS, "why": ["examined 0 candidates"]}
        else:
            res[r.rid] = {"status": PASS, "why": [f"{seen} candidates examined"]}
    return res


def report(paths: list[Path]) -> int:
    res = run(paths)
    rank = {FAIL: 0, SUPPRESSED: 1, VACUOUS: 2, PASS: 3}
    for rid in sorted(res, key=lambda r: (rank[res[r]["status"]], r)):
        print(f"  {rid:<10} {res[rid]['status']}")
        for w in res[rid]["why"][:6]:
            print(f"             {w}")
        if len(res[rid]["why"]) > 6:
            print(f"             ... and {len(res[rid]['why']) - 6} more")
    n = {s: sum(1 for v in res.values() if v["status"] == s) for s in rank}
    kinds: dict[str, int] = {}
    for k, _ in BLIND.values():
        kinds[k] = kinds.get(k, 0) + 1
    print(f"\n  {n[PASS]} pass · {n[FAIL]} fail · {n[VACUOUS]} vacuous "
          f"· {n[SUPPRESSED]} suppressed")
    print(f"  {len(RULES)} rules carry a witness. {len(BLIND)} properties this pass "
          "cannot see:")
    for k in ("ELSEWHERE", "NO-BEHAVIOUR", "NOT-EXPRESSIBLE", "NOT-CHECKABLE"):
        print(f"    {kinds.get(k, 0):>2} {k}")
    print("  A static pass is single-frame: no promotion, no import, no second scale.")
    return 1 if n[FAIL] else 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        for rid, v in sorted(selftest().items()):
            print(f"  {rid:<10} {v}")
        return 0
    if "--blind" in argv:
        for rid, (kind, why) in sorted(BLIND.items()):
            print(f"  {rid:<5} {kind:<16} {why}")
        return 0
    args = [a for a in argv if not a.startswith("--")]
    root = Path(__file__).parent
    paths = [Path(a) for a in args] if args else sorted(root.glob("*.py"))
    print(f"lint: {len(paths)} file(s)\n")
    return report(paths)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
