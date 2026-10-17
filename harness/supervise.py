import sys

sys.dont_write_bytecode = True   # first, before any other import (Isaiah 10-17 05:01)
# ruff: noqa: E402 -- every import follows the bytecode switch above
"""The run supervisor: every long run goes through it (the reviewer 2026-10-17 05:05, Q2/Q3).

A Windows Job Object holds the command and everything it spawns:
  - a per-process commit ceiling (JOB_OBJECT_LIMIT_PROCESS_MEMORY), set before the run;
  - KILL_ON_JOB_CLOSE: the handle lives only here, so if this process, the seat it watches or
    the IDE dies, every process in the job ends (the 10-17 night: lanes outlived the IDE);
  - BELOW_NORMAL priority for the whole job.
A pre-set stop, like the time cap; never chosen during a run. Harness only: nothing the agent
imports imports this, and the agent never sees the ceiling.

    python -B harness/supervise.py --out DIR --watch-pid PID [--ceiling-gb G] [--max-s S] -- CMD...

Writes in DIR: sup.log (events), mem.tsv (every 10 s: each process in the job, private commit and
working set), memcap.tsv (one row per process the job saw at its ceiling: the job's own
notification, never the agent's say-so), sup.json (the ending).
"""
import contextlib
import ctypes
import ctypes.wintypes as wt
import json
import os
import subprocess
import threading
import time

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
psapi = ctypes.WinDLL("psapi", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")

LIMIT_PROCESS_MEMORY = 0x100
LIMIT_KILL_ON_JOB_CLOSE = 0x2000
LIMIT_PRIORITY_CLASS = 0x20
BELOW_NORMAL = 0x4000
CREATE_SUSPENDED = 0x4
EXT_LIMITS, ASSOC_PORT, PID_LIST = 9, 7, 3
MSG_EXIT, MSG_ABNORMAL_EXIT, MSG_NEW, MSG_ZERO, MSG_MEMORY = 7, 8, 6, 4, 9
QUERY_LIMITED, SYNCHRONIZE = 0x1000, 0x100000
INVALID = ctypes.c_void_p(-1).value


class IO(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in
                ("r", "w", "o", "rb", "wb", "ob")]


class BASIC(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wt.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wt.DWORD),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", wt.DWORD),
                ("SchedulingClass", wt.DWORD)]


class EXT(ctypes.Structure):
    _fields_ = [("Basic", BASIC), ("Io", IO), ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t)]


class PORT(ctypes.Structure):
    _fields_ = [("CompletionKey", ctypes.c_void_p), ("CompletionPort", wt.HANDLE)]


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
        (n, ctypes.c_size_t) for n in (
            "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage",
            "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage",
            "PeakPagefileUsage", "PrivateUsage")]


k32.CreateJobObjectW.restype = wt.HANDLE
k32.CreateIoCompletionPort.restype = wt.HANDLE
k32.CreateIoCompletionPort.argtypes = [wt.HANDLE, wt.HANDLE, ctypes.c_void_p, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.GetQueuedCompletionStatus.argtypes = [wt.HANDLE, ctypes.POINTER(wt.DWORD),
                                          ctypes.POINTER(ctypes.c_void_p),
                                          ctypes.POINTER(ctypes.c_void_p), wt.DWORD]
psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]


def total_ram() -> int:
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", wt.DWORD), ("dwMemoryLoad", wt.DWORD)] + [
            (n, ctypes.c_ulonglong) for n in (
                "ullTotalPhys", "ullAvailPhys", "ullTotalPageFile", "ullAvailPageFile",
                "ullTotalVirtual", "ullAvailVirtual", "ullAvailExtendedVirtual")]
    m = MS()
    m.dwLength = ctypes.sizeof(m)
    k32.GlobalMemoryStatusEx(ctypes.byref(m))
    return int(m.ullTotalPhys)


def mem_of(pid: int) -> tuple[int, int] | None:
    h = k32.OpenProcess(QUERY_LIMITED, False, pid)
    if not h:
        return None
    try:
        c = PMC()
        c.cb = ctypes.sizeof(c)
        if not psapi.GetProcessMemoryInfo(h, ctypes.byref(c), c.cb):
            return None
        return int(c.PrivateUsage), int(c.WorkingSetSize)
    finally:
        k32.CloseHandle(h)


def alive(pid: int) -> bool:
    h = k32.OpenProcess(SYNCHRONIZE | QUERY_LIMITED, False, pid)
    if not h:
        return False
    try:
        return k32.WaitForSingleObject(h, 0) == 0x102   # WAIT_TIMEOUT: still running
    finally:
        k32.CloseHandle(h)


class PIDS(ctypes.Structure):
    _fields_ = [("Assigned", wt.DWORD), ("InList", wt.DWORD), ("Ids", ctypes.c_size_t * 1024)]


def job_pids(job) -> list[int]:
    b = PIDS()
    if not k32.QueryInformationJobObject(job, PID_LIST, ctypes.byref(b), ctypes.sizeof(b), None):
        return []
    return [int(b.Ids[i]) for i in range(min(int(b.InList), 1024))]


