"""R2, ONE HELD LEDGER HANDLE AND rows(start), TETHER_LEDGER_HANDLE (the reviewer 2026-10-17 17:58,
18:04).

  E     the fake ARC game, 12 actions, C-seed-X, the arm ON vs OFF: the ledger FILES byte-identical,
        the @run header (which lists the arms) aside
  K     a child recording rows is killed after N: every row it had recorded is on disk, each line
        parseable (the loss window is one row, as with a file opened per row)
  MF-K  the flush removed: rows the child had recorded are missing from the file after the kill
  S     rows(k) == rows()[k:] for every k on a 50-row ledger
  MF-S  an off-by-one planted in rows(start) fails S (on the fake it changes nothing
        observable: a step's first row is rarely a bet, so S checks rows(start) directly)

    python tests/test_ledger_handle.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from conform.identity_mod_rows import mask_timings

sys.dont_write_bytecode = True
HERE = _repo.ROOT

CHILD = r'''
import os, sys, tempfile
sys.dont_write_bytecode = True
import ledger, tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "h.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''

WRITER = r'''
import os, sys, time
sys.dont_write_bytecode = True
import ledger
path, count, mode = sys.argv[1], sys.argv[2], sys.argv[3]
led = ledger.Ledger(path)
n = 0
while True:
    led.record(n, "PERCEIVE", "s", "bet", mass=1.0, pad="x" * 40)
    if mode == "noflush" and n == 0:
        class NoFlush:
            def __init__(self, fh):
                self.fh = fh
            def write(self, s):
                return self.fh.write(s)
            def flush(self):
                pass
            def close(self):
                self.fh.close()
        led._fh = NoFlush(led._fh)
    n += 1
    with open(count, "w") as fh:
        fh.write(str(n))
        fh.flush()
        os.fsync(fh.fileno())
    time.sleep(0.002)
'''


def env(extra: dict | None = None) -> dict:
    e = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    e.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    return e


def fake(mode: str = "", extra: dict | None = None) -> bytes:
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode or "-"], capture_output=True,
                       text=True, env=env(extra), cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    with open(led, "rb") as fh:
        return fh.read()


def body(raw: bytes) -> list:
    """The ledger's lines, the @run header aside (it names the arms, so it differs by design), the
    shared TIMINGS masked (the step clock's wall_s)."""
    rows = [json.loads(x) for x in raw.splitlines() if x.strip() and b'"slot": "@run"' not in x]
    return [json.dumps(r, sort_keys=True) for r in mask_timings(rows)]


def killed(mode: str, n: int) -> tuple[int, int, bool]:
    """(rows recorded before the kill, lines in the file, every line parses)."""
    d = tempfile.mkdtemp()
    path, count = os.path.join(d, "k.jsonl"), os.path.join(d, "n.txt")
    p = subprocess.Popen([sys.executable, "-B", "-c", WRITER, path, count, mode], env=env(),
                         cwd=HERE, stdin=subprocess.DEVNULL)
    t0 = time.time()
    try:
        while time.time() - t0 < 60:
            try:
                with open(count) as fh:
                    if int(fh.read() or 0) >= n:
                        break
            except (OSError, ValueError):
                pass
            time.sleep(0.01)
    finally:
        p.kill()
        p.wait()
    with open(count) as fh:
        rec = int(fh.read())
    with open(path, encoding="utf-8") as fh:
        lines = [x for x in fh.read().splitlines() if x.strip()]
    ok = True
    for x in lines:
        try:
            json.loads(x)
        except ValueError:
            ok = False
    return rec, len(lines), ok


def main() -> int:
    on, off = body(fake()), body(fake(extra={"TETHER_LEDGER_HANDLE": "0"}))
    assert on == off, (len(on), len(off))                                                 # E
    print("E ledger files byte-identical, handle ON vs OFF (the @run header, which lists the "
          "arms, aside):", len(on), "lines")
    rec, lines, ok = killed("flush", 200)
    assert ok and lines >= rec, (rec, lines, ok)                                          # K
    print("K killed after", rec, "rows recorded:", lines, "lines on disk, all parse:", ok)
    rec2, lines2, _ = killed("noflush", 200)
    assert lines2 < rec2, ("MF-K: nothing lost with the flush removed", rec2, lines2)     # MF-K
    print("MF-K flush removed: killed after", rec2, "rows recorded, only", lines2, "on disk")
    sys.path.insert(0, HERE)
    import ledger
    led = ledger.Ledger()
    for i in range(50):
        led.record(i, "PERCEIVE", f"s{i % 7}", "bet", mass=float(i))
    full = led.rows()
    assert all(led.rows(k) == full[k:] for k in range(52))                                # S
    print("S rows(k) == rows()[k:] for every k in 0..51 on a 50-row ledger")
    real = ledger.Ledger.rows
    ledger.Ledger.rows = lambda self, start=0: real(self, start + 1 if start else 0)
    try:
        assert not all(led.rows(k) == full[k:] for k in range(52)), "MF-S: not caught"     # MF-S
    finally:
        ledger.Ledger.rows = real
    print("MF-S an off-by-one planted in rows(start) fails the same check")
    print("ledger_handle: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
