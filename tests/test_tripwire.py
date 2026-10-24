"""F, THE DATACLASS TRIPWIRE (the reviewer 2026-10-24 11:05 F): the ledger writes a row by asdict
(ledger.py Ledger._row), which walks every nested dataclass, so a new field on any dataclass that
rides in a row changes rows with every switch OFF (SLOT10, 21 routine_cut rows). This reads, in
about a second and without stepping the agent: every dataclass the repo's modules define once
tether and arc_holdout are imported (each field's name, annotation, default and repr flag), and
asdict / repr / says() of a fixed Intent, against tests/tripwire_baseline.json. Any difference
fails here instead of in a 4-minute OFF identity. A deliberate change regenerates the baseline
(--update) in the same commit, and the diff of that file is the record of the change.
    python tests/test_tripwire.py            # rc 0 OK, rc 1 with every difference printed
    python tests/test_tripwire.py --update   # rewrite the baseline from this tree"""
import dataclasses
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).with_name("tripwire_baseline.json")
sys.path.insert(0, str(ROOT))

import arc_holdout  # noqa: E402,F401  the ARC path's modules (perception) with it
import interface  # noqa: E402
import tether  # noqa: E402,F401


def _default(f: dataclasses.Field) -> str:
    if f.default is not dataclasses.MISSING:
        return repr(f.default)
    if f.default_factory is not dataclasses.MISSING:
        return "factory:" + getattr(f.default_factory, "__qualname__", repr(f.default_factory))
    return "required"


def read() -> dict:
    out: dict = {}
    for name, m in sorted(sys.modules.items()):
        p = getattr(m, "__file__", None)
        if not p or ".venv" in p or ROOT not in Path(p).resolve().parents:
            continue
        for k, v in sorted(vars(m).items()):
            if isinstance(v, type) and dataclasses.is_dataclass(v) and v.__module__ == name:
                out[f"{name}.{k}"] = [[f.name, str(f.type), _default(f), f.repr]
                                      for f in dataclasses.fields(v)]
    it = interface.Intent("BECOME", "o1.x", "+")
    out["@intent"] = {"asdict": dataclasses.asdict(it), "repr": repr(it), "says": it.says()}
    return out


if __name__ == "__main__":
    now = read()
    if "--update" in sys.argv:
        BASELINE.write_text(json.dumps(now, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"tripwire: baseline written, {len(now) - 1} dataclasses")
        sys.exit(0)
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    bad = [f"  {k}: {base.get(k)} -> {now.get(k)}" for k in sorted(set(base) | set(now))
           if base.get(k) != now.get(k)]
    assert len(base) > 40, ("tripwire: the baseline holds too few classes", len(base))
    if bad:
        print("tripwire: RED, a logged shape changed (regenerate with --update only if meant):")
        print("\n".join(bad))
        sys.exit(1)
    print(f"tripwire: OK ({len(now) - 1} dataclasses and the Intent renderings unchanged)")
