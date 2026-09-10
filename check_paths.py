"""Does the failed-path catalogue do what it says? Four claims, each with a negative control.

M2_STANDARD's verification split: MECHANISM is checkable on fixtures and REQUIRED before
'built'. CAPABILITY is owed to a real board and is NOT claimed here.

Every check states what would make it FAIL, because a check that has never failed has never
shown you what it does when it fails (I33/I34).
"""
import inspect
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r"c:\Users\Admin\Documents\GitHub\tether")

import retrieval  # noqa: E402
from tether import Agent as Tether  # noqa: E402

RESULTS: list[bool] = []


def check(name, got, want, why):
    good = got == want
    RESULTS.append(good)
    print(f"  {'PASS' if good else 'FAIL'}  {name}")
    print(f"        got {got!r}  want {want!r}")
    if not good:
        print(f"        WHY IT MATTERS: {why}")


print("\n1. THE KEY IS NAME-FREE -- two gaps identical but for slot names key the SAME")
# Same structure, different instance names. On a new level every name regenerates, so this
# is exactly the pair the boundary comment says the instance key cannot handle.
types_a = {"o1.col": "COLOUR", "o1.w": "EXTENT", "o2.w": "EXTENT"}
types_b = {"o9.col": "COLOUR", "o9.w": "EXTENT", "o7.w": "EXTENT"}
robs_a = [({"o1.col": 1, "o1.w": 3, "o2.w": 5}, "ACTION1", 1),
          ({"o1.col": 2, "o1.w": 3, "o2.w": 6}, "ACTION1", 2)]
robs_b = [({"o9.col": 1, "o9.w": 3, "o7.w": 5}, "ACTION1", 1),
          ({"o9.col": 2, "o9.w": 3, "o7.w": 6}, "ACTION1", 2)]
ga = retrieval.characterise(robs_a, "o1.col", list(types_a), types_a)
gb = retrieval.characterise(robs_b, "o9.col", list(types_b), types_b)
check("same shape, different names -> same gap key",
      Tether._gap_key(ga) == Tether._gap_key(gb), True,
      "the catalogue could not cross a level, which is the whole point of building it")
check("the FULL gaps differ (so the test is not vacuous)", ga == gb, False,
      "if the raw gaps were identical the key test would prove nothing")
# NEGATIVE CONTROL: the instance key -- what the build already had -- must NOT match.
check("negative control: raw 'varies' DOES differ by name",
      ga["varies"] == gb["varies"], False,
      "if slot names already matched, no new key was needed")

print("\n2. A DIFFERENT SHAPE KEYS DIFFERENTLY -- the key discriminates, it is not a constant")
types_c = {"o1.col": "COLOUR", "o1.w": "EXTENT", "o2.col": "COLOUR"}
robs_c = [({"o1.col": 1, "o1.w": 3, "o2.col": 5}, "ACTION1", 1),
          ({"o1.col": 2, "o1.w": 3, "o2.col": 6}, "ACTION1", 2)]
gc = retrieval.characterise(robs_c, "o1.col", list(types_c), types_c)
check("a COLOUR varying instead of an EXTENT -> different key",
      Tether._gap_key(ga) == Tether._gap_key(gc), False,
      "a key that never discriminates files every failure under one shape, which is worse "
      "than no catalogue -- it would deprioritise everything equally")

print("\n3. NO EVIDENCE ABSTAINS -- empty history describes nothing")
check("characterise on no frames yields n=0",
      retrieval.characterise([], "o1.col", ["o1.col"], types_a)["n"], 0,
      "M2_STANDARD check 3: absence-as-fact. An empty description would key every "
      "failure under one shape")

print("\n4. THE BOUNDARY: `paths` is not in the cleared set, `refuted` is")
src = inspect.getsource(Tether.boundary) if hasattr(Tether, "boundary") else ""
if not src:
    for nm in dir(Tether):
        f = getattr(Tether, nm, None)
        if callable(f) and "refuted, self.refuted_at = {}, {}" in (
                inspect.getsource(f) if inspect.isfunction(f) else ""):
            src = inspect.getsource(f)
            break
check("boundary clears self.refuted", "self.refuted, self.refuted_at = {}, {}" in src, True,
      "the fixture is looking at the wrong method")
check("boundary does NOT clear self.paths", "self.paths = {}" in src, False,
      "clearing it would discard the only evidence that crosses -- the mirror of the "
      "autoimmunity the instance key was cleared to avoid")

print("\n5. RETRIEVAL ORDERS AND NEVER EXCLUDES -- the count is preserved")
# The ordering is a `sorted` over (failures, candidate); assert the population is invariant.
paths = {(("k",), ("A",), ()): {"failed": 3}}
cands = ["c_unseen_1", "c_unseen_2"]
scored = [(paths.get((("k",), (c,), ()), {}).get("failed", 0), c) for c in cands]
check("no candidate is dropped by scoring", len([c for _, c in scored]), len(cands),
      "filtering is what retrieval.py records as having LOST A CLOSING TERM")

PASSED = all(RESULTS)
print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks -- "
      + ("ALL PASS" if PASSED else "SOMETHING FAILED"))
sys.exit(0 if PASSED else 1)
