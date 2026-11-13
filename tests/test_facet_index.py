"""P3, 8b-0 (TETHER_FACET_INDEX; the reviewer r1838, r1840, r1841; DESIGN_STEP8 B1/B3): the facet
key (src, subj, dk, role) and its index.

  FX1   the door key: two kinds with the same attribute types and different form codes read as ONE
        subject; different attribute types read as two (MF9's rule kept).
  MF-FX1 the form kept in the subject: the two same-type kinds read as two -> RED.
  FX2   source_of on planted histories: a slot whose change follows ANOTHER object's slot (in
        contact) reads BY:<that owner's door kind> with that slot as its first bind; a slot whose
        change follows my press reads SELF with its own lag first; each says the rows it read.
  MF-FX2 source_of answering WORLD for every slot (the plant): FX2's readings fail -> RED.
  FX3   T0 serves the door kind on the dc22 capture (acts forced, c0-9): an entry recorded only
        under objects of the same door kind and ANOTHER form is placed in T0 at an ask served at a
        key that still names the subject (not the (*, *, dk) back-off).
  MF-FX3 the form kept in the subject (the plant): no such entry -> RED.
  FX4   save -> load: the facet counts written by lineage.write come back equal in a fresh agent's
        carried record (facet_n through the store's counts blob); a second save with no new
        counts loads the same (increments, never a double count; r1843 3b).
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_facet_index.py
"""
from __future__ import annotations

import collections
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import test_pay_gap as pg

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = _repo.ROOT


def fx1(kind_text) -> bool:
    a = kind_text(("COLOUR", "POSITION", "form=101"))
    b = kind_text(("COLOUR", "POSITION", "form=202"))
    c = kind_text(("COLOUR", "EXTENT", "form=101"))
    print(f"   same types, other forms: {a!r} vs {b!r}; other types: {c!r}")
    return a == b and a != c


class Stub:
    """Just what source_of reads: history(slot), cycle, _src_cache, _kind(owner)."""

    def __init__(self, rows):
        self.rows, self.cycle, self._src_cache = rows, 9, {}

    def history(self, _slot):
        return self.rows

    def _kind(self, owner):
        return ("COLOUR", "POSITION", f"form={len(owner)}")


def planted(by_other: bool) -> list:
    """o2.col's history: its change follows o1.col (in contact) or my press."""
    xs = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
    acts = ["A1", "A1", "A2", "A2", "A1", "A2", "A1", "A1", "A2", "A2", "A1", "A2", "A2", "A1"]
    rows, y = [], 5
    for x, a in zip(xs, acts, strict=True):
        before = {"o1.col": x, "o2.col": y, "o1~o2.contact": 1}
        y = y + (1 if (x if by_other else a == "A1") else -1)
        rows.append((before, a, y, None, None))
    return rows


def fx2(src_fn) -> tuple:
    by = src_fn(Stub(planted(True)), "o2.col")
    me = src_fn(Stub(planted(False)), "o2.col")
    print(f"   copy of o1.col: {by}; follows the press: {me}")
    return (by[0] == "BY:COLOUR/POSITION" and by[1] == "o1.col" and me[0] == "SELF"
            and me[1] == "o2.col~1"), by, me


SPY = r'''
import atexit
_A = tether.Agent
EV = []
def _raw(kind):
    return [str(x) for x in (kind or ())]
_ti = _A._tiers
def _ti2(self, *a, **k):
    out = _ti(self, *a, **k)
    n0 = out[1].get("T0", 0)
    if n0:
        dk, mine, s = a[2], a[3], k.get("slot")
        EV.append(["A", self.cycle, s, _raw(self._kind(mine)), list(dk),
                   [e for e, _w in out[0][:n0]], tether.context_key(self, dk, mine, s)])
    return out
_A._tiers = _ti2
_fn = _A._fx_note
def _fn2(self, which, dk, entry, kind, role, slot):
    EV.append(["N", self.cycle, slot, _raw(kind), list(dk), entry])
    return _fn(self, which, dk, entry, kind, role, slot)
_A._fx_note = _fn2
atexit.register(lambda: print("EV " + json.dumps(EV, default=list)))
'''
FORM_KEPT = 'tether._kind_text = lambda kind: "/".join(str(x) for x in (kind or ()))\n'


