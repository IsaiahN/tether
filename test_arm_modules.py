"""THE ARMS HEADER COVERS EVERY AGENT MODULE THAT DECLARES AN ARM (the ALL-ON plan B4; the reviewer
2026-10-11 15:26 CDT). instruments.ARM_MODULES is data; this checks it against the source.

  m1 every top-level module (not a test, not conform/) whose source calls armflag.arm( is listed;
  m2 MUST-FAIL: with interface dropped from the list, the check names it;
  m3 live: with TETHER_REALISE_CELL=1, Attribution.arms() lists interface._REALISE_CELL as ON;
  m4 every module-level name assigned from armflag.arm( is _UPPER, the only form arms() records
     (instruments: k.startswith("_") and an upper or a digit next; the digit since 2026-10-16,
     when 13 _7x arms were found missing from every header); lineage.CARRY was public until
     2026-10-15 and no header ever carried it.

    python test_arm_modules.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def declaring() -> set[str]:
    return {p.stem for p in ROOT.glob("*.py")
            if not p.stem.startswith("test_") and "armflag.arm(" in p.read_text(encoding="utf-8")
            and p.stem != "armflag"}


def public_arms() -> list[str]:
    """module:name for each module-level `NAME = armflag.arm(` whose name is not _UPPER."""
    out = []
    for p in sorted(ROOT.glob("*.py")):
        if p.stem.startswith("test_") or p.stem == "armflag":
            continue
        for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*armflag\.arm\(",
                             p.read_text(encoding="utf-8"), re.M):
            if not (m.group(1).startswith("_") and (m.group(1)[1:2].isupper()
                                                   or m.group(1)[1:2].isdigit())):
                out.append(f"{p.stem}:{m.group(1)}")
    return out


def missing(listed: tuple) -> list[str]:
    return sorted(declaring() - set(listed))


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import tether, interface, instruments
print(json.dumps(instruments.Attribution.arms()))
'''

if __name__ == "__main__":
    import instruments
    assert not missing(instruments.ARM_MODULES), missing(instruments.ARM_MODULES)
    print(f"  m1 ARM_MODULES covers all {len(declaring())} declaring modules")
    dropped = tuple(m for m in instruments.ARM_MODULES if m != "interface")
    assert missing(dropped) == ["interface"], missing(dropped)
    print("  m2 must-fail: with interface dropped, the check names ['interface']")
    env = dict(os.environ, TETHER_REALISE_CELL="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=str(ROOT), timeout=300)
    assert p.returncode == 0, p.stderr[-2000:]
    arms = json.loads(p.stdout.strip().splitlines()[-1])
    assert "interface._REALISE_CELL" in arms["on"], arms
    print("  m3 live: interface._REALISE_CELL recorded ON")
    assert not public_arms(), public_arms()
    print("  m4 every module-level arm is _UPPER")
    print("arm modules: OK")
