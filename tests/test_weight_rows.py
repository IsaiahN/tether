"""(5) THE WEIGHT-CHANGE ROWS (the reviewer 2026-11-07 r1356; Isaiah 07:56 "log that event and
console it"): a standing crossing r1243's threshold is a standing_freed row, the halflife's move a
halflife_moved row, the partly recorded changes carry their values, and nsm says each in one WEIGHT
line. No behaviour moves. Gridworld default seed 0 (about 40 s).

check_crossed   12 steps: standing_freed rows, each on the side of 1 + carried + paid its "to" names
                and the opposite of that (form, situation)'s last row; a run whose _rf_crossed
                writes nothing is identical beyond those rows (identity_mod_rows.compare).
                MUST-FAIL: that run has no standing_freed row
check_halflife  a forcing fixture: one vindication planted at c2; one halflife_moved row there (None
                -> 1.0, effective 8.0 -> 1.0) and the books row's halflife_effective 1.0
check_carried   _reinvent_carried with a reflex record: invention_carried names its paid counts
check_line_paid a line under way that pays writes line_paid at the increment (r1357), one WEIGHT
                line. MUST-FAIL: no line under way, no row
check_nsm       every weight row of the run, and a halflife_moved row, said as one WEIGHT line in
                listed NSM words; the Speaker writes them to nsm.log

    python tests/test_weight_rows.py [check ...]
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from conform.identity_mod_rows import compare, mask_timings  # noqa: E402

NEW = ("standing_freed", "halflife_moved")
_RUNS: dict = {}


def agent(game: str = "wr") -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game=game), tether.Config(), ledger.Ledger())


def run(quiet: bool = False, n: int = 12) -> list:
    """The ledger rows of n steps, as a later reader loads them (sort_keys, r1339)."""
    if quiet not in _RUNS:
        real = tether.Agent._rf_crossed
        if quiet:
            tether.Agent._rf_crossed = lambda *_a: None
        try:
            ag = agent()
            for _ in range(n):
                ag.step()
        finally:
            tether.Agent._rf_crossed = real
        _RUNS[quiet] = [json.loads(json.dumps(r, sort_keys=True, default=str))
                        for r in ag.led.rows()]
    return _RUNS[quiet]


def check_crossed() -> None:
    rows = run()
    fr = [r for r in rows if r["event"] == "standing_freed"]
    assert fr, "no standing_freed row"
    last: dict = {}
    for r in fr:
        d = r["detail"]
        under = 1 + d["carried"] + d["paid"] < d["against"]
        assert d["to"] == ("under" if under else "free"), d
        k = (d["form"], tuple(d["situation"]))
        assert last.get(k) != d["to"], (k, d)
        last[k] = d["to"]
    quiet = run(quiet=True)
    assert not [r for r in quiet if r["event"] == "standing_freed"]                       # MF
    body = [r for r in rows if r["event"] not in ("header", "arms")]
    base = [r for r in quiet if r["event"] not in ("header", "arms")]
    bad = compare(mask_timings(base), mask_timings(body), {"standing_freed"})
    assert not bad, bad[:3]
    print(f"  {len(fr)} standing_freed rows over {len(last)} (form, situation); identical beyond "
          f"them to a run that writes none ({len(base)} rows)")


def check_halflife() -> None:
    ag = agent()
    for _ in range(2):
        ag.step()
    assert ag.gamma.halflife is None
    ag.gamma.vindication.append(1)
    ag.step()
    rows = ag.led.rows()
    hm = [r for r in rows if r["event"] == "halflife_moved"]
    assert len(hm) == 1 and hm[0]["cycle"] == 2, hm
    d = hm[0]["detail"]
    assert (d["old"], d["new"], d["old_effective"], d["new_effective"], d["earned"]) == \
        (None, 1.0, gamma.REJECTION_HALFLIFE, 1.0, True), d
    books = [r["detail"]["halflife_effective"] for r in rows if r["event"] == "books"]
    assert books == [gamma.REJECTION_HALFLIFE] * 2 + [1.0], books
    ag.step()
    assert len([r for r in ag.led.rows() if r["event"] == "halflife_moved"]) == 1
    print("  halflife_moved once at c2: None (8.0) -> 1.0; books halflife_effective 8.0, 8.0, 1.0")


def check_carried() -> None:
    ag = agent()
    ag._reinvent_carried([{"kind": "reflex", "name": "x_reflex_1", "paid": [["walk", ["K"], 2]],
                           "loss": []}])
    ic = [r["detail"] for r in ag.led.rows() if r["event"] == "invention_carried"]
    assert len(ic) == 1, ic
    want = [["walk", ["K"], 2]] if tether._REFLEX_CARRY else None
    assert ic[0].get("reflex_paid_in") == want, ic[0]
    print("  invention_carried reflex_paid_in", ic[0].get("reflex_paid_in"))


def check_line_paid() -> None:
    ag = agent()
    for _ in range(3):
        ag.step()
    slot = "o0.row"
    n0 = len(ag.led.rows())
    ag._leave_check(slot, ag.outstanding(slot) + 1.0)        # no line under way: no paid
    assert not [r for r in ag.led.rows()[n0:] if r["event"] == "line_paid"]               # MF
    ag._leave_line[slot] = {"key": (ag.level, ag._root_id), "first": ag.outstanding(slot) + 1.0,
                            "mints": 0}
    ag._leave_check(slot, ag.outstanding(slot) + 1.0)
    lp = [r["detail"] for r in ag.led.rows()[n0:] if r["event"] == "line_paid"]
    g = ag._line_grade[ag._kind_key(slot)]
    assert len(lp) == 1 and lp[0]["paid"] == g["paid"] == 1 and lp[0]["grade"] == dict(g), lp
    said = nsm.say_row("line_paid", lp[0], (ledger.WIN, ledger.ADVANCE))
    assert said and said[0][0] == "WEIGHT" and not nsm.unlisted(said[0][1]), said
    print("  line_paid at the increment:", lp[0]["route"], lp[0]["paid"], "|", said[0][1][:120])


def check_nsm() -> None:
    rows = [r for r in run() if r["event"] in nsm.WEIGHT_ROWS]
    rows.append({"seq": 0, "cycle": 0, "step": "PLAN", "slot": "@weight",
                 "event": "halflife_moved",
                 "detail": {"old": None, "new": 1.0, "old_effective": 8.0, "new_effective": 1.0,
                            "vindications": 1, "earned": True}})
    seen = {r["event"] for r in rows}
    assert {"standing_freed", "think_settled", "field_class", "halflife_moved"} <= seen, seen
    for r in rows:
        said = nsm.say_row(r["event"], r["detail"], (ledger.WIN, ledger.ADVANCE))
        assert len(said) == 1 and said[0][0] == "WEIGHT", (r["event"], said)
        assert not nsm.unlisted(said[0][1]), (r["event"], said, nsm.unlisted(said[0][1]))
    with tempfile.TemporaryDirectory() as d:
        sp = nsm.Speaker(Path(d) / "run.jsonl", (ledger.WIN, ledger.ADVANCE))
        for r in rows:
            sp.see(r["seq"], r["cycle"], r["step"], r["slot"], r["event"], r["detail"])
        sp.close()
        log = (Path(d) / "nsm.log").read_text(encoding="utf-8").splitlines()
    w = [x for x in log if " WEIGHT " in x]
    assert w and sp.faults == 0, (sp.fault, log[:3])
    print(f"  {len(rows)} weight rows ({sorted(seen)}), {len(w)} WEIGHT lines in nsm.log, e.g.")
    print("   ", w[0][:200])


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_crossed, check_halflife, check_carried, check_line_paid, check_nsm):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_weight_rows OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
