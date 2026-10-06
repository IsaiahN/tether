"""THE ENTRY SEAT -- the Kaggle path, offline, on a FAKE wrapper. No ARC board is touched.

The fake mirrors the real arc_agi wrappers where it matters here: it RESETS IN ITS OWN __init__
(both real ones do), holds the last frame as `observation_space`, and takes
`step(action, data=None, reasoning=None)`. Every command it receives is logged.

What this seat guards (the reviewer, 2026-10-06; Isaiah's 2026-09-29 ruling):
  1. `wire()` on a self-resetting wrapper issues EXACTLY ONE RESET -- F452/F454's fix, held;
  2. a planted RESET,RESET is REFUSED live (not sent, logged, counted);
  3. the same plant RAISES in strict mode -- the failure path is shown to fire;
  4. a RESET after a real action IS sent, and re-arms the guard -- so it refuses pairs, not resets.
"""
from __future__ import annotations

import logging
import os
import sys

import numpy as np
from arcengine import FrameDataRaw, GameAction, GameState

import arc_holdout

sys.dont_write_bytecode = True


class FakeWrapper:
    """A 64x64 board, one block the four directions move. `script` forces a state after N steps."""

    def __init__(self, script=None, actions=(1, 2, 3, 4, 6)):
        self.calls, self._last, self.script = [], None, dict(script or {})
        self.actions, self.pos, self.n = list(actions), [30, 30], 0
        self.reset()

    @property
    def observation_space(self):
        return self._last

    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        r, c = self.pos
        g[r:r + 4, c:c + 4] = 3
        g[5:9, 5:9] = 7
        f = FrameDataRaw(game_id="fake-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f

    def reset(self):
        self.calls.append("RESET")
        self.pos = [30, 30]
        return self._frame(GameState.NOT_FINISHED)

    def step(self, action, data=None, reasoning=None):
        self.calls.append(action.name)
        self.last_data, self.last_reasoning = data, reasoning   # what a click actually carried
        if action is GameAction.RESET:
            self.pos = [30, 30]
            return self._frame(GameState.NOT_FINISHED)
        self.n += 1
        d = {1: (-2, 0), 2: (2, 0), 3: (0, -2), 4: (0, 2)}.get(action.value)
        if d:
            self.pos = [min(max(self.pos[0] + d[0], 0), 60), min(max(self.pos[1] + d[1], 0), 60)]
        return self._frame(self.script.get(self.n, GameState.NOT_FINISHED))


def check_wire_issues_one_reset():
    w = FakeWrapper()
    env = arc_holdout.wire(w, "fake")[0]
    assert w.calls == ["RESET"], f"construction sent {w.calls}; Isaiah: never RESET,RESET"
    assert isinstance(env.w, arc_holdout.ResetGuard), "ArcWorld is not behind the guard"


def check_planted_pair_is_refused_live():
    w = FakeWrapper()
    g = arc_holdout.ResetGuard(w)
    logging.disable(logging.ERROR)
    try:
        g.reset()
        g.step(GameAction.RESET)
    finally:
        logging.disable(logging.NOTSET)
    assert w.calls == ["RESET"], f"a second RESET reached the wrapper: {w.calls}"
    assert g.refused == 2, f"refusals not counted: {g.refused}"


def check_planted_pair_raises_in_strict_mode():
    g = arc_holdout.ResetGuard(FakeWrapper(), strict=True)
    try:
        g.reset()
    except RuntimeError:
        return
    raise AssertionError("strict mode let RESET,RESET through without raising")


def check_reset_after_an_action_is_sent_and_rearms():
    w = FakeWrapper()
    g = arc_holdout.ResetGuard(w, strict=True)
    g.step(GameAction.ACTION1)
    g.step(GameAction.RESET)
    assert w.calls == ["RESET", "ACTION1", "RESET"], f"a lawful RESET was not sent: {w.calls}"
    try:
        g.reset()
    except RuntimeError:
        return
    raise AssertionError("the guard did not re-arm after a sent RESET")



def check_a_death_ends_the_run_with_one_reset():
    """GAME_OVER: the entry point never sends RESET (who-presses rule); until Isaiah rules on
    offering RESET to the agent (F450), a death ENDS the run."""
    import tether_agent
    w = FakeWrapper(script={2: GameState.GAME_OVER})
    out = tether_agent.run(w, "fake", max_actions=6)
    assert out["end"] == "death", f"a death did not end the run: {out}"
    assert w.calls.count("RESET") == 1, f"RESET sent around a death: {w.calls}"
    assert out["acted"] == 2, f"acted past the death: {out}"


def check_a_win_ends_the_run():
    import tether_agent
    w = FakeWrapper(script={2: GameState.WIN})
    out = tether_agent.run(w, "fake", max_actions=6)
    assert out["end"] == "advance", f"a WIN did not end the run: {out}"
    assert w.calls.count("RESET") == 1, f"RESET sent around a win: {w.calls}"


def check_a_click_carries_its_position():
    """Interface bug 3, on the path the entry point uses: ACTION6 with x, y reaches the wrapper
    as `data` -- `set_data` belongs to the GameAction-object path an overridden main() bypasses."""
    w = FakeWrapper()
    env = arc_holdout.wire(w, "fake")[0]
    env.step("ACTION6", 12, 34)
    assert w.calls[-1] == "ACTION6" and w.last_data == {"x": 12, "y": 34}, (
        f"the click arrived as {w.calls[-1]} {w.last_data}")


def check_run_saves_after_a_death_a_win_and_the_cap():
    """THE ENTRY POINT CARRIES (F471): with a library path, run() keeps the game's library
    whatever ended it -- a death, a win, or the cap. Without one it saves nothing."""
    import pathlib
    import tempfile

    import tether_agent
    with tempfile.TemporaryDirectory() as d:
        for i, script in enumerate(({2: GameState.GAME_OVER}, {2: GameState.WIN}, {})):
            path = str(pathlib.Path(d) / f"lib{i}.json")
            out = tether_agent.run(FakeWrapper(script=script), "fake", max_actions=4,
                                   library=path)
            assert out["saved"] and pathlib.Path(path).exists(), f"not kept after {out['end']}"
        out = tether_agent.run(FakeWrapper(), "fake", max_actions=2)
        assert out["saved"] is None, "a run with no library path saved something"


def check_a_save_killed_midway_leaves_the_previous_library_whole():
    """ATOMIC (F471): a save interrupted mid-write -- the platform's time limit -- must leave
    the library already on disk intact and loadable, never a half-written one."""
    import pathlib
    import tempfile

    import gamma
    inc = gamma.Atom("inc", lambda v, _c: v + 1, "val", "val")
    g = gamma.Gamma([inc], game="A")
    g.accept(gamma.Term(atoms=(inc, inc)), seq=0, residual="s@0")
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        g.save(path)
        before = pathlib.Path(path).read_text(encoding="utf-8")
        real = pathlib.Path.write_text

        def dies(self, data, *a, **k):
            real(self, data[: len(data) // 2], *a, **k)
            raise KeyboardInterrupt("killed mid-save")
        pathlib.Path.write_text = dies
        try:
            g.save(path)
        except KeyboardInterrupt:
            pass
        finally:
            pathlib.Path.write_text = real
        assert pathlib.Path(path).read_text(encoding="utf-8") == before, "a kill tore the library"
        rep = gamma.Gamma([inc], game="B").load(path)
        assert rep.get("loaded") == 1 and not rep.get("cold"), rep


def check_an_unreadable_library_loads_cold_and_says_so():
    """A missing or unreadable library is a COLD start, reported -- never a crash (F471)."""
    import pathlib
    import tempfile

    import gamma
    inc = gamma.Atom("inc", lambda v, _c: v + 1, "val", "val")
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "lib.json"
        path.write_text('{"terms": [', encoding="utf-8")
        rep = gamma.Gamma([inc], game="A").load(str(path))
    assert rep.get("loaded") == 0 and rep.get("cold"), rep


def fake_make(_game, _card):
    """Module-level, so a worker PROCESS can take it -- as the real maker must be."""
    return FakeWrapper()


def check_the_runner_carries_in_order_per_worker():
    """THE K-WORKER RUNNER (F472): games assigned by ORDER, each worker its OWN library, and the
    second game in a worker LOADS what the first saved -- the carry. Run once in-process and once
    with real processes, so the parallel path itself executes."""
    import os
    import tempfile

    import tether_runner
    games = ["g0", "g1", "g2", "g3"]
    assert tether_runner.assign(games, 2) == [["g0", "g2"], ["g1", "g3"]]
    # IN-PROCESS: one worker, the whole sequence -- each game after the first LOADS the last.
    # (In-process workers run one after another, so a second one would find the ceiling spent;
    # that is the time budget working, not a defect.)
    with tempfile.TemporaryDirectory() as d:
        rec = tether_runner.run(games, "card", fake_make, d, k=1, processes=False,
                                ceiling_s=30, margin_s=1)
        loaded = [g["loaded"] for g in rec["records"][0]["games"]]
        assert loaded == [False, True, True, True], rec
    # REAL PROCESSES: two workers in parallel, each its OWN library, each carrying.
    with tempfile.TemporaryDirectory() as d:
        rec = tether_runner.run(games, "card", fake_make, d, k=2, processes=True,
                                ceiling_s=20, margin_s=1)
        assert rec["workers"] == 2 and len(rec["records"]) == 2, rec
        libs = {r["library"] for r in rec["records"]}
        assert len(libs) == 2 and all(os.path.exists(p) for p in libs), rec
        for r in rec["records"]:
            assert [g["loaded"] for g in r["games"]] == [False, True], r
            assert all(g["allowance_s"] > 0 for g in r["games"]), r


def check_serve_opens_one_card_and_always_closes_it():
    """THE OFFICIAL SCORING PATH (F473): the games the gateway serves, ONE card, every game made
    with it, the card closed once after the workers -- and closed even when a worker fails."""
    import contextlib
    import tempfile

    import tether_runner
    log = []
    made = []

    def make(game, card):
        made.append((game, card))
        return FakeWrapper()
    with tempfile.TemporaryDirectory() as d:
        rec = tether_runner.serve(lambda: ["g0", "g1"], lambda: log.append("open") or "C1",
                                  lambda c: log.append(("close", c)), make, d, k=1,
                                  processes=False, ceiling_s=20, margin_s=1)
    assert log == ["open", ("close", "C1")], log
    assert made == [("g0", "C1"), ("g1", "C1")] and rec["card"] == "C1", (made, rec)

    def broken(_game, _card):
        raise RuntimeError("a worker failed")
    log.clear()
    with tempfile.TemporaryDirectory() as d, contextlib.suppress(RuntimeError):
        tether_runner.serve(lambda: ["g0"], lambda: log.append("open") or "C2",
                            lambda c: log.append(("close", c)), broken, d, k=1,
                            processes=False, ceiling_s=20, margin_s=1)
    assert log == ["open", ("close", "C2")], f"a failed run left the card open: {log}"


def check_the_notebook_runs_our_runner_in_place_of_swarm():
    """The generator changes exactly two things in ARC's sample (F473): the my_agent.py body, and
    the run line -- `python main.py --agent myagent` becomes our runner. Checked on a minimal
    synthetic sample with the shape it relies on, so it runs in every checkout."""
    import json
    import pathlib
    import tempfile

    import kaggle_bundle
    cells = [{"cell_type": "code", "source": ["!pip install arc-agi"], "outputs": [],
              "execution_count": 1, "metadata": {}},
             {"cell_type": "code", "source": ["%%writefile /kaggle/working/my_agent.py\nold\n"],
              "outputs": [], "execution_count": 2, "metadata": {}},
             {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": 3,
              "source": ['f.write("""\"myagent\": MyAgent""")\n',
                         "!cd /kaggle/working/ARC-AGI-3-Agents && "
                         "python main.py --agent myagent\n"]}]
    with tempfile.TemporaryDirectory() as d:
        sample = pathlib.Path(d) / "sample.ipynb"
        sample.write_text(json.dumps({"cells": cells, "metadata": {}, "nbformat": 4,
                                      "nbformat_minor": 5}), encoding="utf-8")
        mine = pathlib.Path(d) / "my_agent.py"
        mine.write_text("x = 1\n", encoding="utf-8")
        out = kaggle_bundle.notebook(str(mine), d, str(sample))
        nb = json.loads(pathlib.Path(out).read_text(encoding="utf-8"))
    run = "".join(nb["cells"][2]["source"])
    assert "python -m agents.templates.my_agent" in run and "main.py" not in run, run
    assert "".join(nb["cells"][1]["source"]).endswith("x = 1\n"), "the agent body was not written"


def check_the_bundle_carries_every_module_the_harness_file_imports():
    """The bundle's file list is an IMPORT CENSUS from its entry. kaggle_agent imports the runner
    only inside runner_main(), so a census from tether_agent missed it -- an ImportError that
    would surface on Kaggle and nowhere else (F473). Every module it imports must be in it."""
    import ast
    import inspect

    import kaggle_bundle
    entry = inspect.signature(kaggle_bundle.build).parameters["entry"].default
    files = set(kaggle_bundle.census(entry))
    with open("kaggle_agent.py", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    ours = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    ours |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
    local = {m for m in ours if (m.split(".")[0] + ".py") in set(os.listdir("."))}
    missing = sorted(m for m in local if m.split(".")[0] + ".py" not in files)
    assert not missing, f"the bundle lacks {missing}"


if __name__ == "__main__":
    checks = [v for k, v in sorted(globals().items()) if k.startswith("check_")]
    for fn in checks:
        fn()
    print(f"entry: {len(checks)} checks passed")
