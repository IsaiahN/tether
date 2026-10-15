"""(b'-g) D3, THE HELD INDEX CARRIED BESIDE THE GENERATION: R-d3 as registered (the reviewer
2026-10-14 21:59). Real gridworld Agents through lineage.load / lineage.write; both arms
(TETHER_LINEAGE_CARRY, TETHER_INDEX_HOLD) set in each child's environment at start; every role is
its own process, so the held store starts empty in each.

  R-d3 (i)   same signature: B, given A's chain, compiles exactly the (entry, role) pairs it lit
             that A's index did not carry -- "R-d3 rebuilt from scratch".
  R-d3 (ii)  signature grown by ADDITIONS ONLY (A2 wrote under a signature without one template
             atom; C has it): C compiles exactly its new pairs plus the carried pairs holding a
             Refusal -- "R-d3 additions rebuilt".
  R-d3 (iii) every carried or re-keyed compile equals the compile made fresh -- "R-d3 carried
             differs".
  Cheap check: a signature that LOST an atom (D) installs nothing and writes an index_rebuild row.
  CONVERSE pair (A3, E): an added CONVERSE atom re-keys nothing (compile_term 236); SKIPPED and
  printed where the world's signature holds no "below". First-ask timings print as description.

A2 and D narrow compile_term.signature in their own process (the fixture's device: the compiles
themselves are made with every atom; only the key changes).

    python test_index_carry.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

N = 20


CONV = {n for row in compile_term.CONVERSE.values() for n in row[0]}


def _narrow(drop=None):
    """compile_term.signature without one template atom: `drop` by name, or else the first one
    NOT in CONVERSE (so (ii) re-keys; an added CONVERSE atom re-keys nothing, compile_term 236).
    Returns the dropped name, or None when the signature does not hold `drop`."""
    real = compile_term.signature
    g = gamma.Gamma(world.bind(gridworld.family("default", 0)).atoms())
    present = sorted(t[0] for t in real({a.name: a for a in g.atoms})[1])
    gone = drop if drop is not None else next(n for n in present if n not in CONV)
    if gone not in present:
        return None

    def narrowed(atoms):
        arm, tup = real(atoms)
        return arm, tuple(t for t in tup if t[0] != gone)
    compile_term.signature = narrowed
    return gone


_REQ: set = set()   # the (entry, role) pairs this process actually asked the held index for
_T: dict = {}       # (entry, role) -> seconds its FIRST ask took in this process


def _run(d, seed, n):
    real = tether.Agent._held_index

    def spy(self, lib, key, role, atoms, sig):
        first = (key, role) not in _REQ
        _REQ.add((key, role))
        t0 = time.perf_counter()
        out = real(self, lib, key, role, atoms, sig)
        if first:   # the first ask: a compile, or a resolution (description, not a refuter)
            _T[(key, role)] = time.perf_counter() - t0
        return out
    tether.Agent._held_index = spy
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    rep = lineage.load(d, ag)
    for _ in range(n):
        ag.step()
    ag.end_run("cap")
    return ag, rep


def _lit(ag):
    """The signature, and the pairs this process LIT (asked for), never the store's whole keys."""
    return compile_term.signature({a.name: a for a in ag.gamma.atoms}), set(_REQ)


def _carried(d, refusals):
    """(entry, role) pairs in d's index files; refusals=False drops entries holding a Refusal."""
    out = set()
    for f in Path(d).glob(f"{lineage.IDX}*.json"):
        for e in json.loads(f.read_bytes())["entries"]:
            if refusals or not any(z and "refusal" in z for x in e["items"]
                                   for z in (x["c"], x["t"])):
                out.add((e["key"], e["role"]))
    return out


def _fresh(ag, sig, pairs, label):
    """(iii): each pair's held compile equals the compile made fresh, as _held_index makes it."""
    lib, atoms = tether._library(), {a.name: a for a in ag.gamma.atoms}

    def comp(cond):
        return compile_term.compile_candidate({"condition": cond}, atoms)
    for key, role in pairs:
        fresh = [(c, comp(c["if"]), comp(c["then"])) if role == "CAUSE"
                 else (c, None if "quantifier" in c else comp(c["condition"]), None)
                 for c in lib.view(key, role, tether.PH_O, tether.PH_X)]
        assert tether._INDEX_STORE[(sig, key, role)] == fresh, ("R-d3 carried differs", label, key,
                                                                role)


