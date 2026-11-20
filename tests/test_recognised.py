"""RECOGNISED (TETHER_RECOGNISED, default ON; write-up 42 handoff item 4, "Recognition into the
agent"): a picture's class read exactly as a shape_name. Fixtures by hand.
  R1  a fixture observation carrying a drawn circle -> a `recognised` row (circle / disc, synset,
      route, distance, margin, not abstained, stamp) and an affordance_prior for ball, through
      the word map's shape_bridge (the landed sources)
  R2  the same picture again: no second row (once per holder and picture); a per-object picture
      ('o1.picture') is recognised for that object
  R3  a class memory present -> a second row, route class_memory (votes, margin, inliers)
  R6  MUST-FAIL: env var RDL_RECOGNITION_DIR -> empty dir -> one recognised_inert naming the
      absence (the old hardcoded path dropped this route silently on Kaggle); real memory ->
      a class_memory row. Both halves are asserted.
  R4  cv2 is not imported by importing affordance / tether (lazy, never at module level)
  MF-R1 TETHER_RECOGNISED OFF: no recognised rows and no prior from the picture -> RED as required
  R5  gridworld 12 steps ON and OFF both pass the gate; ON carries only the one recognised_inert
Seconds.
    python tests/test_recognised.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import affordance  # noqa: E402
import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

NO_MEMORY = Path(tempfile.gettempdir()) / "tether_recognised_no_class_memory"


def circle(seed=4242):
    """A circle as a PICTURE OF THE KIND THE MEMORY HOLDS: one rendered variant from the
    generator, with its own seed, colour, scale and offset.
    Why not a hand-drawn cv2.circle: a mathematically ideal circle has every higher Hu moment
    EXACTLY zero, a case no rendered variant and no photograph ever is. Charging a picture for
    the symmetry of an idealisation tested the arithmetic, not the recogniser (measured
    2026-11-16: the ideal circle abstained at distance 7.58 while a rendered variant is named
    at once). The ideal case is recorded as a known limit in the status page."""
    import numpy as np

    import recognize as R
    sys.path.insert(0, str(Path(_repo.ROOT) / "library"))
    import build_shapes  # the generator itself: the same drawing the memory came from
    return build_shapes._render_2d(R._cv2(), "circle", np.random.default_rng(seed))


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    ag._aff_book = affordance.Book()
    ag._aff_src = affordance.load_sources()
    ag._rec = None
    ag.env.shape_name = lambda _o: None          # no grid shape names: only the picture names
    return ag, led


def rows(led, n0, prefix):
    return [r for r in led.rows()[n0:] if r["event"].startswith(prefix)]


def see(ag, obs):
    if affordance._RECOGNISED:
        ag._rec_see(obs)
    ag._aff_see(obs)


def main() -> int:
    mods = set(sys.modules)
    assert "cv2" not in mods, "R4: cv2 imported at module level by affordance / tether / gate"
    print("R4 importing affordance, tether, gate, gridworld: cv2 not imported: GREEN")
    assert affordance._RECOGNISED is True, "the arm defaults ON"
    try:
        import cv2  # noqa: F401
    except ImportError:
        print("R1-R3 SKIP: OpenCV is not installed in this interpreter")
        return 0
    affordance.CLASS_MEMORY_DIR = NO_MEMORY
    affordance._CLASS_MEMORY.clear()
    if affordance.load_sources()[3] is not None:
        print("R1 SKIP: the word map is not on this tree")
        return 0

    pic = circle()
    ag, led = agent()
    obs = dict(ag.env.observe(), picture=pic)
    n0 = len(led.rows())
    see(ag, obs)
    see(ag, obs)                                  # the same picture again: no second row
    rr = rows(led, n0, "recognised")
    # the class-memory dir here is empty (NO_MEMORY), so one recognised_inert names its absence
    assert [r["event"] for r in rr] == ["recognised", "recognised_inert"], rr
    assert "absent" in rr[1]["detail"]["reads"] and rr[1]["detail"]["route"] == "class_memory", rr
    d = rr[0]["detail"]
    assert d["class"] == "circle" and d["grid_shape_name"] == "disc" and not d["abstained"], d
    for k in ("class", "synset", "dim", "grid_shape_name", "bridge", "route", "votes", "distance",
              "margin", "abstained", "stamp"):
        assert k in d, (k, d)
    assert d["synset"] == "n13873502" and d["dim"] == 2 and d["route"] in ("contour", "akaze")
    assert d["stamp"]["stage"] == "instance" and d["standing"] is None, d
    pr = [r for r in rows(led, n0, "affordance_prior") if r["slot"] == "@picture"]
    assert pr and {r["detail"]["concept"] for r in pr} == {"ball"}, pr
    p0 = pr[0]["detail"]
    assert p0["recognised"] == "circle" and p0["via"] == "shape_bridge", p0
    print(f"R1 drawn circle -> recognised {d['class']} ({d['grid_shape_name']}, {d['synset']}, "
          f"route {d['route']}, distance {d['distance']}, margin {d['margin']}) -> "
          f"affordance_prior {p0['shape_name']} -> {p0['form']} -> {p0['concept']} "
          f"({[r['detail']['property'] for r in pr]}): GREEN")

    ag2, led2 = agent()
    obs2 = dict(ag2.env.observe(), **{"o1.picture": pic[:, :, 0].copy()})   # grey, per object
    n0 = len(led2.rows())
    see(ag2, obs2)
    r2 = [r for r in rows(led2, n0, "recognised") if r["event"] == "recognised"]
    assert [(r["slot"], r["detail"]["class"]) for r in r2] == [("o1", "circle")], r2
    p2 = [r for r in rows(led2, n0, "affordance_prior") if r["slot"] == "o1"]
    assert p2 and p2[0]["detail"]["concept"] == "ball", p2
    print("R2 once per picture; a per-object grey picture o1.picture -> o1 recognised circle -> "
          "ball: GREEN")

    import recognize
    with tempfile.TemporaryDirectory() as tdir:
        import cv2 as _cv
        root = recognize.SHAPES_DIR
        by = {c: [_cv.imread(str(root / "2d" / c / f"{i}.png")) for i in range(4)]
              for c in ("circle", "star")}
        recognize.save(recognize.build_memory(by, synsets={"circle": "n13873502"},
                                              source="fixture"), Path(tdir) / "memory")
        affordance._CLASS_MEMORY.clear()
        affordance.CLASS_MEMORY_DIR = Path(tdir)
        try:
            ag3, led3 = agent()
            see(ag3, dict(ag3.env.observe(), picture=by["star"][0]))
            r3 = [r for r in rows(led3, 0, "recognised") if r["event"] == "recognised"]
            routes = [r["detail"]["route"] for r in r3]
            assert len(r3) == 2 and routes[1] == "class_memory", r3
            assert not [r for r in rows(led3, 0, "recognised")
                        if r["event"] == "recognised_inert"
                        and r["detail"].get("route") == "class_memory"], r3
            c3 = r3[1]["detail"]
            assert "votes" in c3 and "margin" in c3 and c3["stamp"]["source"] == "fixture", c3
            print(f"R3 class memory present -> a class_memory row: class {c3['class']}, votes "
                  f"{c3['votes']}, margin {c3['margin']}, inliers {c3['inliers']}, abstained "
                  f"{c3['abstained']}: GREEN")
        finally:
            affordance.CLASS_MEMORY_DIR = NO_MEMORY
            affordance._CLASS_MEMORY.clear()

    # R6 (AKAZE verification 2026-11-16, MUST-FAIL): the class-memory dir comes from the plain
    # env var RDL_RECOGNITION_DIR. An EMPTY dir must write one recognised_inert naming the
    # absence -- the old hardcoded Windows path dropped the route SILENTLY on Kaggle. A real
    # memory at the configured dir must write a class_memory row. Delete either assertion and
    # the corresponding half fails: this is a must-fail, not a smoke test.
    _saved_rdl = os.environ.get("RDL_RECOGNITION_DIR")
    try:
        with tempfile.TemporaryDirectory() as empty:
            os.environ["RDL_RECOGNITION_DIR"] = empty
            affordance._CLASS_MEMORY.clear()
            ag6, led6 = agent()
            see(ag6, dict(ag6.env.observe(), picture=pic))
            ev6 = rows(led6, 0, "recognised")
            inert6 = [r for r in ev6 if r["event"] == "recognised_inert"
                      and r["detail"].get("route") == "class_memory"]
            assert len(inert6) == 1 and "absent" in inert6[0]["detail"]["reads"], ev6
            assert inert6[0]["detail"]["route"] == "class_memory", ev6
            assert not any(r["event"] == "recognised"
                           and r["detail"].get("route") == "class_memory" for r in ev6), ev6
            print("R6 env var -> empty dir: one recognised_inert naming the absence:",
                  inert6[0]["detail"]["reads"], "GREEN")

        with tempfile.TemporaryDirectory() as real:
            import cv2 as _cv
            root = recognize.SHAPES_DIR
            pics = {c: [_cv.imread(str(root / "2d" / c / f"{i}.png")) for i in range(4)]
                    for c in ("circle", "star")}
            recognize.save(recognize.build_memory(pics, synsets={"circle": "n13873502"},
                                                  source="fixture-env"), Path(real) / "memory")
            os.environ["RDL_RECOGNITION_DIR"] = real
            affordance._CLASS_MEMORY.clear()
            ag7, led7 = agent()
            see(ag7, dict(ag7.env.observe(), picture=pics["star"][0]))
            ev7 = rows(led7, 0, "recognised")
            cm7 = [r for r in ev7 if r["event"] == "recognised"
                   and r["detail"].get("route") == "class_memory"]
            assert len(cm7) == 1 and cm7[0]["detail"]["stamp"]["source"] == "fixture-env", ev7
            assert not [r for r in ev7 if r["event"] == "recognised_inert"
                        and r["detail"].get("route") == "class_memory"], ev7
            print("R6 env var -> real memory: one class_memory row:", cm7[0]["detail"]["class"],
                  "GREEN")
    finally:
        if _saved_rdl is None:
            os.environ.pop("RDL_RECOGNITION_DIR", None)
        else:
            os.environ["RDL_RECOGNITION_DIR"] = _saved_rdl
        affordance._CLASS_MEMORY.clear()

    affordance._RECOGNISED = False
    try:
        ag4, led4 = agent()
        see(ag4, dict(ag4.env.observe(), picture=pic))
        off = rows(led4, 0, "recognised")
        offp = [r for r in rows(led4, 0, "affordance_prior") if r["slot"] == "@picture"]
        assert not off and not offp and ag4.__dict__.get("_rec") is None, (off, offp)
    finally:
        affordance._RECOGNISED = True
    print("MF-R1 TETHER_RECOGNISED OFF: no recognised rows, no prior from the picture -> "
          "RED as required")

    for on in (True, False):
        affordance._RECOGNISED = on
        try:
            env = world.bind(gridworld.family("default", 0))
            led5 = ledger.Ledger()
            ag5 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"),
                               tether.Config(), led5)
            for _ in range(12):
                ag5.step()
            ag5.end_run("cap")
            v = gate.check(led5.rows())["verdict"]
            assert v == "pass", ("R5", on, v)
            rr5 = [r["event"] for r in rows(led5, 0, "recognised")]
            assert rr5 == (["recognised_inert"] if on else []), (on, rr5)
            print(f"   gridworld {'ON' if on else 'OFF'}: gate {v}, recognition rows {rr5}")
        finally:
            affordance._RECOGNISED = True
    print("R5 gridworld 12 steps ON and OFF: both pass the gate; ON only the one inert row: GREEN")
    print("recognised: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
