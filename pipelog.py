"""7d, THE PIPELINE LOG (Isaiah 2026-11-03 15:29 "a log that shows every function that fires
alongside the agents thought log"; the reviewer r895 4, r992 3): one line per stage per step,
written at the stage's exit, to pipeline.log beside the ledger. It reads the rows the ledger writes
and the agent's stage scopes, and writes nothing back: the ledger and every decision are the same
ON or OFF (Fig 13: "That record is not documentation of the term. It is the term.").
  STAGE  c<cycle> <STAGE> <ms>ms rows=<event:n,...> slots=<n> stop=<reason|->
         rows: the ledger rows written inside the stage, its innermost scope (route -> mint nests);
         slots: the distinct slots they name; stop: a cap cut (cut), the stage's park verdict, or
         the mint's hold (mint_deferred / try_first / contact_first), else -.
  DEEP   TETHER_PIPELINE_DEEP="c<a>-c<b>": inside those cycles, function-level timing
         (sys.setprofile) under each outermost stage: "  fn <module>.<function> calls=<n>
         ms=<x> self=<y>", ms inclusive (a caller holds its callees') and self its own body
         only, the largest self first (r999: an inclusive list names the wrapper, never where
         the time goes).
  ROTATE segments of TETHER_PIPELINE_SEG_MB (about 100); a closed one is gzipped; past
         TETHER_PIPELINE_CAP_MB (2048 to start; Isaiah "increase the cap as needed") the oldest
         unpinned segment is dropped, and the drop is a line. A segment covering a level won, a
         fault or a cut (an overrun) is PINNED and never dropped. The ledger is never rotated.
  GUARD  nothing here raises into play: the first error turns the log off for the run, counted.
"""
from __future__ import annotations

import collections
import gzip
import os
import shutil
import sys
import time
from pathlib import Path

import armflag
import narrate

_PIPELINE_LOG = armflag.arm("TETHER_PIPELINE_LOG", default=True)
SEG_BYTES = int(float(os.environ.get("TETHER_PIPELINE_SEG_MB", "100")) * 1024 * 1024)
CAP_BYTES = int(float(os.environ.get("TETHER_PIPELINE_CAP_MB", "2048")) * 1024 * 1024)
HOLDS = ("mint_deferred", "try_first", "contact_first")
DEEP_TOP = 15                 # the slowest functions said per stage; the rest summed in one line


def _window(spec: str) -> tuple | None:
    """'c100-c110' -> (100, 110); anything else -> None (deep mode off)."""
    try:
        a, b = spec.strip().lower().replace("c", "").split("-")
        return int(a), int(b)
    except ValueError:
        return None


class PipeLog:
    def __init__(self, path: Path | None, ends: tuple) -> None:
        self.on = _PIPELINE_LOG and path is not None
        self._ends = ends
        self.faults = 0
        self.fault: str | None = None
        if not self.on:
            return
        self._cur = narrate.log_beside(path, "pipeline.log")
        self._dir = self._cur.parent
        self._cur.write_text("", encoding="utf-8")
        self._seg, self._size, self._pin = 0, 0, False
        self._stack: list = []
        self._deep = _window(os.environ.get("TETHER_PIPELINE_DEEP", ""))
        self._prof: dict | None = None

    def _guard(self, fn, *a) -> None:
        if not self.on:
            return
        try:
            fn(*a)
        except Exception as e:           # a log error must never reach play
            self.on = False
            self.faults += 1
            self.fault = f"{type(e).__name__}: {e}"
            if self._prof is not None:
                sys.setprofile(None)

    def see(self, _cycle: int, _step: str, slot: str, event: str, detail: dict) -> None:
        self._guard(self._see, slot, event, detail)

    def _see(self, slot: str, event: str, detail: dict) -> None:
        if event == "agent_fault" or (event == "ending" and detail.get("how") in self._ends):
            self._pin = True
        if not self._stack:
            return
        top = self._stack[-1]
        top[3][event] += 1
        if slot and not str(slot).startswith("@"):
            top[4].add(slot)
        if event == "park":
            top[5] = f"park:{detail.get('verdict')}"
        elif event in HOLDS and top[5] is None:
            top[5] = event

    def enter(self, step: str, cycle: int) -> None:
        self._guard(self._enter, step, cycle)

    def _enter(self, step: str, cycle: int) -> None:
        if (not self._stack and self._deep is not None and self._prof is None
                and self._deep[0] <= cycle <= self._deep[1]):
            self._prof = {"stack": [], "fn": collections.defaultdict(lambda: [0, 0.0, 0.0])}
            sys.setprofile(self._profile)
        self._stack.append([step, cycle, time.perf_counter(), collections.Counter(), set(),
                            None])

    def _profile(self, frame, event, _arg) -> None:
        p = self._prof
        if p is None:
            return
        if event == "call":
            p["stack"].append([frame.f_code, time.perf_counter(), 0.0])
        elif event == "return" and p["stack"]:
            code, t0, inner = p["stack"].pop()
            dt = time.perf_counter() - t0
            f = p["fn"][(code.co_filename, code.co_name)]
            f[0] += 1
            f[1] += dt
            f[2] += dt - inner
            if p["stack"]:
                p["stack"][-1][2] += dt

    def exit(self, _step: str, _cycle: int, cut: bool) -> None:
        self._guard(self._exit, cut)

    def _exit(self, cut: bool) -> None:
        if not self._stack:
            return
        step, cyc, t0, rows, slots, stop = self._stack.pop()
        if cut:
            self._pin = True            # a cut is the slice overrun
        ms = (time.perf_counter() - t0) * 1000
        evs = ",".join(f"{e}:{n}" for e, n in sorted(rows.items()))
        out = [f"c{cyc} {step} {ms:.1f}ms rows={evs or '-'} slots={len(slots)} "
               f"stop={'cut' if cut else stop or '-'}\n"]
        if not self._stack and self._prof is not None:
            sys.setprofile(None)
            fns = sorted(self._prof["fn"].items(), key=lambda kv: -kv[1][2])
            for (fname, name), (n, s, own) in fns[:DEEP_TOP]:
                out.append(f"  fn {Path(fname).stem}.{name} calls={n} ms={s * 1000:.1f} "
                           f"self={own * 1000:.1f}\n")
            if len(fns) > DEEP_TOP:
                rest = fns[DEEP_TOP:]
                out.append(f"  fn +{len(rest)} more calls={sum(v[0] for _k, v in rest)} "
                           f"self={sum(v[2] for _k, v in rest) * 1000:.1f}\n")
            self._prof = None
        self._write("".join(out))

    def _write(self, text: str) -> None:
        with self._cur.open("a", encoding="utf-8") as fh:
            fh.write(text)
        self._size += len(text.encode("utf-8"))
        if self._size >= SEG_BYTES:
            self._rotate()

    def _rotate(self) -> None:
        name = f"pipeline.{self._seg:05d}{'.pin' if self._pin else ''}.log.gz"
        with self._cur.open("rb") as src, gzip.open(self._dir / name, "wb") as dst:
            shutil.copyfileobj(src, dst)
        self._cur.write_text("", encoding="utf-8")
        self._seg, self._size, self._pin = self._seg + 1, 0, False
        segs = sorted(self._dir.glob("pipeline.*.log.gz"))
        total = sum(p.stat().st_size for p in segs)
        for p in segs:
            if total <= CAP_BYTES:
                break
            if ".pin." in p.name:
                continue
            total -= p.stat().st_size
            p.unlink()
            self._write(f"rotation: dropped {p.name} (past the cap, unpinned)\n")
