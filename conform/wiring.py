"""wiring: built-but-never-wired, made a check that fires rather than a census that is run.

`F119` asked Isaiah's question -- can the agent do everything `WHAT_THE_AGENT_SEES` says it
can -- and its three-questions-per-item design was right: DECLARED, has a PRODUCER, has ever
OCCURRED, because a single present-or-absent column merges all three and the merge is why the
class keeps being rediscovered. It was an INSTRUMENT: it ran once, published, and was not kept,
so when its `negate` row turned out to be refuted by its own evidence the error could be
refuted and never located.

FOUR DEFECTS, EACH FOUND BY A CENSUS GOING WRONG ONCE, AND EACH A FIXTURE BELOW. Reintroduce
the defect, never disable the check:

    A   substring matching          `traction` read 6 and is `subtraction`
    B   refusals read as occurred   `reuse_refused` carries `detail.term`, and a term the loop
                                    turned away read identically to one it accepted
    C   events conflated            offered, minted, accepted and settled are four facts
    D   chain-position blindness    `above . negate . all` was credited to its ENDS, so the
                                    middle link read as never-occurred while it was minting,
                                    settling against the ground, and driving bets

TRANSITIONS, NOT COUNTS. Counts move with every run and a check that fires on them is ceremony
nobody reads. What matters is a capability going never-occurred -> occurred, or the reverse:
the manifest records STATUS and the check refuses a status that has changed without the
manifest being updated in the same commit. That is the sum being computed -- the focus seat's
lesson, where drift was visible only in the sum and nothing computed the sum.

THE DENOMINATOR IS THE ARTIFACT SET, AND IT IS RECORDED. Occurrence is counted over the run
files that exist, so adding a run can move a status legitimately. `computed_over` names them,
per source rather than per inferred game -- the stem is an artifact, not a claim about which
board it is.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent
MANIFEST = Path(__file__).parent / "wiring.json"

# event -> (which detail key carries the term, which status it is evidence of). Defect B is
# exactly this table having one column: `reuse_refused` is OFFERED and nothing more.
EVIDENCE: dict[str, tuple[str, str]] = {
    "reuse_refused": ("term", "offered"),
    "bet":           ("bound", "bound"),
    "mint":          ("term", "minted"),
    "accept":        ("term", "accepted"),
    "settle":        ("term", "settled"),
    "cite":          ("term", "cited"),
    "hold":          ("term", "bound"),
    "pull":          ("term", "offered"),
    "rebind":        ("term", "bound"),
    "demote":        ("term", "settled"),
    "retro":         ("term", "promoted"),
    "reuse_install": ("term", "promoted"),
    "promote":       ("term", "promoted"),
}

STATUSES = ("offered", "bound", "minted", "accepted", "settled", "cited", "promoted")


def parse_term(s: str) -> list[tuple[str, str]]:
    """`atom . atom<operand>?GUARD` -> [(name, position)].

    Defect A is fixed by construction: the grammar is split on its own separators, so a name
    is a whole field and never a substring of one. Defect D is the `mid` position existing at
    all -- an implementation that returns only the ends passes every other check here.
    """
    out: list[tuple[str, str]] = []
    body = s
    if "?" in body:
        body, guard = body.split("?", 1)
        out.append((guard.strip(), "guard"))
    if "<" in body:
        body, operand = body.split("<", 1)
        out.append((operand.rstrip(">").strip(), "operand"))
    links = [p.strip() for p in body.split(".") if p.strip()]
    for i, name in enumerate(links):
        if len(links) == 1:
            pos = "sole"
        elif i == 0:
            pos = "head"
        elif i == len(links) - 1:
            pos = "tail"
        else:
            pos = "mid"
        out.append((name, pos))
    return out


def declared() -> dict[str, str]:
    """Every name the build says it has, and whether anything can produce it.

    DECLARED and PRODUCER are two columns because `ONE` is a declared quantifier with no
    producing atom -- `F47`, and a merged column hides it.
    """
    # the repo, not this folder -- the subject is the build, and `lint.py` walks it the same way
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import arc_atoms
    import arc_predict
    import grammar
    import sensors

    out: dict[str, str] = {}
    for p in list(grammar.PRIMES) + list(grammar.HEADS):
        out[p] = "declared"
    for a in arc_atoms.three_spaces(arc_predict.predict()):
        out[a.name] = "producer"
    for name in sensors.minimum_set()._by_name:
        out[name] = "producer"
    return out


def scan(paths: list[Path]) -> dict[str, dict[str, Any]]:
    """name -> {statuses: [...], positions: [...], sources: [...]}, from the ledger alone."""
    seen: dict[str, dict[str, set[str]]] = {}
    for p in paths:
        src = p.stem
        with p.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"event"' not in line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                ev = EVIDENCE.get(row.get("event"))
                if ev is None:
                    continue
                key, status = ev
                detail = row.get("detail")
                term = detail.get(key) if isinstance(detail, dict) else None
                if not isinstance(term, str):
                    continue
                for name, pos in parse_term(term):
                    rec = seen.setdefault(name, {"statuses": set(), "positions": set(),
                                                 "sources": set()})
                    rec["statuses"].add(status)
                    rec["positions"].add(pos)
                    rec["sources"].add(src)
    return {n: {k: sorted(v) for k, v in rec.items()} for n, rec in seen.items()}


def status_of(kind: str, rec: dict[str, Any] | None) -> dict[str, Any]:
    occurred = [s for s in (rec or {}).get("statuses", []) if s != "offered"]
    return {
        "producer": kind == "producer",
        "offered": bool(rec) and "offered" in rec.get("statuses", []),
        "occurred": sorted(occurred),
        "positions": sorted((rec or {}).get("positions", [])),
        "sources": sorted((rec or {}).get("sources", [])),
    }


def current(paths: list[Path]) -> dict[str, Any]:
    dec, found = declared(), scan(paths)
    items = {name: status_of(kind, found.get(name)) for name, kind in sorted(dec.items())}
    return {"computed_over": sorted(p.name for p in paths), "items": items}


def runs() -> list[Path]:
    return sorted((ROOT / "runs").glob("*.jsonl"))


def transitions(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """What changed in STATUS. Counts are deliberately not compared."""
    out = []
    oi, ni = old.get("items", {}), new.get("items", {})
    for name in sorted(set(oi) | set(ni)):
        a, b = oi.get(name), ni.get(name)
        if a is None:
            out.append(f"{name}: NEW in the declared set -> {b['occurred'] or 'never occurred'}")
            continue
        if b is None:
            out.append(f"{name}: NO LONGER DECLARED")
            continue
        for field in ("producer", "occurred", "positions"):
            if a.get(field) != b.get(field):
                out.append(f"{name}: {field} {a.get(field)!r} -> {b.get(field)!r}")
    return out


# ---- the four defects, reintroduced ------------------------------------------------------

def selftest() -> dict[str, str]:
    out: dict[str, str] = {}

    names = [n for n, _ in parse_term("subtraction")]
    out["A substring"] = ("ok" if names == ["subtraction"] and "traction" not in names
                          else f"UNWITNESSED (parsed {names})")

    refused = {"event": "reuse_refused", "detail": {"term": "above . negate . all"}}
    minted = {"event": "mint", "detail": {"term": "above . negate . all"}}
    r_ev, m_ev = EVIDENCE[refused["event"]][1], EVIDENCE[minted["event"]][1]
    out["B refusal"] = ("ok" if r_ev == "offered" and m_ev != "offered"
                        else f"UNWITNESSED ({r_ev} vs {m_ev})")

    classes = {EVIDENCE[e][1] for e in ("mint", "accept", "settle", "reuse_refused")}
    out["C conflation"] = ("ok" if len(classes) == 4
                           else f"UNWITNESSED (four events collapsed to {sorted(classes)})")

    parsed = dict(parse_term("above . negate . all<o11.h>?ACTION1"))
    want = {"above": "head", "negate": "mid", "all": "tail",
            "o11.h": "operand", "ACTION1": "guard"}
    out["D chain-position"] = ("ok" if parsed == want
                               else f"UNWITNESSED (parsed {parsed})")

    # the control: a fixture that examines nothing cannot demonstrate a clean state, so the
    # discriminating case must actually discriminate -- `negate` is MID and an ends-only
    # reading loses it, which is the defect this file exists for.
    ends_only = {n for n, p in parse_term("above . negate . all") if p in ("head", "tail")}
    out["D control"] = ("ok" if "negate" not in ends_only
                        else "UNWITNESSED (the ends-only reading still finds it)")
    return out


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        bad = 0
        for rid, verdict in sorted(selftest().items()):
            print(f"  {rid:<18} {verdict}")
            bad += verdict != "ok"
        return 1 if bad else 0

    paths = runs()
    new = current(paths)

    if "--update" in argv:
        MANIFEST.write_text(json.dumps(new, indent=1) + "\n", encoding="utf-8")
        print(f"wiring: manifest written over {len(paths)} artifact(s)")
        return 0

    if "--unwired" in argv:
        # NO LEDGER ROW IS NOT NEVER-COMPOSED, and `F125` was the correction that cost a
        # published headline: the closure composes 34 of the 48 atoms, so most of what is
        # silent here ENTERED the contest and was lost after it. This column is OCCURRENCE.
        for name, it in new["items"].items():
            if it["producer"] and not it["occurred"]:
                mark = "offered, never used" if it["offered"] else "no ledger row"
                print(f"  {name:<18} {mark}")
        print("\noccurrence, not reach: a name silent here may still be composed and lost "
              "in the contest (F125).")
        return 0

    if not MANIFEST.exists():
        print("wiring: no manifest. Run --update to record the current status.")
        return 1
    old = json.loads(MANIFEST.read_text(encoding="utf-8"))
    moved = transitions(old, new)
    if moved:
        print(f"WIRING: {len(moved)} status transition(s) the manifest does not record.\n")
        for line in moved:
            print(f"  {line}")
        print("\nA capability changing between never-occurred and occurred is the event this "
              "check exists for.\nIf the change is intended, `python conform/wiring.py "
              "--update` and commit the manifest with it.")
        return 1
    print(f"wiring: {len(new['items'])} declared, status unchanged "
          f"over {len(paths)} artifact(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
