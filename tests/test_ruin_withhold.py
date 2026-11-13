"""7a(5) C, ruin ordered first (R3 Part 1; the reviewer 2026-10-10 10:41Z, 11:53Z). With TETHER_RUIN
on, a pair the veto floor holds for THIS board is withheld from the one choose() call, at the sites
below the seam where the button and coordinate are chosen, unless every option is vetoed.

  must-pass: snaps AVOID (s0 must never read 3) from s0=2, 4 attempts, the agent CHOOSING: with C
     OFF it repeats its own game loss (a held key loses the game again); with C ON no held key loses
     the game again, every @ruin row's choice is outside its withheld set, and the FULL gate passes;
  1. on a DIFFERENT board nothing is withheld;
  2. a positioned action at another coordinate on the same board is offered (only the vetoed
     coordinate is skipped), at _made's spots and at TOUCH route 1;
  3. every option vetoed: the step still acts, chosen_held True (no all_vetoed key, r1900 7c),
     and `why` says so;
  4. choose() is called exactly once per step;
  5. TETHER_RUIN without TETHER_RUIN_RECORD refuses to start;
  6. a library saved after a game loss carries no veto (Fig 4: a recording never crosses up);
  7. a withheld set built on board A and passed while the env shows board B is refused;
  8. EXPLORATION: with the board's only untried action vetoed, the step acts, and no draw, tried
     count or table entry is recorded for the withheld action.
  9. HOLD (r1743): a still press the floor withholds is not held with (a hyp_still_withheld row,
     no still press left); with every action withheld it is.
  10. STEP ORDER (r1744): in the must-pass run an earlier level's park on a live slot name ("L1:s0")
     is swept after s0's ACCEPT; its reuse_refused row is filed under the park's key, so the full
     gate's step order holds (filed under "s0" it refused: "s0: MINT after ACCEPT"). The occasion
     is the store clock's path; under TETHER_FADE_BY_STORE=0 the run never sweeps such a park.

  The must-pass's CONTRAST (ON loses fewer games than OFF) is read on BOTH clocks, each in its
  own child process (TETHER_FADE_BY_STORE=1 and =0; r1738, r1747): pinned (below), the unvetoed
  agent repeats its own game loss on either (2 repeats, 4 losses in 4 attempts, measured on
  8464907), so the veto pays on the default clock too. The veto's own laws (no held key repeated,
  no withheld pair chosen, the gate) are read in the parent, and every numbered check below runs
  there.

  The agent's seed is pinned (TETHER_AGENT_SEED off, the constant seed, as test_lineage_merge):
  each process otherwise draws its own seed at start, and one law read over four short attempts
  is then a different sample every run (the reviewer r1740 1).

    python tests/test_ruin_withhold.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gate
import interface as IFace
import snaps
import test_ruin_record as R
import tether
from world import bind

sys.dont_write_bytecode = True
tether._AGENT_SEED = False          # r1740 1: one seed, so the attempts replay exactly


def _on() -> None:
    tether._RUIN_RECORD = tether._RUIN = True


def _rows(ag: tether.Agent, event: str) -> list[dict]:
    return [r for r in ag.led.rows() if r["event"] == event]


class _Spy:
    """Counts choose() calls and keeps every _withhold verdict, wrapping the bound methods."""

    def __init__(self, ag: tether.Agent) -> None:
        self.chose, self.every = 0, []
        inner_choose, inner_w = ag.choose, ag.iface._withhold

        def choose(before):
            self.chose += 1
            return inner_choose(before)

        def withhold(w, offered, state, env):
            out = inner_w(w, offered, state, env)
            self.every.append((bool(w), out[0], out[2]))
            return out
        ag.choose, ag.iface._withhold = choose, withhold


def _attempts(start: int, ruin: bool, attempts: int = 4, steps: int = 12) -> tuple:
    """The agent CHOOSING, from the same board each attempt (deterministic, so a retry re-meets it):
    (agent, ending per attempt, veto keys in order, the spy). An attempt ends at a game loss or
    `steps`."""
    tether._RUIN_RECORD, tether._RUIN = True, ruin
    snap = snaps.Snap(R._spec(start))
    ag = R._agent(snap)
    spy, ends, acted = _Spy(ag), [], 0
    for lv in range(attempts):
        end = None
        for _ in range(steps):
            acted += 1
            ag.step()
            if snap.terminal():
                end = snap.terminal()
                break
        ends.append(end)
        snap = snaps.Snap(R._spec(start))
        ag.retarget(bind(snap), lv + 1, end or "run_end")
    keys = [(d["fingerprint"], d["action"], tuple(d["coord"] or ()))
            for d in (r["detail"] for r in _rows(ag, "veto"))]
    return ag, ends, keys, spy, acted


def _contrast() -> str:
    """The must-pass's contrast, in a child process started on one fade clock (r1747)."""
    off, off_ends, off_keys, _s, _n = _attempts(2, False)
    _c, c_ends, c_keys, _cs, _cn = _attempts(2, True)
    off_rep, c_rep = len(off_keys) - len(set(off_keys)), len(c_keys) - len(set(c_keys))
    assert off_rep > 0, (off_ends, off_keys)          # OFF: the agent repeats its own game loss
    assert c_rep == 0 and c_ends.count("game_loss") < off_ends.count("game_loss"), (c_ends, c_keys)
    clock = "store clock" if tether.G_FADE_BY_STORE else "cycle clock"
    return f"{clock} OFF endings {off_ends}, {off_rep} repeat a held key; ON {c_ends}, 0 repeats"