def main(argv: list[str]) -> int:
    i = argv.index("--")
    opts, cmd = argv[:i], argv[i + 1:]
    o = {opts[j].lstrip("-"): opts[j + 1] for j in range(0, len(opts), 2)}
    out = o["out"]
    os.makedirs(out, exist_ok=True)
    ceiling = int(float(o["ceiling-gb"]) * 2**30) if "ceiling-gb" in o else total_ram() // 2
    max_s = float(o.get("max-s", "0")) or None
    watch = int(o["watch-pid"])
    log = open(os.path.join(out, "sup.log"), "a", buffering=1)   # noqa: SIM115 -- held for the run

    def note(msg: str) -> None:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")

    job = k32.CreateJobObjectW(None, None)
    ext = EXT()
    ext.Basic.LimitFlags = LIMIT_PROCESS_MEMORY | LIMIT_KILL_ON_JOB_CLOSE | LIMIT_PRIORITY_CLASS
    ext.Basic.PriorityClass = BELOW_NORMAL
    ext.ProcessMemoryLimit = ceiling
    if not k32.SetInformationJobObject(job, EXT_LIMITS, ctypes.byref(ext), ctypes.sizeof(ext)):
        note(f"SetInformationJobObject failed {ctypes.get_last_error()}")
        return 2
    port = k32.CreateIoCompletionPort(INVALID, None, None, 1)
    assoc = PORT(None, port)
    k32.SetInformationJobObject(job, ASSOC_PORT, ctypes.byref(assoc), ctypes.sizeof(assoc))

    # never a TETHER_ name: that namespace is the agent's arms, and test_gate_ledger refuses one
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "SUP_CEILING": str(ceiling),
           "SUP_OUT": out}
    p = subprocess.Popen(cmd, env=env, stdin=subprocess.DEVNULL, creationflags=CREATE_SUSPENDED,
                         stdout=open(os.path.join(out, "child.out"), "w"),   # noqa: SIM115
                         stderr=subprocess.STDOUT)
    if not k32.AssignProcessToJobObject(job, wt.HANDLE(int(p._handle))):
        note(f"AssignProcessToJobObject failed {ctypes.get_last_error()}; child killed, never run")
        p.kill()
        return 2
    ntdll.NtResumeProcess(wt.HANDLE(int(p._handle)))
    note(f"start pid {p.pid} ceiling {ceiling / 2**30:.2f} GiB per process, watch {watch}, "
         f"max_s {max_s}, cmd {cmd}")

    state = {"memcap": [], "seen": set(), "ending": None}

    def ports() -> None:
        msg, key, ov = wt.DWORD(), ctypes.c_void_p(), ctypes.c_void_p()
        while True:
            if not k32.GetQueuedCompletionStatus(port, ctypes.byref(msg), ctypes.byref(key),
                                                 ctypes.byref(ov), 1000):
                continue
            pid = ov.value or 0
            if msg.value == MSG_MEMORY:
                state["memcap"].append(pid)
                with open(os.path.join(out, "memcap.tsv"), "a") as fh:
                    fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{pid}\n")
                note(f"MEMORY LIMIT hit by pid {pid}")
            elif msg.value == MSG_NEW:
                state["seen"].add(pid)
                note(f"new process in job {pid}")
            elif msg.value in (MSG_EXIT, MSG_ABNORMAL_EXIT):
                note(f"exit pid {pid}{' (abnormal)' if msg.value == MSG_ABNORMAL_EXIT else ''}")
            elif msg.value == MSG_ZERO:
                note("no process left in job")

    threading.Thread(target=ports, daemon=True).start()
    t0 = time.time()
    with open(os.path.join(out, "mem.tsv"), "a") as mem:
        mem.write("t_s\tpid\tprivate_mb\tws_mb\n")
        while p.poll() is None:
            now = time.time()
            for pid in job_pids(job):
                m = mem_of(pid)
                if m:
                    mem.write(f"{now - t0:.0f}\t{pid}\t{m[0] / 2**20:.0f}\t{m[1] / 2**20:.0f}\n")
            mem.flush()
            if not alive(watch):
                state["ending"] = "OWNER_GONE"
                note(f"watched pid {watch} gone: closing the job (every process in it ends)")
                break
            if max_s and now - t0 > max_s:
                state["ending"] = "SUP_MAX"
                note(f"max_s {max_s} reached: a pre-set stop; terminating the job")
                break
            with contextlib.suppress(subprocess.TimeoutExpired):
                p.wait(timeout=10)
    if state["ending"]:
        k32.TerminateJobObject(job, 1)
        p.wait()
    q = EXT()
    k32.QueryInformationJobObject(job, EXT_LIMITS, ctypes.byref(q), ctypes.sizeof(q), None)
    ending = state["ending"] or ("MEM_CAP" if state["memcap"] else "EXIT")
    res = {"rc": p.returncode, "ending": ending,
           "memcap_pids": state["memcap"], "processes_seen": sorted(state["seen"]),
           "ceiling_gib": round(ceiling / 2**30, 2),
           "peak_process_commit_gib": round(q.PeakProcessMemoryUsed / 2**30, 2),
           "peak_job_commit_gib": round(q.PeakJobMemoryUsed / 2**30, 2),
           "wall_s": round(time.time() - t0, 1)}
    with open(os.path.join(out, "sup.json"), "w") as fh:
        json.dump(res, fh)
    note(f"end {res}")
    k32.CloseHandle(job)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
