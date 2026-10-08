"""All 25 public games OFFLINE, confirm-only, cold library, the same cycles each, K at a time.
argv: tree cycles k outdir. Every game in the kit's environment_files is played; none is chosen."""
import sys, os, subprocess, time
tree, cycles, k, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
games = sorted(os.listdir(os.path.join(tree, "environment_files")))
assert len(games) == 25, games
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
queue, running = list(games), {}
t0 = time.time()
while queue or running:
    while queue and len(running) < k:
        g = queue.pop(0)
        fh = open(os.path.join(out, f"{g}.out"), "w")
        running[g] = (subprocess.Popen([sys.executable, os.path.join(here, "rb_one.py"), tree, g, cycles,
                                        os.path.join(out, f"{g}.jsonl")], stdout=fh, stderr=subprocess.STDOUT, env=env), fh)
    for g, (p, fh) in list(running.items()):
        if p.poll() is not None:
            fh.close(); del running[g]
            print(f"{time.time() - t0:7.0f}s  {g} exit {p.returncode}", flush=True)
    time.sleep(5)
print("ALL DONE", round(time.time() - t0), "s", flush=True)
