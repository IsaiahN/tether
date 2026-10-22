"""DS mf5, THE EVENT-MEMBER GUARD (the reviewer 2026-10-20 09:47 item 9). _event_prices hands
_event_shared only the NON-derived members (its `ind` drops env.derived()), so the guard at the
member bind is unreachable from there; this feeds a declared-derived slot into _event_shared
DIRECTLY, on the fake ARC game, with the offers and prices planted so the shared term binds both.

  ON   the derived member is refused -- one derived_unbound row, site "event", and it is not
       bound -- while the other member binds
  OFF  (TETHER_DERIVED_SUBJECT=0, a child) both members bind: the guard is what refused

    python tests/test_ds_event_guard.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
D, M = "o1.dcol_o2", "o1.col"


def child() -> dict:
    from test_g1 import agent, rows_of
    tether, env, ag = agent()
    rows = rows_of(ag)
    t = tether.Term((ag.gamma.atoms[0],))
    env.derived = lambda: {D: ("o1.col", "o2.col")}
    ag._lib_offers = {D: [{"term": t}], M: [{"term": t}]}
    ag._ev_base = {D: 10.0, M: 10.0}
    ag._bits = lambda *_a, **_k: 1.0
    ag._units_for = lambda *_a, **_k: ()
    ag._bind_bits = lambda *_a: 0.5
    ag._left = lambda *_a: 0.0
    ag._joint = lambda *_a: 20.0
    ag.history = lambda _s: []
    ag.explain = lambda *_a: (0.0, 0.0)
    ag.gamma.accept = lambda *_a, **_k: None
    ag._event_shared("o1", [D, M], {})
    return {"arm": tether._DERIVED_SUBJECT, "d_bound": ag.bound.get(D), "m_bound": ag.bound.get(M),
            "term": t.name, "unbound": [s.get("site") for e, s_, s in rows
                                        if e == "derived_unbound" and s_ == D]}


def run(arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_DERIVED_SUBJECT=arm, PYTHONDONTWRITEBYTECODE="1")
    here = _repo.ROOT
    p = subprocess.run([sys.executable, "-B", __file__, "--child"], capture_output=True, text=True,
                       env=env, stdin=subprocess.DEVNULL, cwd=here)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    on, off = run("1"), run("0")
    print("ON ", on)
    print("OFF", off)
    assert on["arm"] is True and off["arm"] is False, (on, off)
    assert on["d_bound"] is None and on["unbound"] == ["event"], on                     # ON
    assert on["m_bound"] == on["term"], on
    assert off["d_bound"] == off["term"] and off["m_bound"] == off["term"], off         # OFF
    assert off["unbound"] == [], off
    print("ds_event_guard: OK")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--child"]:
        print(json.dumps(child()))
        sys.exit(0)
    sys.exit(main())