def role_a(d, narrow):
    if narrow == "below":
        if _narrow("below") is None:
            print("  CONVERSE check: SKIPPED, the gridworld signature holds no \"below\"",
                  flush=True)
            return
    elif narrow:
        _narrow()
    ag, _ = _run(d, 0, N)
    w = lineage.write(d, ag, "default")
    assert w["index"] and w["index"].get("entries"), ("fixture: A wrote no index entries", w)
    idx = next(Path(d).glob(f"{lineage.IDX}{w['hash']}_*.json"))
    print(f"  A: first asks {len(_T)} took {sum(_T.values()):.2f} s (compiles); index "
          f"{idx.stat().st_size} B", flush=True)
    print(f"  A{'2' if narrow else ''}: {w['written']} with index {w['index']}", flush=True)


def role_b(d):
    carried = _carried(d, True)
    ag, rep = _run(d, 0, 2 * N)
    sig, lit = _lit(ag)
    assert lit & carried, ("fixture: B lit nothing A carried", len(lit), len(carried))
    held = tether._INDEX_N["held"]
    assert held == len(lit - carried), ("R-d3 rebuilt from scratch", held, len(lit - carried),
                                        len(lit), len(carried))
    assert not lineage._RESOLVE["unresolved"], ("fixture: unresolved references", lineage._RESOLVE)
    _fresh(ag, sig, lit & carried, "(i)")
    print(f"  B: first asks of carried pairs took {sum(_T[k] for k in lit & carried):.2f} s "
          f"(resolutions); {lineage._RESOLVE}", flush=True)
    print(f"  R-d3 (i): B lit {len(lit)} pairs, {len(lit & carried)} carried; compiled {held} "
          f"= {len(lit - carried)} new; index {rep['index']}", flush=True)


def role_c(d):
    ok, every = _carried(d, False), _carried(d, True)
    ag, rep = _run(d, 0, 2 * N)
    sig, lit = _lit(ag)
    idx = rep["index"]
    assert lit & ok, ("fixture: C lit nothing A2 carried", len(lit), len(ok))
    held = tether._INDEX_N["held"]
    assert idx["rekeyed"] and not idx["rebuild"] and held == len(lit - ok), (
        "R-d3 additions rebuilt", held, len(lit - ok), idx)
    assert not lineage._RESOLVE["unresolved"], ("fixture: unresolved references", lineage._RESOLVE)
    _fresh(ag, sig, lit & ok, "(ii)")
    print(f"  R-d3 (ii): re-keyed {idx['rekeyed']}, Refusals recompiled {idx['refusals_recompile']}"
          f" of {len(every)} carried; C lit {len(lit)}, compiled {held} = {len(lit - ok)}",
          flush=True)


def role_d(d):
    _narrow()
    ag, rep = _run(d, 0, 0)
    idx = rep["index"]
    rows = [e for e in ag.led.entries if e.event == "index_rebuild"]
    assert idx["rebuild"] and not idx["installed"] and not idx["rekeyed"] and rows, (
        "a lost atom installed something", idx)
    print(f"  removal: {idx['rebuild'][0]['reason']}; installed 0, re-keyed 0", flush=True)


def role_e(d):
    if not any(Path(d).glob(f"{lineage.IDX}*.json")):
        return   # the a3 role said why it skipped
    ag, rep = _run(d, 0, 0)
    idx = rep["index"]
    rows = [e for e in ag.led.entries if e.event == "index_rebuild"]
    assert len(rows) == 1 and "236" in rows[0].detail["reason"] and not idx["rekeyed"], (
        "an added CONVERSE atom re-keyed", idx, [r.detail for r in rows])
    print(f"  CONVERSE check: {rows[0].detail['reason']}; re-keyed 0", flush=True)


def _child(role, d):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_LINEAGE_CARRY="1", TETHER_INDEX_HOLD="1")
    r = subprocess.run([sys.executable, "-B", __file__, "--role", role, str(d)], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"{role} failed:\n{r.stderr[-3000:]}"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="index_"))
    _child("a", tmp / "same")
    _child("b", tmp / "same")
    _child("a2", tmp / "grown")
    _child("c", tmp / "grown")
    _child("d", tmp / "same")
    _child("a3", tmp / "conv")
    _child("e", tmp / "conv")
    print("index carry: OK")


if __name__ == "__main__":
    if "--role" in sys.argv:
        role, d = sys.argv[sys.argv.index("--role") + 1], sys.argv[sys.argv.index("--role") + 2]
        assert lineage.CARRY and tether._INDEX_HOLD, "the child must be started with both arms"
        {"a": lambda: role_a(d, False), "a2": lambda: role_a(d, True),
         "a3": lambda: role_a(d, "below"), "b": lambda: role_b(d), "c": lambda: role_c(d),
         "d": lambda: role_d(d), "e": lambda: role_e(d)}[role]()
    else:
        main()
