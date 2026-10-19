"""Proof for the driver's py-spy pid fix (the reviewer 18:50): a throwaway venv python sleeps; the launcher pid
gets no stack, its child does. Same children() as e4_driver.py. Not the agent."""
import subprocess
import sys
import time

sys.dont_write_bytecode = True
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
PYSPY = ("C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/"
         "2043231f-437e-4548-ac19-702f1efcfb71/scratchpad/spyenv/Scripts/py-spy.exe")


def children(pid: int) -> list:
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          f"(Get-CimInstance Win32_Process -Filter 'ParentProcessId={pid}').ProcessId"],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
    return [int(x) for x in out.split() if x.isdigit()]


p = subprocess.Popen([PY, "-B", "-c", "import time\ndef snooze():\n    time.sleep(40)\nsnooze()"],
                     stdin=subprocess.DEVNULL)
time.sleep(4)
for q in [p.pid] + children(p.pid):
    r = subprocess.run([PYSPY, "dump", "--pid", str(q)], capture_output=True, text=True)
    print(f"--- pid {q} rc {r.returncode}")
    print((r.stdout + r.stderr).strip()[:600])
p.wait()
