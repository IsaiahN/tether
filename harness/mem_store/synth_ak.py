"""S5 (c)'s TEST (the reviewer 2026-10-19 09:36 item 3c): ONE encoder of the form-2 ak_ file on the synthetic bp35
counter (synth_prep.py's pickle), in its own process, so each mode's peak is its own. A stub agent carries the counter
(_ak_asked), _atoms_token "T" and an empty whole memo (no pair held whole). Modes:
  s4      S4's encoder as tested at 08:42: _ak_rows (a re-keyed copy), a list of dicts sorted by repr of the whole
          key (signature included), the body encoded whole by _dumps, written "xb"
  whole   the NEW order (_ak_entries), the body encoded whole by _dumps, written "xb" -- the byte reference
  stream  the NEW order through _put_memo_stream (bounded chunks, a running sha256, renamed to its hash name)
Reported: commit (private bytes) just before the write, the process's PEAK commit (Windows' own peak counter, exact,
not sampled) after it, their difference, the wall, the file name and size. whole and stream must name the SAME file.
argv: repo pickle out_dir mode"""
import ctypes
import ctypes.wintypes as wt
import hashlib
import itertools
import os
import pickle
import sys
import time
from collections import Counter
from pathlib import Path

REPO, PKL, OUT, MODE = sys.argv[1:5]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import lineage  # noqa: E402
import tether  # noqa: E402


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                *((n, ctypes.c_size_t) for n in (
                    "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                    "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage"))]


_k32, _ps = ctypes.WinDLL("kernel32"), ctypes.WinDLL("psapi")
_k32.GetCurrentProcess.restype = wt.HANDLE
_ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]


def mem() -> tuple:
    c = _PMC()
    c.cb = ctypes.sizeof(_PMC)
    _ps.GetProcessMemoryInfo(_k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return int(c.PagefileUsage), int(c.PeakPagefileUsage)


class Stub:
    _atoms_token = "T"
    _bound_cache: dict = {}


assert not tether._BOUND_MEMO, "no pair is held whole in this test"
with open(PKL, "rb") as fh:
    d = pickle.load(fh)
ag = Stub()
ag._ak_asked = Counter(dict(d["items"]))
sig = d["sig"]
del d
p = Path(OUT) / MODE
p.mkdir(parents=True)
h = "synthbp35000000"
before, peak_before = mem()
t0 = time.perf_counter()
if MODE == "s4":
    rows = lineage._ak_rows(ag)
    entries = [{"key": key, "role": role, "o": o, "x": x, "slot": slot, "n": n}
               for (t, s, key, role, o, x, slot), n in sorted(rows.items(), key=repr) if t == "T" and s == sig]
    arm, parts = lineage._sig_parts(sig)
    raw = lineage._dumps({"gen": h, "sig_arm": arm, "sig_atoms": parts, "entries": entries, "refused": [],
                          "form": 2})
    name = f"ak_{h}_{hashlib.sha256(raw).hexdigest()[:16]}.json"
    with open(p / name, "xb") as fh:
        fh.write(raw)
elif MODE == "whole":
    entries = list(lineage._ak_entries(ag, "T", sig))
    arm, parts = lineage._sig_parts(sig)
    raw = lineage._dumps({"gen": h, "sig_arm": arm, "sig_atoms": parts, "entries": entries, "refused": [],
                          "form": 2})
    name = f"ak_{h}_{hashlib.sha256(raw).hexdigest()[:16]}.json"
    with open(p / name, "xb") as fh:
        fh.write(raw)
elif MODE == "stream":
    gen = lineage._ak_entries(ag, "T", sig)
    first = next(gen)                # the sort happens here, before the first chunk
    after_sort, peak_sort = mem()
    print("SORTED_LIST", f"commit_after_sort {after_sort}", f"over_before {after_sort - before}",
          f"= {(after_sort - before) / 2**30:.3f} GiB", f"peak_so_far {peak_sort}", sep="\t", flush=True)
    name = lineage._put_memo_stream(p, h, "ak_", sig, itertools.chain([first], gen), {"form": 2})["written"]
else:
    raise SystemExit(f"mode {MODE}")
wall = time.perf_counter() - t0
_now, peak = mem()
print("RESULT", MODE, f"entries {len(ag._ak_asked)}", f"commit_before {before}", f"peak_before {peak_before}",
      f"peak_after {peak}", f"write_peak_over_before {peak - before}", f"= {(peak - before) / 2**30:.3f} GiB",
      f"wall_s {wall:.1f}", f"file {name}", f"bytes {os.path.getsize(p / name)}", sep="\t", flush=True)
