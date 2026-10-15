"""C-hold-4, THE BOUND MEMO OUTLIVES THE GAME (the reviewer 2026-10-15 06:10, 06:13, 06:56, 07:00;
Isaiah 06:01, 06:13). WRITTEN, NOT RUN: it runs in the end-of-step-7 checklist (Isaiah 05:25).
Every role is its own process, its arms set in the environment at start (TETHER_ATOMS_ONCE,
TETHER_INDEX_HOLD, and for W/R TETHER_LINEAGE_CARRY).

  T1   the content token is equal in two processes; equal when the source reads CRLF or LF; a
       source change moves it; a function with no source is refused (None, counted) and
       primitives_once hands the atoms back unchanged.
  B    (b) no shared list: two Gammas built from the cached primitives hold the SAME atom objects
       in DIFFERENT lists, and the cached tuple is unchanged after both played.
  X1   a second game (another seed, a new Agent) is served game 1's bound answer: 0 binds, equal
       to the named compile, holding the second Gamma's atoms.
  X2   a Gamma over atoms that are NOT the shared objects has no token, and is bound afresh onto
       its own atoms.
  MF-X MUST-FAIL: the same Gamma handed the shared token is served objects that are not its own,
       and X2's check fires.
  X3   W plays and writes a generation with its memo file; R, a new process, loads it: carried
       answers are pending, resolved at first ask with 0 unresolved, each equal to the named
       compile and holding R's atoms.

    python test_bound_memo.py
"""
from __future__ import annotations

import inspect
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from test_index_hold import _form, _named, _pairs, _real  # noqa: E402

N = 10


def _agent(seed, atoms=None):
    env = world.bind(gridworld.family("default", seed))
    return env, tether.Agent(env, gamma.Gamma(env.atoms() if atoms is None else atoms,
                                              game=f"fam_default_{seed}"),
                             tether.Config(), ledger.Ledger())


def _question(env, ag):
    lib = tether._library()
    keys = list(dict.fromkeys([*lib.seed, *lib.runtime, *lib.learnings]))
    o, x = _pairs(env)[0]
    k = next(k for k in keys if lib.view(k, "STATE", o, x))
    atoms = {a.name: a for a in ag.gamma.atoms}
    import compile_term
    return lib, k, o, x, atoms, compile_term.signature(atoms)


def _spy_bound(nb):
    real = tether._bound
    tether._bound = lambda *a: nb.append(1) or real(*a)
    return real


def _own(got, atoms):
    return all(a is atoms[a.name] for _c, *cs in got for c in cs
               if c is not None and hasattr(c, "term") for a in c.term.atoms)


def role_token():
    atoms = world.bind(gridworld.family("default", 0)).atoms()
    print(f"TOKEN {gamma.atoms_token(atoms)}", flush=True)


def role_x():
    assert gamma._ATOMS_ONCE and tether._INDEX_HOLD, "role x needs both arms ON at start"
    real_src = inspect.getsource
    atoms = world.bind(gridworld.family("default", 0)).atoms()
    tok = gamma.atoms_token(atoms)
    try:
        gamma.inspect.getsource = lambda f: real_src(f).replace("\n", "\r\n")
        assert gamma.atoms_token(atoms) == tok, "T1: CRLF moved the token"
        first = atoms[0].fn
        gamma.inspect.getsource = lambda f: real_src(f) + ("\nX = 2\n" if f is first else "")
        assert gamma.atoms_token(atoms) != tok, "T1: a source change left the token"

        def nosrc(_f):
            raise OSError("no source")
        gamma.inspect.getsource = nosrc
        n = gamma._PRIMITIVES_REFUSED["no_source"]
        fresh = gridworld._toy.Transitions().atoms()
        assert gamma.atoms_token(fresh) is None and gamma._PRIMITIVES_REFUSED["no_source"] > n
        assert gamma.primitives_once(fresh) is fresh, "T1: a refused set was not handed back"
    finally:
        gamma.inspect.getsource = real_src
    print("  T1 CRLF/LF equal; a source change moves the token; no source refused, counted")

    env1, ag1 = _agent(0)
    env2, ag2 = _agent(1)
    held = gamma._PRIMITIVES[ag1._atoms_token]
    assert ag1._atoms_token and ag1._atoms_token == ag2._atoms_token, "X1: no shared token"
    assert ag1.gamma.atoms is not ag2.gamma.atoms and all(
        a is b for a, b in zip(ag1.gamma.atoms, ag2.gamma.atoms, strict=True)), "B: lists"
    nb: list = []
    real = _spy_bound(nb)
    try:
        lib, k, o, x, atoms1, sig = _question(env1, ag1)
        _real(ag1, lib, k, o, x, atoms1, sig)
        assert nb, "X1: game 1 bound nothing"
        before = len(nb)
        _l, _k, _o, _x, atoms2, sig2 = _question(env2, ag2)
        assert sig2 == sig
        got = _real(ag2, lib, k, o, x, atoms2, sig)
        assert len(nb) == before, ("X1: game 2 bound again", len(nb) - before)
        named = _named(lib, k, "STATE", o, x, atoms2)
        assert [(_form(a), _form(b)) for _c, a, b in got] == \
            [(_form(a), _form(b)) for _c, a, b in named], "X1: served answer differs"
        assert _own(got, atoms2), "X1: not game 2's atoms"
        print(f"  X1 a second game served game 1's answer: 0 binds ({before} in game 1)")

        env3, ag3 = _agent(0, gridworld._toy.Transitions().atoms())
        assert ag3._atoms_token is None, "X2: a non-shared Gamma got the token"
        _l, _k, _o, _x, atoms3, _s = _question(env3, ag3)
        before = len(nb)
        got = _real(ag3, lib, k, o, x, atoms3, sig)
        assert len(nb) > before and _own(got, atoms3), "X2: served across objects"
        print(f"  X2 other atom objects: no token, bound afresh ({len(nb) - before} binds)")

        ag3._atoms_token = ag1._atoms_token     # MF-X: the key no longer separates the objects
        got = _real(ag3, lib, k, o, x, atoms3, sig)
        assert not _own(got, atoms3), "MF-X MUST-FAIL did not fail: X2's check is blind"
        print("  MF-X must-fail fired: given the shared token, ag3 was served others' atoms")
    finally:
        tether._bound = real
    for _ in range(N):
        ag1.step()
        ag2.step()
    assert gamma._PRIMITIVES[ag1._atoms_token] is held and len(held) == len(ag1.gamma.atoms), "B"
    print("  B the cached tuple is unchanged after two Agents played; each Gamma its own list")


