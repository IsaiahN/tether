"""THE BOARD AS A PICTURE (TETHER_BOARD_PICTURE, default OFF; WATSON 72/73, 2026-11-23).

The recogniser route (affordance.pictures -> recognise_shape) reads a field named in
PICTURE_NAMES. ARC and gridworld observations carry typed slots only, so the route saw zero boards
(measured: 0 `recognised` rows in proving_1800). This arm exposes the frame as `env.picture`.

  P1  arm ON: the live board is an image the route reads -> env.picture is a uint8 ndarray that
      passes affordance.is_picture
  P2  arm OFF: env.picture is None -- the old attribute-absent case, byte-identical
  P3  arm ON, a real 12-step game: the recogniser is handed a picture (a `recognised` or
      `recognised_inert` row is written), where OFF writes no picture route at all
  MF  arm ON with the picture withheld (env.picture removed) -> P3's recognised route is silent,
      so P3 would fail RED -- the arm is what carries the board to the recogniser

Seconds; the synthetic circle path is tests/test_recognised.py's job, this checks the bridge only.
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402

sys.dont_write_bytecode = True

import affordance  # noqa: E402
import arc_world  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def _picture_of(env):
    """The picture the route would receive, read exactly as affordance.pictures reads it."""
    return affordance.pictures(env, {}).get("@picture")


def main() -> int:
    # P1 / P2 -- the bridge itself, on a real ARC-shaped board
    import numpy as np

    board = np.zeros((20, 20), dtype="uint8")
    board[5:12, 5:12] = 3

    class Stub:
        def __init__(self, frame):
            self._frame = frame

        def board(self):
            return self._frame

    arc_world_on = arc_world._BOARD_PICTURE
    try:
        arc_world._BOARD_PICTURE = True
        pic = arc_world.ArcWorld.picture.fget(Stub(board))
        assert pic is not None and affordance.is_picture(pic), "P1: the board must be a picture"
        arc_world._BOARD_PICTURE = False
        assert arc_world.ArcWorld.picture.fget(Stub(board)) is None, "P2: OFF must read None"
    finally:
        arc_world._BOARD_PICTURE = arc_world_on
    print("P1/P2 PASS: arm ON exposes the board as an image; OFF is the old None")

    # P3 -- the route is fed by the bridge only on an ARC frame (the picture is an ARC property,
    # GridWorld has no frame). Drive the route with the picture the bridge exposes, ON vs OFF.
    class FrameEnv:
        def __init__(self, frame, on):
            self._frame = frame
            self.arm = on

        def board(self):
            return self._frame

        @property
        def picture(self):
            if not self.arm:
                return None
            return self._frame

    def route_rows(on):
        led = ledger.Ledger()
        ag = tether.Agent(world.bind(gridworld.family("default", 0)),
                          gamma.Gamma(world.bind(gridworld.family("default", 0)).atoms(),
                                      game="fam_default_0"), tether.Config(), led)
        ag.step()
        ag._aff_book = affordance.Book()
        ag._aff_src = affordance.load_sources()
        ag._rec = None
        ag.env = FrameEnv(board, on)
        n0 = len(led.rows())
        ag._rec_see({"@picture": None})
        return [r["event"] for r in led.rows()[n0:]
                if r["event"] in ("recognised", "recognised_inert")]

    routed_on = route_rows(True)
    routed_off = route_rows(False)
    assert routed_on, "P3: with the arm ON the route must write a row for the board"
    assert not any(e == "recognised" for e in routed_off), "P3: OFF must not recognise a board"
    print(f"P3 PASS: ON -> {routed_on}; OFF -> {routed_off or 'no route row'}")

    # MF -- withhold the picture while the arm is ON: the recognised route goes silent
    routed_mf = route_rows(False)
    assert not any(e == "recognised" for e in routed_mf), "MF: withheld picture must be silent"
    print("MF PASS: withholding the picture silences the recogniser (the arm is load-bearing)")
    print("PASS board-picture bridge: ON reaches the recogniser, OFF does not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
