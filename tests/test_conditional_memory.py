"""CONDITIONAL IMAGE CLASS MEMORY (Isaiah 2026-11-20): the ImageNet class memory is OPTIONAL, not
BLOCKED. It ACTIVATES only when a memory has been built and loads (parquet data detected through
the plain env var IMAGENET_PARQUET_DIR); otherwise one legible row names the exact state.
  C1  no parquet, no memory          -> recognised_inert ('no data'), no class_memory_active
  C2  synthetic parquet, no memory   -> recognised_inert ('not built'), no class_memory_active
  C3  after a TINY offline build     -> class_memory_active with the right class count (2)
  MF  a mutation that disables the detector makes the active case inert -> 'RED as required'
The offline builder is CLI-only and never runs on the agent path. The fixture is 2 x 2 synthetic
parquet rows made from the repo's shipped shape pictures; no ImageNet data is committed or read.
Seconds.
    python tests/test_conditional_memory.py
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
import gridworld  # noqa: E402
import ledger  # noqa: E402
import recognize  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    ag._aff_book = affordance.Book()
    ag._aff_src = affordance.load_sources()
    ag._rec = None
    ag.env.shape_name = lambda _o: None          # only the picture route, no grid shape
    return ag, led


def events(led):
    return [r for r in led.rows() if r["event"].startswith("recognised")
            or r["event"] == "class_memory_active"]


def picture():
    """A rendered circle (a picture of the kind the memory holds). build_shapes makes it."""
    import numpy as np

    sys.path.insert(0, str(Path(_repo.ROOT) / "library"))
    import build_shapes
    return build_shapes._render_2d(recognize._cv2(), "circle", np.random.default_rng(4242))


def write_parquet(pq_dir: Path) -> None:
    """TINY synthetic ImageNet-shaped fixture: 2 classes x 2 rows, {image:{bytes}, label}."""
    import cv2
    import pyarrow as pa
    import pyarrow.parquet as pq

    pq_dir.mkdir(parents=True, exist_ok=True)
    root = recognize.SHAPES_DIR
    imgs, labels = [], []
    for label, cls in enumerate(("circle", "star")):
        for i in range(2):
            pic = cv2.imread(str(root / "2d" / cls / f"{i}.png"))
            ok, buf = cv2.imencode(".png", pic)
            assert ok
            imgs.append({"bytes": buf.tobytes()})
            labels.append(label)
    pq.write_table(pa.table({"image": pa.array(imgs), "label": pa.array(labels)}),
                   pq_dir / "tiny.parquet")


def run_case(pic) -> list:
    """One live run with a picture; return the recognition-state rows."""
    affordance._CLASS_MEMORY.clear()
    ag, led = agent()
    ag._rec_see(dict(ag.env.observe(), picture=pic))
    return events(led)


def cm_rows(ev: list, event: str) -> list:
    return [r for r in ev if r["event"] == event and r["detail"].get("route") == "class_memory"]


def main() -> int:
    try:
        import cv2  # noqa: F401
    except ImportError:
        print("conditional-memory SKIP: OpenCV is not installed in this interpreter")
        return 0
    assert affordance._RECOGNISED is True, "TETHER_RECOGNISED defaults ON"
    if affordance.load_sources()[3] is not None:
        print("conditional-memory SKIP: the word map is not on this tree")
        return 0

    saved_rdl = os.environ.get("RDL_RECOGNITION_DIR")
    saved_pq = os.environ.get("IMAGENET_PARQUET_DIR")
    pic = picture()
    try:
        with tempfile.TemporaryDirectory() as td:
            pq_dir = Path(td) / "parquet"
            out_dir = Path(td) / "memory"
            out_dir.mkdir(parents=True, exist_ok=True)
            write_parquet(pq_dir)

            # C1: no parquet detected and no memory built -> inert, no active row.
            os.environ.pop("IMAGENET_PARQUET_DIR", None)
            os.environ["RDL_RECOGNITION_DIR"] = str(out_dir)
            e1 = run_case(pic)
            i1 = cm_rows(e1, "recognised_inert")
            assert len(i1) == 1 and "no data" in i1[0]["detail"]["reads"] and \
                "absent" in i1[0]["detail"]["reads"], e1
            assert not [r for r in e1 if r["event"] == "class_memory_active"], e1
            print(f"C1 no parquet + no memory -> {i1[0]['event']}:", i1[0]["detail"]["reads"])

            # C2: synthetic parquet present but no memory built -> inert with 'not built'.
            os.environ["IMAGENET_PARQUET_DIR"] = str(pq_dir)
            e2 = run_case(pic)
            i2 = cm_rows(e2, "recognised_inert")
            assert len(i2) == 1 and "not built" in i2[0]["detail"]["reads"], e2
            assert not [r for r in e2 if r["event"] == "class_memory_active"], e2
            print(f"C2 parquet + no memory -> {i2[0]['event']}:", i2[0]["detail"]["reads"])

            # C3: a TINY offline build, then the same live run -> active with 2 classes.
            built = recognize.build_class_memory_from_parquet(pq_dir, out_dir, per_class=2)
            assert built is not None and Path(built).with_suffix(".json").exists() and \
                Path(built).with_suffix(".npz").exists(), built
            st = recognize.class_memory_status(out_dir)
            assert st["active"] and st["classes"] == 2, st
            e3 = run_case(pic)
            a3 = [r for r in e3 if r["event"] == "class_memory_active"]
            assert len(a3) == 1 and a3[0]["detail"]["classes"] == 2, e3
            assert not cm_rows(e3, "recognised_inert"), e3
            assert any(r["event"] == "recognised" and r["detail"].get("route") == "class_memory"
                       for r in e3), e3
            print(f"C3 after tiny build -> {a3[0]['event']} classes={a3[0]['detail']['classes']}:",
                  a3[0]["detail"]["reads"])

            # MF: disable the detector (force it inert) and confirm the active case flips to
            # inert -- the detector is load-bearing, not decorative. The negative is the point.
            real = recognize.class_memory_status
            try:
                recognize.class_memory_status = lambda _dir=None: {
                    "active": False, "classes": 0, "event": "recognised_inert",
                    "reason": "DETECTOR DISABLED (mutation)"}
                em = run_case(pic)
                assert not [r for r in em if r["event"] == "class_memory_active"], em
                im = cm_rows(em, "recognised_inert")
                assert len(im) == 1 and "mutation" in im[0]["detail"]["reads"], em
                print("MF detector disabled -> active case reports inert:",
                      im[0]["detail"]["reads"], "RED as required")
            finally:
                recognize.class_memory_status = real
    finally:
        if saved_rdl is None:
            os.environ.pop("RDL_RECOGNITION_DIR", None)
        else:
            os.environ["RDL_RECOGNITION_DIR"] = saved_rdl
        if saved_pq is None:
            os.environ.pop("IMAGENET_PARQUET_DIR", None)
        else:
            os.environ["IMAGENET_PARQUET_DIR"] = saved_pq
        affordance._CLASS_MEMORY.clear()

    print("conditional-memory: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
