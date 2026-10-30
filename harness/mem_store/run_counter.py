"""THE COUNTER-PEAK PROBE, launched (the reviewer 2026-10-19 08:45 item 4): probe_counter.py -> game_one.py on ONE
game, --cap-s 600 (E4a's play cap), on a fresh lineage COPY, TETHER_MEMORY_STORE=1 and every other TETHER_ variable
stripped, PYTHONHASHSEED 0, under harness/supervise.py at its default ceiling with --max-s 2700 (the estimate is
about 25 min; a cap below it would be a kill by setup). Alone.
argv: repo lineage_copy out_dir game"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, lin, OUT, GAME = sys.argv[1:5]
PY = sys.executable      # the interpreter running this (r456: no machine path)
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "counter_at_write.jsonl")), "the out dir already holds a reading"
assert os.path.isdir(lin) and len([f for f in os.listdir(lin) if f.endswith(".json")]) == 54, "54 originals"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
ENV["TETHER_MEMORY_STORE"] = "1"
os.makedirs(OUT, exist_ok=True)
CHILD = [PY, "-B", os.path.join(HERE, "probe_counter.py"), "--repo", repo, "--game", GAME, "--cap-s", "600",
         "--out", OUT, "--lineage", lin]
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", "2700", "--", *CHILD],
                   env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode} (the child's rc is in sup/sup.json)\n")
