"""THE LOG INDEX, L4 (harness/log_index.py; the reviewer 2026-10-21 23:27, 2026-10-22 00:03), on
temp copies of three small committed-shape ledgers: one with a @run header and a result.json, one
old with no header, one with a torn last line. Nothing outside the temp folder is written; the
real C:/TETHER_RUNS is only read (by the pins scan).

  ADD  three ledgers indexed, one row each; verify OK on all three.
  MF1  a byte flipped in a ledger -> verify refuses (sha256).
  MF2  an index row with one tally count changed -> verify refuses (tally).
  SUM  the same row with only its summariser stamp changed verifies (the stamp moves with any edit
       to log_index.py; at be741fd all 1,030 (B) rows failed on it alone).
  MF8  that earlier-stamped row with a changed tally still FAILS (the reviewer 2026-10-22 04:25):
       a must-fail crosses the version boundary it guards.
  MF3  a pinned ledger and a window ledger are never eligible; the third is.
  MF4  a torn last line is counted as bad, and the row still writes.
  MF5  retire refuses a list holding a ledger that fails verify, and renames nothing; the eligible
       one alone retires to .dead-<UTC> with a LOG_REMOVALS line.
  MF6  the pins generated from docs/LEDGER.md pass --check; a planted LEDGER citation of a box
       with no folder and no pin makes --check FAIL.
  MF7  the same for a planted worktree citation (wt_..., the reviewer 2026-10-22 00:30 (c)).
  The planted tokens are built at run time, so no source the pins read can ever cite them.

    python tests/test_log_index.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = Path(_repo.ROOT)
spec = importlib.util.spec_from_file_location("log_index", HERE / "harness" / "log_index.py")
li = importlib.util.module_from_spec(spec)
spec.loader.exec_module(li)

ROW = {"mode": "specified", "seq": 0, "cycle": 0, "step": "PLAN", "slot": "@run",
       "event": "arms", "detail": {"head": "abc", "on": ["t._A"], "off": ["t._B"], "game": "fake"}}


def ledger(p: Path, header: bool, n: int = 40, torn: bool = False) -> Path:
    rows = [ROW] if header else []
    rows += [{"mode": "specified", "seq": i + 1, "cycle": i // 4, "step": "PERCEIVE",
              "slot": f"o{i % 3}.col", "event": "bet", "detail": {"v": i}} for i in range(n)]
    rows.append({"mode": "specified", "seq": n + 1, "cycle": n // 4, "step": "IMPORT",
                 "slot": "@boundary", "event": "ending", "detail": {"how": "death"}})
    text = "".join(json.dumps(r) + "\n" for r in rows)
    if torn:
        text += '{"mode": "specified", "seq": 99, "cyc'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def run(*argv: str) -> int:
    return li.main(list(argv))


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="log_index_"))
    try:
        idx, pins, rem = tmp / "LOG_INDEX.jsonl", tmp / "LOG_PINS.tsv", tmp / "LOG_REMOVALS.tsv"
        common = ["--index", str(idx), "--pins", str(pins), "--removals", str(rem)]
        root = tmp / "runs"
        a = ledger(root / "box_a" / "fake.jsonl", header=True)
        (root / "box_a" / "fake.result.json").write_text('{"won": false, "actions": 9}')
        b = ledger(root / "box_b" / "old.jsonl", header=False)
        c = ledger(root / "box_c" / "torn.jsonl", header=True, torn=True)
        for i, p in enumerate((a, b, c)):
            os.utime(p, (1_700_000_000 + i, 1_700_000_000 + i))   # c newest, a oldest
        assert run(*common, "add", str(root)) == 0
        rows = [json.loads(x) for x in idx.read_text(encoding="utf-8").splitlines()]
        assert len(rows) == 3, len(rows)
        ra = next(r for r in rows if r["path"].endswith("fake.jsonl"))
        assert ra["header"]["arms_sha"] and ra["result"] == {"won": False, "actions": 9}
        assert ra["tally"]["PERCEIVE|bet"] == [40, 0, 9] and ra["kept_rows"][0]["event"] == "ending"
        assert run(*common, "verify", str(a), str(b), str(c)) == 0
        print(f"  ADD: 3 rows ({', '.join(str(len(json.dumps(r))) + ' B' for r in rows)}); "
              "verify OK on all three; tally PERCEIVE|bet [40, first 0, last 9]")

        rc = next(r for r in rows if r["path"].endswith("torn.jsonl"))
        assert rc["bad"] == 1 and rc["rows"] == 43, (rc["bad"], rc["rows"])
        print("  MF4: the torn last line is counted (bad 1 of 43 rows) and the row still writes")

        f = tmp / "flip" / "fake.jsonl"
        f.parent.mkdir()
        shutil.copyfile(a, f)
        assert run(*common, "add", str(f.parent)) == 0
        data = bytearray(f.read_bytes())
        data[data.index(b'"v": 7')+5] = ord("8")
        f.write_bytes(bytes(data))
        d = li.verify_one(li.load_index(idx), f)
        assert "sha256" in d, d
        print(f"  MF1: one byte flipped -> verify refuses ({', '.join(d)})")

        lines = idx.read_text(encoding="utf-8").splitlines()
        k = next(i for i, x in enumerate(lines) if json.loads(x)["path"].endswith("old.jsonl"))
        r = json.loads(lines[k])
        r["tally"]["PERCEIVE|bet"][0] += 1
        lines[k] = json.dumps(r, sort_keys=True)
        bad_idx = tmp / "BAD_INDEX.jsonl"
        bad_idx.write_text("\n".join(lines) + "\n", encoding="utf-8")
        d = li.verify_one(li.load_index(bad_idx), b)
        assert d == ["tally"], d
        print("  MF2: one tally count changed in the index -> verify refuses (tally)")

        lines = idx.read_text(encoding="utf-8").splitlines()
        r = json.loads(lines[k])
        r["summariser"] = "0" * 16
        lines[k] = json.dumps(r, sort_keys=True)
        old_idx = tmp / "OLD_SUMMARISER.jsonl"
        old_idx.write_text("\n".join(lines) + "\n", encoding="utf-8")
        d = li.verify_one(li.load_index(old_idx), b)
        assert d == [], d
        print("  SUM: a row stamped by an earlier summariser verifies on its content (the stamp is "
              "provenance)")
        r["tally"]["PERCEIVE|bet"][0] += 1
        lines[k] = json.dumps(r, sort_keys=True)
        old_idx.write_text("\n".join(lines) + "\n", encoding="utf-8")
        d = li.verify_one(li.load_index(old_idx), b)
        assert d == ["tally"], d
        print("  MF8: the same earlier-stamped row with its content changed (tally) still FAILS: "
              "the skip is the stamp only")

        pins.write_text(f"{li.norm(root / 'box_b')}\thand pin for the test\n", encoding="utf-8")
        real_w = li.WINDOW
        li.WINDOW = 1
        try:
            ok, held = li.eligible(li.load_index(idx), [a, b, c], li.read_pins(pins), True)
        finally:
            li.WINDOW = real_w
        assert [p for p, _ in ok] == [a], ok
        why = {p.name: w for p, w in held}
        assert why == {"old.jsonl": "hand pin for the test", "torn.jsonl": "window"}, why
        print(f"  MF3: pinned and window ledgers held ({why}); only {a.name} eligible")

        li.WINDOW = 1
        try:
            lst = tmp / "retire.txt"
            lst.write_text(f"{a}\n{f}\n", encoding="utf-8")
            roots = ["--roots", str(root), str(f.parent)]
            assert run(*common, "retire", str(lst), "--approval", "test", *roots) == 1
            assert a.is_file() and f.is_file() and not rem.exists()
            lst.write_text(f"{a}\n", encoding="utf-8")
            assert run(*common, "retire", str(lst), "--approval", "test", *roots) == 0
        finally:
            li.WINDOW = real_w
        dead = list(a.parent.glob("fake.jsonl.dead-*"))
        line = rem.read_text(encoding="utf-8").splitlines()
        assert not a.exists() and len(dead) == 1 and len(line) == 1 and ra["sha256"] in line[0]
        print("  MF5: a list holding a ledger that fails verify retires nothing; the eligible one "
              f"alone -> {dead[0].name}, one LOG_REMOVALS line")

        real_pins = tmp / "REAL_PINS.tsv"
        shutil.copyfile(HERE / "docs" / "log_index" / "LOG_PINS.tsv", real_pins)   # hand rows
        assert run("--pins", str(real_pins), "pins", str(HERE / "docs" / "LEDGER.md")) == 0
        assert run("--pins", str(real_pins), "pins", str(HERE / "docs" / "LEDGER.md"),
                   "--check") == 0
        n = len(li.read_pins(real_pins))
        planted = tmp / "LEDGER_planted.md"
        for mf, tok in (("MF6", "S9" + "ZQ"), ("MF7", "wt_" + "zz9")):
            planted.write_text((HERE / "docs" / "LEDGER.md").read_text(encoding="utf-8")
                               + f"\n- planted: the {tok} box measured nothing.\n",
                               encoding="utf-8")
            assert run("--pins", str(real_pins), "pins", str(planted), "--check") == 1, mf
            print(f"  {mf}: {n} pins from docs/LEDGER.md pass --check; a planted {tok} "
                  "citation with no folder or pin FAILS it")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("test_log_index: pass")


if __name__ == "__main__":
    main()