if __name__ == "__main__" and sys.argv[1:] == ["--contrast"]:
    print(_contrast())
    sys.exit(0)

if __name__ == "__main__":
    said = []
    for clock in ("1", "0"):
        env = {**os.environ, "TETHER_FADE_BY_STORE": clock}
        r = subprocess.run([sys.executable, "-B", __file__, "--contrast"], env=env, text=True,
                           capture_output=True, stdin=subprocess.DEVNULL, check=False)
        assert r.returncode == 0, (clock, r.stderr[-1500:])
        said.append(r.stdout.strip().splitlines()[-1])
    said = "; ".join(said)
    ag, ends, keys, spy, acted = _attempts(2, True)   # the veto's laws, on the shipped clock
    rep = len(keys) - len(set(keys))
    assert rep == 0, (ends, keys)
    w = _rows(ag, "withheld")
    assert w and all(r["slot"] == "@ruin" and r["step"] == "PLAN" for r in w), w[:2]
    assert all(not r["detail"]["chosen_held"] for r in w), [r["detail"] for r in w]
    assert all(r["detail"]["chosen"] not in r["detail"]["withheld"] for r in w), w
    out = gate.check(ag.led.rows())
    assert out["verdict"] == gate.PASS, out
    rr = [r for r in _rows(ag, "reuse_refused") if r["detail"].get("cross_level")
          and r["detail"]["held"].rsplit(":", 1)[-1] in ag.slots]
    # the occasion is the store clock's path (the muse rival); the cycle clock never sweeps it
    assert rr or not tether.G_FADE_BY_STORE, "precondition: no earlier-level park refused"
    assert all(r["slot"] == r["detail"]["held"] for r in rr), [(r["slot"], r["detail"]["held"])
                                                               for r in rr]
    print(f"  must-pass, s0=2, 4 attempts of up to 12 steps, the agent choosing: {said}; "
          f"parent ({'store' if tether.G_FADE_BY_STORE else 'cycle'} clock) ON endings {ends}, "
          "0 repeats, "
          f"{len(w)} @ruin rows, none choosing a withheld pair; full gate passes "
          f"({len(ag.led.rows())} rows)")
    print(f"  10: {len(rr)} earlier-level park row(s) on a live slot name filed under the park "
          f"({rr[0]['slot']}, step {rr[0]['step']}); step order holds" if rr else
          "  10: no earlier-level park swept on this clock (no occasion); step order holds")
    # 4
    assert spy.chose == acted, (spy.chose, acted)
    print(f"  4: choose() called {spy.chose} times for {acted} steps")
    _on()
    # 1
    other = R._agent(snaps.Snap(R._spec(2)))
    other.step("A")
    other.retarget(bind(snaps.Snap(R._spec(1))), 1, "game_loss")
    sp1 = _Spy(other)
    other.step()
    assert not _rows(other, "withheld") and not any(on for on, _o, _e in sp1.every), sp1.every
    print("  1: on another board nothing is withheld (no @ruin row; every _withhold call empty)")
    # 2
    fi = IFace.Interface()
    st = {"o0.row": 1, "o0.col": 2, "o1.row": 5, "o1.col": 6}

    class _Env:
        def observe(self):
            return dict(st)
    env = _Env()
    fp = IFace.fingerprint(env, st)[0]
    c0, c1 = (2, 1), (6, 5)
    r = fi.realise(IFace.Intent(IFace.ELICIT), ("ACTION6",), (), st, env,
                   IFace.Withheld(fp, frozenset({("ACTION6", c0)})))
    assert r.action == "ACTION6" and r.coord == c1, r
    t0 = fi.realise(IFace.Intent(IFace.TOUCH, object="o0"), ("ACTION6",), (), st, env,
                    IFace.Withheld(fp, frozenset({("ACTION6", c0)})))
    t1 = fi.realise(IFace.Intent(IFace.TOUCH, object="o0"), ("ACTION6",), (), st, env,
                    IFace.Withheld(fp, frozenset({("ACTION6", c1)})))
    assert t0 is None and t1.coord == c0, (t0, t1)
    print(f"  2: ACTION6 at {c0} vetoed -> explore aims at {c1}; TOUCH o0 refused at the vetoed "
          f"spot, taken at {c0} when only {c1} is vetoed")
    # 3
    al = R._agent(snaps.Snap(R._spec(2)))
    al.step("B")
    fpa = al._fingerprint(al.env.observe())[0]
    al._vetoes |= {(fpa, a, None) for a in snaps.ACTIONS}
    sp3 = _Spy(al)
    acted = al.step()
    w3 = _rows(al, "withheld")
    assert acted and w3 and w3[-1]["detail"]["chosen_held"], (acted, w3)
    assert not any("all_vetoed" in r["detail"] for r in w3), w3[-1]["detail"]
    assert any(e for _on, _o, e in sp3.every), sp3.every
    print(f"  3: every option vetoed -> the step acts ({w3[-1]['detail']['chosen']}), "
          f"chosen_held True, '{IFace.ALL_VETOED}' set")
    # 5
    env5 = {**os.environ, "TETHER_RUIN": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    env5["TETHER_RUIN_RECORD"] = "0"     # default ON since 083c07b: unset is no longer OFF
    p5 = subprocess.run([sys.executable, "-c", "import tether"], env=env5, capture_output=True,
                        text=True, cwd=Path(_repo.ROOT), check=False)
    ok5 = subprocess.run([sys.executable, "-c", "import tether"],
                         env={**env5, "TETHER_RUIN_RECORD": "1"}, capture_output=True,
                         text=True, cwd=Path(_repo.ROOT), check=False)
    assert p5.returncode != 0 and "TETHER_RUIN_RECORD" in p5.stderr, p5.stderr[-300:]
    assert ok5.returncode == 0, ok5.stderr[-300:]
    print("  5: TETHER_RUIN alone refuses to import; with TETHER_RUIN_RECORD it imports")
    # 6
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "lib.json"
        ag.gamma.save(str(path))
        text = path.read_text(encoding="utf-8") if path.exists() else ""
    vfp = _rows(ag, "veto")[0]["detail"]["fingerprint"]
    assert ag._vetoes and vfp not in text and "veto" not in text, text[:200]
    print(f"  6: the library saved after the game loss ({len(text)} chars) carries no veto")
    # 7
    a7 = R._agent(snaps.Snap(R._spec(2)))
    wa = IFace.Withheld(a7._fingerprint({"s0": 5, "s1": 0})[0], frozenset({("A", None)}))
    for call in (lambda: a7.iface.realise(IFace.Intent(IFace.ELICIT), tuple(a7.actions), (),
                                          a7.env.observe(), a7.env, wa),
                 lambda: a7.iface.undirected(tuple(a7.actions), 0, wa, env=a7.env)):
        try:
            call()
        except ValueError:
            continue
        raise AssertionError("a set built on board A was accepted on board B")
    print("  7: a set built on board A is refused on board B (realise and undirected)")
    # 8
    a8 = R._agent(snaps.Snap(R._spec(4)))
    a8.step("B")
    a8.step("C")
    assert "A" not in a8.iface.table and {"B", "C"} <= set(a8.iface.table), a8.iface.table.keys()
    fp8 = a8._fingerprint(a8.env.observe())[0]
    a8._vetoes.add((fp8, "A", None))
    acted8 = a8.step()
    chosen8 = _rows(a8, "withheld")[-1]["detail"]["chosen"][0]
    assert acted8 and chosen8 != "A", chosen8
    assert "A" not in a8.drive.tried and "A" not in a8.iface.table, (a8.drive.tried, chosen8)
    print(f"  8: the only untried action A vetoed -> the step acts ({chosen8}); A has no draw, "
          f"tried or table entry")
    # 9
    a9 = R._agent(snaps.Snap(R._spec(2)))
    a9._hyp = {"slots": ["s1"], "cond": SimpleNamespace(slot="s1", operand=None), "key": "planted"}
    a9._hyp_plat = set()
    a9.iface.table.clear()
    a9.iface.table.update({"A": {"n": 1, "delta": {}}, "B": {"n": 1, "delta": {("o", "s1"): 1}}})
    a9._withheld = IFace.Withheld("fp9", frozenset({("A", None)}))
    still9 = a9._hyp_still()
    r9 = [r["detail"] for r in _rows(a9, "hyp_still_withheld")]
    assert still9 is None and r9 and r9[-1]["action"] == "A", (still9, r9)
    a9._withheld = IFace.Withheld("fp9", frozenset((x, None) for x in a9.actions))
    assert a9._hyp_still() == "A"
    print(f"  9: hold's only still press A withheld -> none held, row {r9[-1]}; every action "
          f"withheld -> A")
    print("ok")
