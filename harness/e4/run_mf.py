"""The stream driver's MF pair (mf must be caught, plain must be clean) on a given tree, each mode under the
supervisor with this process as the watch pid. argv: repo out"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, out = sys.argv[1:3]
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
lines = []
for mode in ("mf", "plain"):
    o = os.path.join(out, mode)
    os.makedirs(o, exist_ok=True)
    cmd = [PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(o, "sup"),
           "--watch-pid", str(os.getpid()), "--max-s", "1500", "--", PY, "-B", os.path.join(HERE, "e4_stream.py"),
           repo, o, "--seed", "mftest01", "--slice-s", "60", "--n-games", "2"] + (["--mf"] if mode == "mf" else [])
    subprocess.run(cmd, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sup = open(os.path.join(o, "sup", "sup.json"), encoding="utf-8").read()
    lines.append(f"{mode} sup {sup[:120]}")
for mode, extra in (("mf", ["--expect-fail"]), ("plain", [])):
    p = subprocess.run([PY, "-B", os.path.join(HERE, "e4_stream_check.py"), os.path.join(out, mode), *extra],
                       env=ENV, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    lines.append(f"{mode} check rc={p.returncode} {p.stdout.strip()[:400]}")
with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\nEND\n")
print("\n".join(lines))
