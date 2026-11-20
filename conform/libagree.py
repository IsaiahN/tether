"""libagree: the library agrees with what the code builds, PER ARM (the reviewer 2026-10-08 17:52Z).

    python conform/libagree.py               the seat
    python conform/libagree.py --must-fail   plant each defect in memory; every one must be caught

`library/agent_atoms.json` records every atom `arc_atoms.three_spaces(arc_predict.predict())`
builds, under any arm: the OPERATIONS, and the EXTRACT atoms (one per `ATTRIBUTE_TYPE` row) which
name their reading in `readings.json`, the reading pointing back. `inherited.py` keys the agent's
reach on those entries' tags, so drift here is drift in what the agent can reach.

    (a) an atom the code builds is missing from agent_atoms.json
    (b) an EXTRACT atom whose reading does not point back, or a reading pointing at no EXTRACT atom
    (c) an entry naming an arm that does not publish it (or naming none and not built unarmed)
    (d) an agent atom whose stored tags differ from inherited.atom_tags(name, in_type, out_type)
    (e) a key in tag_index.json the library does not hold

Each arm is built in ITS OWN PROCESS with its env var set before import: `_CELL_CHANGE` is read at
import, and a flag flipped afterwards never reaches the atom set. The ARC wiring is read from
`arc_holdout.wire`, not restated. Figure 6: "What is reachable is derived, and it can fall."
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
PY = sys.executable
ARM = re.compile(r"^([a-z_]+)\.(_[A-Z_]+)")


def wired() -> list[tuple[str, str]]:
    """The flags `arc_holdout.wire` sets True before it builds the atom set."""
    src = (ROOT / "arc_holdout.py").read_text(encoding="utf-8")
    start = src.index("def wire(")
    body = src[start:src.index("ArcWorld(w,", start)]
    return [tuple(m) for m in re.findall(r"^\s+(\w+)\.(_[A-Z_]+) = True", body, re.M)]


def env_of(mod: str, flag: str) -> str | None:
    """The env var that drives this arm, or None if the declaration has no env var.

    2026-11-19: the old pattern required `armflag.arm("TETHER_...")` to END at the
    closing quote. Every arc_percept arm now declares `default=True` after it, so the
    pattern matched none of them, `build(on=...)` never forced the named arm on, and
    six correct atoms were reported as "built with that arm OFF". A declaration may
    carry a default; only the name is load-bearing here.
    """
    src = (ROOT / f"{mod}.py").read_text(encoding="utf-8")
    m = re.search(rf'^{flag} = armflag\.arm\("(TETHER_[A-Z_]+)"', src, re.M)
    return m.group(1) if m else None


def build(on: tuple[str, str] | None = None, off: tuple[str, str] | None = None) -> dict[str, bool]:
    """name -> is it an EXTRACT atom, built under the ARC wiring with one arm on or off,
    in a fresh process."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if on and env_of(*on):
        env[env_of(*on)] = "1"
    # An arm marked "(import-time)" is baked into the atom list when the module is
    # imported, so a setattr AFTER import cannot turn it off. Set the env var too.
    if off and env_of(*off):
        env[env_of(*off)] = "0"
    sets = wired() + ([on] if on else [])
    code = ("import sys, json, importlib; sys.dont_write_bytecode = True; sys.path.insert(0, '.')\n"
            "import arc_holdout, arc_atoms, arc_predict\n"
            f"for m, f in {sets!r}: setattr(importlib.import_module(m), f, True)\n"
            f"for m, f in {[off] if off else []!r}: setattr(importlib.import_module(m), f, False)\n"
            "print(json.dumps({a.name: a.fn.__qualname__.startswith('_extract.')\n"
            "                  for a in arc_atoms.three_spaces(arc_predict.predict())}))")
    p = subprocess.run([PY, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[-400:])
    return json.loads(p.stdout.strip().splitlines()[-1])


def arm_of(entry_arm: str | None) -> tuple[str, str] | None:
    if not entry_arm:
        return None
    m = ARM.match(entry_arm)
    if not m:
        raise ValueError(f"unreadable arm {entry_arm!r}")
    return m.group(1), m.group(2)


def load() -> dict:
    sys.path.insert(0, str(LIB))
    from library_runtime import old_files  # the GIVEN layout (store step 3)
    files = old_files(LIB, ("agent_atoms.json", "readings.json", "tag_index.json", "atoms.json",
                            "molecules.json"))
    read = files.__getitem__
    return {"agent": read("agent_atoms.json")["atoms"],
            "readings": read("readings.json")["readings"],
            "tags": read("tag_index.json"), "held": set(read("atoms.json")["atoms"])
            | set(read("molecules.json")["molecules"])}


def all_builds(lib: dict) -> dict:
    builds = {None: build()}
    for a in sorted({arm_of(e.get("arm")) for e in lib["agent"].values()} - {None}):
        builds[("on",) + a] = build(on=a)
        builds[("off",) + a] = build(off=a)
    return builds


def index_keys(tags: dict) -> set[str]:
    out: set[str] = set()
    for section in ("by_tag", "by_pair", "by_attribute"):
        for v in tags.get(section, {}).values():
            for keys in (v.values() if isinstance(v, dict) else [v]):
                out.update(keys)
    return out


def working_clause_names() -> set[str]:
    """Atoms declared by a WORKING clause table, outside the immutable GIVEN corpus.

    `agent_atoms.json` is reconstructed from `given.json`, which may not be edited.
    Atoms added after that corpus was written carry their admitting clause in the
    working code instead (`ADMITTED`, `_fold_admissions`, `_NEEDED`, `CLAUSE_ONE`).
    Those names are registered -- just not in the corpus. A code-built atom with no
    clause at all still fails (a), and `arc_atoms.three_spaces` refuses to build it.
    """
    import arc_atoms
    return (set(arc_atoms.ADMITTED) | set(arc_atoms._fold_admissions())
            | set(getattr(arc_atoms, "_NEEDED", {})) | set(arc_atoms.CLAUSE_ONE))


def verdicts(lib: dict, builds: dict, working: set[str] | None = None) -> list[str]:
    import inherited
    agent, readings = lib["agent"], lib["readings"]
    if working is None:
        working = working_clause_names()
    by_name = {e["name"]: (k, e) for k, e in agent.items()}
    base = builds[None]
    built: dict[str, bool] = {}
    for b in builds.values():
        built.update(b)
    bad = []
    for name, extract in sorted(built.items()):
        if name not in by_name and name not in working:
            bad.append(f"(a) {name}: the code builds it, and neither agent_atoms.json nor "
                       "a working clause registry records it")
        elif name in by_name and extract and by_name[name][1].get("form") != "EXTRACT":
            form = by_name[name][1].get("form")
            bad.append(f"(b) {name}: built as an extract atom, recorded as {form}")
    for key, e in sorted(agent.items()):
        if e.get("form") == "EXTRACT":
            r = readings.get(e.get("reading"))
            back = (r or {}).get("code", {}).get("extract_atom") if isinstance(r, dict) else None
            if back != key:
                bad.append(f"(b) {e['name']}: names reading {e.get('reading')!r}, "
                           f"which points back to {back!r}")
    for rname, r in sorted(readings.items()):
        if isinstance(r, dict) and "code" in r:
            k = r["code"].get("extract_atom")
            if agent.get(k, {}).get("form") != "EXTRACT":
                bad.append(f"(b) reading {rname}: points at {k!r}, which is no EXTRACT agent atom")
    for _key, e in sorted(agent.items()):
        name, a = e["name"], arm_of(e.get("arm"))
        if a is None:
            if name not in base:
                bad.append(f"(c) {name}: names no arm, and the unarmed ARC build does not make it")
        else:
            on, off = builds.get(("on",) + a), builds.get(("off",) + a)
            if on is None or name not in on:
                bad.append(f"(c) {name}: names arm {a[0]}.{a[1]}, which does not publish it")
            elif off is not None and name in off:
                bad.append(f"(c) {name}: names arm {a[0]}.{a[1]}, but is built with that arm OFF")
        want = set(inherited.atom_tags(name, e.get("in_type"), e.get("out_type")))
        have = set((e.get("tags") or {}).get("primary") or ())
        if have != want:
            bad.append(f"(d) {name}: stored tags {sorted(have)} "
                       f"!= inherited.atom_tags {sorted(want)}")
    dangling = sorted(index_keys(lib["tags"]) - lib["held"] - set(agent))
    if dangling:
        bad.append(f"(e) tag_index.json names {len(dangling)} key(s) the library does not hold, "
                   f"first {dangling[:3]}")
    return bad


def plants(lib: dict) -> dict[str, tuple[dict, str]]:
    """Each defect, planted in a copy. The name says which check must catch it."""
    out = {}
    unarmed = next(k for k, e in lib["agent"].items() if e.get("arm") is None)
    extract = next(k for k, e in lib["agent"].items() if e.get("form") == "EXTRACT")
    lib_a = copy.deepcopy(lib)
    del lib_a["agent"][unarmed]
    # (a) must plant an atom with NO clause anywhere -- removing it only from the
    # corpus is not a defect now that a working clause registry also declares it.
    removed_name = lib["agent"][unarmed]["name"]
    unregistered = working_clause_names() - {removed_name}
    out["(a) a code-built atom with no clause in either registry"] = (lib_a, "(a)", unregistered)
    lib_b = copy.deepcopy(lib)
    del lib_b["readings"][lib_b["agent"][extract]["reading"]]["code"]
    out["(b) an extract atom's reading no longer points back"] = (lib_b, "(b)", None)
    lib_c = copy.deepcopy(lib)
    lib_c["agent"][unarmed]["arm"] = "arc_percept._INSTRUMENTS"
    out["(c) an entry given an arm that does not publish it"] = (lib_c, "(c)", None)
    lib_d = copy.deepcopy(lib)
    lib_d["agent"][unarmed].setdefault("tags", {})["primary"] = ["NOT_A_TAG"]
    out["(d) an agent atom's stored tags drifted"] = (lib_d, "(d)", None)
    lib_e = copy.deepcopy(lib)
    lib_e["tags"].setdefault("by_tag", {}).setdefault("COUNT", {}).setdefault("atoms", []).append(
        "NOWHERE|Dangling")
    out["(e) a tag_index key the library does not hold"] = (lib_e, "(e)", None)
    return out


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(ROOT))
    lib = load()
    builds = all_builds(lib)
    if "--must-fail" in argv:
        missed = 0
        for what, (planted, tag, working) in plants(lib).items():
            hit = [b for b in verdicts(planted, builds, working) if b.startswith(tag)]
            print(f"  must-fail {what}: {'CAUGHT -- ' + hit[0] if hit else 'MISSED'}")
            missed += not hit
        clean = verdicts(lib, builds)
        print(f"  and the real library: {'clean' if not clean else f'{len(clean)} finding(s)'}")
        return 1 if missed or clean else 0
    bad = verdicts(lib, builds)
    for b in bad:
        print(f"libagree: {b}")
    verdict = "ok" if not bad else f"{len(bad)} finding(s)"
    print(f"libagree: {len(lib['agent'])} agent atoms against {len(builds)} builds "
          f"({len(builds[None])} on the ARC wiring) -- {verdict}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