def fx3(form_kept: bool) -> list:
    """(cycle, asking slot, entry, its form, the forms it was recorded under) for each T0 entry
    served at a key that still names the subject (not the (*, *, dk) back-off) and recorded before
    ONLY under objects of the same door kind and another form."""
    spy = SPY + (FORM_KEPT if form_kept else "")
    code = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                             "tether._AGENT_SEED = False\n" + spy, 1)
    assert spy in code
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    led = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", code, data, "10", led], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    ev = next(json.loads(x[3:]) for x in p.stdout.splitlines() if x.startswith("EV "))

    def door(k):
        return [x for x in k if not x.startswith("form=")]

    def form(k):
        return next((x for x in k if x.startswith("form=")), None)
    cross, asks = [], 0
    for i, e in enumerate(ev):
        if e[0] != "A" or not e[6] or e[6][1] == "*":
            continue
        asks += 1
        _a, cyc, slot, kind, dk, t0, _ck = e
        for entry in t0:
            seen = [n for n in ev[:i] if n[0] == "N" and n[5] == entry and n[4] == dk
                    and door(n[3]) == door(kind)]
            if seen and all(form(n[3]) != form(kind) for n in seen):
                cross.append((cyc, slot, entry, form(kind), sorted({form(n[3]) for n in seen})))
    print(f"   asks served at a subject key {asks}; cross-form entries {len(cross)}"
          + (f" (first {cross[0]})" if cross else ""))
    return cross


def _agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def fx4() -> tuple:
    d = Path(tempfile.mkdtemp(prefix="facet_"))
    a = _agent()
    key = ("BY:COLOUR/POSITION", "COLOUR/POSITION", ("POSITION", "+", 1), "PROCESS")
    a._fx[key] = collections.Counter({"O|LIB|X": 2, "L|LIB|X": 3, "L|LIB|Y": 1})
    lineage.write(d, a, "default")
    b = _agent()
    lineage.load(d, b)
    got = b._fx_in.get(key)
    sql = any(p.suffix == ".db" for p in d.rglob("*"))
    print(f"   written {dict(a._fx[key])}; loaded {got}; a .db store in the lineage: {sql}")
    lineage.write(d, a, "default")          # r1843 3b: a second save with no new counts
    c = _agent()
    lineage.load(d, c)
    again = c._fx_in.get(key)
    print(f"   saved again with no new counts; loaded {again}")
    return got == dict(a._fx[key]) and again == got, sql


def main() -> int:
    ok1 = fx1(tether._kind_text)
    print("FX1 door key: " + ("GREEN" if ok1 else "RED"))
    assert ok1

    def with_form(k):
        return "/".join(str(x) for x in k)
    bad1 = fx1(with_form)
    print("MF-FX1 the form kept in the subject: " + ("GREEN (the plant went unseen)" if bad1
                                                      else "RED"))
    assert not bad1

    ok2, _by, _me = fx2(tether.source_of)
    print("FX2 source_of: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    bad2, *_ = fx2(lambda _ag, _s: ("WORLD", None, 0, 0))
    print("MF-FX2 source_of forced to WORLD: " + ("GREEN (the plant went unseen)" if bad2
                                                  else "RED"))
    assert not bad2

    on = fx3(False)
    print("FX3 dc22 c0-9: an entry recorded under another form of the same door kind is served "
          "in T0: " + ("GREEN" if on else "RED"))
    assert on, "no cross-form entry served in T0 -- no occasion on this capture"
    kept = fx3(True)
    print("MF-FX3 the form kept in the subject: " + ("RED" if not kept
                                                     else "GREEN (the plant went unseen)"))
    assert not kept

    ok4, sql = fx4()
    print(f"FX4 save -> load (store .db present: {sql}): " + ("GREEN" if ok4 else "RED"))
    assert ok4
    print("facet_index: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
