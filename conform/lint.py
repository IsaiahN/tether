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

WHY A STATIC SEAT EXISTS AT ALL, given it catches a fraction of what a record-reader
does. Because there is a class only structure can see:

    A COUPLING THAT PRODUCES THE RIGHT ANSWER IS INVISIBLE TO ANY TEST OF RESULTS.

snaps imported world's atom set. Every value identical, every output correct, every
check green -- and `in_closure`, the denominator under every abstention number snaps
reports, was defined against a vocabulary chosen for a different world. Change one and
the other moves silently. No ledger check can find that, because nothing in the record
is wrong; the defect is the dependency, not the value.

The record-readers test what the code DID. This tests what it is ATTACHED TO. A boundary
crossing that happens to agree is findable only by the second, and it stays findable
only while it stays green -- once the values diverge it is a bug anyone can see, and by
then it has been load-bearing for months.

AND HOW TO WITNESS A CHECKER, which is not the same as witnessing a rule:

    A WITNESS FOR A CHECKER MUST REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK.

Disabling the check tests that the check exists. Reintroducing the defect tests that the
harness can REACH it -- and the second is the property in question, because "found
nothing because the subject is clean" and "found nothing because the harness cannot go
red" produce identical output. Two states, one report, which is the same structural
argument as VACUOUS and as the denominator witness.

Learned by doing the wrong one: breaking A5's implementation found nothing, correctly,
because unbind-on-hold had already fixed the defect at source. Only breaking the FRAME
showed the harness could reach the case.

AND ONE THAT IS NOT ABOUT GOING QUIET, but about layers:

    A REPAIR CAN SATISFY ITS OWN LAYER AND VIOLATE THE CONTRACT AT THE LAYER ABOVE.

Making an unchecked file exit non-zero was right here and routed it to check.py's FAIL
branch, which attaches a cause -- so `lint FAIL: dead code, an unanchored constant, or a
singleton` when the truth was that a file did not parse. Correct locally, wrong at the
boundary, and the boundary is where the cause gets asserted. It recreated the defect that
had been fixed one commit earlier.

The repair for THAT is worth stating too, because it is the substitution this whole
exercise has been removing:

    AN EXIT CODE IS A DECLARATION. A PATTERN MATCH OVER STDOUT IS A GUESS.

Three codes, not a better filter: 0 clean, 1 found something, 2 could not check
everything -- matching the three states inside each seat.

THESE SEVEN ARE A RECORD OF HOW THIS CHECKER FAILED, not a philosophy of checkers. Every
one came from a defect and none from reasoning about what a good checker should do. Four
name a site where a checker goes quiet, the fifth names where one lies instead, and the
sixth names where a measurement is invented that never had to be:

    fixtures before changes             an ordering with an observable half-state
    witness the boundary, not the rule  exemptions and denominators, never decisions
    exemptions as data, not logic       a table can be pinned; logic widens quietly
    reintroduce, never disable          tests reach rather than existence
    a repair can break the layer above  and the layer above is where causes are asserted
    assume it is already specified      an improvised metric is fitted to the case that
                                        prompted it
    the metric's subject must not move  a denominator the mechanism changes measures
                                        itself

THE SIXTH IS A DEFAULT RATHER THAN A CAUTION, on nine instances where the corpus had
already named the instrument and the specified one was better every time:

    lib ok here / lib          for `chunk reuse count` -- and its denominator can only
                               grow under a never-delete library, so it could not rise
                               whatever the loop did
    depth_exhausted at rung 0  for `UNREACHED`, which is reserved for after an escalation
                               ladder of five priced rungs that was never built
    an extension-class index   for retrieval keyed by residual shape -- arity, symmetry,
                               scale, effect shape -- which needs nothing materialised
    R_T as a row               where the ruling says it is the admission criterion
    a boundary revert          where reset-vs-advance was the stated discriminator

**The design step is a search of the corpus, not a design.** Every one of these was built
first and found afterwards.