def role_w(d):
    env, ag = _agent(0)
    lineage.load(d, ag)
    for _ in range(N):
        ag.step()
    ag.end_run("cap")
    w = lineage.write(d, ag, "default")
    assert w["memo"] and w["memo"].get("entries"), ("X3: W wrote no memo entries", w)
    print(f"  X3 W: memo {w['memo']}", flush=True)


def role_r(d):
    """X3: EVERY pending key asked directly through Agent._compiled, the path _index_reach calls
    (its o and x are id strings and resolve reads the library's held view, never the board), so
    nothing rests on R's play overlapping W's (the reviewer 2026-10-15 07:18)."""
    env, ag = _agent(1)
    rep = lineage.load(d, ag)
    assert rep["memo"] and rep["memo"]["pending"], ("X3: nothing carried", rep)
    pending = list(lineage._MEMO_PENDING)
    lib = tether._library()
    atoms = {a.name: a for a in ag.gamma.atoms}

    def named(_cond):
        raise AssertionError("X3: the held path made a named compile")
    for sig, key, role, o, x in pending:
        got = ag._compiled(lib, key, role, o, x, named, atoms, sig)
        want = _named(lib, key, role, o, x, atoms)
        assert [(_form(a), _form(b)) for _c, a, b in got] == \
            [(_form(a), _form(b)) for _c, a, b in want], ("X3 differs", key, role, o, x)
        assert _own(got, atoms), ("X3: not R's atoms", key, role)
    res = dict(lineage._MEMO_RESOLVE)
    assert res == {"resolved": len(pending), "unresolved": 0}, ("X3", res, len(pending))
    for _ in range(N):      # play after the check; nothing above rests on it
        ag.step()
    print(f"  X3 R: {rep['memo']}; {res}; all {len(pending)} carried keys asked, each equal to "
          "the named compile")


def _child(role, d=None, carry=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_ATOMS_ONCE="1", TETHER_INDEX_HOLD="1")
    if carry:
        env["TETHER_LINEAGE_CARRY"] = "1"
    r = subprocess.run([sys.executable, "-B", __file__, "--role", role, str(d)], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"{role} failed:\n{r.stderr[-3000:]}"
    return r.stdout


def main():
    toks = [line for _ in range(2) for line in _child("token").splitlines()
            if line.startswith("TOKEN ")]
    assert len(toks) == 2 and toks[0] == toks[1] and "None" not in toks[0], ("T1", toks)
    print("  T1 the token is equal in two processes")
    _child("x")
    d = Path(tempfile.mkdtemp(prefix="memo_"))
    _child("w", d, carry=True)
    _child("r", d, carry=True)
    print("bound memo: OK")


if __name__ == "__main__":
    if "--role" in sys.argv:
        i = sys.argv.index("--role")
        role, d = sys.argv[i + 1], sys.argv[i + 2]
        {"token": lambda _d: role_token(), "x": lambda _d: role_x(), "w": role_w,
         "r": role_r}[role](d)
    else:
        main()
