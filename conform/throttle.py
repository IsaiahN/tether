"""throttle: launch a batch of runs without slowing Isaiah's machine (Isaiah 2026-10-09 21:16 CDT,
the reviewer 2026-10-10 02:17Z).

Decides only WHEN a run starts, never what it computes, so no ledger changes. It lives outside the
panel stamp's hashed set: nothing a run imports imports it.

    python conform/throttle.py panel                 # every panel member, then the panel seat
    python conform/throttle.py cmds FILE             # per line: cwd<TAB>log<TAB>K=V,K=V<TAB>command
"""
from __future__ import annotations

import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

# THE SETTINGS, in one place; Isaiah may change them.
BUFFER_CORES = 2            # anchor: Isaiah 2026-10-09 21:16 CDT, cores left free for his own use
CPU_GATE = 75.0             # anchor: the reviewer 02:17Z, start a run only while total CPU % < this
POLL_S = 15                 # anchor: a declared convention, not measured; movable
CAP = max(1, (os.cpu_count() or 1) - BUFFER_CORES)

ROOT = Path(__file__).resolve().parent.parent
BELOW_NORMAL = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)


def cpu_percent() -> float:
    """Total CPU %, one ~1 s sample. psutil when installed, else PowerShell's counter."""
    try:
        import psutil
        return float(psutil.cpu_percent(interval=1.0))
    except ImportError:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1"
             " -MaxSamples 1).CounterSamples[0].CookedValue"],
            capture_output=True, text=True, check=False)
        try:
            return float(out.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            return 100.0        # unreadable load reads as busy: wait, never pile on


def may_start(live: int, seen: list | None = None) -> bool:
    """One more job may start: a slot is free AND load is under the gate. For launchers that keep
    their own loop (fast_check, the harness); `run` below is the same rule."""
    if live >= CAP:
        return False
    load = cpu_percent()
    if seen is not None:
        seen.append(load)
    return load < CPU_GATE


def run(jobs: list[tuple]) -> int:
    """Start each (argv, cwd, log[, env]) when a slot is free AND load is under the gate. Never
    kills a running job for load. Returns the number of jobs that exited non-zero."""
    pending, live, bad, seen = list(jobs), [], 0, []
    while pending or live:
        for p, name, fh in list(live):
            if p.poll() is not None:
                live.remove((p, name, fh))
                fh.close()
                bad += p.returncode != 0
                print(f"[throttle] done {name} exit={p.returncode}", flush=True)
        if pending and may_start(len(live), seen):
            argv, cwd, log, *extra = pending.pop(0)
            env = {**os.environ, **extra[0]} if extra else None
            # held open for the run's whole life and closed when it exits (above)
            fh = open(log, "w", encoding="utf-8")  # noqa: SIM115
            p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=fh,
                                 stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL)
            live.append((p, log.stem, fh))
            print(f"[throttle] start {log.stem} (cpu {seen[-1]:.0f}%, live {len(live)}/{CAP})",
                  flush=True)
            continue
        time.sleep(POLL_S if pending else 5)
    if seen:
        print(f"[throttle] cap {CAP} of {os.cpu_count()} logical cores; gate {CPU_GATE}%; "
              f"cpu at launch checks min {min(seen):.0f} max {max(seen):.0f}", flush=True)
    return bad


def _panel() -> int:
    sys.path.insert(0, str(ROOT / "conform"))
    import panel
    bad = panel._produce()
    seat = subprocess.run([sys.executable, str(ROOT / "conform" / "panel.py")], cwd=ROOT,
                          check=False)
    return bad or seat.returncode


def _cmds(path: str) -> int:
    jobs = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            cwd, log, env, cmd = line.split("\t", 3)
            pairs = dict(kv.split("=", 1) for kv in env.split(",") if kv)
            jobs.append((shlex.split(cmd, posix=False), Path(cwd), Path(log), pairs))
    return run(jobs)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "panel"
    sys.exit(_panel() if mode == "panel" else _cmds(sys.argv[2]))