THE SEVENTH is the one that cost a correct mechanism. STAGE 1 moved the claim from MINT to
SETTLE -- the corpus's own `if nothing settled it, the result is a candidate` -- and was
graded by `false_mint_rate`, which is computed OVER CLAIMS. A mechanism that converts
claims into candidates moves the numerator and the denominator together, so the rate could
not detect it, read null, and the mechanism was reverted.

    before pinning a falsifier, ask whether the mechanism moves the quantity the
    metric is computed over. if it does, the metric is measuring itself.

    python lint.py              check this repo
    python lint.py --selftest   witnesses only
    python lint.py --blind      what a static pass cannot see, and who can
"""

from __future__ import annotations

import ast
import io
import sys
import tokenize
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

PASS, FAIL, VACUOUS, SUPPRESSED = "PASS", "FAIL", "VACUOUS", "SUPPRESSED"

# Runners that collect by convention from OUTSIDE the package, where no in-package
# reference exists to find. (module suffix, name prefix) -- both must match, which is
# what keeps the exemption from swallowing an orphan that merely looks like a test.
# An exemption expressed as DATA is one a fixture can pin; expressed as logic it widens
# quietly, which is how this rule swallowed its own real finding once already.
COLLECTORS = (
    ("test_", "test_"),      # pytest functions, in a pytest module
    ("_test.py", "test_"),
    ("test_", "Test"),       # pytest classes, in a pytest module
    ("_test.py", "Test"),
    ("", "pytest_"),         # pytest hooks: a documented namespace, any module
    ("stateful", "teardown"), # hypothesis calls it on a RuleBasedStateMachine
)


def _collected(fname: str, name: str) -> bool:
    """Collected by a runner OUTSIDE the package, where no in-package reference exists
    to find. An empty module pattern means the name alone is the convention, which is
    true only of the hook namespace -- and is pinned by a fixture so it cannot spread."""
    return any((not mod or mod in fname) and name.startswith(pre)
               for mod, pre in COLLECTORS)


@dataclass
class Rule:
    rid: str
    cite: str
    fn: Callable[..., tuple[list[str], int]]
    bad: str
    ok: str
    n_bad: int
    n_ok: int
    # the denominator alone cannot witness WHICH defect a rule reaches: "bad produced
    # findings" holds just as well when it found six of seven. A rule that quietly stops
    # catching one shape keeps its seen count and keeps producing findings, so the count
    # that has to move is this one.
    n_found: int = 0
    crossfile: bool = False
    bad_name: str = "mod.py"       # the fixture's filename: some exemptions depend on it
    ok_name: str = "mod.py"
    # a SECOND file, for a rule whose subject is the package rather than the file. Until
    # this existed a crossfile rule was witnessed with others=(), so the half of it that
    # reads other files was never exercised by its own fixture.
    bad_other: tuple[str, str] | None = None
    ok_other: tuple[str, str] | None = None


RULES: list[Rule] = []


def rule(rid, cite, bad, ok, *, n_bad, n_ok, n_found=0, crossfile=False,
         bad_name="mod.py", ok_name="mod.py", bad_other=None, ok_other=None):
    def deco(fn):
        RULES.append(Rule(rid, cite, fn, bad, ok, n_bad, n_ok, n_found, crossfile,
                          bad_name, ok_name, bad_other, ok_other))
        return fn
    return deco


# ---------------------------------------------------------------------------------------


@rule("ANCHOR",
      "DECLARING THE MODE: 'an unmeasured number is a specification of what to measure "
      "and can be worth a great deal' -- labelled as such, which is the whole condition",
      # a comment separated by a BLANK LINE is attached to nothing, so both constants
      # below must still be flagged. Widen the exemption to "an anchor anywhere in the
      # file" and the witness stops producing findings; drop the block form and the
      # control starts producing them. Both edges of the attachment rule.
      "ONE = 1\n"
      "# anchor: attached to nothing\n"
      "\n"
      "EPS = 0.02\n"
      "WARM = 12\n"
      "class Cfg:\n    depth: int = 3\n",
      "ONE = 1\n"
      "# anchor: human play completes a level in <500 actions; this is the 2x ceiling\n"
      "EPS = 0.02\n"
      "WARM = 12  # anchor: same measurement, stated inline\n"
      "class Cfg:\n"
      "    # anchor: the depth at which the falsifier sits one step past\n"
      "    depth: int = 3\n",
      n_bad=3, n_ok=3, n_found=3)
def _anchor(src: str, *_: Any) -> tuple[list[str], int]:
    """A constant with no stated basis is an invented metric. Comments are invisible to the
    AST, so this is one of the few things only a token pass can see.

    THE SUBJECT IS MODULE LEVEL **AND CLASS FIELDS**. It was module level alone, and the
    two numbers that set the whole search -- `Config.max_depth` and `Config.budget` -- are
    dataclass field defaults, so the rule could not see the place its property mattered
    most. Sixth time a rule's subject turned out narrower than the property it states.

    NOT default arguments, and that is a scope decision rather than an oversight: fifteen
    exist in this package and most are harness conveniences overridden at every call site.
    A rule widened until it fires on everything is the lesson ISOLATED taught by inflicting
    it on itself. **The form is named here so the gap is known rather than rediscovered.**
    """
    # A basis may need more than one line, so a contiguous comment block IMMEDIATELY
    # above counts as well as a same-line comment. Immediately: a blank line between
    # them means the comment is attached to whatever preceded it, not to this constant.
    comments: set[int] = set()
    anchors: set[int] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                comments.add(tok.start[0])
                if "anchor:" in tok.string:
                    anchors.add(tok.start[0])
    except (tokenize.TokenError, IndentationError):
        pass
    anchored = set(anchors)
    for ln in sorted(anchors):
        row = ln + 1
        while row in comments:          # walk down through the rest of the block
            row += 1
        anchored.add(row)               # the statement the block sits directly above
    out, seen = [], 0
    tree = ast.parse(src)
    # module level, plus one level into any class body. A field default is a constant that
    # happens to live behind a name, and the name being lowercase is a convention about
    # where it sits rather than about what it does.
    subject = list(tree.body)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            subject += node.body
    for node in subject:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            t, v = node.target, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            t, v = node.targets[0], node.value
        else:
            continue
        if not isinstance(t, ast.Name):
            continue
        if not (t.id.isupper() or isinstance(node, ast.AnnAssign)):
            continue
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


@rule("REACH",
      "A1: 'closure(Gamma) -- everything expressible by combining the primitives, at any "
      "depth' -- generated, never a second producer",
      # THE PROPERTY, NOT THE PROXY. `nothing is stored` is what an effect-index breaks
      # while leaving A1's actual guarantee intact, so the subject is the two things
      # storing the closure would have destroyed: a second writer for the library, and a
      # second place that extends an atom sequence.
      #
      # `memo` in the control is the discrimination. It stores what the generator
      # produced, which the proxy forbids and the property allows -- it composes nothing
      # and writes nothing, so reach still has one producer and the library one writer.
      "class G:\n"
      "    def accept(self, t):\n        self.library[t.name] = t\n"
      "    def enumerate_closure(self, d):\n"
      "        for u in self.units:\n            yield Term(self.chain + u.atoms)\n"
      "    def precompute(self):\n"
      "        return [self.chain + u.atoms for u in self.units]\n",
      "class G:\n"
      "    def accept(self, t):\n        self.library[t.name] = t\n"
      "    def enumerate_closure(self, d):\n"
      "        for u in self.units:\n            yield Term(self.chain + u.atoms)\n"
      "    def memo(self):\n"
      "        return list(self.enumerate_closure(3))\n",
      n_bad=3, n_ok=2, n_found=2, crossfile=True,
      # the second writer sits in ANOTHER FILE, because that is where it would really
      # appear: the loop reaching past accept() to write the library directly. Per-file
      # counting sees one writer in each and reports nothing.
      bad_other=("loop.py", "def bind(g, t):\n    g.library[t.name] = t\n"),
      ok_other=("loop.py", "def read(g, n):\n    return g.library[n]\n"))
def _reach(src: str, others: tuple = (), _scan=None, name: str = "") -> tuple[list, int]:
    """Two clauses, both about who is allowed to act rather than about what exists."""
    files = {name or "mod.py": src}
    for fname, text in others:
        files.setdefault(fname, text)

    def sites(text):
        """(library-write function names, [(function name, is a generator)] compositions).
        Walks with the innermost enclosing function, so a nested def is not credited to
        its parent."""
        writes, comps = set(), []

        def walk(node, fn, gen):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    sub_gen = any(isinstance(x, (ast.Yield, ast.YieldFrom))
                                  for x in ast.walk(child))
                    walk(child, child.name, sub_gen)
                    continue
                if isinstance(child, ast.Assign):
                    for t in child.targets:
                        if (isinstance(t, ast.Subscript)
                                and isinstance(t.value, ast.Attribute)
                                and t.value.attr == "library"):
                            writes.add(fn)
                if (isinstance(child, ast.BinOp) and isinstance(child.op, ast.Add)
                        and any(isinstance(x, ast.Attribute) and x.attr == "atoms"
                                for x in (child.left, child.right))):
                    comps.append((fn, gen))
                walk(child, fn, gen)
        walk(ast.parse(text), "<module>", False)
        return writes, comps

    here_w, here_c = sites(src)
    everywhere = set()
    for text in files.values():
        everywhere |= sites(text)[0]

    out = []
    if here_w and len(everywhere) > 1:
        out.append(f"the library has {len(everywhere)} writers {sorted(everywhere)}: "
                   "accept() is not its only writer, so a stored reach is indistinguishable "
                   "from the library")
    for fn, gen in here_c:
        if not gen:
            out.append(f"`{fn}` extends an atom sequence and does not yield: reach has a "
                       "second producer, so enumerate_closure is not the only one")
    return out, len(here_w) + len(here_c)


@rule("ISOLATED",
      "'No isolated code. No silent code. No code without reason.'",
      # BOTH directions of the exemption. `sniff` uses startswith on something that is
      # NOT a namespace listing, so `head_` must not become a convention and head_dead
      # must still be flagged -- which is the poisoning this rule inflicted on itself,
      # now a fixture rather than a memory. And the control holds a REAL registry, so a
      # scope tightened until it exempts nothing would fail the control instead.
      # `prosed` is named in an ENGLISH SENTENCE and nowhere else, which is how a
      # docstring-heavy package exempts every ordinary-word identifier it owns.
      # `orphan` is a METHOD, which the rule could not see while it read tree.body.
      "\"\"\"A note on prosed, and why the thing works.\"\"\"\n"
      "def used():\n    return 1\n"
      "def never():\n    return 2\n"
      "def prosed():\n    return 7\n"
      "def sniff(n):\n    return n.startswith('head_')\n"
      "def head_dead():\n    return 3\n"
      "@reg\ndef decorated_dead():\n    return 4\n"
      "def test_orphan():\n    return 5\n"
      "def pytestish():\n    return 6\n"
      "class Testish:\n    pass\n"
      "def teardown():\n    return 10\n"
      "class Holder:\n"
      "    def orphan(self):\n        return 8\n"
      "    def spoken(self):\n        return 9\n"
      "print(used(), sniff, Holder)\n",
      # the control keeps BOTH shapes alive: `livewire` is named by a registry string,
      # which is a real reference; `alive` is a method that is called. Tighten the
      # string rule until it exempts nothing and livewire is flagged here instead.
      "def used():\n    return 1\n"
      "def exported():\n    return 6\n"
      "def livewire():\n    return 4\n"
      "REG = {'livewire': livewire}\n"
      "def test_a():\n    return 2\n"
      "def pytest_configure():\n    return 3\n"
      "class TestThing:\n    pass\n"
      "class Keeper:\n"
      "    def alive(self):\n        return 5\n"
      "print(used(), REG, Keeper().alive())\n",
      n_bad=12, n_ok=5, n_found=8, crossfile=True,
      # BOTH DIRECTIONS OF THE SCOPE. `stranger` spells `never` and does not import the
      # module that defines it, so `never` must still be flagged -- the shape that had
      # `world.py`'s "ladder" slot clearing `snaps.ladder`. `consumer` DOES import, and
      # `exported` is referenced from nowhere else, so a scope tightened to the defining
      # module alone flags it and the control fires instead.
      bad_other=("stranger.py",
                 'SLOTS = {"never": 1}\nprint(SLOTS, SLOTS.spoken)\n'),
      ok_other=("consumer.py",
                'import test_thing\nprint(test_thing.exported())\n'),
      # THE FILENAMES ARE PART OF THE FIXTURE. bad is NOT a collector module, so its
      # `test_orphan` must still be flagged; ok IS one, so its `test_a` must not be.
      # Three ways the exemption can move and all three break a count:
      #   it vanishes            -> ok's test_a is flagged      -> the control fires
      #   it widens by name only -> bad's test_orphan is exempt -> bad examines 6 not 7
      # The two module-independent shapes are pinned the same way:
      # `pytestish` and `Testish` sit in a NON-collector module and
      # must still be flagged, so the hook prefix cannot loosen from
      # `pytest_` to `pytest`, and the class row cannot stop requiring
      # a collector module.
      #   it widens by module    -> ok's `used` is exempt       -> ok examines 0 not 1
      bad_name="helpers.py", ok_name="test_thing.py")
def _isolated(src: str, others: tuple[str, ...] = (),
              scan: tuple[Counter, set] | None = None,
              name: str = "") -> tuple[list[str], int]:
    """Defined and referenced nowhere in the package. Cross-file by nature, which is why
    it cannot be a per-file ruff rule.

    The package is scanned ONCE and cached on the identity of the source tuple: scanning
    it per file is quadratic, and at 541 files that is 292k parses rather than 541.
    Self-references are subtracted exactly -- a recursive function refers to itself, and
    a count threshold guessing at that is the kind of approximation that goes quiet.
    """
    fname = name
    tree = ast.parse(src)
    # a DECORATED definition is registered by its decorator -- that is what a decorator
    # is for -- so its name need never appear again. Flagging it would report the
    # registry pattern as dead code, which is a rule firing on correct code: worse than
    # no rule, because it trains you to ignore the output.
    # tree.body ONLY was module scope, so every method in the package sat outside the
    # subject -- and a method is reached by attribute, which this already counts. Class
    # bodies are walked one level down; deeper nesting is a closure, not an interface.
    top = [n for n in tree.body
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    meths = [m for n in top if isinstance(n, ast.ClassDef) for m in n.body
             if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
    defined = {n.name: n for n in top + meths
               if not n.name.startswith("__") and not n.decorator_list}
    is_method = {m.name for m in meths}
    if not defined:
        return [], 0
    per, imports, conventions = (scan if scan is not None
                                 else _scan(((fname, src), *others)))
    mod = fname[:-3] if fname.endswith(".py") else fname
    # A MODULE-LEVEL NAME MUST BE IMPORTED TO BE USED; A METHOD MUST NOT. The first is
    # reached through the module namespace, so a module that never imports this one
    # cannot mean this name whatever word it spells -- which is how `world.py`'s
    # "ladder" slot was clearing `snaps.ladder` two files away. The second is reached
    # through an OBJECT: `agent.phases.level_done()` names instruments from a file that
    # never imports it, and `world.bind` reaches a Snap method by getattr over a string.
    # Scoping methods by imports invents dead code instead of finding it.
    visible = {mod} | {m for m, imp in imports.items() if mod in imp}
    scoped: Counter = Counter()
    for m in visible:
        scoped.update(per.get(m, Counter()))
    package: Counter = Counter()
    for c in per.values():
        package.update(c)
    out, seen = [], 0
    for name, node in defined.items():
        if any(name.startswith(c) or name.endswith(c) for c in conventions if c):
            continue                       # collected by an in-package registry
        if _collected(fname, name):
            continue                       # collected by an external runner
        seen += 1
        own = sum(1 for n in ast.walk(node)
                  if (isinstance(n, ast.Name) and n.id == name)
                  or (isinstance(n, ast.Attribute) and n.attr == name))
        refs = package if name in is_method else scoped
        if refs.get(name, 0) - own <= 0:
            where = ("the package" if name in is_method
                     else "any module that imports this one")
            out.append(f"`{name}`: defined and referenced nowhere in {where}")
    return out, seen


def _scan(files: tuple[tuple[str, str], ...]) -> tuple[dict, dict, set]:
    """(per-module reference counts, per-module imports, registry prefixes).

    Counts are kept PER MODULE rather than summed over the package, because a bare name
    matched everywhere lets any module clear a dead definition in any other. `world.py`
    holds `RULES = {"ladder": _ladder}` naming a slot; that string was clearing
    `snaps.ladder`, an unrelated and genuinely dead function two files away.

    Called ONCE per run and the result handed to the rule, rather than cached: keying a
    cache on id() of a transient tuple is unsound, because CPython reuses the address
    after the tuple is freed -- the control fixture got the witness's scan and the rule
    suppressed itself. Which is the witness working, on the optimisation that broke it.
    """
    per: dict[str, Counter] = {}
    imports: dict[str, set[str]] = {}
    conventions: set[str] = set()
    for fname, text in files:
        mod = fname[:-3] if fname.endswith(".py") else fname
        refs = per.setdefault(mod, Counter())
        seen_imports = imports.setdefault(mod, set())
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                seen_imports.update(a.name.split(".")[-1] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                seen_imports.add(n.module.split(".")[-1])
        # `[v for k, v in globals().items() if k.startswith("test_")]` registers by
        # convention rather than by reference, the way a decorator registers by call.
        # Both are real uses. But a prefix only counts as a registry if it is applied to
        # a NAMESPACE listing -- otherwise this rule's own `startswith("check")` would
        # exempt every name ending in check, including the dead one it should catch.
        for stmt in ast.walk(tree):
            if not isinstance(stmt, ast.stmt):
                continue
            sub = list(ast.walk(stmt))
            if not any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                       and c.func.id in ("globals", "vars", "dir") for c in sub):
                continue
            for c in sub:
                if (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)
                        and c.func.attr in ("startswith", "endswith")):
                    conventions.update(a.value for a in c.args
                                       if isinstance(a, ast.Constant)
                                       and isinstance(a.value, str))
        for n in ast.walk(tree):
            if isinstance(n, ast.Name):
                refs[n.id] += 1
            elif isinstance(n, ast.Attribute):
                refs[n.attr] += 1
            # A REGISTRY NAMES ONE THING; PROSE MENTIONS MANY. Splitting on whitespace
            # made every word of every docstring a reference, so an identifier that is
            # also an ordinary English word could never be flagged -- and the better the
            # prose, the wider the hole. The whole string must BE the identifier:
            # `{"ladder": _ladder}` still counts, `"a DS-controlled level ladder"` does
            # not.
            elif (isinstance(n, ast.Constant) and isinstance(n.value, str)
                  and n.value.isidentifier()):
                refs[n.value] += 1
    return per, imports, conventions


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
    "A9": ("NOT-EXPRESSIBLE", "the reference is not the subject -- SINGLETON catches the "
                              "commonest shape; the general property is not static"),
    "A6i": ("NOT-EXPRESSIBLE", "one label covering two mechanisms -- a property of the "
                               "code, invisible to a record AND to a shape pass. TWO "
                               "INSTANCES FOUND 2026-08-26: `molecule` is a prior term in "
                               "gamma and a quantified objective in DISCOVERY Q21; "
                               "`DIRECTED` is `by == discriminate` here and `bets with "
                               "bound terms` in ARC_AGENT 22.2, which read 9% and 37% on "
                               "the same runs. BOTH SURFACED WHERE A HEADLINE WAS ABOUT "
                               "TO BE MADE, and neither was catchable in advance"),
    "B13": ("NOT-EXPRESSIBLE", "the ground is not a frame -- injection is visible, "
                               "nature is not"),
    "B14": ("NOT-CHECKABLE", "a seat is not a person -- a reading discipline"),
    "B16": ("NOT-CHECKABLE", "R is always a slice -- a reading discipline"),
    "B17": ("NOT-CHECKABLE", "PRE-REGISTRATION DOES NOT PROTECT A READING IF THE "
                             "INSTRUMENT MEASURES SOMETHING ELSE -- a reading discipline, "
                             "and the one with no signature. A wrong denominator has one; "
                             "a null the panel can only produce has one; this looks "
                             "exactly like a correct result AND THE PRE-REGISTRATION IS "
                             "WHAT MAKES IT CONVINCING. Cost nothing on the phase sweep "
                             "only because 9-vs-37 is impossible to miss; 15-vs-18 passes "
                             "straight through"),
}


# ---------------------------------------------------------------------------------------


def selftest() -> dict[str, str]:
    out = {}
    for r in RULES:
        try:
            bad, nb = r.fn(r.bad, (r.bad_other,) if r.bad_other else (), None, r.bad_name)
            ok, no = r.fn(r.ok, (r.ok_other,) if r.ok_other else (), None, r.ok_name)
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
        elif r.n_found and len(bad) != r.n_found:
            # WHICH defects the rule reaches, not merely that it reaches one. A rule that
            # stops catching a single shape keeps its denominator and still produces
            # findings, so nothing above this line moves. Opt-in: a rule that has not
            # pinned its findings leaves n_found at 0 and is checked as before.
            out[r.rid] = (f"UNWITNESSED (the witness produced {len(bad)} findings, "
                          f"the fixture pins {r.n_found})")
        else:
            out[r.rid] = "ok"
    return out


def run(paths: list[Path]) -> dict[str, dict]:
    """Returns one entry per rule, plus `_unusable` -- files that could not be read or
    parsed, which is neither a pass nor a finding about them."""
    trusted = {k for k, v in selftest().items() if v == "ok"}
    # A file becomes a SUBJECT by being read AND parsed, and it can fail at either.
    # Decode, I/O and syntax are three routes to the same state: not checked. Leaving
    # syntax in the rule loop reported it four times over -- once per rule, each with an
    # asserted cause about the code -- and took the board from three clean rules to zero.
    srcs, unusable = {}, []
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8")
            ast.parse(text)
        except (UnicodeDecodeError, OSError) as e:
            unusable.append(f"{p.name}: {type(e).__name__}")
        except SyntaxError as e:
            unusable.append(f"{p.name}: SyntaxError line {e.lineno}")
        else:
            srcs[p] = text
    allsrc = tuple((p.name, src) for p, src in srcs.items())
    shared = _scan(allsrc)          # once per run, handed in rather than cached
    res: dict[str, dict] = {}
    for r in RULES:
        if r.rid not in trusted:
            res[r.rid] = {"status": SUPPRESSED, "why": ["its witness did not fire"]}
            continue
        found, seen = [], 0
        for p, src in srcs.items():
            others = allsrc if r.crossfile else ()
            # no SyntaxError guard here: a file that does not parse never enters
            # `srcs`, so by this point every source is a real subject
            f, n = (r.fn(src, others, shared, p.name) if r.crossfile else r.fn(src))
            found += [f"{p.name}: {x}" for x in f]
            seen += n
        if found:
            res[r.rid] = {"status": FAIL, "why": found}
        elif seen == 0:
            res[r.rid] = {"status": VACUOUS, "why": ["examined 0 candidates"]}
        else:
            res[r.rid] = {"status": PASS, "why": [f"{seen} candidates examined"]}
    res["_unusable"] = unusable
    return res


def report(paths: list[Path]) -> int:
    res = run(paths)
    unusable = res.pop("_unusable", [])
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
    if unusable:
        print(f"  {len(unusable)} file(s) could not be read or parsed, so were not "
              "checked: " + ", ".join(unusable[:4]))
    # THREE EXIT CODES, because there are three outcomes. 0 clean · 1 found something ·
    # 2 could not check everything. A file that could not be checked has not passed, but
    # it is not a finding about the code either, and collapsing it into 1 makes the
    # caller assert a cause it never observed.
    if n[FAIL]:
        return 1
    return 2 if unusable else 0


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
    # the repo, not this folder: the rule set is about the build it grades, and a
    # checker that only scanned its own directory would report a clean package
    root = Path(__file__).parent.parent
    paths = ([Path(a) for a in args] if args else
             sorted(p for p in root.rglob("*.py")
                    if ".venv" not in p.parts and "runs" not in p.parts))
    print(f"lint: {len(paths)} file(s)\n")
    return report(paths)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
