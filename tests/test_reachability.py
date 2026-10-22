"""THE COMPOSE ITEMS' REACHABILITY (the reviewer 2026-10-11 09:31 plan, 13:31 CDT): for each item
the comparison set composes rather than builds, whether the agent's own machinery reaches it -- a
chain in enumerate_closure at the composer's depth, a stated condition compile_term compiles, the
mint's operand list holding the second slot. A NOT REACHED is a demand row, printed with its reason
for the ALL-ON census, never hidden. No run.

  between, chained order        two comparisons, each compiles, and the conjunction holds where it
                                should and not where it should not;
  odd one out (object level)    is_mode . holds . negate in the closure at depth d;
  near/far, same relation as    stated over two pair slots (compile), and reached by the mint
                                (the second slot is an operand of the first, and the atom types);
  more/fewer                    count . above in the closure at depth d, and on a scene;
  MUST-FAILS: with is_mode withheld, odd one out reads NOT REACHED; with above and below withheld,
  between reads NOT REACHED naming them.

    python tests/test_reachability.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import compile_term as C, gamma, tether
from arc_atoms import PRED
from test_goal_condition import _agent
ag = _agent()
atoms = {a.name: a for a in ag.gamma.atoms}
depth, budget = ag.cfg.max_depth, ag.cfg.budget
types = ag.slot_types

def closure(g, in_t, out_t, names):
    for t in g.enumerate_closure(in_t, out_t, depth, budget, {}):
        if tuple(a.name for a in t.atoms) == tuple(names):
            return f"reached at depth {len(names)}"
    return f"NOT REACHED: {'.'.join(names)} not in the {in_t}->{out_t} closure at depth {depth}"

def comp(text, at=None):
    c = C.compile_candidate({"condition": text}, at or atoms)
    return c if isinstance(c, C.Compiled) else "NOT COMPILED: " + c.reason

def conj(texts, yes, no, at=None):
    cs = [comp(t, at) for t in texts]
    bad = [c for c in cs if isinstance(c, str)]
    if bad:
        return "NOT REACHED: " + "; ".join(bad)
    hold = lambda st: all(C.run(c, st) is True for c in cs)
    return "compiled, holds" if hold(yes) and not hold(no) else "NOT REACHED: conjunction misreads"

def mint(subj, other, atom):
    b = [x for x in ag._bindings(subj, []) if x]
    if other not in b:
        return f"NOT REACHED: {other} is not an operand of {subj}"
    t = types.get(subj)
    why = C._typed((atoms[atom],), t, types.get(other))
    return f"mint reaches {atom}<{other}> on {subj}" if why is None else "NOT REACHED: " + why

col = types["o0.colour"]
out = {
 "between": conj(["o0.row > o1.row", "o0.row < o2.row"],
                 {"o0.row": 3, "o1.row": 1, "o2.row": 5}, {"o0.row": 6, "o1.row": 1, "o2.row": 5}),
 "chained order": conj(["o0.row > o1.row", "o1.row > o2.row"],
                       {"o0.row": 5, "o1.row": 3, "o2.row": 1},
                       {"o0.row": 5, "o1.row": 1, "o2.row": 3}),
 "odd one out": closure(ag.gamma, col, PRED, ("is_mode", "holds", "negate")),
 "near/far (goal)": comp("o0.dist_o3 < o0.dist_o4"),
 "near/far (mint)": mint("o0.dist_o3", "o0.dist_o4", "below"),
 "same relation as (goal)": comp("o0.dist_o3 == o1.dist_o4"),
 "same relation as (mint)": mint("o0.dist_o3", "o1.dist_o4", "same"),
 "more/fewer": closure(ag.gamma, col, PRED, ("count", "above")),
}
out = {k: (v if isinstance(v, str) else f"compiled: {[a.name for a in v.term.atoms]} on {v.slot}")
       for k, v in out.items()}
# more/fewer on a scene (the reviewer 13:40): count . above holds where more peers share the value
# than the operand says, and fails on the swap
t = gamma.Term((atoms["count"], atoms["above"]), operand="x")
yes = t.apply(5, gamma.Ctx(group=(5, 5, 5, 5, 5, 1), operands=(1,)))
no = t.apply(5, gamma.Ctx(group=(5, 1, 1, 1), operands=(4,)))
out["more/fewer"] += f"; on a scene: {bool(yes)} (many vs 1), {bool(no)} (one vs 4)"
scene = [bool(yes), bool(no)]
g2 = gamma.Gamma([a for a in ag.gamma.atoms if a.name != "is_mode"], game="mf")
mf_odd = closure(g2, col, PRED, ("is_mode", "holds", "negate"))
no_order = {k: v for k, v in atoms.items() if k not in ("above", "below")}
mf_between = conj(["o0.row > o1.row", "o0.row < o2.row"], {}, {}, no_order)
print(json.dumps({"depth": depth, "items": out, "mf_odd": mf_odd, "mf_between": mf_between,
                  "scene": scene}))
'''


def main() -> int:
    env = dict(os.environ, TETHER_RELATION_SET="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    out = json.loads(p.stdout.strip().splitlines()[-1])
    print(f"  composer depth {out['depth']}")
    for k, v in out["items"].items():
        print(f"  {k}: {v}")
    assert out["mf_odd"].startswith("NOT REACHED") and "is_mode" in out["mf_odd"], out["mf_odd"]
    assert out["mf_between"].startswith("NOT REACHED") and "above" in out["mf_between"], out
    assert out["scene"] == [True, False], out["scene"]
    print(f"  must-fail, is_mode withheld: {out['mf_odd']}")
    print(f"  must-fail, above/below withheld: {out['mf_between']}")
    print("reachability: recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
