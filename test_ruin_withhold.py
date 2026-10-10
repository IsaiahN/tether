"""7a(5) C, ruin ordered first (R3 Part 1; the reviewer 2026-10-10 10:41Z, 11:53Z). With TETHER_RUIN
on, a pair the veto floor holds for THIS board is withheld from the one choose() call, at the sites
below the seam where the button and coordinate are chosen, unless every option is vetoed.

  must-pass: snaps AVOID (s0 must never read 3) from s0=2, 4 lives, the agent CHOOSING: with C
     OFF it repeats its own death (a held key dies again); with C ON no held key dies again,
     every @ruin row's choice is outside its withheld set, and the FULL gate passes;
  1. on a DIFFERENT board nothing is withheld;
  2. a positioned action at another coordinate on the same board is offered (only the vetoed
     coordinate is skipped), at _made's spots and at TOUCH route 1;
  3. every option vetoed: the step still acts, all_vetoed True, and `why` says so;
  4. choose() is called exactly once per step;
  5. TETHER_RUIN without TETHER_RUIN_RECORD refuses to start;
  6. a library saved after a death carries no veto (Fig 4: a recording never crosses up);
  7. a withheld set built on board A and passed while the env shows board B is refused;
  8. EXPLORATION: with the board's only untried action vetoed, the step acts, and no draw, tried
     count or table entry is recorded for the withheld action.

    python test_ruin_withhold.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import gate
import interface as IFace
import snaps
import test_ruin_record as R
import tether
from world import bind

sys.dont_write_bytecode = True


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


def _lives(start: int, ruin: bool, lives: int = 4, steps: int = 12) -> tuple:
    """The agent CHOOSING, from the same board each life (deterministic, so a retry re-meets it):
    (agent, ending per life, veto keys in order, the spy). A life ends at a death or `steps`."""
    tether._RUIN_RECORD, tether._RUIN = True, ruin
    snap = snaps.Snap(R._spec(start))
    ag = R._agent(snap)
    spy, ends, acted = _Spy(ag), [], 0
    for lv in range(lives):
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


if __name__ == "__main__":
    off, off_ends, off_keys, _s, _n = _lives(2, False)
    ag, ends, keys, spy, acted = _lives(2, True)
    off_rep, rep = len(off_keys) - len(set(off_keys)), len(keys) - len(set(keys))
    assert off_rep > 0, (off_ends, off_keys)          # OFF: the agent repeats its own death
    assert rep == 0 and ends.count("death") < off_ends.count("death"), (ends, keys)
    w = _rows(ag, "withheld")
    assert w and all(r["slot"] == "@ruin" and r["step"] == "PLAN" for r in w), w[:2]
    assert all(not r["detail"]["all_vetoed"] for r in w), [r["detail"] for r in w]
    assert all(r["detail"]["chosen"] not in r["detail"]["withheld"] for r in w), w
    out = gate.check(ag.led.rows())
    assert out["verdict"] == gate.PASS, out
    print(f"  must-pass, s0=2, 4 lives of up to 12 steps, the agent choosing: OFF endings "
          f"{off_ends}, {off_rep} deaths repeat a held key; ON endings {ends}, 0 repeats, "
          f"{len(w)} @ruin rows, none choosing a withheld pair; full gate passes "
          f"({len(ag.led.rows())} rows)")
    # 4
    assert spy.chose == acted, (spy.chose, acted)
    print(f"  4: choose() called {spy.chose} times for {acted} steps")
    _on()
    # 1
    other = R._agent(snaps.Snap(R._spec(2)))
    other.step("A")
    other.retarget(bind(snaps.Snap(R._spec(1))), 1, "death")
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
    assert acted and w3 and w3[-1]["detail"]["all_vetoed"], (acted, w3)
    assert any(e for _on, _o, e in sp3.every), sp3.every
    print(f"  3: every option vetoed -> the step acts ({w3[-1]['detail']['chosen']}), "
          f"all_vetoed True, '{IFace.ALL_VETOED}' set")
    # 5
    env5 = {**os.environ, "TETHER_RUIN": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    env5.pop("TETHER_RUIN_RECORD", None)
    p5 = subprocess.run([sys.executable, "-c", "import tether"], env=env5, capture_output=True,
                        text=True, cwd=Path(__file__).parent, check=False)
    ok5 = subprocess.run([sys.executable, "-c", "import tether"],
                         env={**env5, "TETHER_RUIN_RECORD": "1"}, capture_output=True,
                         text=True, cwd=Path(__file__).parent, check=False)
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
    print(f"  6: the library saved after the death ({len(text)} chars) carries no veto")
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
    print("ok")
