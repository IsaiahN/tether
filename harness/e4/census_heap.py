"""THE SAMPLED MEMORY CENSUS (the reviewer 2026-10-19 02:52, 03:00: approved with A1-A5). HARNESS SIDE, READ ONLY on the
agent: called by e4_stream.py BETWEEN steps only. No gc.collect, no write to any agent object, nothing sorted or
copied in place; the sampler's RNG is this module's own random.Random(SEED), never the agent's or the global one.

At a point: private commit FIRST; Python's allocator statistics (sys._debugmallocstats through an fd-2 redirect, and
sys.getallocatedblocks); then, per ROOT (a named container), len, the container's own getsizeof, and a SAMPLED deep
size: a reservoir sample of K entries, each walked with gc.get_referents and sys.getsizeof, never through the
STOP set (A1: the agent, gamma, the ledger, every other root container, every module; classes, functions and code
are skipped by type), capped at CAP objects per entry (A2: cap hits counted; a root with any is a LOWER BOUND).
est_bytes = table + len x the sample mean. Roots are NOT deduplicated; already_seen counts sampled objects of a root
already met in an earlier root's samples at the same point. Commit is read again after; the walk is cut if commit
reaches GUARD (25.0 GiB), checked every 100,000 objects.
TSV: <out>/census.tsv, one POINT row and one ROOT row per root per point."""
import ctypes
import ctypes.wintypes as wt
import gc
import os
import random
import re
import sys
import time
import types

SEED = 20261019
K = 1000
CAP = 10_000
GUARD = 25 * 2**30
CHECK_EVERY = 100_000
TIME_CAP = 600                # seconds of walking per point (the design, 02:47)
IMMORTAL = 2**32 - 1          # 3.13's refcount for an immortal object (read: sys.getrefcount(None) = 4294967295)
SKIP = (types.ModuleType, type, types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.CodeType,
        types.FrameType, types.WrapperDescriptorType, types.MethodDescriptorType, types.GetSetDescriptorType,
        types.MemberDescriptorType)
KIND = ("_kind_landed", "_kind_pairs", "_dk_this", "_kind_landed_n", "_kind_last", "_kind_cls", "_kind_cls_keys",
        "_kind_landed_dk", "_kdk_last")
MODULE_STORES = ("_INDEX_STORE", "_LANDING", "_PAIR_TALLY", "_BS_CARRIED", "_BM_CARRIED")
BOUND_MODULE = ("_BOUND_MEMO", "_BOUND_SLOT_MEMO", "_BOUND_SLOT_IDX", "_PAIRS_SEEN", "_BOUND_SLOT_MAP", "_BOUND_TERM")
BOUND_OWN = ("_bound_cache", "_bound_slot_cache", "_bound_slot_idx", "_pairs_seen", "_bound_slot_map")
SCAN_MODULES = ("tether", "gamma", "ledger", "lineage", "arc_world", "arc_holdout", "arc_atoms", "arc_percept",
                "arc_predict", "grammar", "routine", "observer", "sensors", "sensors_heavy", "compile_term")
_RNG = random.Random(SEED)


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
        (n, ctypes.c_size_t) for n in ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                                       "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                                       "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage",
                                       "PrivateUsage")]


