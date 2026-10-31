"""17 CHANGE_TALLY (TETHER_CHANGE_TALLY, default ON; the reviewer r481; Isaiah 2026-10-31 02:15).
The interface alone, on hand-made presses (audit), no game; each check in its own process.
  check_mustfail_dead_last  two mapped actions, both unknown in a new context (the variety rule's
                            "not yet known here" tier): A pressed in 2 contexts and never changed
                            anything, B always did. OFF, the tier's own draw realises A for some
                            context; ON, A goes last there and B is realised, with the tally's note
  check_hold_unmapped_first an unmapped action is still realised first under ON
  check_hold_reset          after a RESET, ELICIT with only RESET offered is refused, ON as OFF
  check_hold_collapse       ON never repeats a high-ratio action while another offered action's
                            effect here is unknown: the tier decides, the tally only inside it
  check_off_identity        MUST-HOLD: TETHER_CHANGE_TALLY=0 (off_env) byte-equal to 3813c79 on the
                            fake whole run
    python tests/test_change_tally.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "3813c79"        # general-agent before 17

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import interface as IF
mode = sys.argv[2]
A, B, C = "ACTION1", "ACTION2", "ACTION3"
before, same, moved = {"o1.row": 1}, {"o1.row": 1}, {"o1.row": 2}
out = {}


def fresh():
    t = IF.Interface()
    for ctx in ((("k", 1),), (("k", 2),)):
        t.audit(IF.Realisation(A), before, same, ctx=ctx)     # A: never changes anything
        t.audit(IF.Realisation(B), before, moved, ctx=ctx)    # B: always does
    return t


if mode == "dead":
    picks = {}
    for i in range(3, 40):
        t = fresh()
        r = t.realise(IF.Intent(IF.ELICIT), (A, B), ctx=(("k", i),))
        picks[i] = [r.action if r else None, t.tally_note]
    out["picks"] = picks
    out["table"] = {a: {k: v for k, v in fresh().table[a].items() if k in ("n", "changed_n")}
                    for a in (A, B)}
elif mode == "unmapped":
    t = fresh()
    r = t.realise(IF.Intent(IF.ELICIT), (A, B, C), ctx=(("k", 9),))
    out["pick"] = r.action if r else None
elif mode == "reset":
    t = fresh()
    t.audit(IF.Realisation(IF.RESET), before, same, ctx=(("k", 1),))
    t.note_sent(IF.RESET)
    r = t.realise(IF.Intent(IF.ELICIT), (IF.RESET,), ctx=(("k", 1),))
    out["pick"] = r.action if r else None
elif mode == "collapse":
    t = IF.Interface()
    k1, k2 = (("k", 1),), (("k", 2),)
    for _ in range(3):
        t.audit(IF.Realisation(B), before, moved, ctx=k1)      # B known here, always changes
    t.audit(IF.Realisation(A), before, same, ctx=k2)           # A mapped, unknown in k1
    r = t.realise(IF.Intent(IF.ELICIT), (A, B), ctx=k1)
    out["pick"] = r.action if r else None
print(json.dumps(out, default=str))
'''


def _probe(mode: str, arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_CHANGE_TALLY=arm)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), mode], env=env,
                         capture_output=True, text=True, timeout=600, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def check_mustfail_dead_last() -> None:
    off, on = _probe("dead", "0"), _probe("dead", "1")
    assert on["table"]["ACTION1"] == {"n": 2, "changed_n": 0}, on["table"]
    assert on["table"]["ACTION2"] == {"n": 2, "changed_n": 2}, on["table"]
    dead_off = [i for i, (a, _n) in off["picks"].items() if a == "ACTION1"]
    assert dead_off, ("MUST-FAIL occasion: OFF never realised the dead action", off["picks"])
    assert all(a == "ACTION2" for a, _n in on["picks"].values()), on["picks"]
    i = dead_off[0]
    note = on["picks"][i][1]
    assert note and note["pick"] == "ACTION2" and note["inert_last"] == ["ACTION1"], note
    print(f"  OFF: the tier's draw realised the dead ACTION1 in {len(dead_off)} of "
          f"{len(off['picks'])} new contexts; ON: ACTION2 in all {len(on['picks'])}, the note "
          f"says inert_last {note['inert_last']}, ratio {note['ratio']}")


def check_hold_unmapped_first() -> None:
    on = _probe("unmapped", "1")
    assert on["pick"] == "ACTION3", on
    print("  ON: the unmapped ACTION3 is realised first, over the tallied ACTION1 and ACTION2")


def check_hold_reset() -> None:
    off, on = _probe("reset", "0"), _probe("reset", "1")
    assert on == off and on["pick"] is None, (off, on)
    print(f"  after a RESET, ELICIT over RESET alone is refused: OFF {off['pick']}, ON "
          f"{on['pick']} (alike)")


def check_hold_collapse() -> None:
    on = _probe("collapse", "1")
    assert on["pick"] == "ACTION1", on
    print("  ON: ACTION2 changed every press here, ACTION1's effect here is unknown: ACTION1 is "
          "realised (the tier decides; the tally only orders inside it)")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_CHANGE_TALLY")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    print(f"  OFF (TETHER_CHANGE_TALLY=0, fake): {len(base)} rows against {BASE}, 0 differences")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"change_tally: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
