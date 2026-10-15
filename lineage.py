"""(b'-g) THE LINEAGE CARRY (Fig 12, Fig 10, Fig 4, Fig 6; the reviewer 2026-10-14 20:18, 20:22;
Isaiah 2026-10-14 11:05 "whats in the library STAYS in the library", 19:05).

At every game and run boundary the lineage writes a GENERATION, and the next instance loads the
chain. ONE PATH: an in-process game is a boundary like any other, so nothing is handed on in memory.

A generation holds only what CHANGED since its parent: new term rows, status changes, new settle/
refute evidence, the vindication tail, changed book keys, new inventions, and the instance's dormant
record. The library at load is the chain FOLDED, root to tip.

THE FORMAT HAS NO DELETION (Isaiah 11:05). No row type removes a key: a later status row for a key
supersedes an earlier one in the folded view, and the earlier one stays in its file.

A generation is named by the hash of its own bytes and names its parent's. It is never overwritten.
More than one tip, or a link that does not verify, RAISES with the tips or the bad link named: never
a silent pick of a tip, never a silent cold start. An empty or absent folder is the root, said so.

The evidence and the dormant record are the RECORD: written and folded, never read back into
standing or into a live store (standing is 7i's; the kind forms are (b'-l) phase 2's)."""
from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path
from typing import Any

import armflag
import gamma
import sensors

CARRY = armflag.arm("TETHER_LINEAGE_CARRY")
PREFIX = "gen_"


def _key(row: dict) -> str:
    """A term row's composition (atom chain, guard, operand tree): what load dedups on. Never a
    row's identity in the record, which is (born, handle) below."""
    return json.dumps([row["atoms"], row.get("guard"), row.get("operand_term")])


def _rid(row: dict) -> tuple:
    """A row's identity in the lineage: its birth handle, qualified by the generation it was
    first written in, so two games' same-text handles never fold together (the reviewer 20:45)."""
    return (row["born"], row.get("handle"))


def enc(x: Any) -> Any:
    """Tagged JSON for the dormant record, so it reads back equal: tuples, sets, non-str dict keys,
    NOT_RESOLVED and gamma.Standing keep their types. Anything else unknown raises."""
    if x is sensors.NOT_RESOLVED:
        return {"__nr__": 1}
    if isinstance(x, dict):
        return {"__d__": [[enc(k), enc(v)] for k, v in x.items()]}
    if isinstance(x, tuple):
        return {"__t__": [enc(v) for v in x]}
    if isinstance(x, (set, frozenset)):
        tag = "__fs__" if isinstance(x, frozenset) else "__s__"
        return {tag: sorted((enc(v) for v in x), key=lambda v: json.dumps(v, sort_keys=True))}
    if isinstance(x, list):
        return [enc(v) for v in x]
    if isinstance(x, gamma.Standing):
        return {"__standing__": {f.name: enc(getattr(x, f.name)) for f in dataclasses.fields(x)}}
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    raise Unencodable(type(x).__name__)


class Unencodable(TypeError):
    """enc met a type it has no form for; `.type` names it (write records it, item by item)."""

    def __init__(self, tname: str) -> None:
        super().__init__(f"lineage.enc: no form for {tname}")
        self.type = tname


def dec(x: Any) -> Any:
    if isinstance(x, list):
        return [dec(v) for v in x]
    if not isinstance(x, dict):
        return x
    if "__nr__" in x:
        return sensors.NOT_RESOLVED
    if "__d__" in x:
        return {dec(k): dec(v) for k, v in x["__d__"]}
    if "__t__" in x:
        return tuple(dec(v) for v in x["__t__"])
    if "__s__" in x:
        return {dec(v) for v in x["__s__"]}
    if "__fs__" in x:
        return frozenset(dec(v) for v in x["__fs__"])
    if "__standing__" in x:
        return gamma.Standing(**{k: dec(v) for k, v in x["__standing__"].items()})
    raise TypeError(f"lineage.dec: an untagged object {sorted(x)[:4]}")


def _chain(d: Path) -> list[tuple[str, dict]]:
    """Every generation in `d`, root to tip, each verified against its own name. Raises on a bad
    hash, a missing parent, more than one root or more than one tip (N3)."""
    gens: dict[str, dict] = {}
    for f in sorted(d.glob(f"{PREFIX}*.json")):
        raw = f.read_bytes()
        h = hashlib.sha256(raw).hexdigest()[:16]
        if f.stem != PREFIX + h:
            raise ValueError(f"lineage: {f.name} does not hash to its name ({h})")
        gens[h] = json.loads(raw)
    if not gens:
        return []
    parents = {h: g["parent"] for h, g in gens.items()}
    bad = {h: p for h, p in parents.items() if p is not None and p not in gens}
    if bad:
        raise ValueError(f"lineage: a parent that is not in the chain: {bad}")
    roots = [h for h, p in parents.items() if p is None]
    tips = sorted(set(gens) - {p for p in parents.values() if p is not None})
    if len(roots) != 1 or len(tips) != 1:
        raise ValueError(f"lineage: not one chain (roots {sorted(roots)}, tips {tips}); merging "
                         "branches is not this item's")
    order, h = [], tips[0]
    while h is not None:
        order.append((h, gens[h]))
        h = parents[h]
    if len(order) != len(gens):
        raise ValueError(f"lineage: {len(gens) - len(order)} generation(s) off the chain")
    return order[::-1]


