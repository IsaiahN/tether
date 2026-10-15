"""C-S1d-1, A PROMOTED PAIR IS CARRIED ONCE, AS ITS WHOLE (the reviewer 2026-10-15 12:42). WRITTEN,
NOT RUN: it runs in the end-of-step-7 checklist. The game is the 12:38 carry read's: the 3-action
fake game through tether_agent.run with a lineage folder, all defaults, each role its own process.

  W    a cold process plays and writes its generation. The fixture's OWN count, from a spy on
       Agent._compiled (never tether's seen set): the held pairs asked for exactly ONE distinct
       slot. bs_ entries written == that count (precondition: some pair was promoted).
  R    a second process loads the folder and plays the same game: bm_ resolved > 0, and index, bm_
       and bs_ unresolved == 0; every whole resolved from bm_ equals the named compile of its entry,
       holding R's atoms.
  MF   MUST-FAIL: _bs_source carrying every slot answer (S1b+S1c as built) writes more bs_ entries
       than the single-slot pairs.

    python test_bs_promoted.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

CHILD = r"""
import json, sys
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
from test_entry import FakeWrapper
ROLE, D = {role!r}, {d!r}
slots, asked = {{}}, []
real = tether.Agent._compiled
def compiled(self, lib, key, role, o, x, comp, atoms, sig, slot=None):
    if (slot is not None and sig is not None and role in tether._HELD_ROLES and o != x
            and all(tether._PLAIN.fullmatch(v) and "PH" not in v for v in (o, x))):
        slots.setdefault((sig, key, role, o, x), set()).add(slot)
        asked.append((self, lib, key, role, o, x, atoms, sig))
    return real(self, lib, key, role, o, x, comp, atoms, sig, slot=slot)
tether.Agent._compiled = compiled
if ROLE == "mf":
    def all_slots(ag):
        tok = getattr(ag, "_atoms_token", None)
        memo = tether._BOUND_SLOT_MEMO if tok else ag._bound_slot_cache
        idx = tether._BOUND_SLOT_IDX if tok else ag._bound_slot_idx
        return [(k[1:], idx[k], v) for k, v in memo.items() if k[0] == tok and k in idx]
    lineage._bs_source = all_slots
r = tether_agent.run(FakeWrapper(), "g0", 3, lineage_dir=D)
gen = r.get("lineage") or {{}}
out = {{"bs_written": (gen.get("slot_memo") or {{}}).get("entries"),
        "single": sum(1 for v in slots.values() if len(v) == 1), "pairs": len(slots),
        "promoted": tether._INDEX_N["bound_slot_promoted"],
        "resolve": [dict(lineage._RESOLVE), dict(lineage._MEMO_RESOLVE),
                    dict(lineage._BS_RESOLVE)]}}
if ROLE == "r":
    from test_index_hold import _form, _named
    bad, n = [], 0
    memo = tether._BOUND_MEMO
    seen = set()
    for ag, lib, key, role, o, x, atoms, sig in asked:
        mkey = (ag._atoms_token, sig, key, role, o, x)
        if mkey in seen or mkey not in memo:
            continue
        seen.add(mkey)
        n += 1
        got = [(_form(a), _form(b)) for _c, a, b in memo[mkey]]
        want = [(_form(a), _form(b)) for _c, a, b in _named(lib, key, role, o, x, atoms)]
        own = all(t is atoms[t.name] for _c, *cs in memo[mkey] for c in cs
                  if c is not None and hasattr(c, "term") for t in c.term.atoms)
        if got != want or not own:
            bad.append(repr(mkey)[:100])
    out.update(wholes_checked=n, wholes_bad=bad[:5], wholes_bad_n=len(bad))
print("OUT " + json.dumps(out, default=repr))
"""


def _child(role: str, d: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(role=role, d=str(d))], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, f"{role} failed:\n{r.stderr[-3000:]}"
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def main() -> None:
    d = Path(tempfile.mkdtemp(prefix="bsp_"))
    w = _child("w", d)
    assert w["promoted"] > 0, ("precondition: no pair was promoted, so nothing is tested", w)
    assert w["bs_written"] == w["single"], ("W: bs_ entries are not the single-slot pairs", w)
    print(f"  W: bs_ {w['bs_written']} entries == {w['single']} single-slot pairs of "
          f"{w['pairs']}; {w['promoted']} promoted")
    r = _child("r", d)
    res_index, res_bm, res_bs = r["resolve"]
    assert res_bm["resolved"] > 0, ("R: no whole was read from bm_", r)
    assert not (res_index["unresolved"] or res_bm["unresolved"] or res_bs["unresolved"]), r
    assert r["wholes_checked"] > 0 and not r["wholes_bad_n"], ("R: a carried whole differs", r)
    print(f"  R: bm_ {res_bm}, bs_ {res_bs}, index {res_index}; {r['wholes_checked']} carried "
          "wholes equal the named compile, holding R's atoms")
    mf = _child("mf", Path(tempfile.mkdtemp(prefix="bsp_mf_")))
    assert mf["bs_written"] > mf["single"], ("MF MUST-FAIL did not fail", mf)
    print(f"  MF must-fail fired: carrying every slot answer writes {mf['bs_written']} > "
          f"{mf['single']}")
    print("bs promoted: OK")


if __name__ == "__main__":
    main()
