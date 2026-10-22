"""C-S1-2, S1c: PROMOTE ON REUSE and THE HELD WHOLE INDEXED BY SLOT (the reviewer 2026-10-15 12:02).
WRITTEN, NOT RUN: it runs in the end-of-step-7 checklist. C-S1-1 (test_slot_filter) still carries
(a) the same _index_reach answers and (b) whole-game identity, ON vs OFF.

The game is the 11:55 read's: one cold fake game, tether_agent.run(FakeWrapper(), 'g0', 3), a
fresh process per role, no TETHER vars but the one each role names. THE TAIL is from the 3rd
action reaching FakeWrapper.step to run() returning.

  (c)  for every promoted whole, every slot its map holds and one slot it does not: the map's
       rows equal the _lands filter's rows over the whole, in order.
  (d)  warm bound, WHOLE GAME (the reviewer 2026-10-15 12:14): _bound calls ON <= _bound calls
       with TETHER_SLOT_FILTER=0 + FIRST_ROWS, where FIRST_ROWS is the fixture's OWN count, never
       the agent's seen set: for each held pair (entry, role, o, x), 2 x the rows _lands keeps
       over the held view for the FIRST slot the pair was asked for. Each pair costs ON at most
       its first-slot rows plus one whole (only if reused); OFF pays one whole per pair. The
       tail figures are printed for the walls report and do not gate.
  (e)  scan bound: tail _lands calls == the held rows scanned on first-slot paths in the tail
       (a held whole is a lookup, never a scan).
  MF-D MUST-FAIL: a pairs-seen set that never holds anything (S1 as built: no promotion) binds
       MORE than promotion on the same game (the reviewer 12:19).
  MF-E MUST-FAIL: _whole_rows replaced by N1's scan fails (e).

    python tests/test_slot_promote.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = """
import json, sys
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
MODE = {mode!r}


class NeverSeen(set):
    def add(self, _k):
        pass


if MODE == "never":
    tether._PAIRS_SEEN = NeverSeen()
    init = tether.Agent.__init__

    def init2(self, *a, **k):
        init(self, *a, **k)
        self._pairs_seen = NeverSeen()
    tether.Agent.__init__ = init2
if MODE == "scan":
    tether._whole_rows = lambda role, whole, slot, maps, mkey: tuple(
        i for i, r in enumerate(whole) if tether._lands(role, r[1], r[2], slot, tether._same))
n = {{"bound": 0, "lands": 0, "bound_all": 0}}
first = {{}}
real_compiled = tether.Agent._compiled


def compiled(self, lib, key, role, o, x, comp, atoms, sig, slot=None):
    if (slot is not None and sig is not None and role in tether._HELD_ROLES and o != x
            and all(tether._PLAIN.fullmatch(v) and "PH" not in v for v in (o, x))):
        first.setdefault((sig, key, role, o, x), (slot, self, lib, atoms))
    return real_compiled(self, lib, key, role, o, x, comp, atoms, sig, slot=slot)


tether.Agent._compiled = compiled
tail = [False]
real_bound, real_lands = tether._bound, tether._lands


def bound(*a):
    n["bound_all"] += 1
    if tail[0]:
        n["bound"] += 1
    return real_bound(*a)


def lands(*a):
    if tail[0]:
        n["lands"] += 1
    return real_lands(*a)


tether._bound, tether._lands = bound, lands
sent, step = [0], FakeWrapper.step
base = {{}}


def step2(self, action, data=None, reasoning=None):
    r = step(self, action, data, reasoning)
    sent[0] += 1
    if sent[0] == 3:
        tail[0] = True
        base.update(tether._INDEX_N)
    return r


FakeWrapper.step = step2
tether_agent.run(FakeWrapper(), 'g0', 3)
tail[0] = False
d = {{k: tether._INDEX_N[k] - base.get(k, 0) for k in tether._INDEX_N}}
from functools import partial
first_rows = 0
for (sig, key, role, o, x), (slot, ag, lib, atoms) in first.items():
    sub = partial(tether._ph_sub, o=o, x=x)
    first_rows += 2 * sum(1 for _c, a, b in ag._held_index(lib, key, role, atoms, sig)
                          if real_lands(role, a, b, slot, sub))
c_bad, c_n = [], 0
if MODE == "on":
    memo = tether._BOUND_MEMO
    for mkey, smap in list(tether._BOUND_SLOT_MAP.items()):
        whole, role = memo[mkey], mkey[3]
        for slot in [*smap[0], "no.such.slot"]:
            c_n += 1
            want = tuple(i for i, r in enumerate(whole)
                         if real_lands(role, r[1], r[2], slot, tether._same))
            if tether._whole_rows(role, whole, slot, {{}}, mkey) != want:
                c_bad.append([repr(mkey)[:80], slot])
print("OUT " + json.dumps({{"tail": n, "delta": d, "c_n": c_n, "c_bad": c_bad,
                            "first_rows": first_rows, "pairs": len(first),
                            "promoted": tether._INDEX_N["bound_slot_promoted"]}}))
"""


def _child(mode: str, arms: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(arms or {})
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(mode=mode)], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def _d(o: dict, off: dict) -> bool:
    return o["tail"]["bound_all"] <= off["tail"]["bound_all"] + o["first_rows"]


def _e(o: dict) -> bool:
    return o["tail"]["lands"] == o["delta"].get("bound_slot_scanned", 0)


def main() -> None:
    on = _child("on")
    off = _child("off", {"TETHER_SLOT_FILTER": "0"})
    # THE PANEL PRECONDITION: a pair was promoted, and the tail read a held whole at least once
    assert on["promoted"] > 0, ("precondition: no pair was promoted", on)
    assert on["delta"].get("bound_slot_from_whole", 0) > 0, ("precondition: no held whole read "
                                                              "in the tail", on["delta"])
    assert on["c_n"] > 0 and not on["c_bad"], ("(c) the slot map differs from _lands", on["c_bad"])
    print(f"  (c) {on['c_n']} slots of promoted wholes: the map equals the _lands rows, in order")
    assert on["pairs"] > 0, ("precondition: no held pair was asked by slot", on)
    assert _d(on, off), ("(d) warm bound", on["tail"], off["tail"], on["first_rows"])
    print(f"  (d) whole-game binds ON {on['tail']['bound_all']} <= OFF {off['tail']['bound_all']} "
          f"+ FIRST_ROWS {on['first_rows']} ({on['pairs']} pairs); tail ON {on['tail']['bound']}, "
          f"OFF {off['tail']['bound']} (printed, not gated)")
    assert _e(on), ("(e) scan bound", on["tail"], on["delta"])
    print(f"  (e) tail _lands {on['tail']['lands']} == rows scanned on first-slot paths")
    never = _child("never")
    # MF-D tests the defect's own claim (the reviewer 2026-10-15 12:19): without promotion the
    # same game binds MORE than with it. _d(never, off) is printed, not gated (the bound is loose)
    assert never["tail"]["bound_all"] > on["tail"]["bound_all"], (
        "MF-D MUST-FAIL did not fail: without promotion the game bound no more",
        never["tail"], on["tail"])
    print(f"  MF-D must-fail fired: without promotion {never['tail']['bound_all']} binds > "
          f"{on['tail']['bound_all']} with it; the loose bound (d) would have "
          f"{'passed' if _d(never, off) else 'caught'} it")
    scan = _child("scan")
    assert not _e(scan), ("MF-E MUST-FAIL did not fail: the scan passed (e)", scan)
    print("  MF-E must-fail fired: N1's scan over a held whole fails the scan bound")
    print("slot promote: OK")


if __name__ == "__main__":
    main()