def fold(chain: list[tuple[str, dict]]) -> dict:
    """The chain read as one library, root to tip. Every row is kept, each stamped with the
    generation it was first written in ("born"); nothing is removed (N2)."""
    rows: dict[tuple, dict] = {}
    out = {"terms": [], "invented": {}, "vindication": [], "book": {}, "evidence": [],
           "dormant": []}
    for h, g in chain:
        for r in g["terms"]:
            row = {**r, "born": h}
            rows[_rid(row)] = row
        for s in g["status"]:
            rows[(s["born"], s["handle"])]["admitted"] = s["admitted"]
        out["invented"].update(g["invented"])
        out["vindication"].extend(g["vindication_tail"])
        out["book"].update(g["book"])
        out["evidence"].extend(g["evidence"])
        out["dormant"].extend(dec(g["dormant"]))
    out["terms"] = list(rows.values())
    return out


def head(d: str | Path) -> tuple[str | None, dict]:
    """The tip's hash and the fold. An absent or empty folder is the ROOT: (None, an empty fold)."""
    p = Path(d)
    chain = _chain(p) if p.is_dir() else []
    return (chain[-1][0] if chain else None), fold(chain)


def write(d: str | Path, ag: Any, game: str) -> dict:
    """The boundary's generation: only what changed since the parent the instance LOADED
    (ag.lineage_parent), against that parent's fold. Named by its own hash; never overwritten."""
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    parent = getattr(ag, "lineage_parent", None)
    chain = _chain(p)
    upto = chain[:[h for h, _ in chain].index(parent) + 1] if parent else []
    base = fold(upto)
    prev = {_rid(r): r for r in base["terms"]}
    blob = ag.gamma.blob(with_names=True)
    terms, status = [], []
    for r in blob["terms"]:
        # NEW = minted by this instance; a term it LOADED from the lineage carries its identity
        # in carried (born, handle), and only a non-marker change of its status is written (N1).
        c = ag.gamma.carried.get(r.pop("name")) or {}
        rid = (c.get("born"), c.get("handle"))
        if rid not in prev:
            terms.append(r)
        elif r.get("admitted") not in (None, gamma.IMPORTED, prev[rid].get("admitted")):
            status.append({"born": rid[0], "handle": rid[1], "admitted": r["admitted"]})
    # THE DORMANT RECORD ITEM BY ITEM (the reviewer 21:14, I3): an item enc has no form for is
    # not written, and is named; it never costs the generation its terms, status or evidence.
    dormant, refused = [], []
    for i, item in enumerate(getattr(ag, "_dormant", [])):
        try:
            dormant.append(enc(item))
        except Unencodable as e:
            refused.append({"i": i, "type": e.type})
    gen = {"lineage": 1, "parent": parent, "game": game, "terms": terms, "status": status,
           "evidence": list(ag.gamma.evidence),
           "vindication_tail": list(blob["vindication"])[len(base["vindication"]):],
           "book": {k: v for k, v in blob["book"].items() if base["book"].get(k) != v},
           "invented": {n: r for n, r in blob["invented"].items() if n not in base["invented"]},
           "dormant": dormant, "dormant_refused": refused}
    raw = json.dumps(gen, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(raw)
    except FileExistsError:
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}
    return {"written": f"{PREFIX}{h}.json", "hash": h, "parent": parent, "terms": len(terms),
            "status": len(status), "evidence": len(gen["evidence"]), "dormant": len(dormant),
            "dormant_refused": len(refused)}


def load(d: str | Path, ag: Any) -> dict:
    """The next instance's start: the chain folded into its Gamma as IMPORTED terms naming the tip,
    and the evidence record turned on. The fold's evidence and dormant record are not read back."""
    h, f = head(d)
    ag.lineage_parent = h
    ag.gamma.keep_evidence = True
    if h is None:
        return {"parent": None, "root": "no generation yet; this instance writes the first"}
    rep = ag.gamma.load_blob({"terms": f["terms"], "invented": f["invented"],
                              "vindication": f["vindication"], "book": f["book"]}, parent=h)
    return {"parent": h, **rep}
