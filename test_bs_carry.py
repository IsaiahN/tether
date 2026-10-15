"""C-S1b-1, THE SLOT ANSWERS CARRIED (the reviewer 2026-10-15 11:05, 11:22). WRITTEN, NOT RUN: it
runs in the end-of-step-7 checklist. Every role is its own process, its arms set in the
environment at start (TETHER_ATOMS_ONCE, TETHER_INDEX_HOLD, TETHER_SLOT_FILTER,
TETHER_LINEAGE_CARRY). The bs_ mirror of test_bound_memo's X3 and test_lineage_boundary's L4.

  W    a cold instance plays under ON (precondition: bound_slot > 0) and writes bs_ entries. W
       plays with PROMOTION held off (a seen set that never holds): since S1d (the reviewer
       2026-10-15 12:42) a promoted pair is carried as its whole by bm_, never by bs_, so this
       fixture, which tests the bs_ family itself, needs first-slot answers to carry.
  R    a new process loads them: every pending slot key asked through Agent._compiled is read
       from the carry before binding (bound_slot_from_carry == pending > 0), 0 unresolved, each
       equal to the slot-filtered named compile.
  MF-T MUST-FAIL: a truncated bs_ file is counted unreadable, nothing is pending, and the asked
       key is bound fresh (from_carry 0), equal to the named compile.
  MF-S MUST-FAIL: a bs_ entry whose rows are not the held view's rows for that slot (one item
       dropped, the file renamed to its own hash so it loads) is unresolved, never used, and
       the answer is bound fresh.

    python test_bs_carry.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import lineage  # noqa: E402
import tether  # noqa: E402
from test_bound_memo import _agent, _own  # noqa: E402
from test_index_hold import _form, _named  # noqa: E402

N = 10


def _want(lib, key, role, o, x, slot, atoms):
    return [(_form(a), _form(b)) for _c, a, b in _named(lib, key, role, o, x, atoms)
            if tether._lands(role, a, b, slot, tether._same)]


def _ask(ag, k):
    sig, key, role, o, x, slot = k
    lib = tether._library()
    atoms = {a.name: a for a in ag.gamma.atoms}

    def named(_cond):
        raise AssertionError("the held path made a named compile")
    got = ag._compiled(lib, key, role, o, x, named, atoms, sig, slot=slot)
    assert [(_form(a), _form(b)) for _c, a, b in got] == _want(lib, key, role, o, x, slot,
                                                                atoms), ("differs", k)
    assert _own(got, atoms), ("not this instance's atoms", k)


class _NeverSeen(set):
    def add(self, _k):
        pass


def role_w(d):
    tether._PAIRS_SEEN = _NeverSeen()
    env, ag = _agent(0)
    ag._pairs_seen = _NeverSeen()
    lineage.load(d, ag)
    for _ in range(N):
        ag.step()
    assert tether._INDEX_N["bound_slot"] > 0, "precondition: W never took the filtered path"
    ag.end_run("cap")
    w = lineage.write(d, ag, "default")
    assert w["slot_memo"] and w["slot_memo"].get("entries"), ("W wrote no bs_ entries", w)
    print(f"  W: bound_slot {tether._INDEX_N['bound_slot']}; bs_ {w['slot_memo']}", flush=True)


def role_r(d):
    env, ag = _agent(1)
    rep = lineage.load(d, ag)
    assert rep["slot_memo"] and rep["slot_memo"]["pending"], ("R: nothing carried", rep)
    pending = list(lineage._BS_PENDING)
    for k in pending:
        _ask(ag, k)
    res = dict(lineage._BS_RESOLVE)
    assert res == {"resolved": len(pending), "unresolved": 0}, ("R", res, len(pending))
    assert tether._INDEX_N["bound_slot_from_carry"] == len(pending), (
        "R: a carried slot answer was not read before binding", dict(tether._INDEX_N))
    print(f"  R: {rep['slot_memo']}; {res}; all {len(pending)} carried slot keys read from the "
          "carry, each equal to the named compile")


def _one_key(d):
    """A pending key as W wrote it, read from the file itself (a truncated file loads nothing)."""
    f = sorted(Path(d).glob(f"{lineage.BSMEMO}*.json"))[0]
    e = next(e for e in json.loads(f.read_bytes())["entries"] if e["items"])
    return f, e


def role_t(d):
    f, e = _one_key(d)
    raw = f.read_bytes()
    f.write_bytes(raw[:len(raw) // 2])
    env, ag = _agent(1)
    rep = lineage.load(d, ag)
    assert rep["slot_memo"]["unreadable"] >= 1 and not lineage._BS_PENDING, ("MF-T", rep)
    import compile_term
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    _ask(ag, (sig, e["key"], e["role"], e["o"], e["x"], e["slot"]))
    assert tether._INDEX_N["bound_slot_from_carry"] == 0, "MF-T: a truncated file was used"
    print("  MF-T must-fail fired: the truncated bs_ file is unreadable and the key bound fresh")


def role_s(d):
    f, e = _one_key(d)
    body = json.loads(f.read_bytes())
    for b in body["entries"]:
        if b["key"] == e["key"] and b["role"] == e["role"] and b["o"] == e["o"] and \
                b["x"] == e["x"] and b["slot"] == e["slot"]:
            b["items"] = b["items"][:-1]
    raw = json.dumps(body, sort_keys=True, indent=1).encode("utf-8")
    gh = f.stem[len(lineage.BSMEMO):].rsplit("_", 1)[0]
    f.unlink()
    (Path(d) / f"{lineage.BSMEMO}{gh}_{hashlib.sha256(raw).hexdigest()[:16]}.json").write_bytes(raw)
    env, ag = _agent(1)
    rep = lineage.load(d, ag)
    import compile_term
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    k = (sig, e["key"], e["role"], e["o"], e["x"], e["slot"])
    assert k in lineage._BS_PENDING, ("MF-S: the altered entry did not load", rep)
    _ask(ag, k)
    assert lineage._BS_RESOLVE["unresolved"] == 1 and \
        tether._INDEX_N["bound_slot_from_carry"] == 0, ("MF-S: a wrong slot answer was used",
                                                        dict(lineage._BS_RESOLVE))
    print("  MF-S must-fail fired: rows that are not the slot's held rows are unresolved, the key "
          "bound fresh")


def _child(role, d):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_ATOMS_ONCE="1", TETHER_INDEX_HOLD="1", TETHER_SLOT_FILTER="1",
               TETHER_LINEAGE_CARRY="1")
    r = subprocess.run([sys.executable, "-B", __file__, "--role", role, str(d)], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"{role} failed:\n{r.stderr[-3000:]}"


def main():
    d = Path(tempfile.mkdtemp(prefix="bs_"))
    _child("w", d)
    copies = {}
    for role in ("t", "s"):
        copies[role] = Path(tempfile.mkdtemp(prefix=f"bs_{role}_")) / "lineage"
        shutil.copytree(d, copies[role])
    _child("r", d)
    _child("t", copies["t"])
    _child("s", copies["s"])
    print("bs carry: OK")


if __name__ == "__main__":
    if "--role" in sys.argv:
        i = sys.argv.index("--role")
        role, d = sys.argv[i + 1], sys.argv[i + 2]
        {"w": role_w, "r": role_r, "t": role_t, "s": role_s}[role](d)
    else:
        main()