def commit_bytes() -> int:
    c = _PMC()
    c.cb = ctypes.sizeof(c)
    k32 = ctypes.windll.kernel32
    k32.GetCurrentProcess.restype = wt.HANDLE
    f = ctypes.windll.psapi.GetProcessMemoryInfo
    f.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]
    f(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return int(c.PrivateUsage)


def mallocstats(path: str) -> dict:
    """sys._debugmallocstats writes to the C stderr (fd 2): redirect fd 2 to a file for the call, then parse."""
    sys.stderr.flush()
    saved = os.dup(2)
    with open(path, "w", encoding="utf-8") as fh:
        os.dup2(fh.fileno(), 2)
        try:
            sys._debugmallocstats()
        finally:
            sys.stderr.flush()
            os.dup2(saved, 2)
            os.close(saved)
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    def num(label):
        m = re.search(r"#\s*" + re.escape(label) + r"\s*=\s*([\d,]+)", text)
        return int(m.group(1).replace(",", "")) if m else None
    return {"pymalloc": "Small block threshold" in text, "chars": len(text),
            "arenas": num("arenas allocated current"), "alloc_bytes": num("bytes in allocated blocks"),
            "free_bytes": num("bytes in available blocks")}


def _deep(obj, stop: set, budget: list) -> tuple[int, int, bool, set]:
    """Bytes and objects reachable from obj, never through the stop set or a skipped type; capped at CAP."""
    seen, stack, size, n = set(), [obj], 0, 0
    while stack:
        o = stack.pop()
        i = id(o)
        if i in stop or i in seen or isinstance(o, SKIP) or sys.getrefcount(o) >= IMMORTAL:
            continue                                  # immortal (None, bools, small ints, interned): shared, not owned
        seen.add(i)
        size += sys.getsizeof(o)
        n += 1
        budget[0] += 1
        if n >= CAP:
            return size, n, True, seen
        stack.extend(gc.get_referents(o))
    return size, n, False, seen


def _sample(container) -> list:
    """A reservoir sample of K entries; a dict's entry is its (key, value) pair. Iteration only, read only."""
    items = container.items() if isinstance(container, dict) else container
    out = []
    for j, e in enumerate(items):
        if j < K:
            out.append(e)
        else:
            r = _RNG.randrange(j + 1)
            if r < K:
                out[r] = e
    return out


def roots_of(ag) -> list:
    """(name, container) for every named root, in a fixed order."""
    tm = sys.modules.get("tether")
    out = [("ledger._entries", getattr(ag.led, "_entries", None)), ("ag._ak_kept", getattr(ag, "_ak_kept", None))]
    out += [(f"kind.{n}", getattr(ag, n, None)) for n in KIND]
    g = ag.gamma
    out += [(f"gamma.{n}", v) for n, v in sorted(vars(g).items()) if isinstance(v, (dict, list, set, tuple))]
    out += [(f"tether.{n}", getattr(tm, n, None)) for n in MODULE_STORES]
    out += [(f"bound.tether.{n}", getattr(tm, n, None)) for n in BOUND_MODULE]
    out += [(f"bound.ag.{n}", getattr(ag, n, None)) for n in BOUND_OWN]
    named = {id(c) for _n, c in out if c is not None}
    for n, v in sorted(vars(ag).items()):
        if isinstance(v, (dict, list, set, tuple, frozenset)) and id(v) not in named:
            out.append((f"ag.{n}", v))
            named.add(id(v))
    for mn in SCAN_MODULES:
        m = sys.modules.get(mn)
        if m is None:
            continue
        for n, v in sorted(vars(m).items()):
            if isinstance(v, (dict, list, set, frozenset)) and id(v) not in named and len(v) >= 1000:
                out.append((f"mod.{mn}.{n}", v))
                named.add(id(v))
    return [(n, c) for n, c in out if c is not None]


def point(label: str, ag, out: str, commit_first: int | None = None) -> None:
    t0 = time.perf_counter()
    c0 = commit_first if commit_first is not None else commit_bytes()
    ms = mallocstats(os.path.join(out, f"mallocstats_{label}.txt"))
    blocks = sys.getallocatedblocks()
    roots = roots_of(ag)
    stop = {id(ag), id(ag.gamma), id(ag.led)} | {id(c) for _n, c in roots} | {id(m) for m in list(sys.modules.values())}
    path = os.path.join(out, "census.tsv")
    new = not os.path.exists(path)
    rows, budget, truncated, met = [], [0], None, set()
    for k, (name, c) in enumerate(roots):
        try:
            n_len = len(c)
        except TypeError:
            n_len = None
        sizes, caps, objs, mine = [], 0, 0, set()
        for e in _sample(c):
            parts = e if isinstance(c, dict) else (e,)
            s, nobj, capped, seen = 0, 0, False, set()
            for p in parts:
                s_, n_, cap_, seen_ = _deep(p, stop, budget)
                s, nobj, capped, seen = s + s_, nobj + n_, capped or cap_, seen | seen_
            sizes.append(s)
            caps += capped
            objs += nobj
            mine |= seen
            if budget[0] >= CHECK_EVERY:
                budget[0] = 0
                if commit_bytes() >= GUARD:
                    truncated = f"truncated at root {k} {name}, RAM guard"
                    break
                if time.perf_counter() - t0 >= TIME_CAP:
                    truncated = f"truncated at root {k} {name}, time cap {TIME_CAP} s"
                    break
        already = len(mine & met)                     # met = the EARLIER roots' sampled objects only
        met |= mine
        table = sys.getsizeof(c)
        srt = sorted(sizes)
        mean = sum(sizes) / len(sizes) if sizes else 0.0
        var = sum((x - mean) ** 2 for x in sizes) / (len(sizes) - 1) if len(sizes) > 1 else 0.0
        se = (var / len(sizes)) ** 0.5 if sizes else 0.0
        est = table + (n_len or 0) * mean
        rows.append(f"ROOT\t{label}\t{name}\t{type(c).__name__}\t{n_len}\t{table}\t{len(sizes)}\t{round(mean, 1)}\t"
                    f"{srt[len(srt) // 2] if srt else 0}\t{srt[-1] if srt else 0}\t{caps}\t{round(se, 1)}\t"
                    f"{round(est)}\t{'lower bound' if caps else ''}\t{already}\t{objs}")
        if truncated:
            break
    c1 = commit_bytes()
    secs = round(time.perf_counter() - t0, 1)
    with open(path, "a", encoding="utf-8") as fh:
        if new:
            fh.write(f"# sampled memory census; sampler random.Random({SEED}), K {K} entries per root, CAP {CAP} "
                     f"objects per entry, stop set: the agent, gamma, the ledger, every root container, every "
                     f"module (classes, functions, code skipped by type). Points: after_load, after_step1, "
                     f"after_step2, switch. Roots are NOT deduplicated (already_seen counts overlaps within the "
                     f"samples). Absolute commit minus the roots' sum includes the interpreter and the program; "
                     f"only CHANGES between points are readings.\n")
            fh.write("POINT\tlabel\tcommit_before\tcommit_after\tsecs\tpymalloc\tarenas\talloc_block_bytes\t"
                     "free_block_bytes\tallocated_blocks\troots\tsampled_seen\ttruncated\n")
            fh.write("ROOT\tlabel\troot\ttype\tlen\ttable_bytes\tsampled\tmean\tmedian\tmax\tcap_hits\tstderr\t"
                     "est_bytes\tbound\talready_seen\tsampled_objects\n")
        fh.write(f"POINT\t{label}\t{c0}\t{c1}\t{secs}\t{ms['pymalloc']}\t{ms['arenas']}\t{ms['alloc_bytes']}\t"
                 f"{ms['free_bytes']}\t{blocks}\t{len(rows)}\t{len(met)}\t{truncated or ''}\n")
        fh.write("\n".join(rows) + "\n")


def dry(out: str) -> None:
    """A4: the version and build, the allocator, and one malloc-stats capture parsed, before any launch."""
    import sysconfig
    os.makedirs(out, exist_ok=True)
    ms = mallocstats(os.path.join(out, "mallocstats_dry.txt"))
    with open(os.path.join(out, "dry.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"python {sys.version}\nPYTHONMALLOC {os.environ.get('PYTHONMALLOC')}\n"
                 f"PYTHONHASHSEED {os.environ.get('PYTHONHASHSEED')} hash_randomization "
                 f"{sys.flags.hash_randomization}\nPy_GIL_DISABLED {sysconfig.get_config_var('Py_GIL_DISABLED')}\n"
                 f"mallocstats {ms}\nallocated_blocks {sys.getallocatedblocks()}\ncommit {commit_bytes()}\n")
