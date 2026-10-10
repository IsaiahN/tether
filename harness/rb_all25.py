"""All 25 public games OFFLINE, confirm-only, cold library, the same cycles each, K at a time.
argv: tree cycles k outdir. Every game in the kit's environment_files is played; none is chosen."""
import os
import subprocess
import sys
import time

tree, cycles, k, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
games = sorted(os.listdir(os.path.join(tree, "environment_files")))
assert len(games) == 25, games
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "conform"))
import throttle  # noqa: E402  -- K is a request; the throttle's cap and load gate bind

env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
queue, running = list(games), {}
t0 = time.time()
while queue or running:
    while queue and len(running) < k and throttle.may_start(len(running)):
        g = queue.pop(0)
        fh = open(os.path.join(out, f"{g}.out"), "w")  # noqa: SIM115 -- the child's stdout, closed on exit
        running[g] = (subprocess.Popen([sys.executable, os.path.join(here, "rb_one.py"), tree, g,
                                        cycles, os.path.join(out, f"{g}.jsonl")],
                                       stdout=fh, stderr=subprocess.STDOUT, env=env,
                                       creationflags=throttle.BELOW_NORMAL), fh)
    for g, (p, fh) in list(running.items()):
        if p.poll() is not None:
            fh.close()
            del running[g]
            print(f"{time.time() - t0:7.0f}s  {g} exit {p.returncode}", flush=True)
    time.sleep(5)
print("ALL DONE", round(time.time() - t0), "s", flush=True)
