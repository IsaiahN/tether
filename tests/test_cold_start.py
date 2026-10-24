"""THE COLD START (Isaiah 2026-10-21 19:26: a fresh clone with no lineage runs, creates its
lineage and fills it by itself; the reviewer 19:47 (i), 22:59). The fake ARC game
(test_entry.FakeWrapper), in temp folders; the agent's own lineage is never read.

  CS1  a lineage path that does not exist (three levels deep) is created at load, the game
       plays, and a generation is written.
  MF1  MUST-FAIL: with lineage._ensure_dir made a no-op (the old code), the same play raises
       sqlite3.OperationalError at the store's open.
  CS2  an EXISTING lineage loads identically with and without the fix: two fresh processes,
       each a wire() on the folder CS1 wrote, report the same load and hold the same library.
  CS3  a game arc_agi cannot make (make() returns None) gives the one plain message: the game
       named, the games not shipped with the code, the ONE fetch (a NORMAL-mode make()), and
       offline after it; nothing plays (wire() is never reached: its lineage folder is not made).
  LR1  MUST-FAIL (ii): a temp library copy with one required file removed (Library.load's
       index.json; the frame's frame.json, step 3) fails at wire(), naming the file, before the
       wrapper is touched (no lineage folder made).
  LR2  MUST-FAIL (ii): in a copy of the code with no library/, wire() fails naming the folder.
  LR3  the same copy with TETHER_LIBRARY_REQUIRED=0 (the ablation) plays, and its @run header
       records the arm OFF and library "absent (ablation)".
  MF3  MUST-FAIL: the same ablation with compile_term.readings's old reader (no absence rule)
       raises FileNotFoundError on library/readings.json at the first lookup.
  LR4  with the library present nothing changes: CS1/CS2 as above, header library "present".

Run from a venv OUTSIDE the scratchpad: the children drop every sys.path entry containing
"scratchpad" (so a tree there cannot shadow this one), which also drops a scratchpad venv's
site-packages, and CS2 then fails on its imports -- the filter, not the clone (the reviewer
2026-10-21 23:45).

    python tests/test_cold_start.py
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path = [sys.argv[1]] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
os.chdir(sys.argv[1])
import arc_holdout, lineage
from test_entry import FakeWrapper
if sys.argv[3] == "noop":
    lineage._ensure_dir = lambda d: None
out = arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=sys.argv[2])
ag, loaded = out[1], out[5]
hdr = next(e.detail for e in out[2].by_event("arms") if e.slot == "@run")
print(json.dumps({"lineage": loaded["lineage"], "library": sorted(ag.gamma.library),
                  "state": hdr["library"]}, sort_keys=True, default=str))
'''

ABLATE = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path = [sys.argv[1]] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
os.chdir(sys.argv[1])
import arc_holdout, tether
from test_entry import FakeWrapper
assert os.path.dirname(os.path.abspath(tether.__file__)) == os.path.abspath(sys.argv[1])
if sys.argv[3] == "old":
    import compile_term
    from pathlib import Path
    compile_term.readings = lambda: json.loads((Path(compile_term.__file__).parent / "library"
                                                / "readings.json").read_text())["readings"]
assert not os.path.exists(os.path.join(sys.argv[1], "library"))
class Arc:
    def make(self, _game):
        return FakeWrapper()
led = os.path.join(sys.argv[2], "run.jsonl")
try:
    r = arc_holdout.play("fake", 3, arc=Arc(), lineage_dir=os.path.join(sys.argv[2], "lin"),
                         led_path=led)
except FileNotFoundError as e:
    print(json.dumps({"raised": str(e)}))
else:
    rows = [json.loads(x) for x in open(led, encoding="utf-8")]
    h = next(x["detail"] for x in rows if x.get("slot") == "@run" and x.get("event") == "arms")
    print(json.dumps({"state": h["library"], "off": "tether._LIBRARY_REQUIRED" in h["off"],
                      "rows": len(rows), "error": r.get("error")}))
'''


class Arc:
    def make(self, _game):
        return FakeWrapper()


class NoGame:
    def make(self, _game):
        return None


def child(d: Path, mode: str, code: str = CHILD, home: str = HERE, **arms: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    out = subprocess.run([sys.executable, "-B", "-c", code, home, str(d), mode], env=env,
                         capture_output=True, text=True, timeout=600, cwd=HERE)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="cold_start_"))
    try:
        d = tmp / "a" / "b" / "lineage"
        assert not d.exists()
        r = arc_holdout.play("fake", 3, arc=Arc(), lineage_dir=str(d))["persistence"]
        gens = sorted(p.name for p in d.glob("gen_*.json"))
        assert d.is_dir() and r["lineage"]["written"] and gens, ("CS1", r["lineage"], gens)
        print(f"  CS1: {d.relative_to(tmp)} did not exist; created at load; played; wrote "
              f"{r['lineage']['hash']} ({len(gens)} generation file)")
        real = lineage._ensure_dir
        lineage._ensure_dir = lambda _d: None
        try:
            m = tmp / "x" / "y" / "lineage"
            try:
                arc_holdout.play("fake", 3, arc=Arc(), lineage_dir=str(m))
            except sqlite3.OperationalError as e:
                print(f"  MF1: without the fix, a missing folder raises "
                      f"sqlite3.OperationalError ({e})")
            else:
                raise AssertionError("MF1 did not fail: the old code played on a missing folder")
        finally:
            lineage._ensure_dir = real
        a, b = child(d, "fixed"), child(d, "noop")
        assert a == b and a["state"] == "present", ("CS2", {k: (a[k] == b[k]) for k in a})
        print(f"  CS2: an existing lineage loads identically with and without the fix "
              f"(parent {a['lineage'].get('parent')}, {len(a['library'])} library entries)")
        g = tmp / "g" / "lineage"
        out = arc_holdout.play("zz99", 3, arc=NoGame(), lineage_dir=str(g))
        msg = out.get("error") or ""
        need = ("zz99", "environment_files/", "not shipped", "OperationMode.NORMAL",
                "make('zz99')", "offline")
        assert all(n in msg for n in need) and set(out) == {"error"}, ("CS3", out)
        assert not g.exists(), ("CS3: a missing game reached wire()", g)
        print(f"  CS3: a missing game gives the plain message and plays nothing: {msg[:72]}...")
        home = tmp / "home"
        shutil.copytree(Path(HERE) / "library", home / "library")
        real_home = tether.LIBRARY_HOME
        tether.LIBRARY_HOME = str(home)
        try:
            for f in ("index.json", "frame.json"):
                (home / "library" / f).rename(home / "library" / (f + ".gone"))
                lr = tmp / f"lr1_{f}" / "lineage"
                try:
                    arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=str(lr))
                except FileNotFoundError as e:
                    assert f"library/{f}" in str(e) and not lr.exists(), ("LR1", f, str(e))
                    print(f"  LR1: library/{f} removed -> wire() fails before any step: "
                          f"{str(e)[len(str(home)):][:70]}...")
                else:
                    raise AssertionError(f"LR1 did not fail: library/{f} missing, wire() ran")
                (home / "library" / (f + ".gone")).rename(home / "library" / f)
            assert tether.library_check() == "present", "LR1: the restored copy reads present"
        finally:
            tether.LIBRARY_HOME = real_home
        code = tmp / "code"
        code.mkdir()
        for p in Path(HERE).glob("*.py"):
            shutil.copyfile(p, code / p.name)
        (tmp / "lr2").mkdir()
        (tmp / "lr3").mkdir()
        r2 = child(tmp / "lr2", "-", ABLATE, str(code))
        assert "library is absent" in r2.get("raised", "") or "absent:" in r2.get("raised", ""), r2
        assert not (tmp / "lr2" / "lin").exists(), "LR2: the absent library reached wire()'s body"
        print(f"  LR2: no library/ -> wire() fails naming the folder: "
              f"{r2['raised'][len(str(code)):][:70]}...")
        r3 = child(tmp / "lr3", "-", ABLATE, str(code), TETHER_LIBRARY_REQUIRED="0")
        assert r3.get("state") == "absent (ablation)" and r3["off"] and not r3["error"], r3
        print(f"  LR3: TETHER_LIBRARY_REQUIRED=0 (the ablation) plays with no library/: header "
              f"library {r3['state']!r}, arm OFF, {r3['rows']} rows")
        (tmp / "mf3").mkdir()
        m3 = child(tmp / "mf3", "old", ABLATE, str(code), TETHER_LIBRARY_REQUIRED="0")
        assert "readings.json" in m3.get("raised", ""), ("MF3 did not fail", m3)
        print("  MF3: with the old reader the ablation raises FileNotFoundError on "
              "library/readings.json")
        print(f"  LR4: with the library present, CS1/CS2 unchanged; header library {a['state']!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("test_cold_start: pass")


if __name__ == "__main__":
    main()
