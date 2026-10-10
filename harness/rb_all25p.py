"""All 25 public games OFFLINE, confirm-only, cold library, from a tree PINNED to one commit.
argv: tree commit cycles k outdir [game ...]. With no games named, every game in the kit is played.
The pin is checked before the run and again by each game before it imports anything."""
import os
import subprocess
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import rb_heads  # noqa: E402

sys.path.insert(0, os.path.join(here, "..", "conform"))
import throttle  # noqa: E402  -- K is a request; the throttle's cap and load gate bind

tree, commit, cycles, k, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
commit = subprocess.run(["git", "-C", tree, "rev-parse", commit], capture_output=True, text=True,
                        check=True).stdout.strip()
rb_heads.refuse_unless_pinned(tree, commit)
games = sys.argv[6:] or sorted(os.listdir(os.path.join(tree, "environment_files")))
if not sys.argv[6:]:
    assert len(games) == 25, games
os.makedirs(out, exist_ok=True)
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
queue, running, refused = list(games), {}, False
t0 = time.time()
print(f"pinned {commit}", flush=True)
while queue or running:
    while queue and len(running) < k and not refused and throttle.may_start(len(running)):
        g = queue.pop(0)
        fh = open(os.path.join(out, f"{g}.out"), "w")  # noqa: SIM115 -- the child's stdout, closed on exit
        running[g] = (subprocess.Popen([sys.executable, os.path.join(here, "rb_onep.py"), tree, g,
                                        cycles, os.path.join(out, f"{g}.jsonl"), commit],
                                       stdout=fh, stderr=subprocess.STDOUT, env=env,
                                       creationflags=throttle.BELOW_NORMAL), fh)
    for g, (p, fh) in list(running.items()):
        if p.poll() is not None:
            fh.close()
            del running[g]
            if not refused and p.returncode != 0:
                with open(os.path.join(out, f"{g}.out")) as log:
                    refused = "REFUSED" in log.read()
            print(f"{time.time() - t0:7.0f}s  {g} exit {p.returncode}", flush=True)
    if refused and queue:
        print(f"STOPPED: the tree left its pin; {len(queue)} games not started: {queue}",
              flush=True)
        queue = []
    time.sleep(5)
print("ALL DONE", round(time.time() - t0), "s", flush=True)
sys.exit(1 if refused else 0)
